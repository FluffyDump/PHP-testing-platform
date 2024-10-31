<script lang="ts">
    let showRegisterForm = false;
    let showLoginForm = false;

    // Registration fields
    let username = '';
    let firstName = '';
    let lastName = '';
    let email = '';
    let password = '';
    let registrationError = ''; // Error state for registration

    // Login fields
    let loginUsername = '';
    let loginPassword = '';
    let loginError = ''; // Error state for login

    function toggleRegister() {
        showRegisterForm = !showRegisterForm;
        showLoginForm = false; // Hide login form when showing register
        registrationError = ''; // Reset error message
    }

    function toggleLogin() {
        showLoginForm = !showLoginForm;
        showRegisterForm = false; // Hide register form when showing login
        loginError = ''; // Reset error message
    }

    async function registerUser() {
        const response = await fetch('http://localhost:5000/register', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username,
                firstName,
                lastName,
                email,
                password,
            }),
        });

        if (response.ok) {
            console.log('Registration successful!');
            username = '';
            firstName = '';
            lastName = '';
            email = '';
            password = '';
            registrationError = ''; // Clear any previous errors
        } else {
            const errorData = await response.json();
            registrationError = errorData.message || 'Registration failed!';
        }
    }

    async function loginUser() {
    const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: loginUsername,
            password: loginPassword,
        }),
    });

    if (response.ok) {
        const responseData = await response.json();  // Get the response data
        console.log('Login successful!');

        if (responseData.role === 'teacher') {
            window.location.href = '/Teacher';
        } else if (responseData.role === 'student') {
            window.location.href = '/Student';
        } else {
            console.error('User role is unknown.');
        }

        // Reset login fields after login
        loginUsername = '';
        loginPassword = '';
        loginError = ''; // Clear previous errors
    } else {
        const errorData = await response.json();
        loginError = errorData.message || 'Login failed!';
    }
}

</script>

<style>
    :global(html, body) {
        margin: 0;
        height: 100vh;
        padding: 0;
        font-family: Arial, sans-serif;
        overflow: hidden; /* Prevent scrolling */
        background: linear-gradient(270deg, #f0f4f8, #4A90E2, #f0f4f8);
        background-size: 400% 400%; /* Make the gradient larger for smooth movement */
        animation: gradientFlow 15s ease infinite; /* Animation for flowing effect */
    }

    @keyframes gradientFlow {
        0% {
            background-position: 0% 50%; /* Start position */
        }
        50% {
            background-position: 100% 50%; /* Middle position */
        }
        100% {
            background-position: 0% 50%; /* End position */
        }
    }

    /* Use flexbox to center items */
    .main {
        display: flex;
        flex-direction: column;
        align-items: center; /* Center horizontally */
        justify-content: center; /* Center vertically */
        height: 100vh; /* Full height */
        text-align: center; /* Center text */
    }

    h1 {
        font-size: 2.5rem;
        color: #333;
        margin-bottom: 10px; /* Space below the header */
    }

    p {
        font-size: 1.2rem;
        color: #555;
        margin: 5px 0; /* Space between paragraphs */
    }

    .button {
        padding: 10px 20px;
        margin: 10px; /* Space around buttons */
        border: none;
        border-radius: 5px;
        background-color: #4A90E2;
        color: white;
        font-size: 1rem;
        cursor: pointer;
        transition: background-color 0.3s, transform 0.2s;
    }

    .button:hover {
        background-color: #357ABD;
        transform: scale(1.05);
    }

    .form {
        display: flex;
        flex-direction: column;
        margin-top: 20px;
        width: 300px;
        background-color: white;
        border-radius: 8px; 
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    .form input {
        margin: 10px 0;
        padding: 10px;
        border: 1px solid #ccc; 
        border-radius: 5px;
    }

    .form button {
        margin-top: 10px;
        padding: 10px;
        border: none;
        border-radius: 5px;
        background-color: #4A90E2;
        color: white;
        cursor: pointer;
        transition: background-color 0.3s, transform 0.2s;
    }

    .form button:hover {
        background-color: #357ABD;
        transform: scale(1.05); 
    }

    .error {
        color: red; 
        font-size: 0.9rem; 
        margin-top: 5px; 
    }
</style>

<div class="main">
    <h1>PHP testavimo platforma</h1>
    <p>Autorius: Tomas Petrauskas</p>

    <div>
        <button class="button" on:click={toggleRegister}>Registruotis</button>
        <button class="button" on:click={toggleLogin}>Prisijungti</button>
    </div>

    {#if showRegisterForm}
        <div class="form">
            <h2>Registravimasis</h2>
            <input type="text" placeholder="Vartotojo vardas" bind:value={username} required />
            <input type="text" placeholder="Vardas" bind:value={firstName} required />
            <input type="text" placeholder="Pavardė" bind:value={lastName} required />
            <input type="email" placeholder="Elektroninis paštas" bind:value={email} required />
            <input type="password" placeholder="Slaptažodis" bind:value={password} required />
            <button type="button" on:click={registerUser}>Registruotis</button>
            {#if registrationError}
                <div class="error">{registrationError}</div> 
            {/if}
        </div>
    {/if}

    {#if showLoginForm}
        <div class="form">
            <h2>Prisijungimas</h2>
            <input type="text" bind:value={loginUsername} placeholder="Vartotojo vardas" />
            <input type="password" bind:value={loginPassword} placeholder="Slaptažodis" />
            <button on:click={loginUser}>Prisijungti</button>
            {#if loginError}
                <div class="error">{loginError}</div>
            {/if}
        </div>
    {/if}
</div>