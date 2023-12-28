document.addEventListener('DOMContentLoaded', () => {
    let currentTidbitIndex = 0;
    const tidbitContainer = document.getElementById('tidbitContainer');
    const nextButton = document.getElementById('nextButton');
    const previousButton = document.getElementById('previousButton');
    const indexDisplay = document.getElementById('indexDisplay');
    const checkbox = document.getElementById('myCheckbox');
    const hashMap = new Map();

    // Check if tidbitContainer exists and has the data-tidbits attribute
    if (!tidbitContainer || !tidbitContainer.getAttribute('data-tidbits')) {
        console.error('Tidbit container not found or missing data-tidbits attribute');
        return;
    }
    const tidbits = JSON.parse(tidbitContainer.getAttribute('data-tidbits'));

    function updateIndexDisplay(currentIndex, total) {
        indexDisplay.textContent = `${currentIndex + 1}/${total}`;
    }
    
    function checkCheckbox(index) {
        if (hashMap.get(tidbits[index])) {
            checkbox.checked = true;
        }
        else {
            checkbox.checked = false;
        }
    }

    function displayTidbit(index) {
        const tidbitContainer = document.getElementById('tidbitContainer');
        tidbitContainer.textContent = tidbits[index];
        
    }

    checkbox.addEventListener('change', () => {
        if (checkbox.checked) {
            // Checkbox is checked, add tidbit to the data structure
            hashMap.set(tidbits[currentTidbitIndex], true);
        } else {
            // Checkbox is unchecked, remove tidbit from the data structure
            hashMap.delete(tidbits[currentTidbitIndex]);
        }
    });

    document.getElementById('homeButton').addEventListener('click', () => {
        window.location.href = '/';
    });
    
    document.getElementById('nextButton').addEventListener('click', () => {
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

    document.getElementById('previousButton').addEventListener('click', () => {
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

    document.getElementById('finishButton').addEventListener('click', () => {
        fetch('/process-checked-tidbits', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(Array.from(hashMap.keys())),
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error(error));
        
        window.location.href = '/';
    })

    // Initialize the screen showing the first tidbit
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
