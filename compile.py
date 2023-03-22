import json
import glob
import asyncio
from watcher import watcher
from websockets import serve
from bs4 import BeautifulSoup as bs

class compiler:
    configPath = "./config.json"
    config = None

    componentFilePaths = []
    componentFiles = []

    pageFilePaths = []
    pageFiles = []

    compiledPages = []

    def __init__(self):
        self.config = json.loads(open(self.configPath, "r").read())

        self.componentFilePaths = self.getFromDir(self.config["html"], self.config["pages"])
        self.componentFiles = self.getFiles(self.componentFilePaths)

        self.pageFilePaths = self.getFromDir(self.config["html"], self.componentFilePaths)
        self.pageFiles = self.getFiles(self.config["pages"])
        self.compiledPages = self.parseFiles_html(self.pageFiles)
        self.build()

        _w = watcher()
        _w.start(edited=lambda: self.refresh(), new_file=lambda: self.refresh(), ignore=self.config["autoRefresh"]["ignore"])

    def refresh(self):
        self.componentFilePaths = self.getFromDir(self.config["html"], self.config["pages"])
        self.componentFiles = self.getFiles(self.componentFilePaths)

        self.pageFiles = self.getFiles(self.config["pages"])
        self.compiledPages = self.parseFiles_html(self.pageFiles)
        self.build()

    def getFromDir(self, p, m):
        ret = []
        for i in range(len(p)):
            for files in glob.glob(f"{p[i]}/*.html"):
                files = files.replace("\\","/")
                for j in m:
                    if j not in files:
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

        for i in range(len(self.config["pages"])):
            _n = self.config["pages"][i].split("/")
            with open(f'{self.config["buildPath"]}/{_n[len(_n)-1]}', "w") as f:
                self.compiledPages[i] = self.compiledPages[i].replace('<doctype! html="">', "<DOCTYPE! html>")
                self.compiledPages[i] = self.compiledPages[i].replace('</doctype!>', "")
                f.write(self.compiledPages[i])
        print("COMPILER::LOG -> Build succeeded")

x = compiler()
