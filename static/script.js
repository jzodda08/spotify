// script.js
document.getElementById('removerForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission

    // Get user inputs
    const clientId = document.getElementById('clientId').value;
    const clientSecret = document.getElementById('clientSecret').value;
    const redirectUri = document.getElementById('redirectUri').value;
    const playlistId = document.getElementById('playlistId').value;

    // Simulated response (replace this with actual API call)
    const outputDiv = document.getElementById('output');
    outputDiv.innerHTML = `<p>Removing duplicates from playlist ID: ${playlistId}...</p>`;

    // Simulate a delay for the API call
    setTimeout(() => {
        outputDiv.innerHTML += `<p>Duplicates removed successfully!</p>`;
    }, 2000);
});
