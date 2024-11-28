<script lang="ts">
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";
    import { refreshAccessToken } from '../../../utils/auth';

    interface User {
        username: string;
        name: string;
        surname: string;
        email: string;
        registration_date: string;
    }

    let user: User | null = null;
    let error: string = '';

    onMount(async () => {
        await fetchUserData();
    });

    async function fetchUserData(retry = true) {
        const access_token = sessionStorage.getItem("access_token");

        const response = await fetch('http://localhost:8000/user', {
            method: "GET",
            credentials: "include",
            headers: {
                "Authorization": `Bearer ${access_token}`,
                "Content-Type": "application/json",
            }
        });

        if (response.ok) {
            user = await response.json();
        } else if (response.status === 401) {
            if (retry) {
                await refreshAccessToken();
                await fetchUserData(false);
            } else {
                sessionStorage.removeItem("access_token");
                goto("/");
            }
        } else {
            const errorData = await response.json();
            error = `${errorData.message}`;
        }
    }
</script>

<style>
    body {
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: flex-start;
        align-items: flex-start;
        height: 100vh;
    }

    .user-data {
        background: #fff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        position: absolute;
        top: 80px;
        left: 20px;
        width: auto;
        max-width: 600px;
    }

    .user-data h3 {
        margin: 0 0 10px;
        font-size: 1.6rem;
        color: #333;
    }

    .user-data p {
        margin: 5px 0;
        font-size: 1rem;
        color: #555;
    }
</style>

<div class="user-data">
    {#if user}
        <h3>Vartotojo duomenys</h3>
        <p><strong>Vardas:</strong> {user.name}</p>
        <p><strong>Pavardė:</strong> {user.surname}</p>
        <p><strong>Vartotojo vardas:</strong> {user.username}</p>
        <p><strong>El. paštas:</strong> {user.email}</p>
        <p><strong>Registracijos data:</strong> {new Date(user.registration_date).toLocaleDateString()}</p>
    {/if}
</div>
