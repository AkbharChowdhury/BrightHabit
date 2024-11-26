window.onload = function () {
    document.querySelector('#like_toggle_form').addEventListener('submit', (e) => {
        e.preventDefault();
        toggleLike().then(data => {
            document.querySelector('#total_likes').textContent = data['total_likes']
            document.querySelector('#like_icon').setAttribute('class', `${data['liked_icon']} fa-heart fa-lg`)
        });
    });

    async function toggleLike() {
        try {
            const response = await fetch(document.querySelector('#url').value, {
                method: 'POST',
                body: JSON.stringify({'post_id': document.querySelector('#post_id').value}),
                headers: {
                    'Content-Type': 'application/json',
                    "X-CSRFToken": document.querySelector("input[name=csrfmiddlewaretoken]").value,
                },
            });
            return await response.json();
        } catch (error) {
            console.error('Error:', error.message);
        }
    }

}