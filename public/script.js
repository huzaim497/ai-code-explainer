
/* ==========================================
   AI CODE EXPLAINER
   Frontend JavaScript Logic
========================================== */

// 1. Get HTML Elements

const explainBtn = document.getElementById("explainBtn");
const copyBtn = document.getElementById("copyBtn");

const codeInput = document.getElementById("code");
const languageSelect = document.getElementById("language");
const levelSelect = document.getElementById("level");

const summaryElement = document.getElementById("summary");
const stepsElement = document.getElementById("steps");
const suggestionsElement = document.getElementById("suggestions");

const errorMessage = document.getElementById("errorMessage");


// 2. Backend API URL

const API_URL = "/api/explain";


// 3. Show Error Message

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.hidden = false;
}


// 4. Clear Error Message

function clearError() {
    errorMessage.textContent = "";
    errorMessage.hidden = true;
}


// 5. Display AI Explanation

function displayExplanation(data) {

    // Display summary
    summaryElement.textContent = data.summary;

    // Display step-by-step explanation
    stepsElement.replaceChildren();

    data.steps.forEach((step) => {

        const listItem = document.createElement("li");

        listItem.textContent = step;

        stepsElement.appendChild(listItem);

    });


    // Display suggestions
    suggestionsElement.replaceChildren();

    data.suggestions.forEach((suggestion) => {

        const listItem = document.createElement("li");

        listItem.textContent = suggestion;

        suggestionsElement.appendChild(listItem);

    });

    // Enable copy button
    copyBtn.disabled = false;

}


// 6. Explain Code Button Functionality

explainBtn.addEventListener("click", async () => {

    // Get user input
    const code = codeInput.value.trim();

    const language = languageSelect.value;

    const level = levelSelect.value;

    clearError();


    // Validate empty code
    if (!code) {

        showError("Please enter your source code first.");

        return;

    }


    // Loading state
    explainBtn.disabled = true;

    explainBtn.textContent = "Generating Explanation...";

    copyBtn.disabled = true;


    try {

        // Send request to FastAPI backend
        const response = await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                code: code,

                language: language,

                level: level

            })

        });


        // Convert response into JSON
        const data = await response.json();
        console.log("BACKEND RESPONSE:", data);


        // Check response status
        if (!response.ok) {

            throw new Error(
                data.detail || "Unable to explain the code."
            );

        }


        // Display AI explanation
        displayExplanation(data);


    } catch (error) {

        // Handle connection and API errors
        if (error.message.includes("Failed to fetch")) {

            showError(
                "Backend is not connected. Please start the backend server."
            );

        } else {

            showError(error.message);

        }

    } finally {

        // Restore button
        explainBtn.disabled = false;

        explainBtn.textContent = "Explain Code";

    }

});


// 7. Copy Result Functionality

copyBtn.addEventListener("click", async () => {

    const summary = summaryElement.textContent;


    const steps = Array.from(stepsElement.children)

        .map((item, index) => {

            return `${index + 1}. ${item.textContent}`;

        })

        .join("\n");


    const suggestions = Array.from(suggestionsElement.children)

        .map((item) => {

            return `- ${item.textContent}`;

        })

        .join("\n");


    // Prepare complete explanation
    const finalText =

        `CODE SUMMARY\n${summary}\n\n` +

        `STEP-BY-STEP EXPLANATION\n${steps}\n\n` +

        `ISSUES & IMPROVEMENTS\n${suggestions}`;


    try {

        await navigator.clipboard.writeText(finalText);

        copyBtn.textContent = "Copied!";

        setTimeout(() => {

            copyBtn.textContent = "Copy Result";

        }, 1500);


    } catch (error) {

        showError("Unable to copy the explanation.");

    }

});
