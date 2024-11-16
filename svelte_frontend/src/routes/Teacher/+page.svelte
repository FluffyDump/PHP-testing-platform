<script lang="ts">
    import { onMount } from 'svelte';

    // Define the interface for a Test
    interface Test {
        name: string;
        description: string;
    }

    let testName = '';
    let testDescription = '';
    let tests: Test[] = []; // Explicitly define tests as an array of Test objects
    let error: string = ''; // To capture any errors

    // Fetch created tests when the component mounts
    onMount(async () => {
        await fetchCreatedTests();
    });

    // Function to fetch tests created by the teacher
    async function fetchCreatedTests() {
        const response = await fetch('http://localhost:5000/tests'); // Adjust the endpoint as necessary
        if (response.ok) {
            tests = await response.json(); // Assuming the response is of type Test[]
        } else {
            const errorData = await response.json();
            console.error('Failed to fetch tests:', errorData.message);
            error = 'Failed to load tests.';
        }
    }

    // Function to add a new test
    async function addTest() {
        const response = await fetch('http://localhost:5000/tests', {
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
            // Reset form fields
            testName = '';
            testDescription = '';
            // Re-fetch tests to include the new one
            await fetchCreatedTests();
            error = ''; // Clear any previous errors
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
        <button on:click={addTest}>Add Test</button>
        {#if error}
            <div class="error">{error}</div> <!-- Show error message -->
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
