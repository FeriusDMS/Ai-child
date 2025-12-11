// API Configuration
const API_BASE = window.location.origin;

// Elements
const chatContainer = document.getElementById('chatContainer');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const voiceBtn = document.getElementById('voiceBtn');
const micBtn = document.getElementById('micBtn');
const levelEl = document.getElementById('level');
const interactionsEl = document.getElementById('interactions');
const descriptionEl = document.getElementById('description');
const avatar = document.getElementById('avatar');

// State
let isTyping = false;
let voiceEnabled = true;  // Activé par défaut
let isListening = false;

// Speech Synthesis (Text-to-Speech)
let synth = window.speechSynthesis;
let selectedVoice = null;

// Speech Recognition (Speech-to-Text)
let recognition = null;
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.lang = 'fr-FR';
    recognition.continuous = false;
    recognition.interimResults = false;
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadStats();
    loadVoices();
    userInput.focus();
    
    // Activer le bouton voix par défaut
    voiceBtn.classList.add('active');
    
    // Event listeners
    sendBtn.addEventListener('click', sendMessage);
    voiceBtn.addEventListener('click', toggleVoice);
    micBtn.addEventListener('click', toggleListening);
    
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Load voices when they're ready
    if (synth.onvoiceschanged !== undefined) {
        synth.onvoiceschanged = loadVoices;
    }
    
    // Setup speech recognition
    if (recognition) {
        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            userInput.value = transcript;
            sendMessage();
        };
        
        recognition.onerror = (event) => {
            console.error('Erreur reconnaissance vocale:', event.error);
            stopListening();
        };
        
        recognition.onend = () => {
            stopListening();
        };
    } else {
        // Désactiver le bouton micro si non supporté
        micBtn.disabled = true;
        micBtn.style.opacity = '0.3';
    }
});

// Load available voices
function loadVoices() {
    const voices = synth.getVoices();
    
    // Priorité: voix française féminine/enfantine
    const preferredVoices = [
        'Google français',
        'Microsoft Julie',
        'Microsoft Hortense',
        'Amelie',
        'Thomas',
        'fr-FR',
        'French'
    ];
    
    // Chercher une voix féminine française
    for (let pref of preferredVoices) {
        selectedVoice = voices.find(voice => 
            voice.name.includes(pref) || 
            voice.lang.includes('fr')
        );
        if (selectedVoice) break;
    }
    
    // Fallback: première voix française disponible
    if (!selectedVoice) {
        selectedVoice = voices.find(voice => voice.lang.startsWith('fr')) || voices[0];
    }
    
    console.log('Voix sélectionnée:', selectedVoice?.name);
}

// Toggle voice on/off
function toggleVoice() {
    voiceEnabled = !voiceEnabled;
    voiceBtn.classList.toggle('active', voiceEnabled);
    
    if (!voiceEnabled) {
        synth.cancel(); // Stop speaking
    }
}

// Speak text
function speak(text) {
    if (!voiceEnabled || !synth) return;
    
    // Cancel any ongoing speech
    synth.cancel();
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.voice = selectedVoice;
    utterance.rate = 1.1; // Un peu plus rapide pour sonner plus jeune
    utterance.pitch = 1.3; // Voix plus aiguë pour sonner enfantine
    utterance.volume = 1;
    utterance.lang = 'fr-FR';
    
    // Animation de l'avatar pendant qu'il parle
    utterance.onstart = () => {
        avatar.style.transform = 'scale(1.05)';
    };
    
    utterance.onend = () => {
        avatar.style.transform = 'scale(1)';
    };
    
    synth.speak(utterance);
}

// Toggle listening (Speech-to-Text)
function toggleListening() {
    if (!recognition) return;
    
    if (isListening) {
        stopListening();
    } else {
        startListening();
    }
}

function startListening() {
    if (!recognition || isListening) return;
    
    isListening = true;
    micBtn.classList.add('recording');
    userInput.placeholder = '🎤 Parle maintenant...';
    
    try {
        recognition.start();
    } catch (e) {
        console.error('Erreur démarrage reconnaissance:', e);
        stopListening();
    }
}

function stopListening() {
    if (!recognition || !isListening) return;
    
    isListening = false;
    micBtn.classList.remove('recording');
    userInput.placeholder = 'Écris ton message...';
    
    try {
        recognition.stop();
    } catch (e) {
        // Ignore errors when stopping
    }
}

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
        
        // Make AI speak the response
        speak(data.response);
        
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
