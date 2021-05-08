let post_removal_btns = document.getElementsByClassName("remove-button-post")
let user_removal_btns = document.getElementsByClassName("remove-btn-user")
console.log(user_removal_btns)

function setup_post_buttons(removal_btns) {
	for (let i = 0; i < removal_btns.length; i++) {
		removal_btns[i].addEventListener("click", function (e) {
			let target_id = e.target.id
			let xhr = new XMLHttpRequest()
			xhr.open("DELETE", `http://localhost:8080/posts/${target_id}`)
			xhr.send()
		})
	}
}

function setup_user_buttons (removal_btns) {
	for (let i = 0; i < removal_btns.length; i++) {
		removal_btns[i].addEventListener("click", function (e) {
			let target_id = e.target.id
			let xhr = new XMLHttpRequest()
			xhr.open("DELETE", `http://localhost:8080/users/${target_id}`)
			xhr.send()
		})
	}
}


setup_post_buttons(post_removal_btns)
setup_user_buttons(user_removal_btns)
