#!/usr/bin/env python
# -*- coding: utf-8 -*- 

"""
NAME
  dropcopy

DESCRIPTION
  Python script to automate archival of Dropbox photo and video uploads from smartphones.

AUTHOR
  Jesús Rozano <jesus@rozano.es>

VERSION
  1.0-dev

LICENSE
  BSD (3-Clause) License
  
  Copyright (c) 2014, Jesús Rozano Segura
  All rights reserved.

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are met:

  * Redistributions of source code must retain the above copyright notice, this
    list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

  * Neither the name of the author nor the names of its
    contributors may be used to endorse or promote products derived from
    this software without specific prior written permission.

  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import time, sys, os, traceback, optparse, shutil

# CONFIGURATION
DROPBOX_UPLOAD_DIR = '/media/datos/Dropbox/Camera Uploads/'
ARCHIVE_DIR        = '/media/datos/Fotos/'

# LOGIC
def main ():
	global options, args
	
	for root, dirs, files in os.walk(DROPBOX_UPLOAD_DIR):   
		for file in files:
			if not file.startswith('.'):
				date = file.split()
				COPY_DIR = os.path.join(ARCHIVE_DIR, date[0])
				SOURCE_FILE = os.path.join(root, file)
				DESTIN_FILE = os.path.join(COPY_DIR, file)

  				if not os.path.exists(COPY_DIR):
  					if options.verbose: print "Creating directory", COPY_DIR
  					os.makedirs(COPY_DIR)
  
  				if not os.path.exists(DESTIN_FILE):
					if options.verbose: print "Moving \"" + SOURCE_FILE + "\" to", DESTIN_FILE
  					shutil.move(SOURCE_FILE, COPY_DIR)
  				else:
  					if options.verbose: print "File \"" + DESTIN_FILE + "\" already exists. Ignoring."


if __name__ == '__main__':
	try:
		# Script bootstrap
		start_time = time.time()
		parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), usage=globals()['__doc__'], version='1.0-dev')
		parser.add_option ('-v', '--verbose', action='store_true', default=False, help='Enable verbose output.')
		(options, args) = parser.parse_args()

		if options.verbose: print time.asctime()
		if options.verbose: print "Program start."
		main()
		if options.verbose: print time.asctime()
		if options.verbose: print 'TOTAL EXECUTION TIME (in seconds): '
		if options.verbose: print (time.time() - start_time)
		sys.exit(0)

	except KeyboardInterrupt, e: # Ctrl-C
		raise e
	except SystemExit, e: # sys.exit()
		raise e
	except Exception, e:
		print 'Unexpected error.'
		print str(e)
		traceback.print_exc()
		os._exit(1)
