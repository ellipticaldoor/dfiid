// Global editor variables
var editor_section = document.getElementById('editor_section');
var view_section = document.getElementById('view_section');
var textAreaLines = 0;

// Form editor variables
var id_title = document.getElementById('id_title');
var id_body = document.getElementById('id_body');
var id_sub = document.getElementById('id_sub');
var id_pub_date = document.getElementById('id_pub_date');
var editor_hidden = false;

// Post view variables
var postTitle = document.getElementById('post_title');
var postBody = document.getElementById('post_content');
var postSub = document.getElementById('post_sub');
var postPubdate = document.getElementById('post_pub_date');


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
	postSub.innerHTML = id_sub.value;
	postSub.setAttribute('href', '/sub/' + id_sub.value);
	postPubdate.innerHTML = id_pub_date.value;
}