let post_removal_btns = document.getElementsByClassName("remove-button-post")
let user_ban_btns = document.getElementsByClassName("ban-btn-user")
let user_unban_btns = document.getElementsByClassName("unban-btn-user")

console.log(user_ban_btns)
console.log(user_unban_btns)



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

function setup_user_bans(removal_btns) {
	for (let i = 0; i < removal_btns.length; i++) {
		removal_btns[i].addEventListener("click", function (e) {
			let target_id = e.target.id
			let xhr = new XMLHttpRequest()
			xhr.open("PATCH", `http://localhost:8080/users/ban/${target_id}`)
			xhr.send()
		})
	}
}


function setup_user_unbans(removal_btns) {
	for (let i = 0; i < removal_btns.length; i++) {
		removal_btns[i].addEventListener("click", function (e) {
			let target_id = e.target.id
			let xhr = new XMLHttpRequest()
			xhr.open("PATCH", `http://localhost:8080/users/unban/${target_id}`)
			xhr.send()
		})
	}
}

setup_post_buttons(post_removal_btns)
setup_user_bans(user_ban_btns)
setup_user_unbans(user_unban_btns)
