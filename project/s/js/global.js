// global
var link_panel = document.getElementById('link_panel');
var mid_panel = document.getElementById('mid_panel');
var info_panel = document.getElementById('info_panel');

var links_nav_link = document.getElementById('links_nav_link');
var mid_nav_link = document.getElementById('mid_nav_link');
var info_nav_link = document.getElementById('info_nav_link');

// UI logic related
var show_mode = 3;
var mid_or_info = true; // true is show mid
var main_panel = 2; // 1 == link, 2 == mid, 2 == info

var window_width = window.innerWidth 


document.addEventListener('DOMContentLoaded', function() {
	window_width = window.innerWidth;
	set_show_mode();
});

window.addEventListener('resize', function(event){
	window_width = window.innerWidth;
	set_show_mode();
});


links_nav_link.addEventListener('click', function() {
	main_panel = 1;
	set_panel_visibility();
});

mid_nav_link.addEventListener('click', function() {
	main_panel = 2;
	mid_or_info = true;
	set_panel_visibility();
});

info_nav_link.addEventListener('click', function() {
	main_panel = 3;
	mid_or_info = false;
	set_panel_visibility();
});


function set_show_mode() {
	if (window_width > 950) { show_mode = 3; }
	else if ( window_width > 600 && window_width < 950) { show_mode = 2; }
	else if ( window_width < 600) { show_mode = 1; }

	set_panel_visibility();
}

function set_selected() {
	if (show_mode == 2 ) {
		mid_nav_link.classList.add('selected');
	}
	else if (show_mode == 1 ) {

	}
}

function set_panel_visibility() {
	if (show_mode == 3) {
		link_panel.style.display = 'block';
		mid_panel.style.display = 'block';
		info_panel.style.display = 'block';
	}
	else if (show_mode == 2 ) {
		link_panel.style.display = 'block';
		if (mid_or_info == true) {
			mid_panel.style.display = 'block';
			info_panel.style.display = 'none';
		}
		else if (mid_or_info == false) {
			mid_panel.style.display = 'none';
			info_panel.style.display = 'block';
		}
		set_selected();
	}
	else if(show_mode == 1) {
		if (main_panel == 1) {
			link_panel.style.display = 'block';
			mid_panel.style.display = 'none';
			info_panel.style.display = 'none';
		}
		else if (main_panel == 2) {
			link_panel.style.display = 'none';
			mid_panel.style.display = 'block';
			info_panel.style.display = 'none';
		}
		else if (main_panel == 3) {
			link_panel.style.display = 'none';
			mid_panel.style.display = 'none';
			info_panel.style.display = 'block';
		}
		set_selected();
	}
}