document.addEventListener('DOMContentLoaded', () => {
    
    // Initialize variables
    let currentTidbitIndex = 0; // Keeps track of the order of tidbits
    const reviewmap = new Map(); // Map to store tidbits that have been reviewed

    // Grab references to the HTML elements
    const tidbitContainer = document.getElementById('tidbitContainer');

    // Check if tidbitContainer exists and has the data-tidbits attribute
    if (!tidbitContainer || !tidbitContainer.getAttribute('data-tidbits')) {
        console.error('Tidbit container not found or missing data-tidbits attribute');
        return;
    }
    const tidbits = JSON.parse(tidbitContainer.getAttribute('data-tidbits'));

    const nextButton = document.getElementById('nextButton');
    const previousButton = document.getElementById('previousButton');
    const indexDisplay = document.getElementById('indexDisplay');
    const checkbox = document.getElementById('review_checkbox');
    const homeButton = document.getElementById('homeButton');

    /* 
    Updates the index display on the page based on the current page
    */
    function updateIndexDisplay(currentIndex, total) {
        indexDisplay.textContent = `${currentIndex + 1}/${total}`;
    }
    
    /* 
    Checks if the incoming page's checkbox has already been checked 
    and reflects it on the page
    */
    function checkCheckbox(index) {
        if (reviewmap.get(tidbits[index])) {
            checkbox.checked = true;
        }
        else {
            checkbox.checked = false;
        }
    }

    /*
    Displays the current tidbit on the page
    */
    function displayTidbit(index) {
        const tidbitContainer = document.getElementById('tidbitContainer');
        tidbitContainer.textContent = tidbits[index];
        
    }

    // Add event listeners

    /*
    When the checkbox is clicked, add or remove the tidbit from 
    the reviewmap data structure
    */
    checkbox.addEventListener('change', () => {
        if (checkbox.checked) {
            // Checkbox is checked, add tidbit to the data structure
            reviewmap.set(tidbits[currentTidbitIndex], true);
        } else {
            // Checkbox is unchecked, remove tidbit from the data structure
            reviewmap.delete(tidbits[currentTidbitIndex]);
        }
    });

    /*
    When the home button is clicked, redirect to the home page
    */
    homeButton.addEventListener('click', () => {
        window.location.href = '/';
    });
    
    /*
    When the next button is clicked, display the 
    next tidbit on the page
    */
    nextButton.addEventListener('click', () => {
        if (currentTidbitIndex < tidbits.length - 1) {
            currentTidbitIndex++;
            displayTidbit(currentTidbitIndex);
            checkCheckbox(currentTidbitIndex);
            previousButton.disabled = false;
            if (currentTidbitIndex === tidbits.length - 1) {
                nextButton.disabled = true;
                finishButton.disabled = false;
            }
        } else {
            nextButton.disabled = true;
        }
        updateIndexDisplay(currentTidbitIndex, tidbits.length);
    });

    /*
    When the previous button is clicked, display the
    previous tidbit on the page
    */
    previousButton.addEventListener('click', () => {
        if (currentTidbitIndex > 0) {
            currentTidbitIndex--;
            displayTidbit(currentTidbitIndex);
            checkCheckbox(currentTidbitIndex);
            nextButton.disabled = false;
            finishButton.disabled = true;
            if (currentTidbitIndex === 0) {
                previousButton.disabled = true;
            }
        } else {
            previousButton.disabled = true;
        }
        updateIndexDisplay(currentTidbitIndex, tidbits.length);
    })

    /*
    When the finish button is clicked, we're done. We send the
    tidbits checked as reviewed to the server (their indices
    stored in reviewmap) to be further processed and redirect 
    the user to the home page
    */
    finishButton.addEventListener('click', () => {
        fetch('/process-checked-tidbits', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(Array.from(reviewmap.keys())),
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error(error));
        
        window.location.href = '/';
    })

    // Initialize the screen showing the first tidbit

    // Case where there are no reviewable tidbits
    if (tidbits.length == 0) {
        tidbitContainer.textContent = "No tidbits currently up for review.";
        console.error('Tidbit container data-tidbits attribute is empty');
        ;
    }
    else {
        displayTidbit(currentTidbitIndex);
        previousButton.disabled = true;
        finishButton.disabled = true;
        updateIndexDisplay(currentTidbitIndex, tidbits.length);
    }
});
