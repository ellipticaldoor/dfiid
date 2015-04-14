var page_number = 2;

$(window).scroll(function() {
	if($(window).scrollTop() + $(window).height() == $(document).height()) {
		$.ajax({
			type: 'GET',
			url: '/',
			data: {
				'page' : page_number,
			},
			success: searchSuccess,
			dataType: 'html'
		});
   }
});

function searchSuccess(data, textStatus, jqXHR) {
	page_number = page_number + 1;
	$(data).insertAfter($('.post').last());
}