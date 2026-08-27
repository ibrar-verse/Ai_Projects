const baseUrl = window.location.origin;
let isProcessing = false;

// 1. Sanitize user input
const cleanTextInput = (value) => {
  return value
    .trim()
    .replace(/<[^>]*>/g, ""); // strip HTML tags
};

// 2. Scroll chat container to bottom
const scrollToBottom = () => {
  const chatMessages = document.getElementById("message-list");
  chatMessages.scrollTop = chatMessages.scrollHeight;
};

// 3. UI Helpers for Loading State
const showLoading = () => {
  isProcessing = true;
  $(".loading-animation").show();
  $("#send-button").prop("disabled", true);
  $("#status-text").text("Thinking...");
  scrollToBottom();
};

const hideLoading = () => {
  isProcessing = false;
  $(".loading-animation").hide();
  $("#send-button").prop("disabled", false);
  $("#status-text").text("Ready");
  scrollToBottom();
};

// 4. Render User Message
const populateUserMessage = (userMessage) => {
  $("#message-input").val("");
  $("#message-list").append(
    `<div class="message-line my-text">
       <div class="message-box my-text">${userMessage}</div>
     </div>`
  );
  scrollToBottom();
};

// 5. Render Bot Response
const populateBotResponse = (botMessage) => {
  $("#message-list").append(
    `<div class="message-line">
       <div class="message-box bot-text">${botMessage}</div>
     </div>`
  );
  scrollToBottom();
};

// 6. Send User Question to Flask Backend
const processUserMessage = async (userMessage) => {
  showLoading();
  try {
    const response = await fetch(`${baseUrl}/process-message`, {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ userMessage }),
    });

    const data = await response.json();
    populateBotResponse(data.botResponse || "Sorry, no response received.");
  } catch (error) {
    populateBotResponse(`⚠️ Connection error: ${error.message}`);
  } finally {
    hideLoading();
  }
};

// 7. Event: Submit Message via Click or Enter Key
const handleSendMessage = () => {
  const rawInput = $("#message-input").val();
  const cleanInput = cleanTextInput(rawInput);

  if (cleanInput && !isProcessing) {
    populateUserMessage(cleanInput);
    processUserMessage(cleanInput);
  }
};

$("#send-button").on("click", handleSendMessage);
$("#message-input").on("keypress", (e) => {
  if (e.which === 13) {
    handleSendMessage();
  }
});

// 8. Event: File Upload & Reader
$("#file-upload").on("change", function () {
  const file = this.files[0];
  if (!file) return;

  if (file.type !== "application/pdf") {
    alert("Please upload a valid .pdf file.");
    return;
  }

  showLoading();
  $("#status-text").text(`Embedding ${file.name}...`);

  const reader = new FileReader();
  reader.readAsDataURL(file);

  reader.onload = async function (e) {
    try {
      const response = await fetch(`${baseUrl}/process-document`, {
        method: "POST",
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ fileData: e.target.result }),
      });

      const data = await response.json();
      populateBotResponse(data.botResponse || `📄 ${file.name} loaded successfully!`);
    } catch (error) {
      populateBotResponse(`⚠️ File upload failed: ${error.message}`);
    } finally {
      hideLoading();
      $("#file-upload").val(""); // reset file input
    }
  };
});

// 9. Event: Reset Chat
$("#reset-button").on("click", () => {
  $("#message-list").html(
    `<div class="message-line">
       <div class="message-box bot-text">
         👋 Chat reset. You can upload a new PDF or continue asking questions.
       </div>
     </div>`
  );
});

// 10. Event: Toggle Dark Mode
$("#light-dark-mode-switch").on("change", function () {
  $("body").toggleClass("dark-mode", this.checked);
});