<script lang="ts">
    import { onMount } from "svelte";
    import { refreshAccessToken } from '../../../../utils/auth';
    import { goto } from "$app/navigation";

    interface Test {
        title: string;
        description: string;
        question_count: number;
        created_at: Date;
        test_id: number;
    }

    let tests: Test[] = [];
    let error: string = "";

    onMount(async () => {
        await fetchCreatedTests();
    });

    async function fetchCreatedTests(retry = true) {
        const access_token = sessionStorage.getItem("access_token");

        const response = await fetch("http://localhost:8000/tests", {
            method: "GET",
            credentials: "include",
            headers: {
                Authorization: `Bearer ${access_token}`,
                "Content-Type": "application/json",
            },
        });

        if (response.ok) {
            tests = await response.json();
        } else if (response.status === 401) {
            if (retry) {
                await refreshAccessToken();
                await fetchCreatedTests(false);
            } else {
                sessionStorage.removeItem("access_token");
                goto("/");
            }
        } else {
            const errorData = await response.json();
            error = `${errorData.message}`;
        }
    }

    async function handleDelete(testId: number, retry=true) {
        const access_token = sessionStorage.getItem("access_token");

        if (!access_token) {
            error = "Prieigos žetonas nerastas!";
            return;
        }

        const decodedToken = JSON.parse(atob(access_token.split('.')[1]));
        const username = decodedToken.sub;

        const response = await fetch('http://localhost:8000/test', {
            method: 'DELETE',
            headers: {
                "Authorization": `Bearer ${access_token}`,
                'Content-Type': 'application/json',
            },
            credentials: "include",
            body: JSON.stringify({
                "test_id": testId
            }),
        });

        if (response.status === 204) {
            await fetchCreatedTests(true)
        } else if (response.status === 401) {
            if (retry) {
                await refreshAccessToken();
                await handleDelete(testId, false);
            }
            else {
                sessionStorage.removeItem("access_token");
                goto("/")
            }
        } else {
            const errorData = await response.json();
            error = errorData.detail || "Nepavyko pašalinti testo!";
        }
    }

    function handleEdit(testId: number) {
    const access_token = sessionStorage.getItem("access_token");
    if (!access_token) {
        error = "Prieigos žetonas nerastas!";
        return;
    }
    
    const decodedToken = JSON.parse(atob(access_token.split('.')[1]));
    const username = decodedToken.sub;

    goto(`/teacher/${username}/tests/${testId}`);
}

</script>

<style>
    .test-list-wrapper {
        display: block;
        text-align: left;
        padding: 20px;
        width: 100%;
    }

    .test-list-title {
        font-size: 2rem;
        font-weight: bold;
        color: #000000;
        background-color: #fff;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 20px;
        text-align: center;
    }

    .test-list {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 20px;
        padding: 0;
        width: 100%;
        list-style-type: none;
    }

    .test-list li {
        background: #fff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        position: relative;
    }

    .test-list li strong {
        color: #333;
    }

    .test-list li.no-tests {
        background: #f9f9f9;
        color: #777;
        text-align: left;
        padding: 20px;
        border-radius: 8px;
    }

    .test-action-buttons {
        display: flex;
        justify-content: space-between;
        margin-top: 10px;
    }

    .test-action-buttons button {
        padding: 8px 16px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 1rem;
    }

    .test-action-buttons .delete-btn {
        background-color: #ff6b6b;
        color: white;
    }

    .test-action-buttons .edit-btn {
        background-color: #4caf50;
        color: white;
    }

    @media (max-width: 768px) {
        .test-list {
            grid-template-columns: 1fr;
        }
    }
</style>

<div class="test-list-wrapper">
    <h2 class="test-list-title">Mano sukurti testai</h2>
    {#if tests.length === 0}
        <li class="no-tests">Dar nėra sukurtų testų.</li>
    {/if}
    <div class="test-list">
        {#each tests as test}
            <li>
                <strong>Pavadinimas:</strong> {test.title}<br>
                <strong>Aprašymas:</strong> {test.description}<br>
                <strong>Klausimų skaičius:</strong> {test.question_count}<br>
                <strong>Sukūrimo data:</strong> {new Date(test.created_at).toLocaleDateString()}<br>
                
                <div class="test-action-buttons">
                    <button class="edit-btn" on:click={() => handleEdit(test.test_id)}>Redaguoti</button>
                    <button class="delete-btn" on:click={() => handleDelete(test.test_id)}>Pašalinti</button>
                </div>
            </li>
        {/each}
    </div>
</div>