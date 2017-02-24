import re
import os
import tkinter
from tkinter.filedialog import askdirectory


root = tkinter.Tk().withdraw()
path = askdirectory(title="Select the folder that contains .TMX files")
tmx_extension = '.tmx'
contents = os.walk(path)
srclangs = {}

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
for srclang in srclangs:
	if srclangs[srclang] != 'EN-GB':
		print("This file diverged from the common srclang value: " + srclang)
	