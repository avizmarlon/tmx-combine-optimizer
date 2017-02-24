import re
import os
import tkinter
from tkinter.filedialog import askdirectory
from clear_console import clear_console
from time import sleep

root = tkinter.Tk().withdraw()
path = askdirectory(title="Select the folder that contains .TMX files")
tmx_extension = '.tmx'
contents = os.walk(path)
srclangs = {}

clear_console()

# look in all folders, subolders and files of each of these folders and subfolders
for dirpath, dirname, filename in contents:
	for file in filename:
		if file.endswith(tmx_extension):
			filepath = dirpath + "/" + file
			data = open(filepath, 'rb') # open in binary read-mode
			for line in data:
				line = str(line.strip()) # we'll use str pattern in RE, so we convert the line in bytes to string
				xcode = re.findall('\Sx[0-9a-z]+', line) # finds all occurences of hex text code
				if len(xcode) > 0:
					for match in xcode:
						line = line.replace(''.join(match), '') # removes the hext text code, leaving only the actual text
				print("\nSearching line />>> " + line)
				# if we find the line with srclang value, harvest it,
				# put it into our srclangs database and jump to the next file in the loop
				# otherwise, go to the next line and just keep searching for the srclang attribute
				if re.search('srclang', line):
					match = re.findall('srclang="(.*)">', line)
					srclangs[filepath] = match[0]
					break
				else:
					continue

# checks if there is any srclang with a value different from 'EN-GB'
# and prints it out for us to see
clear_console()
diverged_files = {}
print("Finished analyzing all files. Now I'll analyze every srclang. Hold on.")
sleep(4)
for srclang in srclangs:
	srclang_value = srclangs[srclang]
	print("\nChecking srclangs values: " + srclang + " --> " + srclang_value)
	if srclang_value != 'EN-GB':
		diverged_files[srclang] = srclang_value

clear_console()

if len(diverged_files) > 0:
	print("The following files contain diverged srclang value: \n")
	sleep(3)
	for diverged_file in diverged_files:
		srclang_value = diverged_files[diverged_file]
		print("# File path: " + diverged_file)
		print("# srclang value: " + srclang_value)
		print("================\n")
else:
	print("No files with srclang diverged. Nice :)")
	sleep(3)
	clear_console()