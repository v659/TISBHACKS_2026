async function sendLogin() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    if (!username.trim() || !password.trim()) {
        alert("Please enter both username and password");
        return;
    }

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });

        if (!response.ok) {
            const text = await response.text();
            console.error("Server error:", response.status, text);
            alert("Login failed");
            return;
        }

        const data = await response.json();
        const returnedUsername = Object.keys(data)[0];
        alert(returnedUsername);
    } catch (error) {
        console.error('Connection failed:', error);
    }
}
