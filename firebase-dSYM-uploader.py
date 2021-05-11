''' 
Upload dSYMS

This script searches the ~/Library/Developer/Xcode/Archives/ folder (Or whichever folder you specify in BASE_ARCHIVES_DIRECTORY) and checks to see if there are any new archives. If so, it will access the folder and upload the dSYMS.

This is was originall built to run on a 2014 Macbook Pro running Mac OS 11.3.1 (Big Sur), so you may need to make slight tweaks to support your device.


NOTE:

To use this correctly, you'll want to download the debug symbols of every build since the last run. To do this, open the .xcarchive file in Xcode and select "Download Debug Symbols" on the right-hand side, or download your dSYMs from your Apple Store Connect > My Apps > {Your Application} > TestFlight > {Your Build} > Build Metadata > Download dSYM.

'''

import sys, getopt
from os import listdir
from os.path import isfile, join, isdir
import json
from datetime import datetime
from tqdm import tqdm
import subprocess
from pathlib import Path

BASE_ARCHIVES_DIRECTORY = ''
OUTPUT_JSON_FILE = ''

INFO_P_LIST_DIRECTORY = ''
FIREBASE_UPLOAD_SYMBOLS_PATH = ''

def setup():
	print("Looking for new directories in", BASE_ARCHIVES_DIRECTORY)
	retrieve_last_JSON_array()
	retrieve_new_archive_directory(BASE_ARCHIVES_DIRECTORY)
	filter_only_new_archives(previous_directory_array, dSYM_paths_this_run)

def teardown():
	print("Tearing down")

def save_new_json_file(new_array):
	data = {}
	data['dSYM_directory_array'] = new_array
	data['saved_at'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

	with open(OUTPUT_JSON_FILE, 'w') as outfile:
		json.dump(data, outfile)

def retrieve_last_JSON_array():
	global previous_directory_array
	previous_directory_array = []

	if isfile(OUTPUT_JSON_FILE):
		with open(OUTPUT_JSON_FILE) as json_file:
			data = json.load(json_file)
			previous_directory_array = data['dSYM_directory_array']
			previous_directory_run_time = data['saved_at']
			print("The last time we ran on", previous_directory_run_time, "the directory had", len(previous_directory_array), "archives.")
	else:
		print("NO PREVIOUS JSON FILE EXISTS")

def retrieve_new_archive_directory(path):
	global dSYM_paths_this_run
	directory_contents = [f for f in listdir(path)]
	dSYM_paths_this_run = create_dSYM_paths_in(directory_contents)
	print("The new directory has", len(dSYM_paths_this_run), "archives")

def format_path(string):
	return string.replace(" ", "\\ ")

def create_dSYM_paths_in(archive_list):
	dSYM_directory_paths = []
	for archive_item in archive_list:
		if archive_item != ".DS_Store":
			archive_date_path = BASE_ARCHIVES_DIRECTORY + archive_item + "/"
			dSYM_directory_paths += [format_path(archive_date_path + f + "/dSYMs") for f in listdir(archive_date_path) if isdir(join(archive_date_path, f))]

	return dSYM_directory_paths

def filter_only_new_archives(old_directory, new_directory):
	global filtered_new_archives

	filtered_new_archives = []
	if len(old_directory) < len(new_directory):
		filtered_new_archives = (list(list(set(new_directory)-set(old_directory)) + list(set(old_directory)-set(new_directory))))
		print("The following are new archives since the last run:\n", filtered_new_archives, "")
	else:
		print("The new directory is smaller than the old one, so we'll skip for now")

def upload_dSYMs():
	if len(filtered_new_archives) > 0:
		print("⬆️  Uploading", len(filtered_new_archives), "new archives...\n")

		filtered_new_archives.sort(reverse=True)
		print("First archive: ", filtered_new_archives[0])
		print("Last archive: ", filtered_new_archives[-1])

		for new_archive in tqdm(filtered_new_archives):
			shell_command = FIREBASE_UPLOAD_SYMBOLS_PATH + " -gsp " + INFO_P_LIST_DIRECTORY + " -p ios " + new_archive
			upload_symbols = subprocess.Popen(shell_command, shell=True, stdout=subprocess.PIPE)
			for line in upload_symbols.stdout:
				print(line)
			upload_symbols.wait()
			print(upload_symbols.returncode)

		print("✔️  Upload complete as of", datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), " Saving new list on disk")
		save_new_json_file(dSYM_paths_this_run)
	else:
		print("\nNo new DSYMs to upload. Exiting.\n")

