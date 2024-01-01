document.addEventListener('DOMContentLoaded', () => {
    
    // Grab references to the HTML elements
    const addTidbitsButton = document.getElementById('addTidbitsButton');
    const reviewTidbitsButton = document.getElementById('reviewTidbitsButton');

    // Send user to page for adding new tidbits
    addTidbitsButton.addEventListener('click', () => {
        window.location.href = '/newtidbits';
    })

    // Send user to page for reviewing tidbits
    reviewTidbitsButton.addEventListener('click', () => {
        window.location.href = '/review';
    })
})