class VibeGame {
    constructor() {
        this.chatContainer = document.getElementById('chatContainer');
        this.playerInput = document.getElementById('playerInput');
        this.sendButton = document.getElementById('sendButton');
        this.loading = document.getElementById('loading');
        
        this.conversationHistory = [];
        this.setupEventListeners();
        this.setupDungeonMasterPrompt();
        this.showWelcomeMessage();
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
    
    showWelcomeMessage() {
        // Show a welcome message when the game starts
        this.addMessage("🎲 Welcome to the Vibe Game! You stand at the entrance to a mysterious dungeon. Ancient runes glow faintly on the stone archway before you. What do you do?", 'dm');
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
            let errorMessage = '*The mystical connection to the Dungeon Master has been disrupted. ';
            errorMessage += 'Please try again in a moment.*';
            this.addMessage(errorMessage, 'dm');
        } finally {
            this.showLoading(false);
        }
    }
    
    async callLLM(userMessage) {
        // Add user message to conversation history
        this.conversationHistory.push({
            role: 'user',
            content: userMessage
        });

        try {
            return await this.callNetlifyFunction();
        } catch (error) {
            console.error('Netlify Function Error:', error);
            // Fall back to mock response
            return this.getMockResponse(userMessage);
        }
    }

    async callNetlifyFunction() {
        // Use Netlify serverless function (API key handled server-side)
        console.log('🔧 Calling Netlify serverless function');
        
        const response = await fetch('/.netlify/functions/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                messages: this.conversationHistory
            })
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        
        // Handle response format from Netlify function
        let assistantMessage;
        if (data.choices && data.choices[0] && data.choices[0].message) {
            assistantMessage = data.choices[0].message.content;
        } else if (data.fallback_response) {
            assistantMessage = data.fallback_response;
        } else {
            throw new Error('Unexpected response format from API');
        }
        
        // Add assistant response to conversation history
        this.conversationHistory.push({
            role: 'assistant',
            content: assistantMessage
        });

        // Keep conversation history manageable (last 10 exchanges)
        if (this.conversationHistory.length > 20) {
            this.conversationHistory = this.conversationHistory.slice(-20);
        }

        // Show status indicator if using fallback
        if (data.fallback || data.mode === 'mock' || data.mode === 'fallback') {
            console.log(`🎭 Using ${data.mode || 'fallback'} mode`);
        } else if (data.mode === 'live') {
            console.log('🤖 Using live AI responses');
        }

        return assistantMessage;
    }

    getMockResponse(userMessage) {
        const input = userMessage.toLowerCase();
        
        if (input.includes('attack') || input.includes('fight') || input.includes('combat')) {
            return "You draw your weapon and prepare for battle! The creature before you snarls and circles, looking for an opening. Roll for initiative - what's your strategy?";
        }
        
        if (input.includes('look') || input.includes('examine') || input.includes('search')) {
            return "As you carefully examine your surroundings, you notice intricate details previously hidden in shadow. Ancient carvings tell a story of heroes past, and you spot something glinting in a nearby alcove. What catches your attention?";
        }
        
        if (input.includes('north') || input.includes('south') || input.includes('east') || input.includes('west') || input.includes('go')) {
            return "You move cautiously in that direction, your footsteps echoing off the stone walls. The path ahead curves mysteriously, and you hear distant sounds that make your heart race with excitement. What do you do as you continue forward?";
        }
        
        if (input.includes('talk') || input.includes('speak') || input.includes('say')) {
            return "Your words echo in the chamber, and to your surprise, you hear a response! A mysterious voice seems to come from everywhere and nowhere at once: 'Welcome, brave soul. Your journey has only just begun...' How do you respond?";
        }
        
        // Default random responses
        const fallbackResponses = [
            "You venture deeper into the dungeon. The torch light flickers across ancient stone walls carved with mysterious runes. Ahead, you hear the distant sound of dripping water and something else... footsteps? What do you do?",
            "A cool breeze carries the scent of adventure from the passage ahead. The shadows dance as your torch illuminates a fork in the path - one way leads up toward distant light, the other down into echoing darkness. Which path calls to you?",
            "Your footsteps echo in the silence as you discover a chamber filled with glittering gems embedded in the walls. But wait - those aren't gems, they're eyes! Dozens of creatures watch you from hidden alcoves. How do you react?",
            "The dungeon floor suddenly gives way beneath your feet! You tumble into a hidden chamber where ancient magic still pulses through crystalline formations. As you dust yourself off, you notice three doorways marked with different symbols. Which one draws your attention?",
            "A wise old sage emerges from the shadows, his beard sparkling with stardust. 'Young adventurer,' he says, 'I sense great potential in you. But first, you must prove your worth.' Will you accept his challenge?",
            "The air shimmers and a magical portal opens before you, revealing glimpses of three different realms: a fiery volcanic landscape, a serene underwater kingdom, and a floating city among the clouds. Which realm calls to your adventurous spirit?"
        ];
        
        return fallbackResponses[Math.floor(Math.random() * fallbackResponses.length)] + "\n\n*(Fallback response - server connection issue)*";
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