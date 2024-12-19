// Mock API data
// Mock Quiz Data
const questions = [
    { id: 1, text: "What is 2 + 2?", options: ["3", "4", "5"], answer: "4" },
    { id: 2, text: "Capital of France?", options: ["Paris", "Rome", "Berlin"], answer: "Paris" },
    { id: 3, text: "Which planet is known as the Red Planet?", options: ["Earth", "Mars", "Venus"], answer: "Mars" }
];

let currentQuestionIndex = 0;

// Mock Leaderboard Data
const leaderboardData = [
    { name: "Alice", score: 120 },
    { name: "Bob", score: 110 },
    { name: "Charlie", score: 105 }
];

// Render leaderboard
function renderLeaderboard() {
    const leaderboard = document.getElementById("leaderboard");
    leaderboard.innerHTML = "";
    leaderboardData.forEach((player, index) => {
        const listItem = document.createElement("li");
        listItem.className = "list-group-item";
        listItem.innerHTML = `<strong>${index + 1}. ${player.name}</strong> - ${player.score} points`;
        leaderboard.appendChild(listItem);
    });
}

// Function to render the next question
function getNextQuestion() {
    const progressBar = document.getElementById('progressBar');
    const questionNumber = document.getElementById('questionNumber');
    const questionText = document.getElementById('questionText');
    const optionsContainer = document.getElementById('options');
    const nextButton = document.getElementById('nextButton');

    if (currentQuestionIndex < questions.length) {
        // Update progress bar
        const progress = ((currentQuestionIndex + 1) / questions.length) * 100;
        progressBar.style.width = `${progress}%`;

        // Update question content
        const question = questions[currentQuestionIndex];
        questionNumber.innerText = `Question ${currentQuestionIndex + 1}`;
        questionText.innerText = question.text;
        optionsContainer.innerHTML = '';

        question.options.forEach(option => {
            const button = document.createElement('button');
            button.className = 'btn btn-outline-primary btn-lg btn-block option-btn';
            button.innerText = option;
            button.onclick = () => selectOption(button);
            optionsContainer.appendChild(button);
        });

        nextButton.disabled = true;
        currentQuestionIndex++;
    } else {
        // Quiz Completed
        questionNumber.innerText = "Quiz Completed!";
        questionText.innerText = "Congratulations! You've finished the quiz.";
        optionsContainer.innerHTML = '';
        nextButton.style.display = 'none';
    }
}

// Function to handle option selection
function selectOption(button) {
    const buttons = document.querySelectorAll('.option-btn');
    buttons.forEach(btn => btn.classList.remove('selected'));
    button.classList.add('selected');

    // Enable the Next button
    const nextButton = document.getElementById('nextButton');
    nextButton.disabled = false;
}

// Initialize first question and leaderboard
document.addEventListener('DOMContentLoaded', () => {
    getNextQuestion();
    renderLeaderboard();
});


function goToSignup() {
    alert("Redirect to Signup Page!");
    // Logic for redirecting to signup can be added here.
}

// For live dashboard (simulated)
setInterval(() => {
    const statsElement = document.getElementById('liveStats');
    if (statsElement) {
        statsElement.innerHTML = `
            <li>Users Online: ${Math.floor(Math.random() * 100)}</li>
            <li>Questions Answered: ${Math.floor(Math.random() * 1000)}</li>
        `;
    }
}, 2000);
