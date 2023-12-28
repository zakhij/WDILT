document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('addTidbitsButton').addEventListener('click', () => {
        window.location.href = '/newtidbits';
    })
    document.getElementById('reviewTidbitsButton').addEventListener('click', () => {
        window.location.href = '/review';
    })
})