def parse_inputs(argv):
	global BASE_ARCHIVES_DIRECTORY
	global OUTPUT_JSON_FILE
	global INFO_P_LIST_DIRECTORY
	global FIREBASE_UPLOAD_SYMBOLS_PATH

	try:
		opts, args = getopt.getopt(argv,"hi:o:p:s:",["idir=","ofile=","p_list_dir=","script_path="])
	except getopt.GetoptError:
		print('Error with provided options')
		sys.exit(0)
		return False

	if ((len(opts) != 1 and opts[0] != '-h')) and len(opts) != 4:
		print('''All options must be specified. 
			Please specify options as follows:
			-i OR --idir= {PATH TO BASE XCODE ARCHIVES DIRECTORY}
			-o OR --ofile= {PATH TO SCRIPT OUTPUT SAVE FILE}
			-p OR --p_list_dir= {PATH TO FIREBASE INFO_P_LIST FILE}
			-s OR --script_path= {PATH TO FIREBASE UPLOAD-SYMBOLS FILE}''')
		sys.exit(0)
		return False

	for opt, arg in opts:
		if opt in ("-h"):
			print('''Usage:

			python3 firebase-dSYM-uploader.py -i {PATH TO BASE XCODE ARCHIVES DIRECTORY} -o {PATH TO SCRIPT OUTPUT SAVE FILE} -p {PATH TO FIREBASE INFO_P_LIST FILE} -s {PATH TO FIREBASE UPLOAD-SYMBOLS FILE}
			
			Options are as follows:
			-i OR --idir= {PATH TO BASE XCODE ARCHIVES DIRECTORY}
			-o OR --ofile= {PATH TO SCRIPT OUTPUT SAVE FILE}
			-p OR --p_list_dir= {PATH TO FIREBASE INFO_P_LIST FILE}
			-s OR --script_path= {PATH TO FIREBASE UPLOAD-SYMBOLS FILE}''')
			sys.exit(0)
			return False

		if opt in ("-i", "--idir"):
			if arg == None or len(arg) == 0 or not isdir(arg):
				print("Base archive directory specified in", opt, "Specified argument: {}".format(arg), "is not a directory. Please ensure that you specify a directory. E.g.: '~/Library/Developer/Xcode/Archives/'")
				sys.exit(0)			
				return False

			BASE_ARCHIVES_DIRECTORY = arg
		elif opt in ("-o", "--ofile"):
			OUTPUT_JSON_FILE = arg

			if arg == None or len(arg) == 0:
				print("Save file specified in", opt, "Specified argument: {}".format(arg), "is empty. Please specify a filename.")
				sys.exit(0)
				return False

		elif opt in ("-p", "--p_list_dir"):
			if arg == None or len(arg) == 0 or not isfile(arg):
				print("InfoPList file specified in", opt, "Specified argument: {}".format(arg), "is not a file. Please ensure that you specify a file. E.g.: '~/{YOUR_APP_DIRECTORY}/Core/InfoPLists/Firebase/ProductionFiles/GoogleService-Info.plist'")
				sys.exit(0)
				return False

			INFO_P_LIST_DIRECTORY = arg
		elif opt in ("-s", "--script_path"):
			if arg == None or len(arg) == 0 or not isfile(arg):
				print("upload-symbols file specified in", opt, "Specified argument: {}".format(arg), "is not a file. Please ensure that you specify a file. E.g.: '~/{YOUR_APP_DIRECTORY}/Pods/FirebaseCrashlytics/upload-symbols'")
				sys.exit(0)			
				return False

			FIREBASE_UPLOAD_SYMBOLS_PATH = arg
		else:
			print("Unsupported argument identifier:", opt)
			sys.exit(0)  
			return False 	

	return True

def main(argv):
	if parse_inputs(argv):
		setup()
		upload_dSYMs()
		teardown()

if __name__ == '__main__':

	try:
		main(sys.argv[1:])
	except KeyboardInterrupt:
		print('\n👋 Bye')
		teardown()
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
	'''except:
		teardown()
		print("Exiting due to an error.")'''