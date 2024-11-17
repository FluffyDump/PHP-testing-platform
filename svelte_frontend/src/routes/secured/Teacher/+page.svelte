<script lang="ts">
    import { onMount } from 'svelte';

    interface Test {
        name: string;
        description: string;
    }

    let testName = '';
    let testDescription = '';
    let tests: Test[] = [];
    let error: string = '';

    onMount(async () => {
        await fetchCreatedTests();
    });


    async function fetchCreatedTests() {
        const response = await fetch('http://localhost:8000/tests');
        if (response.ok) {
            tests = await response.json();
        } else {
            const errorData = await response.json();
            console.error('Failed to fetch tests:', errorData.message);
            error = 'Failed to load tests.';
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
</style>

<div>
    <h2>Add New Test</h2>
    <div class="form">
        <input type="text" placeholder="Test Name" bind:value={testName} required />
        <input type="text" placeholder="Test Description" bind:value={testDescription} required />
        <button type="button" on:click={addTest}>Add Test</button>
        {#if error}
            <div class="error">{error}</div>
        {/if}
    </div>

    <h2>My Created Tests</h2>
    <ul class="test-list">
        {#each tests as test}
            <li>
                <strong>{test.name}</strong>: {test.description}
            </li>
        {/each}
        {#if tests.length === 0}
            <li>No tests created yet.</li>
        {/if}
    </ul>
</div>