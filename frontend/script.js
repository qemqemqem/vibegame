class VibeGame {
    constructor() {
        this.chatContainer = document.getElementById('chatContainer');
        this.playerInput = document.getElementById('playerInput');
        this.sendButton = document.getElementById('sendButton');
        this.loading = document.getElementById('loading');
        
        this.setupEventListeners();
        this.setupDungeonMasterPrompt();
    }
    
    setupEventListeners() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.playerInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
    }
    
    setupDungeonMasterPrompt() {
        this.systemPrompt = `You are an expert Dungeon Master running an immersive fantasy RPG adventure. Your role is to:

1. Create vivid, engaging scenarios that respond to player actions
2. Maintain narrative consistency and world-building
3. Present clear choices and consequences
4. Keep responses concise but descriptive (2-4 sentences)
5. Always end with a question or prompt for the player's next action
6. Be creative with encounters, puzzles, and character interactions
7. Adapt the story based on player decisions

Guidelines:
- Describe scenes with rich sensory details
- Include NPCs with distinct personalities
- Present meaningful choices that impact the story
- Balance challenge with fun
- Keep the tone adventurous and engaging
- Never break character or mention you're an AI

The player has just entered your dungeon. Guide them on an epic adventure!`;
    }
    
    async sendMessage() {
        const message = this.playerInput.value.trim();
        if (!message) return;
        
        this.addMessage(message, 'player');
        this.playerInput.value = '';
        this.showLoading(true);
        
        try {
            const response = await this.callLLM(message);
            this.addMessage(response, 'dm');
        } catch (error) {
            console.error('Error calling LLM:', error);
            this.addMessage('*The mystical connection to the Dungeon Master has been disrupted. Please try again.*', 'dm');
        } finally {
            this.showLoading(false);
        }
    }
    
    async callLLM(userMessage) {
        const messages = [
            {
                role: 'user',
                content: userMessage
            }
        ];
        
        try {
            // Try Netlify function first (for deployed site)
            const apiUrl = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
                ? '/api/chat'  // Local development
                : '/.netlify/functions/chat';  // Deployed site
            
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    messages: messages
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            return data.choices[0].message.content;
        } catch (error) {
            console.error('LLM API Error:', error);
            
            const fallbackResponses = [
                "You venture deeper into the dungeon. The torch light flickers across ancient stone walls carved with mysterious runes. Ahead, you hear the distant sound of dripping water and something else... footsteps? What do you do?",
                "A cool breeze carries the scent of adventure from the passage ahead. The shadows dance as your torch illuminates a fork in the path - one way leads up toward distant light, the other down into echoing darkness. Which path calls to you?",
                "Your footsteps echo in the silence as you discover a chamber filled with glittering gems embedded in the walls. But wait - those aren't gems, they're eyes! Dozens of creatures watch you from hidden alcoves. How do you react?",
                "The dungeon floor suddenly gives way beneath your feet! You tumble into a hidden chamber where ancient magic still pulses through crystalline formations. As you dust yourself off, you notice three doorways marked with different symbols. Which one draws your attention?"
            ];
            
            return fallbackResponses[Math.floor(Math.random() * fallbackResponses.length)];
        }
    }
    
    addMessage(content, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type === 'player' ? 'player-message' : 'dm-message'}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = content;
        
        messageDiv.appendChild(contentDiv);
        this.chatContainer.appendChild(messageDiv);
        
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
    }
    
    showLoading(show) {
        this.loading.style.display = show ? 'flex' : 'none';
        this.sendButton.disabled = show;
        this.playerInput.disabled = show;
        
        if (!show) {
            this.playerInput.focus();
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new VibeGame();
});