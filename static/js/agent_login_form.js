const loginForm = document.getElementById('loginForm');
const errorMessage = document.querySelector('.error-message');
const successMessage = document.querySelector('.success-message');

loginForm.addEventListener('submit', (event) => {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username === '' || password === '') {
        errorMessage.textContent = 'Please fill all fields.';
        errorMessage.style.display = 'block';
        successMessage.style.display = 'none';
        return;
    }

    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/login'); // Replace with your actual backend endpoint
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = () => {
        if (xhr.status >= 200 && xhr.status < 300) {
            const response = JSON.parse(xhr.response);
            if (response.success) {
                successMessage.textContent = 'Login successful!';
                successMessage.style.display = 'block';
                errorMessage.style.display = 'none';
                // Redirect to the desired page after successful login
                window.location.href = '/';
            } else {
                errorMessage.textContent = response.message || 'Invalid credentials.';
                errorMessage.style.display = 'block';
                successMessage.style.display = 'none';
            }
        } else {
            errorMessage.textContent = 'An error occurred. Please try again later.';
            errorMessage.style.display = 'block';
            successMessage.style.display = 'none';
        }
    };
    xhr.onerror = () => {
        errorMessage.textContent = 'An error occurred. Please try again later.';
        errorMessage.style.display = 'block';
        successMessage.style.display = 'none';
    };

    const data = `username=${username}&password=${password}`;
    xhr.send(data);
});