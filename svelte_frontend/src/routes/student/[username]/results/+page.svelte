<script lang="ts">
    import { onMount } from "svelte";
    import { refreshAccessToken } from '../../../../utils/auth';
    import { goto } from "$app/navigation";

    interface TestHistory {
        test_id: number;
        test_name: string;
        correct_count: number;
        question_count: number;
        score: number;
        completed_at: string;
    }

    let testHistory: TestHistory[] = [];
    let error: string = "";

    onMount(async () => {
        await fetchTestHistory();
    });

    async function fetchTestHistory(retry = true) {
        const access_token = sessionStorage.getItem("access_token");

        const response = await fetch("http://localhost:8000/history", {
            method: "GET",
            credentials: "include",
            headers: {
                Authorization: `Bearer ${access_token}`,
                "Content-Type": "application/json",
            },
        });

        if (response.ok) {
            testHistory = await response.json();
        } else if (response.status === 401) {
            if (retry) {
                await refreshAccessToken();
                await fetchTestHistory(false);
            } else {
                sessionStorage.removeItem("access_token");
                goto("/");
            }
        } else {
            const errorData = await response.json();
            error = `${errorData.message}`;
        }
    }

    function viewTestDetails(testId: number) {
        const access_token = sessionStorage.getItem("access_token");

        if (!access_token) {
            error = "Prieigos žetonas nerastas!";
            return;
        }

        try {
            const tokenParts = access_token.split('.');

            if (tokenParts.length !== 3) {
                error = "Neteisingas žetonas!";
                return;
            }

            const payload = JSON.parse(atob(tokenParts[1]));

            const userSub = payload.sub;

            if (!userSub) {
                error = "Žetonas neturi 'sub' lauko!";
                return;
            }

            goto(`/student/${userSub}/results/${testId}`);
        } catch (error) {
            console.error("Token parsing error:", error);
            error = "Nepavyko išgauti naudotojo duomenų iš žetono!";
        }
    }
</script>

<style>
    .test-history-wrapper {
        display: block;
        text-align: left;
        padding: 20px;
        width: 100%;
    }

    .test-history-title {
        font-size: 2rem;
        font-weight: bold;
        color: #000000;
        background-color: #fff;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 20px;
        text-align: center;
    }

    .test-history {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 20px;
        padding: 0;
        width: 100%;
        list-style-type: none;
    }

    .test-history li {
        background: #fff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: center; /* Center content vertically */
        align-items: center; /* Center content horizontally */
    }

    .test-history li strong {
        color: #333;
    }

    .test-history li.no-tests {
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
        width: 100%;
    }

    .test-action-buttons button {
        padding: 8px 16px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 1rem;
    }

    .test-action-buttons .view-details-btn {
        background-color: #4caf50;
        color: white;
    }

    @media (max-width: 768px) {
        .test-history {
            grid-template-columns: 1fr;
        }
    }
</style>

<div class="test-history-wrapper">
    <h2 class="test-history-title">Mano atlikti testai</h2>
    {#if testHistory.length === 0}
        <li class="no-tests">Dar nėra atliktų testų.</li>
    {/if}
    <div class="test-history">
        {#each testHistory as test}
            <li>
                <strong>Pavadinimas:</strong> {test.test_name}<br>
                <strong>Teisingi atsakymai:</strong> {test.correct_count} / {test.question_count}<br>
                <strong>Įvertinimas:</strong> {test.score}%<br>
                <strong>Atlikimo data:</strong> {new Date(test.completed_at).toLocaleDateString()}<br>

                <div class="test-action-buttons">
                    <button class="view-details-btn" on:click={() => viewTestDetails(test.test_id)}>Peržiūrėti atsakymus</button>
                </div>
            </li>
        {/each}
    </div>

    {#if error}
        <div class="error-message">{error}</div>
    {/if}
</div>
