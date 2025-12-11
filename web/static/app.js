// API Configuration
const API_BASE = window.location.origin;

// Elements
const chatContainer = document.getElementById('chatContainer');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const levelEl = document.getElementById('level');
const interactionsEl = document.getElementById('interactions');
const descriptionEl = document.getElementById('description');
const avatar = document.getElementById('avatar');

// State
let isTyping = false;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadStats();
    userInput.focus();
    
    // Event listeners
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
});

// Load AI stats
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE}/api/stats`);
        const data = await response.json();
        
        levelEl.textContent = data.level;
        interactionsEl.textContent = data.interactions_count;
        descriptionEl.textContent = data.description;
        
        // Animation de l'avatar selon le niveau
        updateAvatarAnimation(data.level);
    } catch (error) {
        console.error('Erreur chargement stats:', error);
    }
}

// Update avatar animation based on level
function updateAvatarAnimation(level) {
    if (level <= 2) {
        avatar.style.animation = 'gentle-bounce 2s ease-in-out infinite';
    } else if (level <= 5) {
        avatar.style.animation = 'gentle-bounce 1.5s ease-in-out infinite';
    } else {
        avatar.style.animation = 'gentle-bounce 1s ease-in-out infinite';
    }
}

// Send message
async function sendMessage() {
    const message = userInput.value.trim();
    
    if (!message || isTyping) return;
    
    // Add user message
    addMessage(message, 'user');
    userInput.value = '';
    
    // Show typing indicator
    showTypingIndicator();
    isTyping = true;
    sendBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator();
        
        // Add AI response
        addMessage(data.response, 'ai');
        
        // Update stats
        levelEl.textContent = data.level;
        interactionsEl.textContent = data.interactions;
        
        // Reload full stats for description update
        loadStats();
        
        // Celebrate level up
        if (data.interactions % 20 === 0) {
            celebrateLevelUp();
        }
        
    } catch (error) {
        removeTypingIndicator();
        addMessage('Désolé, j\'ai un problème... 😔', 'ai');
        console.error('Erreur:', error);
    } finally {
        isTyping = false;
        sendBtn.disabled = false;
        userInput.focus();
    }
}

// Add message to chat
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text;
    
    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Show typing indicator
function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message ai';
    typingDiv.id = 'typing-indicator';
    
    const indicator = document.createElement('div');
    indicator.className = 'typing-indicator';
    indicator.innerHTML = '<span></span><span></span><span></span>';
    
    typingDiv.appendChild(indicator);
    chatContainer.appendChild(typingDiv);
    
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Remove typing indicator
function removeTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
        indicator.remove();
    }
}

// Celebrate level up
function celebrateLevelUp() {
    // Animation de l'avatar
    avatar.style.animation = 'celebrate 1s ease-in-out';
    
    setTimeout(() => {
        updateAvatarAnimation(parseInt(levelEl.textContent));
    }, 1000);
    
    // Message de félicitation
    const celebration = document.createElement('div');
    celebration.className = 'celebration';
    celebration.innerHTML = '🎉 Niveau supérieur ! 🎉';
    celebration.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px 40px;
        border-radius: 20px;
        font-size: 24px;
        font-weight: bold;
        z-index: 1000;
        animation: celebration 2s ease-in-out;
    `;
    
    document.body.appendChild(celebration);
    
    setTimeout(() => {
        celebration.remove();
    }, 2000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes gentle-bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
    
    @keyframes celebrate {
        0%, 100% { transform: scale(1) rotate(0deg); }
        25% { transform: scale(1.2) rotate(-10deg); }
        75% { transform: scale(1.2) rotate(10deg); }
    }
    
    @keyframes celebration {
        0% { opacity: 0; transform: translate(-50%, -50%) scale(0.5); }
        50% { opacity: 1; transform: translate(-50%, -50%) scale(1.1); }
        100% { opacity: 0; transform: translate(-50%, -50%) scale(0.8); }
    }
`;
document.head.appendChild(style);
