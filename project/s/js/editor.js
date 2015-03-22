// Global editor variables
var editor_section = document.getElementById('editor_section');
var view_section = document.getElementById('view_section');
var textAreaLines = 0;

// Form editor variables
var id_title = document.getElementById('id_title');
var id_body = document.getElementById('id_body');
var id_tag = document.getElementById('id_tag');
var id_pub_date = document.getElementById('id_pub_date');
var editor_hidden = false;

// Post view variables
var postTitle = document.getElementById('post_title');
var postBody = document.getElementById('post_content');
var postTag = document.getElementById('post_tag');
var postPubdate = document.getElementById('post_pub_date');


window.onload = function() {
	// textAreaAdjust(id_body);
	// textAreaScrollHeight = id_body.scrollHeight;
};

document.addEventListener('keydown', function(event) {
	if (event.shiftKey && event.location === KeyboardEvent.DOM_KEY_LOCATION_RIGHT) {
		if (!editor_hidden) {
			editor_section.style.display = 'none';
			view_section.style.display = 'block';
			editor_hidden = true;

			updatePreview();
			fluidvids.init();
		}
		else {
			editor_section.style.display = 'block';
			view_section.style.display = 'none';
			editor_hidden = false;
		}
	}
});

function updatePreview() {
	postBody.innerHTML = (marked(id_body.value));
	postTitle.innerHTML = id_title.value;
	postTitle.setAttribute('href', '/' + id_title.value.replace(/ |#/g,"_"));
	postTag.innerHTML = id_tag.value;
	postTag.setAttribute('href', '/tag/' + id_tag.value);
	postPubdate.innerHTML = id_pub_date.value;
}

// id_body.addEventListener('input', function(event) {
// 	// console.log(textAreaScrollHeight);
// 	// console.log(id_body.scrollHeight);
// 	console.log(id_body.getAttribute("rows"));
// 	if (textAreaScrollHeight != id_body.scrollHeight) {
// 		console.log('something');
// 		textAreaAdjust(this);
// 		textAreaScrollHeight = id_body.scrollHeight;
// 	}
// });

// function textAreaAdjust(event) {
// 	event.style.height = '1px';
// 	event.style.height = (25 + event.scrollHeight) + 'px';
// }