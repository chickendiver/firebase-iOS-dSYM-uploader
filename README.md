# firebase-iOS-dSYM-uploader

This Python 3 script uploads all your Firebase dSYM files, so that you no longer have to worry about missing dSYMs in your Firebase Dashboard!

The script will crawl through your specified Xcode archives directory and pull all the dSYM files from it that it finds in all the subdirectories. Once it does this, it will compare to a specified output cache to ensure that it doesn't re-upload the same dSYMs again if it doesn't need to. Run this as often as you'd like - the script will only upload newly created dSYM files.

To use this script correctly, you'll want to download the debug symbols of every build since the last run. To do this, open the .xcarchive file in Xcode and select "Download Debug Symbols" on the right-hand side, or download your dSYMs from your Apple Store Connect > My Apps > {Your Application} > TestFlight > {Your Build} > Build Metadata > Download dSYM.

# Installation:
`pip3 install -r requirements.txt`

Will install all prerequisites. Currently uses the third-party library `tqdm` to generate a progress bar.

# Usage: 
`python3 firebase-dSYM-uploader.py -i {PATH TO BASE XCODE ARCHIVES DIRECTORY} -o {PATH TO SCRIPT OUTPUT SAVE FILE} -p {PATH TO FIREBASE INFO_P_LIST FILE} -s {PATH TO FIREBASE UPLOAD-SYMBOLS FILE}`

Options are as follows:

-i OR --idir= {PATH TO BASE XCODE ARCHIVES DIRECTORY}. E.g.: `/Users/{USER}/Library/Developer/Xcode/Archives/`

-o OR --ofile= {PATH TO SCRIPT OUTPUT SAVE FILE}. E.g.: `./last_run_archive_directory_list.json`
			

-p OR --p_list_dir= {PATH TO FIREBASE INFO_P_LIST FILE}. E.g.: `/Users/{USER}/{PROJECT_DIR}/GoogleService-Info.plist`
			

-s OR --script_path= {PATH TO FIREBASE UPLOAD-SYMBOLS FILE}. E.g.: `/Users/{USER}/{PROJECT_DIR}/Pods/FirebaseCrashlytics/upload-symbols`
