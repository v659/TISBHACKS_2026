document.getElementById('btn').addEventListener('click', async () => {
    try {
        const response = await fetch('/api/greet');
        const data = await response.json();
        document.getElementById('output').innerText = data.message;
    } catch (error) {
        console.error('Connection failed:', error);
    }
});
