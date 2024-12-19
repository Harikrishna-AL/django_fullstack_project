let socket;
let isHost = false; // Variable to track if the user is the host

async function joinRoom() {
    const roomCode = document.getElementById('roomCode').value.trim();

    // Store the room code in local storage
    localStorage.setItem('roomCode', roomCode);

    if (!roomCode) {
        alert('Please enter a room code');
        return;
    }

    const token = localStorage.getItem('authToken');
    try {
        document.getElementById('roomCodeDisplay').innerText = roomCode;

        // Establish WebSocket connection
        socket = new WebSocket(`ws://127.0.0.1:8000/ws/quiz/${roomCode}/`);

        socket.onopen = function () {
            console.log('WebSocket connection established');
            socket.send(JSON.stringify({
                action: 'join_room'
            }));

            socket.send(JSON.stringify({
                action: 'host_info'
            }));
        };

        socket.onmessage = function (event) {
            const data = JSON.parse(event.data);
            console.log('Message received:', data);

            if (data.type === 'room_update') {
                // Update the list of users
                const userList = document.getElementById('userList');
                const li = document.createElement('li');
                li.innerText = `${data.message}`;
                userList.appendChild(li);
            } else if (data.type === 'host_info_room') {
                // Check if the current user is the host
                isHost = data.message;
                console.log('Is host:', isHost);

                // Show the "Start Quiz" button if the user is the host
                if (isHost) {
                    document.getElementById('startQuizButton').classList.remove('d-none');
                }
            } else if (data.type === 'quiz_started') {
                // Redirect to quiz page
                window.location.href = 'quiz.html';
            }
        };

        socket.onclose = () => {
            console.log('WebSocket connection closed');
        };

        // Show the waiting screen
        document.getElementById('waitingArea').classList.remove('d-none');
        document.getElementById('loadingScreen').classList.add('d-none');
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while joining the room.');
    }
}

function startQuiz() {
    if (isHost) {
        // Notify the server to start the quiz
        socket.send(JSON.stringify({
            action: "start_quiz"
        }));
        console.log("Start quiz message sent!");
    } else {
        // Show a message if the user is not the host
        alert("Only the host can start the quiz.");
    }
}