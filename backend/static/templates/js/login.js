document.getElementById('loginForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('http://127.0.0.1:8000/api/login/', { // Replace with your login API endpoint
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('authToken', data.token); // Store token for authenticated requests
            window.location.href = 'room.html'; // Redirect to room code page
        } else {
            alert('Invalid login credentials');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during login.');
    }
});

function goToSignup() {
    window.location.href = 'signup.html'; // Redirect to signup page
}
