const baseUrl = 'http://127.0.0.1:8000';
const loginForm = document.getElementById('login-form');

if (loginForm) {
	loginForm.addEventListener('submit', (e) => {
		e.preventDefault();
		let payload = {
			'username': loginForm.username.value,
			'password': loginForm.password.value 
		}
		let loginUrl = `${baseUrl}/api/users/token/`;
		fetch(loginUrl, {
			method: 'POST',
			headers: {
		      Accept: "application/json",
		      "Content-Type": "application/json",
		    },
		    body: JSON.stringify(payload),
		})
		.then(response => response.json())
		.then(token => {
			if (token.access) {
				localStorage.setItem('token', token.access);
				window.location = 'index.html';
			}
		})
	});
}
