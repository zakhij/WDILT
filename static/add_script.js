document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('tidbitForm');
    const tidbitText = document.getElementById('tidbitText');

    document.getElementById('homeButton').addEventListener('click', () => {
        window.location.href = '/';
    });

    form.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent the default form submission

        const text = tidbitText.value;

        fetch('/submit-tidbit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: tidbitText.value }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Tidbit submitted:', data);
            tidbitText.value = ''; // Clear the textbox
        })
        .catch(error => console.error('Error:', error));
    });
});
