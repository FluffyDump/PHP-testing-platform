<script lang="ts">
    import "@/app.css";
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import { jwtDecode } from "jwt-decode";

    export let user: { name: string; role: string } | null;

    interface CustomJwtPayload {
        sub: string;
        role: string;
        exp: number;
    }

    let isLoading = true; // Track loading state for the blur effect

    // Check if the JWT token is valid
    function getRoleFromToken() {
        const token = localStorage.getItem("access_token");

        if (!token) {
            goto("/");
            return null;
        }

        try {
            const decoded = jwtDecode<CustomJwtPayload>(token);
            return decoded.role;
        } catch (error) {
            console.error("Invalid token:", error);
            goto("/");
            return null;
        }
    }

    onMount(() => {
        const role = getRoleFromToken();
        if (!role) return;

        const currentPath = window.location.pathname;
        const basePath = `/secured/${role}`;

        if (currentPath.startsWith(basePath)) {
            isLoading = false; // Token is valid, remove the blur effect
            return;
        }

        // Redirection based on role
        if (role === "teacher" && currentPath.startsWith("/secured/Student")) {
            goto("/secured/Teacher").then(() => {
                isLoading = false; // Update loading state after redirection
            });
        } else if (role === "student" && currentPath.startsWith("/secured/Teacher")) {
            goto("/secured/Student").then(() => {
                isLoading = false; // Update loading state after redirection
            });
        } else {
            goto(`/secured/${role}`).then(() => {
                isLoading = false; // Update loading state after redirection
            });
        }
    });

    function logout() {
        localStorage.removeItem("access_token");
        goto("/");
    }
</script>

<style>
    .layout {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
        transition: filter 0.3s ease; /* Smooth transition for blur effect */
    }

    header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 20px;
        background: rgba(255, 255, 255, 0.8); /* Semi-transparent for a modern look */
        backdrop-filter: blur(10px); /* Smooth blur for a glassy effect */
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* Subtle shadow */
        position: sticky;
        top: 0;
        z-index: 1000;
    }

    header h1 {
        font-size: 1.5rem;
        color: #333;
        margin: 0;
    }

    .user-info {
        font-size: 1rem;
        color: #333;
        margin-right: 15px;
    }

    .button {
        background-color: #e91111;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 8px 15px;
        cursor: pointer;
        font-size: 1rem;
        transition: background-color 0.3s ease;
    }

    .button:hover {
        background-color: #357ABD;
    }

    main {
        flex: 1;
        padding: 20px;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    footer {
        text-align: center;
        padding: 10px;
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        font-size: 0.9rem;
        color: #555;
        box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
    }
</style>

<div class="layout" style="filter: blur({isLoading ? '10px' : '0px'})">
    <header>
        <h1>PHP Testavimo Platforma</h1>
        <div>
            {#if user}
                <span class="user-info">{user.name} ({user.role})</span>
            {/if}
            <button class="button" on:click={logout}>Atsijungti</button>
        </div>
    </header>

    <main>
        <slot />
    </main>

    <footer>
        &copy; {new Date().getFullYear()} PHP testavimo platforma. Visos teisės saugomos.
    </footer>
</div>