#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
NAME
  canalsur

DESCRIPTION
  Fetches and downloads online on-demand videos from Canal Sur by requesting
  information related to the video to a CS web service.

AUTHOR
  Jesus Rozano <jesus@rozano.es>

VERSION
  1.0-dev

LICENSE
  BSD (3-Clause) License

  Copyright (c) 2014, Jesus Rozano Segura
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

import time, sys, os, traceback, optparse, shutil, urllib2, re
from BeautifulSoup import BeautifulSoup

# CONFIGURATION
DOWNLOAD_DIR = os.path.join(os.path.expanduser('~'), 'Canal Sur')

# LOGIC
def download (url):
        """
          Downloads the URL received by parameter to the DOWNLOAD_DIR folder, showing
          the total size (in bytes), the current size transferred (in bytes) and a
          estimated percentage of the download.
        """

        file_name = os.path.join(DOWNLOAD_DIR, url.split('/')[-1])
        u = urllib2.urlopen(url)
        f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Size: %s bytes" % (file_size)
        print "Downloading..."

        file_size_dl = 0
        block_sz = 8192
        while True:
              buffer = u.read(block_sz)
              if not buffer:
                     break

              file_size_dl += len(buffer)
              f.write(buffer)
              status = r"%10d bytes [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
              status = status + chr(8)*(len(status)+1)
              print status,

        print ''
        print ''
        f.close()

def getWsUrl (page):
        """
          Fetches and parses a HTML document that contains the video dispatching
          web-service. Returns the WS URL related to the video displayed in this page.
        """

        html = urllib2.urlopen(page).read()
        parsed_html = BeautifulSoup(html)
        flash_vars = parsed_html.body.find(attrs={'name': 'flashVars'})['value']
        ws_url = re.search("(?P<url>https?://[^\s]+)", flash_vars).group("url")

        return ws_url

def getVideoUrl (ws_url):
        """
          Fetches and parses an XML document returned by the web-service to obtain
          the full video URL and the name of this chapter.
        """

        xml = urllib2.urlopen(ws_url).read()
        parsed_xml = BeautifulSoup(xml)
        video_url = parsed_xml.find('video', attrs={'type': 'content'}).find('url').text
        video_title = parsed_xml.title.text

        return (video_title, video_url)

def main ():
        global options, args

        if not os.path.exists(DOWNLOAD_DIR):
                if options.verbose: print "Creating directory", DOWNLOAD_DIR
                os.makedirs(DOWNLOAD_DIR)

        for page_url in args:
                ws_url = getWsUrl(page_url)
                (video_title, video_url) = getVideoUrl(ws_url)

                print "Title:", video_title
                print "URL:", video_url

                download(video_url)

        # Just a reminder: where the videos are stored.
        print DOWNLOAD_DIR


if __name__ == '__main__':
        try:
                # Script bootstrap
                start_time = time.time()
                parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), usage=main.__doc__, version='1.0-dev')
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
