<script lang="ts">
    import "@/app.css";
    import { getInfoFromToken, logout } from '../../../utils/auth';
    import { onMount } from 'svelte';

    let userSub: string | null = null;

    onMount(() => {
        const token = sessionStorage.getItem('access_token');
        if (token) {
            const { sub } = getInfoFromToken(token);
            userSub = sub;
        }
    });

    const goToCreateTest = () => {
        if (userSub) {
            window.location.href = `/teacher/${userSub}/createTest`;
        }
    };

    const goToTests = () => {
        if (userSub) {
            window.location.href = `/teacher/${userSub}/tests`;
        }
    };

    const goToProfile = () => {
        if (userSub) {
            window.location.href = `/teacher/${userSub}`;
        }
    };
</script>

<style>
    .layout {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
        transition: filter 0.3s ease;
    }

    header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 20px;
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        position: sticky;
        top: 0;
        z-index: 1000;
    }

    header h1 {
        font-size: 1.5rem;
        color: #333;
        margin: 0 20px 0 0;
    }

    .header-buttons-left {
        display: flex;
        gap: 10px;
        margin-right: auto;
    }

    .header-buttons-right {
        display: flex;
        gap: 10px;
        margin-left: auto;
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

    .button-left {
        background-color: #357ABD;
    }

    main {
        flex: 1;
        padding: 20px;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: auto;
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

<div class="layout">
    <header>
        <h1>PHP Testavimo Platforma</h1>
        <div class="header-buttons-left">
            <button class="button button-left" on:click={goToProfile}>Profilis</button>
            <button class="button button-left" on:click={goToTests}>Mano testai</button>
            <button class="button button-left" on:click={goToCreateTest}>Testo kūrimas</button>
        </div>
        <div class="header-buttons-right">
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
