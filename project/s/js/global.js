// global
var link_panel = document.getElementById('link_panel');
var mid_panel = document.getElementById('mid_panel');
var info_panel = document.getElementById('info_panel');
if (show_info) { info_panel.style.display = 'block'; }

var link_nav_link = document.getElementById('link_nav_link');
var mid_nav_link = document.getElementById('mid_nav_link');
var info_nav_link = document.getElementById('info_nav_link');
if (show_info) { info_nav_link.style.display = 'inline-block'; }


// UI logic related
var main_panel = 2; // 1 == link, 2 == mid, 2 == info
var window_width = window.innerWidth;


document.addEventListener('DOMContentLoaded', function() {
	window_width = window.innerWidth;
	set_show_mode();
});


window.addEventListener('resize', function(event){
	window_width = window.innerWidth;
	set_show_mode();
});


$(document).swipeLeft(function(){
	if ( main_panel == 1 ) {
		main_panel = 2;
		set_panel_visibility();
	}
	else if ( main_panel == 2 ) {
		main_panel = 3;
		set_panel_visibility();
	}
})


$(document).swipeRight(function(){
	if ( main_panel == 3 ) {
		main_panel = 2;
		set_panel_visibility();
	}
	else if ( main_panel == 2 ) {
		main_panel = 1;
		set_panel_visibility();
	}
})


link_nav_link.addEventListener('click', function() {
	main_panel = 1;
	set_panel_visibility();
});

mid_nav_link.addEventListener('click', function() {
	main_panel = 2;
	set_panel_visibility();
});

info_nav_link.addEventListener('click', function() {
	main_panel = 3;
	set_panel_visibility();
});


function set_show_mode() {
	if (window_width > 950) { show_mode = 2; }
	else { show_mode = 1; }

	set_panel_visibility();
}


function set_selected() {
	if (main_panel == 1) {
		link_nav_link.classList.add('li_selected');
		mid_nav_link.classList.remove('li_selected');
		info_nav_link.classList.remove('li_selected');
	}
	else if (main_panel == 2) {
		link_nav_link.classList.remove('li_selected');
		mid_nav_link.classList.add('li_selected');
		info_nav_link.classList.remove('li_selected');
	}
	else if (main_panel == 3) {
		link_nav_link.classList.remove('li_selected');
		mid_nav_link.classList.remove('li_selected');
		info_nav_link.classList.add('li_selected');
	}
}


function set_panel_visibility() {
	if (show_mode == 2) {
		link_panel.style.display = 'block';
		mid_panel.style.display = 'block';
		if (show_info) { info_panel.style.display = 'block' };
	}
	else {
		if (main_panel == 1) {
			link_panel.style.display = 'block';
			mid_panel.style.display = 'none';
			if (show_info) { info_panel.style.display = 'none' };
		}
		else if (main_panel == 2) {
			link_panel.style.display = 'none';
			mid_panel.style.display = 'block';
			if (show_info) { info_panel.style.display = 'none' };
		}
		else if (main_panel == 3) {
			link_panel.style.display = 'none';
			mid_panel.style.display = 'none';
			if (show_info) { info_panel.style.display = 'block' };
		}
		set_selected();
	}
}
