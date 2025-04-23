const userId = "{{ user_id }}"; // User ID passed from the backend
const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message");
const messagesDiv = document.getElementById("messages");

// Connect to WebSocket
const protocol = window.location.protocol === "https:" ? "wss" : "ws";
const socket = new WebSocket(`${protocol}://${window.location.host}/ws/${userId}`);


// Handle incoming messages
socket.onmessage = (event) => {
    const message = event.data;
    const [senderId, messageText] = message.split(": ", 2); // Split sender ID and message text
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message");
    messageDiv.classList.add(senderId === userId ? "sent" : "received"); // Sent or received
    messageDiv.textContent = messageText;
    messagesDiv.appendChild(messageDiv);
};

// Send a message
chatForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const message = messageInput.value;

    // Display the message immediately
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", "sent");
    messageDiv.textContent = message;
    messagesDiv.appendChild(messageDiv);

    // Send the message via WebSocket
    socket.send(`${userId}: ${message}`);

    messageInput.value = ""; // Clear the input field
});
