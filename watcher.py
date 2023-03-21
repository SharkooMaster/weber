from os import *
import os
import time

path = "./"
readFiles = {}
class Logger:
    def __init__(self):
        self.should_log = True

    def log(self,msg):
        from time import gmtime, strftime
        tday = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        print(tday,"|INFO|",msg)

class watcher:
    def __init__(self):
        self.sleeptime = 1

    def start(self,new_file=lambda: None, edited=lambda :None, logger=Logger()):
        global path
        global readFiles

        while True: 
            for subdir, dirs, files in os.walk(path):
                for file in files:
                    #print os.path.join(subdir, file)
                    filePath = subdir + os.sep + file
                    fileStatsObj = os.stat ( filePath )
                    t = os.path.getmtime(filePath)
                    if filePath not in readFiles.keys():
                        logger.log("new file detected "+filePath)
                        readFiles[filePath] = t
                    elif readFiles[filePath] != t:
                        logger.log(filePath+" edited")
                        edited()
                        readFiles[filePath] = t
                    

            time.sleep(self.sleeptime)

watcher = watcher()
watcher.start(edited=lambda : print('edited wtd'))



