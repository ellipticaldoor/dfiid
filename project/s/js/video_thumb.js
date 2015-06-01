function video_thumb() {
	var v = document.getElementsByClassName('youtube_player');
	for (var n = 0; n < v.length; n++) {
		var p = document.createElement('div');
		p.innerHTML = youtubeThumb(v[n].dataset.id);
		p.onclick = youtubeIframe;
		v[n].appendChild(p);
	}

	var w = document.getElementsByClassName('vimeo_player');
	for (var n = 0; n < w.length; n++) {
		var p = document.createElement('div');
		p.innerHTML = vimeoThumb(w[n].dataset.id);
		p.onclick = vimeoIframe;
		w[n].appendChild(p);
	}
};


function youtubeThumb(id) {
	var thumb_url = '//i.ytimg.com/vi/' + id + '/maxresdefault.jpg';
	var thumb_image_hq = '//i.ytimg.com/vi/' + id + '/hqdefault.jpg';
	var thumb_id = 'thumb_' + id;

	var thumbImg = new Image();

	thumbImg.onload = function() {
		if (thumbImg.width < 720) {
			var thumb_image = document.getElementById(thumb_id);
			thumb_image.setAttribute('src', thumb_image_hq);
			thumb_image.removeAttribute('id');
		}
	}

	thumbImg.src = thumb_url;

	return '<img id="thumb_' + id + '" class="thumb" src="' + thumb_url + '" ><div class="play_button"></div>';
}


function vimeoThumb(id) {
	var thumb_url = 'http://i.imgur.com/F9MdVFE.jpg'
	return '<img class="thumb" src="' + thumb_url + '" ><div class="play_button"></div>';
}


function youtubeIframe() {
	var iframe = document.createElement('iframe');
	iframe.setAttribute('src', '//www.youtube.com/embed/' + this.parentNode.dataset.id + '?autoplay=1');
	iframe.setAttribute('frameborder', '0');
	iframe.setAttribute('id', 'iframe');
	iframe.setAttribute('allowfullscreen', '1');
	this.parentNode.replaceChild(iframe, this);
}


function vimeoIframe() {
	var iframe = document.createElement('iframe');
	iframe.setAttribute('src', 'https://player.vimeo.com/video/' + this.parentNode.dataset.id + '?autoplay=1');
	iframe.setAttribute('frameborder', '0');
	iframe.setAttribute('id', 'iframe');
	iframe.setAttribute('allowfullscreen', '1');
	this.parentNode.replaceChild(iframe, this);
}

video_thumb();