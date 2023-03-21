import json
import glob
from bs4 import BeautifulSoup as bs

import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

class compiler(LoggingEventHandler):
    configPath = "./config.json"
    config = None

    componentFilePaths = []
    componentFiles = []

    pageFiles = []
    compiledPages = []

    def __init__(self):
        self.config = json.loads(open(self.configPath, "r").read())

        self.componentFilePaths = self.getFromDir(self.config["html"], self.config["gateway"])
        self.componentFiles = self.getFiles(self.componentFilePaths)

        self.pageFiles = self.getFiles(self.config["gateway"])
        self.compiledPages = self.parseFiles_html(self.pageFiles)
        self.build()


    def on_any_event(self,event):
        print("####")
        LoggingEventHandler()

        self.componentFilePaths = self.getFromDir(self.config["html"], self.config["gateway"])
        self.componentFiles = self.getFiles(self.componentFilePaths)

        self.pageFiles = self.getFiles(self.config["gateway"])
        self.compiledPages = self.parseFiles_html(self.pageFiles)
        self.build()

    def getFromDir(self, p, m):
        ret = []
        for i in range(len(p)):
            for files in glob.glob(f"{p[i]}/*.html"):
                if files not in m:
                    ret.append(files)
        return ret

    def getFiles(self, p):
        ret = []
        for i in p:
            ret.append(open(i,"r").read())
        return ret

    def parseFiles_html(self, p):
        compiledPageFiles = []
        for i in p:
            while True:
                if(i.find("<?") == -1):
                    for x in self.config["vars"]:
                        if "{" + x + "}" in i:
                            i = i.replace("{"+x+"}",self.config["vars"][x])
                    compiledPageFiles.append(i)
                    break
                start = i.find("<?")
                end = i.find("?>")

                component = i[start:end]
                compArgs = component.split(" ")[1:]

                compName = compArgs[0]

                compFile = ""
                for j in range(len(self.componentFilePaths)):
                    if(compName in self.componentFilePaths[j]):
                        compFile = self.componentFiles[j]
                        argsLen = len(compArgs) - 1
                        for k in compArgs[1:]:
                            if(k != ''):
                                _tag = k.split("=")[0]
                                _val = k.split("=")[1]
                                if("{" + _tag + "}" in compFile):
                                    compFile = compFile.replace("{" + _tag + "}", _val)
                        break
                i = i[:start] + compFile + i[end + 2:]
                i = bs(i, features="html.parser").prettify()
        return compiledPageFiles

    def build(self):

        for i in range(len(self.config["gateway"])):
            _n = self.config["gateway"][i].split("/")
            with open(f'{self.config["buildPath"]}/{_n[len(_n)-1]}', "w") as f:
                f.write(self.compiledPages[i])

x = compiler()


logging.basicConfig(level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

eventHandler = x
observer = Observer()
observer.schedule(eventHandler, ".", recursive=True)
observer.start()
try:
    while True:
        time.sleep(1)
finally:
    observer.stop()
    observer.join()
