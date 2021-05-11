# firebase-iOS-dSYM-uploader

This Python 3 script uploads all your Firebase dSYM files, so that you no longer have to worry about missing dSYMs in your Firebase Dashboard!

To use this correctly, you'll want to download the debug symbols of every build since the last run. To do this, open the .xcarchive file in Xcode and select "Download Debug Symbols" on the right-hand side, or download your dSYMs from your Apple Store Connect > My Apps > {Your Application} > TestFlight > {Your Build} > Build Metadata > Download dSYM.

Usage: 
`python3 firebase-dSYM-uploader.py -i {PATH TO BASE XCODE ARCHIVES DIRECTORY} -o {PATH TO SCRIPT OUTPUT SAVE FILE} -p {PATH TO FIREBASE INFO_P_LIST FILE} -s {PATH TO FIREBASE UPLOAD-SYMBOLS FILE}`

Options are as follows:

-i OR --idir= {PATH TO BASE XCODE ARCHIVES DIRECTORY}
			

-o OR --ofile= {PATH TO SCRIPT OUTPUT SAVE FILE}
			

-p OR --p_list_dir= {PATH TO FIREBASE INFO_P_LIST FILE}
			

-s OR --script_path= {PATH TO FIREBASE UPLOAD-SYMBOLS FILE}
