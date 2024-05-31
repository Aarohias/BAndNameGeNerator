document.getElementById('bandNameForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    const form = event.target; // Get the form element
    const city = form.elements['city'].value.trim(); // Get the value of the city input
    const pet = form.elements['pet'].value.trim(); // Get the value of the pet input

    if (!city || !pet) {
        document.getElementById('result').textContent = 'Please fill out both fields.';
        return;
    }

    fetch('http://127.0.0.1:5000/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ city: city, pet: pet })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('result').textContent = 'Your band name could be ' + data.bandName;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').textContent = 'An error occurred while generating the band name. Please try again.';
    });
});
