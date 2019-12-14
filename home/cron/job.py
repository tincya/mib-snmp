import datetime
import sys
import os

snow = 'Running: '+os.path.dirname(sys.argv[0])+'\n-----In: '+str(datetime.datetime.now())

fs = open(os.path.dirname(sys.argv[0])+'/log.txt','a')
fs.write(snow+'\n')

fs.close()
