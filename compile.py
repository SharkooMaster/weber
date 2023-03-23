import os
import glob
import json
import shutil
import asyncio
from generateFiles import createConfig
from watcher import watcher, Logger
from flagser import *
from bs4 import BeautifulSoup as bs

logger = Logger()

class compiler:
    configPath = os.getcwd()+"/config.json"

    config = None

    componentFilePaths = []
    componentFiles = []

    pageFilePaths = []
    pageFiles = []

    compiledPages = []

    cssFilePaths = []
    cssInjections = []

    jsFilePaths = []

    def __init__(self, config={}):
        if config == {}:
            self.config = json.loads(open(self.configPath, "r").read())
        else:
            self.config = config

        self.cssFilePaths = self.getFromDir(self.config["cssPath"], [], "/*.css")
        self.cssInjections = self.setCssLinks()
        self.syncFilesToBuild(self.cssFilePaths, ".css")

        self.jsFilePaths = self.getFromDir(self.config["jsPath"], [], "/*.js")
        self.syncFilesToBuild(self.jsFilePaths, ".js")

        self.componentFilePaths = self.getFromDir(self.config["html"], self.config["pages"], "/*.html")
        self.componentFiles = self.getFiles(self.componentFilePaths)

        self.pageFilePaths = self.getFromDir(self.config["html"], self.componentFilePaths, "/*.html")
        self.pageFiles = self.getFiles(self.config["pages"])
        self.compiledPages = self.parseFiles_html(self.pageFiles)


    def refresh(self):
        self.cssFilePaths = self.getFromDir(self.config["cssPath"], [], "/*.css")
        self.cssInjections = self.setCssLinks()
        self.syncFilesToBuild(self.cssFilePaths, ".css")

        self.jsFilePaths = self.getFromDir(self.config["jsPath"], [], "/*.js")
        self.syncFilesToBuild(self.jsFilePaths, ".js")

        self.componentFilePaths = self.getFromDir(self.config["html"], self.config["pages"], "/*.html")
        self.componentFiles = self.getFiles(self.componentFilePaths)

        self.pageFiles = self.getFiles(self.config["pages"])
        self.compiledPages = self.parseFiles_html(self.pageFiles)
        self.build()

    def getFromDir(self, p, m, f):
        ret = []
        for i in range(len(p)):
            for files in glob.glob(f"{p[i]}{f}"):
                files = files.replace("\\","/")
                if(len(m) != 0):
                    for j in m:
                        if j not in files:
                            ret.append(files)
                else:
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

        for w in range(len(compiledPageFiles)):
            headStart = compiledPageFiles[w].find("<head>")
            offset = headStart + 6
            for q in self.cssInjections:
                compiledPageFiles[w] = compiledPageFiles[w][:offset] + q + compiledPageFiles[w][offset: ]
                print(compiledPageFiles[w])
                offset += len(q)
            compiledPageFiles[w] = bs(compiledPageFiles[w], features="html.parser").prettify()
        return compiledPageFiles

    def setCssLinks(self):
        ret = []
        _link = f"<link rel='stylesheet' href='"
        for i in self.cssFilePaths:
            _i = i.split("/")
            ret.append(f"{_link}{_i[len(_i)-1]}' />")
        return ret

    def syncFilesToBuild(self, f, ext):
        for item in os.listdir(self.config["buildPath"]):
            if item.endswith(ext):
                os.remove(os.path.join(self.config["buildPath"], item))

        for fname in f:
            shutil.copy2(fname, self.config["buildPath"])

    def build(self):

        for i in range(len(self.config["pages"])):
            _n = self.config["pages"][i].split("/")
            with open(f'{self.config["buildPath"]}/{_n[len(_n)-1]}', "w") as f:
                self.compiledPages[i] = self.compiledPages[i].replace('<doctype! html="">', "<DOCTYPE! html>")
                self.compiledPages[i] = self.compiledPages[i].replace('</doctype!>', "")
                f.write(self.compiledPages[i])
        print("COMPILER::LOG -> Build succeeded")


# deffault config before user changes things with flags
compileConfig = {
	"localhost": "localhost",
	"port": 8000,
	"buildPath": "./build",
	"root": "index.html",
	"html": [
		"./src"
	],
	"cssPath":
	[
		"./src/css"
	],
	"jsPath":
	[
		"./src/js"
	],
	"pages": [
		"./src/index.html"
	],
	"vars": {
		"logo": "GFX/Logo.svg",
		"logoDark": "GFX/LogoDark.svg",
		"hamIcon": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Hamburger_icon.svg/2048px-Hamburger_icon.svg.png"
	},
	"autoRefresh": {
		"ignore" : ["./build", "./.git", ".py", ".json", "./LICENSE"]
	}
}

#--setters--#
#add variables to
def set_variables(args):
    global compileConfig
    for arg in args:
        key = arg.split("=")[0]
        value = arg.split("=")[1]
        compileConfig["vars"][key] = value
#sets srx
def setsrc(args):
    global compileConfig
    compileConfig["html"] = args
    print(compileConfig)

def setBuild(args):
    global compileConfig
    compileConfig["buildPath"] = args[0]

setters = FlagManager([
    Flag("vars","set-vars","followed by a list of vars (key=value key2=value2) sets the global vars", set_variables),
    Flag("html","set-html","followed by a list of folder paths sets the folder paths which to look for html", lambda arg: set_value(args, "html")),
    Flag("buildpath","set-buildpath","followed by a path sets the path to build to", setBuild),
])
setters.check()

#--runners--#

#npm start
def auto(args):
    logger.log("Starts auto refresh")
    x = compiler()
    w = watcher()
    w.start(edited=lambda: x.refresh(), new_file=lambda: x.refresh(), ignore=x.config["autoRefresh"]["ignore"])
# compiles
def comp(args):
    global compileConfig
    x = compiler(compileConfig)
    x.refresh()

runners = FlagManager([
    Flag("compile", "--compile", "compiles files from folder specifed after flag to a index.html", comp),
    Flag("init", "", "creates a config file. followed på example will create a example project", lambda args : createConfig(args,compileConfig)),
    Flag("start", "", "", auto),
])
runners.check()
