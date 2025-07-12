class VibeGame {
    constructor() {
        this.chatContainer = document.getElementById('chatContainer');
        this.playerInput = document.getElementById('playerInput');
        this.sendButton = document.getElementById('sendButton');
        this.loading = document.getElementById('loading');
        this.apiKeySettingsBtn = document.getElementById('apiKeySettingsBtn');
        
        this.conversationHistory = [];
        this.streamingMessages = new Map();
        this.nextMessageId = 1;
        this.setupEventListeners();
        this.setupDungeonMasterPrompt();
        this.showApiKeyStatus();
    }
    
    setupEventListeners() {
        this.sendButton.addEventListener('click', () => this.sendMessageWithStreaming());
        this.playerInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessageWithStreaming();
            }
        });
        this.apiKeySettingsBtn.addEventListener('click', () => {
            window.apiKeyManager.showApiKeySettings();
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
    
    showApiKeyStatus() {
        const hasApiKey = !!window.apiKeyManager.getStoredApiKey();
        if (hasApiKey) {
            this.apiKeySettingsBtn.style.background = 'rgba(0, 255, 0, 0.3)';
            this.apiKeySettingsBtn.title = 'API Key Configured ✅';
        } else {
            this.apiKeySettingsBtn.style.background = 'rgba(255, 165, 0, 0.3)';
            this.apiKeySettingsBtn.title = 'Click to configure API Key for real AI responses';
        }
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
            
            if (error.message.includes('Invalid API key')) {
                errorMessage += 'Your API key seems to be invalid. Please check your settings.*';
            } else if (error.message.includes('401')) {
                errorMessage += 'Authentication failed. Please verify your API key.*';
            } else {
                errorMessage += 'Please try again in a moment.*';
            }
            
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

        // Try to get API key
        const apiKey = await window.apiKeyManager.getApiKey();
        
        if (apiKey) {
            try {
                return await this.callAnthropicAPI(apiKey);
            } catch (error) {
                console.error('Anthropic API Error:', error);
                // Fall back to mock response
                return this.getMockResponse(userMessage);
            }
        } else {
            // User chose to skip API key, use mock responses
            return this.getMockResponse(userMessage);
        }
    }

    async callAnthropicAPI(apiKey) {
        // Use Netlify serverless function (or CORS proxy for GitHub Pages)
        const isNetlify = window.location.hostname.includes('netlify.app');
        
        let response;
        if (isNetlify) {
            // Use Netlify function
            console.log('🔧 Using Netlify serverless function for game');
            response = await fetch('/.netlify/functions/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    messages: this.conversationHistory,
                    apiKey: apiKey  // Pass API key in body for Netlify function
                })
            });
        } else {
            // Use CORS proxy for GitHub Pages
            console.log('🔧 Using CORS proxy for GitHub Pages');
            response = await fetch('https://corsproxy.io/?https://api.anthropic.com/v1/messages', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-api-key': apiKey,
                    'anthropic-version': '2023-06-01'
                },
                body: JSON.stringify({
                    model: 'claude-3-5-haiku-20241022',
                    max_tokens: 200,
                    temperature: 0.8,
                    system: this.systemPrompt,
                    messages: this.conversationHistory
                })
            });
        }

        if (!response.ok) {
            if (response.status === 401) {
                // Invalid API key - clear it and prompt again
                window.apiKeyManager.clearApiKey();
                this.showApiKeyStatus();
                throw new Error('Invalid API key - please check your key and try again');
            }
            throw new Error(`API Error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        
        // Handle different response formats
        let assistantMessage;
        if (data.choices && data.choices[0] && data.choices[0].message) {
            // Netlify function format (OpenAI-like)
            assistantMessage = data.choices[0].message.content;
        } else if (data.content && data.content[0] && data.content[0].text) {
            // Direct Anthropic API format
            assistantMessage = data.content[0].text;
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
        
        return fallbackResponses[Math.floor(Math.random() * fallbackResponses.length)] + "\n\n*(Mock response - add your Anthropic API key for real Claude AI)*";
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
            // Response handling is done in the streaming callback
        } catch (error) {
            console.error('Error calling LLM:', error);
            let errorMessage = '*The mystical connection to the Dungeon Master has been disrupted. ';
            
            if (error.message.includes('Invalid API key')) {
                errorMessage += 'Your API key seems to be invalid. Please check your settings.*';
            } else if (error.message.includes('401')) {
                errorMessage += 'Authentication failed. Please verify your API key.*';
            } else {
                errorMessage += 'Please try again in a moment.*';
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

        // Try to get API key
        const apiKey = await window.apiKeyManager.getApiKey();
        
        if (apiKey) {
            try {
                return await this.callStreamingAPI(apiKey);
            } catch (error) {
                console.error('Streaming API Error:', error);
                // Fall back to regular response
                const fallbackResponse = this.getMockResponse(userMessage);
                this.addMessage(fallbackResponse, 'dm');
                return fallbackResponse;
            }
        } else {
            // Use mock response with streaming effect
            const fallbackResponse = this.getMockResponse(userMessage);
            await this.simulateStreamingResponse(fallbackResponse);
            return fallbackResponse;
        }
    }

    async callStreamingAPI(apiKey) {
        const isNetlify = window.location.hostname.includes('netlify.app');
        
        if (isNetlify) {
            // Use Netlify function with streaming
            const response = await fetch('/.netlify/functions/chat-stream', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    messages: this.conversationHistory,
                    apiKey: apiKey,
                    stream: true
                })
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.status}`);
            }

            return await this.processStreamingResponse(response);
        } else {
            // Fallback to regular API call for non-Netlify environments
            return await this.callAnthropicAPI(apiKey);
        }
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
            console.error('Streaming error:', error);
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

        return assistantMessage;
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