function generatePoem() {
    const prompt = document.getElementById('prompt').value;
    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `prompt=${encodeURIComponent(prompt)}`
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById('poem').innerText = data;
    })
    .catch(error => console.error('Error:', error));
}
