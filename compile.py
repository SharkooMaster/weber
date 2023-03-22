#!/bin/python
import json
import glob
import asyncio
from watcher import watcher, Logger
from flagser import *
import os
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

    def __init__(self, config={}):
        if config == {}:
            self.config = json.loads(open(self.configPath, "r").read())
        else:
            self.config = config

        self.componentFilePaths = self.getFromDir(self.config["html"], self.config["pages"])
        self.componentFiles = self.getFiles(self.componentFilePaths)

        self.pageFilePaths = self.getFromDir(self.config["html"], self.componentFilePaths)
        self.pageFiles = self.getFiles(self.config["pages"])
        self.compiledPages = self.parseFiles_html(self.pageFiles)


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


# deffault config before user changes things with flags
compileConfig = {
	"localhost": "localhost",
	"port": 8000,
	"buildPath": "./build",
	"root": "index.html",
	"html": [
		"./src"
	],
	"pages": [
		"./src/index.html"
	],
	"vars": {
		"ip": "192.192.192.1",
		"affe": "https://media.discordapp.net/attachments/749271911988592690/1088069665051377684/IMG_20220920_152149.jpg?width=810&height=1080"
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
def createConfig(args):
    global compileConfig
    if "example" in args:
        #creates dirs
        os.mkdir("src")
        os.mkdir("build")
        #writes a index
        f = open('./src/index.html',"w")
        f.write('''
<DOCTYPE! html>
<html>
    <head>
        <meta http-equiv="refresh" content="2">
        <script src="https://cdn.tailwindcss.com"></script>
    </head>

    <body>
        <? navbar title=thi ?>
        {ip}
        <h1>What is the point</h1>
    </body>
</html>
        ''')
        f.close()

        f = open("./src/navbar.html", "w") 
        f.write('''
        <div class="bg-gray-400 w-full h-[80px] flex flex-row items-center justify-center">
            <p>{title}</p>
        </div>
        ''')
        f.close()

    #creates a config file
    f = open('./config.json',"w")
    f.write(json.dumps(
        compileConfig,
    indent=4
    )) 
 
#npm start
def auto(args):
    logger.log("Starts auto refresh")
    x = compiler()
    _w = watcher()
    _w.start(edited=lambda: x.refresh(), new_file=lambda: x.refresh(), ignore=x.config["autoRefresh"]["ignore"])
# compiles
def comp(args):
    global compileConfig
    x = compiler(compileConfig)
    x.refresh()

runners = FlagManager([
    Flag("compile", "--compile", "compiles files from folder specifed after flag to a index.html", comp),
    Flag("init", "", "creates a config file. followed på example will create a example project", createConfig),
    Flag("start", "", "", auto),
])
runners.check()
