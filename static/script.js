// Global variables
let isTyping = false;

// Handle Enter key press
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// Send quick message from buttons
function sendQuickMessage(message) {
    const input = document.getElementById("userInput");
    input.value = message;
    sendMessage();
}

// Main function to send message
async function sendMessage() {
    const input = document.getElementById("userInput");
    const sendButton = document.getElementById("sendButton");
    const chatbox = document.getElementById("chatbox");
    const message = input.value.trim();
    
    if (!message || isTyping) return;

    // Disable input and button
    input.disabled = true;
    sendButton.disabled = true;
    isTyping = true;

    // Add user message to chat
    addUserMessage(message);
    
    // Clear input
    input.value = "";

    // Show typing indicator
    showTypingIndicator();

    try {
        // Send to backend
        const response = await fetch("/chat", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify({ message })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        // Hide typing indicator
        hideTypingIndicator();
        
        // Add bot response
        addBotMessage(data.answer || "I'm sorry, I couldn't process your request. Please try again.");

    } catch (error) {
        console.error('Error:', error);
        
        // Hide typing indicator
        hideTypingIndicator();
        
        // Show error message
        addBotMessage("I'm sorry, I'm having trouble connecting right now. Please check your internet connection and try again.");
    } finally {
        // Re-enable input and button
        input.disabled = false;
        sendButton.disabled = false;
        isTyping = false;
        
        // Focus back on input
        input.focus();
    }
}

// Add user message to chat
function addUserMessage(message) {
    const chatbox = document.getElementById("chatbox");
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message-bubble ml-auto fade-in';
    messageDiv.innerHTML = `
        <div class="bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-2xl rounded-tr-sm p-4 shadow-sm">
            <div class="flex items-start space-x-2">
                <div class="flex-1">
                    <p class="text-white">${escapeHtml(message)}</p>
                </div>
                <div class="w-8 h-8 bg-white bg-opacity-20 rounded-full flex items-center justify-center flex-shrink-0">
                    <i class="fas fa-user text-sm"></i>
                </div>
            </div>
        </div>
    `;
    chatbox.appendChild(messageDiv);
    scrollToBottom();
}

// Add bot message to chat
function addBotMessage(message) {
    const chatbox = document.getElementById("chatbox");
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message-bubble fade-in';
    messageDiv.innerHTML = `
        <div class="bg-white rounded-2xl rounded-tl-sm p-4 shadow-sm">
            <div class="flex items-start space-x-2">
                <div class="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <i class="fas fa-robot text-purple-600 text-sm"></i>
                </div>
                <div class="flex-1">
                    <p class="text-gray-800">${escapeHtml(message)}</p>
                </div>
            </div>
        </div>
    `;
    chatbox.appendChild(messageDiv);
    scrollToBottom();
}

// Show typing indicator
function showTypingIndicator() {
    const typingIndicator = document.getElementById("typingIndicator");
    typingIndicator.classList.add("show");
    scrollToBottom();
}

// Hide typing indicator
function hideTypingIndicator() {
    const typingIndicator = document.getElementById("typingIndicator");
    typingIndicator.classList.remove("show");
}

// Scroll to bottom of chat
function scrollToBottom() {
    const chatbox = document.getElementById("chatbox");
    setTimeout(() => {
        chatbox.scrollTop = chatbox.scrollHeight;
    }, 100);
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize chat when page loads
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById("userInput");
    input.focus();
    
    // Add some sample questions for better UX
    setTimeout(() => {
        addBotMessage("💡 Try asking me about our programs, duration, certificates, or mentors!");
    }, 2000);
});
  