
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
		}
		else{
			document.getElementById(paths[index]).style.display = "none";
		}
	}
	navBarView_mobile.style.display = "none"
}
navPage(0)