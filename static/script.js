async function sendLogin() {
    const email = document.getElementById("email").value;
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    if (!email.trim() || !username.trim() || !password.trim()) {
        alert("Please fill in all fields");
        return;
    }

    if (password.length < 6) {
        alert("Password must be at least 6 characters");
        return;
    }

    try {
        const response = await fetch("/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, username, password })
        });

        const data = await response.json();

        if (!response.ok || data.error) {
            alert(data.error || "Login failed");
            return;
        }

        alert(
            `Status: ${data.status}\nDisplay Name: ${data.display_name}\nUser ID: ${data.user_id}`
        );

        window.location.href = "/dashboard";

    } catch (err) {
        console.error(err);
        alert("Server unreachable");
    }
}
