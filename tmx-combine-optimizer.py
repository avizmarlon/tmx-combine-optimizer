import re
import os
import tkinter
from tkinter.filedialog import askdirectory
from time import sleep
from clear_console import clear_console

#
#
# todo
# .> implement a function to write the resulting 
#     data (output) to a txt file, for 
#     further manipulation and better management
#
# .> make it GUI? (cmd line is so cool and comfortable to use though)
#
#
#

__author__ = "Marlon Aviz"
clear_console()

root = tkinter.Tk().withdraw()
path = askdirectory(title="Select the folder that contains .TMX files")
tmx_extension = '.tmx'
contents = os.walk(path)
srclangs = {}

while True:
	srclang_ref = input("""What should be the srclang value of the TMX files?
eg1: EN-PT
eg2: DE-ES
etc.
Note: Don't use quotes. Also: Case-sensitive
Type 'q' to quit.

~/> """)
	if srclang_ref == 'q':
		clear_console()
		exit()
	if '"' in srclang_ref or "'" in srclang_ref:
		clear_console()
		print("Please, don't use quotes. Try again.\n")
		continue
	else:
		break

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
						# removes the hex text code (\x00n, etc.), leaving only the actual text
						line = line.replace(''.join(match), '')
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

# checks if there is any srclang with a value different from the one defined by the user
# and prints it out for the user to see
clear_console()
diverged_files = {}
print("Finished analyzing all files. Now I'll analyze every srclang. Hold on.")
sleep(4)
for srclang in srclangs:
	srclang_value = srclangs[srclang]
	print("\nChecking srclangs values: " + srclang + " --> " + srclang_value)
	if srclang_value != srclang_ref:
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
	print("All files with consistent srclang value. Nice :)")
	sleep(3)
	clear_console()
