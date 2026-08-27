async function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value.trim();
    if (!message) return;

    const chatBox = document.getElementById("chat-box");

    // Display User Message
    const userDiv = document.createElement("div");
    userDiv.className = "message user-message";
    userDiv.innerText = message;
    chatBox.appendChild(userDiv);
    input.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    // Send HTTP POST request to Flask backend
    try {
        const response = await fetch("/chatbot", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt: message })
        });

        const botReply = await response.text();

        // Display Bot Reply
        const botDiv = document.createElement("div");
        botDiv.className = "message bot-message";
        botDiv.innerText = botReply;
        chatBox.appendChild(botDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    } catch (err) {
        console.error("Error communicating with chatbot:", err);
    }
}

// Allow Enter key to trigger send
document.getElementById("user-input").addEventListener("keypress", function (e) {
    if (e.key === "Enter") sendMessage();
});