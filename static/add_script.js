document.addEventListener('DOMContentLoaded', () => {

    // Grab references to the HTML elements
    const form = document.getElementById('tidbitForm');
    const tidbitText = document.getElementById('tidbitText');
    const homeButton = document.getElementById('homeButton');

    // Redirect user to homepage if they click on the home button
    homeButton.addEventListener('click', () => {
        window.location.href = '/';
    });

    /*
    When the form is submitted, send the tidbit text the user
    wrote in the tidbit textbox to the server to be added
    as a new tidbit and clear the textbox
    */
    form.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent the default form submission

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
