function video_thumb() {
	var v = document.getElementsByClassName('youtube-player');
	for (var n = 0; n < v.length; n++) {
		var p = document.createElement('div');
		p.innerHTML = labnolThumb(v[n].dataset.id);
		p.onclick = labnolIframe;
		v[n].appendChild(p);
	}
};
 
function labnolThumb(id) {
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

	return '<img id="thumb_' + id + '" class="youtube-thumb" src="' + thumb_url + '" ><div class="play-button"></div>';
}
 
function labnolIframe() {
	var iframe = document.createElement('iframe');
	iframe.setAttribute('src', '//www.youtube.com/embed/' + this.parentNode.dataset.id + '?autoplay=1&border=0');
	iframe.setAttribute('frameborder', '0');
	iframe.setAttribute('id', 'youtube-iframe');
	iframe.setAttribute('allowfullscreen', '1');
	this.parentNode.replaceChild(iframe, this);
}

video_thumb();