const baseUrl = 'http://127.0.0.1:8000';
let projectsUrl = baseUrl +'/api/projects/';

let getProjects = () => {
	fetch(projectsUrl)
		.then(response => response.json())
		.then(projects => buildProjects(projects))
};


let buildProjects = (projects) => {
	let projectsWrapper = document.getElementById('projects--wrapper');
	projectsWrapper.innerHTML = '';
	let projectsList = '';
	for (let project of projects) {
		projectsList += `
			<div class="project--card">
				<img src="${baseUrl + project.featured_image}"/>
				<div>
					<div class="card--header">
						<h3>${project.title}</h3>
						<span class="vote--option" data-vote='up' data-project=${project.id}>&#43;</span>
						<span class="vote--option" data-vote='down' data-project=${project.id}>&#8722;</span>
					</div>
					<i><span class='vote-ratio'>${project.vote_ratio}</span>% Positive feedback</i>
					<p>${project.description.substring(0, 150)}</p>
				</div>
			</div>
		`
	}

	projectsWrapper.innerHTML = projectsList;

	// Add an event listener
	addVoteEvents();
};

let addVoteEvents = () => {
	let voteBtns = document.querySelectorAll('.vote--option');
		for (let btn of voteBtns) {
			btn.addEventListener('click', (e) => {
			let vote = e.target.dataset.vote;
			let project = e.target.dataset.project;
			let token = localStorage.getItem('token');

			fetch(`${projectsUrl + project}/vote/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${token}`
				},
				body: JSON.stringify({value: vote}),
			})
			.then(response => response.json())
			.then(data => getProjects())
		})
	}
}

getProjects();


const loginBtn = document.getElementById('login-btn');
const logoutBtn = document.getElementById('logout-btn');

token = localStorage.getItem('token');

if (token) {
	loginBtn.remove();
} else {
	logoutBtn.remove();
}

if (logoutBtn) {
	logoutBtn.addEventListener('click', (e) => {
		e.preventDefault();
		localStorage.removeItem('token');
		window.location = 'index.html';
	});
}
