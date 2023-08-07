let tags = document.getElementsByClassName('project-tag');

for (tag of tags) {
    tag.addEventListener('click', (e) => {
        let tagId = e.target.dataset.tag;
        let projectId = e.target.dataset.project;

        fetch('http://127.0.0.1:8000/api/remove-tag/', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    'project': projectId,
                    'tag': tagId
                })
            })
                .then(response => response.json())
                .then(data => {
                    e.target.remove();
                })
    });
}