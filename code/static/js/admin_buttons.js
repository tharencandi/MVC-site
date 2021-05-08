console.log("akjsdhakjshdaksjdh")
let posts_uls = document.getElementsByClassName("user-post")

function get_post_obj(post_ul) {
	console.log(post_ul.length);
	for (let i = 0; i < post_ul.length; i++) {
		console.log(post_ul[i].childNodes)
	}
}

get_post_obj(posts_uls)
