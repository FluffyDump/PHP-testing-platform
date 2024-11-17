<script lang="ts">
    import { onMount } from "svelte";
    import { goto } from '$app/navigation';
    import { jwtDecode } from "jwt-decode";

    interface CustomJwtPayload {
        sub: string;
        role: string;
        exp: number;
    }

    let showRegisterForm = false;
    let showLoginForm = false;

    // Registration fields
    let username = '';
    let firstName = '';
    let lastName = '';
    let email = '';
    let password = '';
    let registrationError = ''; // Message for registration

    // Login fields
    let loginIdentifier = '';
    let loginPassword = '';
    let loginError = ''; // Error state for login

    let isLoading = true; // Track loading state for the blur effect

    // Function to get role from the JWT token
    function getRoleFromToken() {
        const token = localStorage.getItem("access_token");

        if (token) {
            try {
                const decoded = jwtDecode<CustomJwtPayload>(token);
                return decoded.role;
            } catch (error) {
                console.error("Invalid token:", error);
                return null;
            }
        }
        return null;
    }

    // On component mount, check for the JWT token and role
    onMount(() => {
        const role = getRoleFromToken();
        isLoading = false; // Stop loading once the token check is done

        if (role) {
            goto(`/secured/${role}`);
        }
    });

    function toggleRegister() {
        showRegisterForm = !showRegisterForm;
        showLoginForm = false;
        registrationError = '';
    }

    function toggleLogin() {
        showLoginForm = !showLoginForm;
        showRegisterForm = false;
        loginError = '';
    }

    // Handle user registration
    async function registerUser() {
        const response = await fetch('http://localhost:8000/register', { 
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

        const responseJson = await response.json();
        registrationError = responseJson.message;

        if (response.ok) {
            registrationError = '';
            goto('/secured/Student');
        }
    }

    // Handle user login
    async function loginUser() {
        const response = await fetch('http://localhost:8000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: "include",
            body: JSON.stringify({
                login_identifier: loginIdentifier,
                password: loginPassword,
            }),
        });

        if (response.ok) {
            loginError = '';
            const responseData = await response.json();

            if (responseData.role) {
                localStorage.setItem("access_token", responseData.access_token);
                goto(`/secured/${responseData.role}`);
            } else {
                loginError = responseData.message;
            }
        } else {
            const errorData = await response.json();
            loginError = errorData.message || 'Invalid username/email or password!';
        }
    }

</script>

<style>
    /* Add basic styling for the main container */
    .main {
        display: flex;
        flex-direction: column;
        align-items: center; /* Center horizontally */
        justify-content: center; /* Center vertically */
        height: 100vh; /* Full height */
        text-align: center; /* Center text */
        transition: filter 0.3s ease; /* Smooth transition for blur effect */
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

<div class="main" style="filter: blur({isLoading ? '10px' : '0px'})">
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
            <input type="text" bind:value={loginIdentifier} placeholder="Vartotojo vardas" />
            <input type="password" bind:value={loginPassword} placeholder="Slaptažodis" />
            <button on:click={loginUser}>Prisijungti</button>
            {#if loginError}
                <div class="error">{loginError}</div>
            {/if}
        </div>
    {/if}
</div>
