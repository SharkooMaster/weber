import os
def createConfig(args, compileConfig):
    if "example" in args:
        #creates dirs
        os.mkdir("src")
        os.mkdir("./src/js")
        os.mkdir("./src/css")
        os.mkdir("build")
        #writes a index
        f = open('./src/js/index.js',"w")
        f.write('''

paths =
[
	"Home",
	"About"
];

const navBarView_mobile = document.getElementById("mobNavView")
function mobNav()
{
	if(navBarView_mobile.style.display === "none")
	{
		navBarView_mobile.style.display = "block"
	}else{
		navBarView_mobile.style.display = "none"
	}
}

function navPage(a)
{
	for (let index = 0; index < paths.length; index++) {
		if(a == index){
			document.getElementById(paths[index]).style.display = "block";
			window.history.pushState({id:"100"}, "Page", "/"+paths[index])
		}
		else{
			document.getElementById(paths[index]).style.display = "none";
		}
	}
	navBarView_mobile.style.display = "none"
}
navPage(0)
        ''')
        f.close()
        f = open('./src/css/index.css',"w")
        f.write('''
        ''')
        f.close()
        f = open('./src/navbar.html',"w")
        f.write('''

<div class="shadow-md w-full h-[80px] flex flex-row items-center justify-start px-12 hidden md:flex">
	<img src="{logoDark}" class="h-[50px]" />
	
	<div class="w-full h-full flex flex-row items-center justify-end gap-4">
		<div class="h-full px-4 flex items-center justify-center flex-wrap hover:bg-[#d9d9d9] cursor-pointer" onclick="navPage(0)">
			Home
		</div>
		<div class="h-full px-4 flex items-center justify-center flex-wrap hover:bg-[#d9d9d9] cursor-pointer" onclick="navPage(1)">
			About us
		</div>
	</div>
</div>
        ''')
        f.close()
        f = open('./src/navbarMobile.html',"w")
        f.write('''
<div class="shadow-md w-full h-[80px] flex flex-row items-center justify-start px-4 block md:hidden">
	<p class="text-black text-3xl">{title}</p>

	<div class="w-full h-full flex flex-row items-center justify-end" onclick="mobNav()">
		<img src="{hamIcon}" class="h-[45px] justify-self-end" />
	</div>
</div>
<div class="w-full flex flex-col items-center justify-center gap-4 absolute left-0 right-0 bg-slate-200" id="mobNavView" style="display: none;">
	<div class="w-full text-lg flex items-center justify-center flex-wrap hover:bg-[#d9d9d9] cursor-pointer" onclick="navPage(0)">
		Home
	</div>
	<div class="w-full text-lg flex items-center justify-center flex-wrap hover:bg-[#d9d9d9] cursor-pointer" onclick="navPage(1)">
		About us
	</div>
</div>
        ''')
        f.close()
        f = open('./src/Home.html',"w")
        f.write('''
<div id="{id}" >
	<div class="flex flex-col w-full py-8 items-center px-2">
		<img src="{logoDark}" class="h-[120px]" />
		<p class="text-3xl mt-8 text-center">Welcome to Weber docs!🔥</p>
		<p class="text-xl mt-8 text-center">
			Weber provides html beginners a simple gateway into understanding larger frameworks such as React Js, Vue Js, etc...
			<br/>To get started, click <b class="text-blue-400 underline decoration-2 cursor-pointer" onclick="navPage(1)">here</b>
		</p>
	</div>
</div>
        ''')
        f.close()
        f = open('./src/About.html',"w")
        f.write('''
<div id="{id}">
	This is about page
</div>
        ''')
        f.close()
        f = open('./src/index.html',"w")
        f.write('''
<!DOCTYPE html>
<html>
	<head>
		<script src="https://cdn.tailwindcss.com"></script>
	</head>

	<body id="body">
		<? navbar title=Weber ?>
		<? navbarMobile title=Weber ?>

		<? Home id=Home ?>
		<? About id=About ?>

		<script src="index.js"></script>
	</body>
</html>
        ''')
        f.close()

       

    #creates a config file
    f = open('./config.json',"w")
    f.write(json.dumps(
        compileConfig,
    indent=4
    ))
