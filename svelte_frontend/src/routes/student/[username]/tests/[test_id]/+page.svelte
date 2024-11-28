<script lang="ts">
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import { refreshAccessToken } from '../../../../../utils/auth';

    interface Question {
        question_id: number;
        question_text: string;
        correct_answer: string;
    }

    interface Test {
        test_id: number;
        title: string;
        description: string;
        questions: Question[];
    }

    let test: Test | null = null;
    let answers: { [key: number]: string } = {};
    let error: string = "";
    let isSubmitting: boolean = false;

    const testId = parseInt(window.location.pathname.split("/").pop() || "", 10);

    // Fetch test details and initialize answers with empty strings for all questions
    onMount(async () => {
        await fetchTestDetails();
    });

    async function fetchTestDetails(retry = true) {
        const access_token = sessionStorage.getItem("access_token");

        const response = await fetch(`http://localhost:8000/tests/${testId}`, {
            method: "GET",
            credentials: "include",
            headers: {
                Authorization: `Bearer ${access_token}`,
                "Content-Type": "application/json",
            },
        });

        if (response.ok) {
            test = await response.json();
            
            // Initialize answers object with empty strings for each question
            test.questions.forEach(question => {
                answers[question.question_id] = answers[question.question_id] || ""; // Ensure each question has an entry
            });
        } else if (response.status === 401) {
            if (retry) {
                await refreshAccessToken();
                await fetchTestDetails(false);
            } else {
                sessionStorage.removeItem("access_token");
                goto("/");
            }
        } else {
            const errorData = await response.json();
            error = `${errorData.message}`;
        }
    }

    // Function to check if all questions are answered
    function isFormComplete(): boolean {
        return test?.questions.every(question => answers[question.question_id]?.trim() !== "");
    }

    async function submitAnswers() {
        if (isSubmitting) return;

        const access_token = sessionStorage.getItem("access_token");

        if (!access_token) {
            error = "Prieigos žetonas nerastas!";
            return;
        }

        // Check if all questions are answered
        for (const question_id of Object.keys(answers)) {
            if (answers[parseInt(question_id)] === "") {
                error = "Visi klausimai turi būti atsakyti!";
                return;
            }
        }

        isSubmitting = true;

        const response = await fetch(`http://localhost:8000/tests/${testId}/submit`, {
            method: "POST",
            credentials: "include",
            headers: {
                Authorization: `Bearer ${access_token}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ answers }),
        });

        if (response.ok) {
            const result = await response.json();
            goto(`/tests/${testId}/result/${result.id}`);
        } else {
            const errorData = await response.json();
            error = `${errorData.message}`;
        }

        isSubmitting = false;
    }
</script>

<style>
    .test-taker-wrapper {
        padding: 20px;
    }

    .test-title {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 20px;
    }

    .test-description {
        font-size: 1.2rem;
        margin-bottom: 20px;
    }

    .question {
        background-color: #fff;
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    }

    .question label {
        font-size: 1.2rem;
        margin-bottom: 10px;
        display: block;
    }

    .question input {
        width: 100%;
        padding: 10px;
        font-size: 1rem;
        border: 1px solid #ccc;
        border-radius: 4px;
    }

    .submit-button {
        padding: 10px 20px;
        background-color: #4caf50;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 1rem;
        margin-top: 20px;
    }

    .submit-button:disabled {
        background-color: #ccc;
        cursor: not-allowed;
    }

    .error-message {
        color: red;
        font-size: 1rem;
        margin-top: 20px;
    }

    .test-taker-wrapper {
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
    background-color: #f9f9f9;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.test-title {
    color: #000000;
    margin-bottom: 15px;
    text-align: center;
}

.test-description {
    font-size: 1.2rem;
    color: #555;
    margin-bottom: 30px;
    text-align: left;
    line-height: 1.6;
    font-family: 'Arial', sans-serif;
    padding: 10px;
}

.question {
    background-color: #fff;
    padding: 20px;
    margin-bottom: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    border: 1px solid #f0f0f0;
}

.question label {
    font-size: 1.3rem;
    color: #333;
    margin-bottom: 10px;
    display: block;
    font-weight: 600;
}

.question input {
    width: 100%;
    padding: 12px;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin-top: 5px;
    box-sizing: border-box;
}

.submit-button {
    padding: 12px 25px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1.2rem;
    width: 100%;
    margin-top: 20px;
    transition: background-color 0.3s ease;
}

.submit-button:hover {
    background-color: #388e3c;
}

.submit-button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}

.error-message {
    color: red;
    font-size: 1rem;
    margin-top: 20px;
    text-align: center;
}

</style>

<div class="test-taker-wrapper">
    {#if test}
        <h2 class="test-title">{test.title}</h2>
        <p class="test-description">{test.description}</p>

        {#each test.questions as question}
            <div class="question">
                <label for="question-{question.question_id}">{question.question_text}</label>
                <input
                    id="question-{question.question_id}"
                    type="text"
                    placeholder="Atsakymas"
                    value={answers[question.question_id] || ""}
                    on:input={(e) => answers[question.question_id] = e.target.value}
                />
            </div>
        {/each}

        <button
            class="submit-button"
            on:click={submitAnswers}
            disabled={isSubmitting || !isFormComplete()}
        >
            {isSubmitting ? "Pateikiamas testas..." : "Baigti testą"}
        </button>
    {:else}
        <div class="error-message">{error || "Testas nerastas!"}</div>
    {/if}
</div>