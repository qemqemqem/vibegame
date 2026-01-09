class VibeGame {
    constructor() {
        this.chatContainer = document.getElementById('chatContainer');
        this.playerInput = document.getElementById('playerInput');
        this.sendButton = document.getElementById('sendButton');
        this.loading = document.getElementById('loading');
        
        this.conversationHistory = [];
        this.streamingMessages = new Map();
        this.nextMessageId = 1;
        this.setupEventListeners();
        this.setupDungeonMasterPrompt();
        this.showWelcomeMessage();
    }
    
    setupEventListeners() {
        this.sendButton.addEventListener('click', () => this.sendMessageWithStreaming());
        this.playerInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessageWithStreaming();
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
        this.addMessage("🎭 Welcome to the Stratford Nexus! You materialize on the Globe Nexus Station, where quantum threads shimmer with the echoes of Shakespeare's greatest works. Ancient technology hums with poetic magic, and reality bends like stage lights in an infinite theater. The air sparkles with possibility as seven sphere-worlds await your exploration. What calls to your adventurous spirit?", 'dm');
        
        // Auto-focus the input for immediate typing
        setTimeout(() => {
            this.playerInput.focus();
        }, 100);
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
        // Use world-aware Netlify serverless function (API key handled server-side)
        console.log('🔧 Calling world-aware Netlify serverless function');
        
        const response = await fetch('/.netlify/functions/chat-world-aware', {
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

    // Streaming functionality
    addStreamingMessage(type) {
        if (type !== 'player' && type !== 'dm') {
            throw new Error('Invalid message type');
        }
        
        const id = `msg_${this.nextMessageId++}`;
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type === 'player' ? 'player-message' : 'dm-message'}`;
        messageDiv.id = id;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = '';
        
        // Add cursor for streaming indication
        const cursor = document.createElement('span');
        cursor.className = 'streaming-cursor';
        cursor.textContent = '▋';
        cursor.style.animation = 'blink 1s infinite';
        
        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(cursor);
        this.chatContainer.appendChild(messageDiv);
        
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
        
        const message = {
            id: id,
            type: type,
            content: '',
            isStreaming: true,
            element: messageDiv,
            contentElement: contentDiv,
            cursorElement: cursor
        };
        
        this.streamingMessages.set(id, message);
        return message;
    }

    updateStreamingMessage(id, newContent) {
        const message = this.streamingMessages.get(id);
        if (!message) {
            throw new Error('Streaming message not found');
        }
        
        message.content += newContent;
        message.contentElement.textContent = message.content;
        
        // Auto-scroll to bottom
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
        
        return message;
    }

    finishStreamingMessage(id) {
        const message = this.streamingMessages.get(id);
        if (!message) {
            throw new Error('Streaming message not found');
        }
        
        message.isStreaming = false;
        // Remove cursor
        if (message.cursorElement) {
            message.cursorElement.remove();
        }
        
        return message;
    }

    // Enhanced sendMessage for streaming
    async sendMessageWithStreaming() {
        const message = this.playerInput.value.trim();
        if (!message) return;
        
        this.addMessage(message, 'player');
        this.playerInput.value = '';
        this.showLoading(true);
        
        try {
            const response = await this.callLLMWithStreaming(message);
            if (response) {
                this.addMessage(response, 'dm');
            }
        } catch (error) {
            console.error('Error calling LLM:', error);
            let errorMessage = '*System Error: ';
            
            if (error.message.includes('window.apiKeyManager is undefined')) {
                errorMessage += 'API key management system failed to load. Please refresh the page.*';
            } else if (error.message.includes('Invalid API key')) {
                errorMessage += 'Invalid API key. Please check your configuration.*';
            } else if (error.message.includes('401')) {
                errorMessage += 'Authentication failed (HTTP 401). API key may be invalid.*';
            } else if (error.message.includes('fetch')) {
                errorMessage += 'Network connection failed. Check your internet connection.*';
            } else if (error.message.includes('API Error')) {
                errorMessage += `API request failed: ${error.message}*`;
            } else {
                errorMessage += `${error.message || 'Unknown error occurred'}*`;
            }
            
            this.addMessage(errorMessage, 'dm');
        } finally {
            this.showLoading(false);
        }
    }

    async callLLMWithStreaming(userMessage) {
        // Add user message to conversation history
        this.conversationHistory.push({
            role: 'user',
            content: userMessage
        });

        try {
            // Use Netlify streaming function
            return await this.callStreamingNetlifyFunction();
        } catch (error) {
            console.error('Netlify Streaming Function Error:', error);
            // Fall back to mock response with streaming effect
            const fallbackResponse = this.getMockResponse(userMessage);
            await this.simulateStreamingResponse(fallbackResponse);
            return null; // Don't return response since it's already displayed via streaming
        }
    }

    async callStreamingNetlifyFunction() {
        console.log('🚀 Starting streaming response from Claude AI...');
        
        const response = await fetch('/.netlify/functions/chat-world-aware', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                messages: this.conversationHistory,
                stream: true
            })
        });

        if (!response.ok) {
            throw new Error(`Streaming API Error: ${response.status} ${response.statusText}`);
        }

        // Process the streaming response
        return await this.processStreamingResponse(response);
    }

    async processStreamingResponse(response) {
        const streamingMessage = this.addStreamingMessage('dm');
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let assistantMessage = '';

        try {
            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });
                const lines = chunk.split('\n');

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const data = line.slice(6);
                        if (data === '[DONE]') {
                            this.finishStreamingMessage(streamingMessage.id);
                            break;
                        }
                        
                        try {
                            const parsed = JSON.parse(data);
                            if (parsed.content) {
                                assistantMessage += parsed.content;
                                this.updateStreamingMessage(streamingMessage.id, parsed.content);
                            }
                        } catch (e) {
                            // Skip invalid JSON
                        }
                    }
                }
            }
        } catch (error) {
            console.error('Streaming processing error:', error);
            this.finishStreamingMessage(streamingMessage.id);
        }

        // Add to conversation history
        this.conversationHistory.push({
            role: 'assistant',
            content: assistantMessage
        });

        // Keep conversation history manageable
        if (this.conversationHistory.length > 20) {
            this.conversationHistory = this.conversationHistory.slice(-20);
        }

        console.log('✅ Streaming response complete!');
        return null; // Response already displayed via streaming
    }

    async simulateStreamingResponse(fullResponse) {
        const streamingMessage = this.addStreamingMessage('dm');
        const words = fullResponse.split(' ');
        
        for (let i = 0; i < words.length; i++) {
            const word = words[i] + (i < words.length - 1 ? ' ' : '');
            this.updateStreamingMessage(streamingMessage.id, word);
            
            // Add delay to simulate streaming
            await new Promise(resolve => setTimeout(resolve, 50 + Math.random() * 100));
        }
        
        this.finishStreamingMessage(streamingMessage.id);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new VibeGame();
});