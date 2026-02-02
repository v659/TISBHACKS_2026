async function sendLogin() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    if (!username.trim() || !password.trim()) {
        alert("Please enter both username and password");
        return;
    }

    if (password.length < 6) {
        alert("Password must be at least 6 characters");
        return;
    }

    try {
        const response = await fetch("/api/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const data = await response.json();

        if (!response.ok || data.error) {
            alert(data.error || "Login failed");
            return;
        }

        alert(
            `Status: ${data.status}\nEmail: ${data.email}\nUser ID: ${data.user_id}`
        );


    } catch (err) {
        console.error(err);
        alert("Server unreachable");
    }
}

