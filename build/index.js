
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
//activeIndex = parseInt(new URL(window.location).searchParams.get("id"));

if(new URL(window.location).searchParams.has("id"))
{
	activeIndex = parseInt(new URL(window.location).searchParams.get("id"));
}

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

window.onunload = (e)=>
{
	console.log('test')
	window.location = "/build/index.html?id=" + activeIndex.toString()
}

function navPage(a)
{
	activeIndex = a;
	for (let index = 0; index < paths.length; index++) {
		console.log(index)
		if(a == index){
			document.getElementById(paths[index]).style.display = "block";
			window.history.replaceState({id: paths[index]}, paths[index], "/"+paths[index])
		}
		else{
			document.getElementById(paths[index]).style.display = "none";
		}
	}
	
}
navPage(activeIndex)