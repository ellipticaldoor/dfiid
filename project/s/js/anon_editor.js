// global editor variables
var editor_section = document.getElementById('editor_section');
var view_section = document.getElementById('view_section');

// form editor variables
var id_title = document.getElementById('id_title');
var id_body = document.getElementById('id_body');
var editor_hidden = false;

// post view variables
var post_title = document.getElementById('post_title');
var post_content = document.getElementById('post_content');


document.addEventListener('keydown', function(event) {
	if (event.shiftKey && event.location === KeyboardEvent.DOM_KEY_LOCATION_RIGHT) {
		if (!editor_hidden) {
			editor_section.style.display = 'none';
			view_section.style.display = 'block';
			editor_hidden = true;

			update_preview();
		}
		else {
			editor_section.style.display = 'block';
			view_section.style.display = 'none';
			editor_hidden = false;
		}
	}
});

function update_preview() {
	post_content.innerHTML = (marked(id_body.value));
	post_title.innerHTML = id_title.value;
}