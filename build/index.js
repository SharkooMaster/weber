
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

let activeIndex = 0;

addEventListener("popstate", (event)=>{
	for (let index = 0; index < paths.length; index++) {
		document.getElementById(paths[index]).style.display = "none";
		if(paths[index] === window.history.state["id"])
		{
			activeIndex = index
			document.getElementById(paths[index]).style.display = "block";
		}
	}
})

window.onbeforeunload = (e)=>
{
	if(e)
	{
		e.returnValue = "leaving"
	}
}

window.onunload = (e)=>
{
	console.log('test')
	window.location = "http://127.0.0.1:5500/build?id="+activeIndex
}

function navPage(a)
{
	activeIndex = a;
	for (let index = 0; index < paths.length; index++) {
		console.log(index)
		if(a == index){
			document.getElementById(paths[index]).style.display = "block";
			window.history.pushState({id: paths[index]}, paths[index], "/"+paths[index])
		}
		else{
			document.getElementById(paths[index]).style.display = "none";
		}
	}
	
}
navPage(0)