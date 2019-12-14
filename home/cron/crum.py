from crontab import CronTab
import os
import sys
 

def onjob():
  crums = CronTab(user='tincya')
  tcmd = 'python3 '+os.getcwd()+'/job.py args >> '+os.getcwd()+'/crums.txt 2>&1'
  print(tcmd)
  job = crums.new(command=tcmd)
  job.minute.every(1)
  crums.write()

def offjob():
  crums = CronTab(user=True)
  crums.remove_all()
  crums.write()
  # for job in crums:
  #   crums.remove(job)
  #   crums.write()

if sys.argv.pop()=='off':
  offjob()
else:
  onjob()
