#combine several files into one

import os

#inspired from Recursive File and Directory Manipulation in Python (Part 2)
#Authors: Vinit Gupta, Akshat Dave
 
def merge_files(path):
	# The top argument for name in files
	topdir = path
	 
	extens = ['txt']  # the extensions to search for
	 
	found = {x: [] for x in extens} # lists of found files
	 
	# Directories to ignore
	ignore = ['docs', 'pdf', 'doc']
	write_path = '/'.join([topdir,'merged_file.txt'])
	 
	print('Beginning search for files in %s' % os.path.realpath(topdir))
	 
	# Walk the tree
	for dirpath, dirnames, files in os.walk(topdir):
	    # Remove directories in ignore
	    # directory names must match exactly!
	    for idir in ignore:
	        if idir in dirnames:
	            dirnames.remove(idir)
	 
	    # Loop through the file names for the current step
	    for name in files:
	        # Split the name by '.' & get the last element
	        ext = name.lower().rsplit('.', 1)[-1]
	 
	        # Save the full name if ext matches
	        if ext in extens:
	            found[ext].append(os.path.join(dirpath, name))

	fp = open(write_path,'w')
	file_count = 0
	print 'writing to file {}'.format(write_path)
	# loop thru results
	for ext in found:
	    # Concatenate the result from the found dict
	    #logbody += "<< Results with the extension '%s' >>" % ext
	    #logbody += '\n\n%s\n\n' % '\n'.join(found[ext])


		for fn in found[ext]:
			content = None
			# read file
			with open(fn, 'r') as content_file:
			    content = content_file.read()

			if content is not None:
				file_count +=1
				fp.write(content)

	fp.close()
	print 'completed writing to file {}, total files merged = {}'.format(write_path,file_count)


# main code runs here
AUTO_RUN = False

if AUTO_RUN:
	merge_files('../../scrapedata')