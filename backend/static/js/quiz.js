let socket;

function submitAnswer(questionId, selectedOption) {
    socket.send(JSON.stringify({
        action: 'submit_answer',
        question_id: questionId,
        answer: selectedOption
    }));
    document.getElementById('nextButton').disabled = false;
}


async function nextQuestion() {

    const roomCode = localStorage.getItem('roomCode');

    socket = new WebSocket(`ws://127.0.0.1:8000/ws/quiz/${roomCode}/`);

    const questionId = document.getElementById('questionNumber').innerText.split(' ')[1];
    const selectedOption = document.querySelector('.option-btn.selected').innerText;

    socket.onopen = function () {
        console.log('Connected to the server');

        //  submit the answer
        submitAnswer(questionId, selectedOption);

        if (socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({
                action: 'get_next_question'
            }));
        }


    }

    socket.onmessage = function (e) {
        const data = JSON.parse(e.data);

        if (data.type === 'next_question') {
            console.log(data);
            console.log(data.question.id);
            console.log(data.question.text);
            document.getElementById('questionNumber').innerText = `Question ${data.question.id}`;
            document.getElementById('questionText').innerText = data.question.text;

            const optionsContainer = document.getElementById('options');
            optionsContainer.innerHTML = '';

            data.question.options.forEach(option => {
                const optionButton = document.createElement('button');
                optionButton.className = 'btn btn-outline-primary btn-lg btn-block option-btn';
                optionButton.innerText = option;
                optionButton.onclick = function () {
                    selectOption(this);
                };

                optionsContainer.appendChild(optionButton);
            });

            document.getElementById('nextButton').disabled = true;
        } else if (data.type === 'leaderboard') {
            const leaderboard = document.getElementById('leaderboard');
            leaderboard.innerHTML = '';

            data.leaderboard.forEach((user, index) => {
                const leaderboardItem = document.createElement('li');
                leaderboardItem.className = 'list-group-item';
                leaderboardItem.innerHTML = `<span class="font-weight-bold">${index + 1}. ${user.username}</span> - ${user.score}`;

                leaderboard.appendChild(leaderboardItem);
            });
        }
        else if (data.type == 'submit_answer'){
            console.log(data);
        }
    };
};