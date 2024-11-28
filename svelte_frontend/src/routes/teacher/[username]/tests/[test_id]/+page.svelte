<script lang="ts">
    import { onMount, afterUpdate } from "svelte";
    import { page } from '$app/stores';
    import { goto } from "$app/navigation";
    import { refreshAccessToken } from '../../../../../utils/auth';

    interface Question {
        text: string;
        answer: string;
    }

    let testId: number;
    let testName = '';
    let testDescription = '';
    let questions: Question[] = [];
    let error: string = '';
    let access_token = sessionStorage.getItem("access_token");

    onMount(async () => {
        const { params } = $page;
        testId = Number(params.test_id);

        if (!access_token) {
            error = "Prieigos žetonas nerastas!";
            return;
        }

        const response = await fetch(`http://localhost:8000/test/${testId}`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${access_token}`,
                "Content-Type": "application/json",
            },
            credentials: "include",
        });

        if (response.ok) {
            const data = await response.json();
            testName = data.title;
            testDescription = data.description;
            questions = data.questions.map((q: any) => ({
                text: q.question_text,
                answer: q.correct_answer
            }));
        } else {
            const errorData = await response.json();
            error = errorData.detail || "Nepavyko užkrauti testo!";
        }
    });

    async function saveTest(retry = true) {
        const access_token = sessionStorage.getItem("access_token");

        if (!access_token) {
            error = "Prieigos žetonas nerastas!";
            return;
        }

        const decodedToken = JSON.parse(atob(access_token.split('.')[1]));
        const username = decodedToken.sub;

        const response = await fetch(`http://localhost:8000/test/${testId}`, {
            method: 'PATCH',
            headers: {
                "Authorization": `Bearer ${access_token}`,
                'Content-Type': 'application/json',
            },
            credentials: "include",
            body: JSON.stringify({
                test_id: testId,
                title: testName,
                description: testDescription,
                questions: questions.map(q => ({ text: q.text, correct_answer: q.answer }))
            }),
        });

        if (response.ok) {
            goto(`/teacher/${username}/tests`);
        } else if (response.status === 401) {
            if (retry) {
                await refreshAccessToken();
                await saveTest(false);
            } else {
                sessionStorage.removeItem("access_token");
                goto("/");
            }
        } else {
            const errorData = await response.json();
            error = errorData.detail || "Nepavyko išsaugoti testo!";
        }
    }

    function addQuestion() {
        questions = [...questions, { text: '', answer: '' }];
    }

    function removeQuestion(index: number) {
        questions = questions.filter((_, i) => i !== index);
    }

    function autoResize(event: Event) {
        const textarea = event.target as HTMLTextAreaElement;
        const maxWidth = 535;

        textarea.style.height = 'auto';
        textarea.style.height = `${textarea.scrollHeight}px`;

        textarea.style.whiteSpace = 'pre';
        textarea.style.width = 'auto';
        textarea.style.width = `${textarea.scrollWidth}px`;

        if (textarea.scrollWidth > maxWidth && textarea.scrollWidth > textarea.clientWidth) {
            textarea.style.overflowX = 'auto';
        } else {
            textarea.style.overflowX = 'hidden';
        }
    }

    afterUpdate(() => {
        const textareas = document.querySelectorAll('textarea');
        textareas.forEach((textarea) => {
            autoResize({ target: textarea });
        });
    });
</script>


<style>
    .form-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        background-color: #f4f6f9;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        max-width: 700px;
        margin: 20px auto;
        font-family: 'Arial', sans-serif;
    }

    .form-header {
        font-size: 1.5rem;
        margin-bottom: 20px;
        color: #333;
        text-align: center;
    }

    .styled-input {
        width: 100%;
        padding: 10px;
        margin: 10px 0;
        border: 1px solid #ddd;
        border-radius: 8px;
        font-size: 1rem;
        outline: none;
        transition: border-color 0.3s;
        box-sizing: border-box;
        resize: none;
    }
    .styled-input:focus {
        border-color: #4A90E2;
    }

    textarea {
        width: 100%;
        padding: 10px;
        margin: 10px 0;
        border: 1px solid #ddd;
        border-radius: 8px;
        font-size: 1rem;
        outline: none;
        resize: none;
        transition: border-color 0.3s;
        overflow-y: hidden;
        white-space: pre-wrap;
        word-wrap: break-word;
        min-width: 200px; 
        max-width: 100%;
    }

    .questions {
        font-size: large;
        margin-bottom: 15px;
        margin-top: 10px;
    }

    .question, .answer {
        display: flex;
        flex-direction: column;
        width: 100%;
        margin: 10px 0;
    }

    .question textarea, .answer textarea {
        margin-right: 10px;
    }

    .button-container {
        display: flex;          
        gap: 10px;               
        justify-content: flex-start; 
        width: 100%;            
    }   

    .button {
        padding: 10px 20px;
        margin: 10px 0;
        border: none;
        border-radius: 8px;
        font-size: 1rem;
        cursor: pointer;
        transition: transform 0.2s ease, background-color 0.3s ease;
    }

    .button.add {
        background-color: #4A90E2;
        color: white;
    }

    .button.add:hover {
        background-color: #3e78c1;
        transform: translateY(-2px);
    }

    .button.delete {
        background-color: #e91111;
        color: white;
        margin-bottom: 40px;
    }

    .button.delete:hover {
        background-color: #c10f0f;
        transform: translateY(-2px);
    }

    .button.submit {
        background-color: #28a745;
        color: white;
        align-self: flex-end;
    }

    .button.submit:hover {
        background-color: #218838;
        transform: translateY(-2px);
    }

    .error {
        color: red;
        font-size: 0.9rem;
        margin-top: 10px;
    }
</style>

<div class="form-container">
    <h2 class="form-header">Redaguoti testą</h2>

    <input id="Testo pavadinimas" type="text" placeholder="Testo pavadinimas" bind:value={testName} required class="styled-input" />
    <textarea id="Testo aprašymas" placeholder="Testo aprašymas" bind:value={testDescription} rows="3" required on:input={autoResize}></textarea>

    {#if questions.length > 0}
    <h2 class="questions">Testo klausimai</h2>
    {/if}
    {#each questions as question, index}
        <h3>{index + 1} Klausimas</h3>
        <div id="question" class="question">
            <textarea
                rows="1"
                placeholder={`Klausimas ${index + 1}`}
                bind:value={question.text}
                on:input={autoResize}>
            </textarea>
        </div>
        <div id="answer" class="answer">
            <textarea
                rows="1"
                placeholder={`Atsakymas ${index + 1}`}
                bind:value={question.answer}  
                on:input={autoResize}>
            </textarea>
        </div>
        <button class="button delete" on:click={() => removeQuestion(index)}>Pašalinti klausimą</button>
    {/each}

    <div class="button-container">
        <button class="button add" on:click={addQuestion}>+ Pridėti klausimą</button>
        <button class="button submit" on:click={saveTest(true)}>Išsaugoti testą</button>
    </div>

    {#if error}
        <div class="error">{error}</div>
    {/if}
</div>
