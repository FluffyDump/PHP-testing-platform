<script lang="ts">
	import { goto } from "$app/navigation";
    import { onMount } from "svelte";
    import { refreshAccessToken } from '../../../utils/auth';

    interface Test {
        title: string;
        description: string;
        question_count: number;
        created_at: Date;
    }

    let testName = '';
    let testDescription = '';
    let tests: Test[] = [];
    let error: string = '';

    onMount(async () => {
        await fetchCreatedTests();
    });

    async function fetchCreatedTests(retry = true) {
        const access_token = sessionStorage.getItem("access_token");

        const response = await fetch('http://localhost:8000/tests', {
            method: "GET",
            credentials: "include",
            headers: {
                "Authorization": `Bearer ${access_token}`,
                "Content-Type": "application/json",
            }
        }
        );
        if (response.ok) {
            tests = await response.json();
            return tests;
        } else if (response.status === 401){
            if (retry) {
                await refreshAccessToken();
                await fetchCreatedTests(false);
            }
            else {
                sessionStorage.removeItem("access_token");
                goto("/")
            }
        } else {
            const errorData = await response.json();
            error = `${errorData.message}`;
        }
    }

    async function addTest() {
        const response = await fetch('http://localhost:8000/tests', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: testName,
                description: testDescription,
            }),
        });

        if (response.ok) {
            console.log('Test added successfully!');
            testName = '';
            testDescription = '';
            await fetchCreatedTests();
            error = '';
        } else {
            const errorData = await response.json();
            console.error('Failed to add test:', errorData.message);
            error = errorData.message || 'Failed to add test.';
        }
    }
</script>

<style>
    .form {
        display: flex;
        flex-direction: column;
        margin: 20px; /* Margin for spacing */
        width: 300px; /* Width of the form */
        background-color: white; /* Background color of the form */
        border-radius: 8px; /* Rounded corners */
        padding: 20px; /* Padding inside the form */
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* Shadow for a modern look */
    }

    .error {
        color: red; /* Red color for error messages */
        font-size: 0.9rem; /* Smaller font size */
        margin-top: 5px; /* Space above error messages */
    }

    .test-list {
        margin: 20px;
        list-style-type: none; /* Remove bullet points */
        padding: 0; /* Remove padding */
    }

    .test-list li {
        background: #f9f9f9; /* Light background for list items */
        margin: 5px 0; /* Space between list items */
        padding: 10px; /* Padding inside list items */
        border-radius: 5px; /* Rounded corners for list items */
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
</style>

<div>
    <h2>Add New Test</h2>
    <div class="form">
        <input type="text" placeholder="Test Name" bind:value={testName} required />
        <input type="text" placeholder="Test Description" bind:value={testDescription} required />
        <button class="button" on:click={addTest}>Add Test</button>
        {#if error}
            <div class="error">{error}</div>
        {/if}
    </div>

    <h2>My Created Tests</h2>
    <ul class="test-list">
        {#each tests as test}
            <li>
                <strong>Title:</strong> {test.title}<br>
                <strong>Description:</strong> {test.description}<br>
                <strong>Question Count:</strong> {test.question_count}<br>
                <strong>Created At:</strong> {new Date(test.created_at).toLocaleString()}<br>
            </li>
        {/each}
        {#if tests.length === 0}
            <li>No tests created yet.</li>
        {/if}
    </ul>
</div>