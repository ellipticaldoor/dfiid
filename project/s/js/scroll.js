document.addEventListener('keydown', function(event) {
	if (event.shiftKey && event.location === KeyboardEvent.DOM_KEY_LOCATION_RIGHT) {
		$.ajax({
			type: "GET",
			url: "/ajax_content/",
			data: {
				"query" : "hooola",
			},
			success: searchSuccess,
			dataType: "html"
		});
	}
});

function searchSuccess(data, textStatus, jqXHR) {
	$("#posts_container").html(data);
}