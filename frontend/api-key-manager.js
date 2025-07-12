/**
 * Secure API Key Management for Vibe Game
 * Handles cookie-based storage of user's Anthropic API keys
 */

class ApiKeyManager {
    constructor() {
        this.cookieName = 'vibe_game_api_key';
        this.cookieExpireDays = 30; // API key valid for 30 days
        this.isValidating = false;
    }

    /**
     * Get API key from secure cookie
     */
    getStoredApiKey() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === this.cookieName) {
                try {
                    // Basic decoding (not encryption, but obfuscated)
                    return atob(decodeURIComponent(value));
                } catch (e) {
                    console.warn('Invalid stored API key, clearing cookie');
                    this.clearApiKey();
                    return null;
                }
            }
        }
        return null;
    }

    /**
     * Store API key in secure cookie
     */
    storeApiKey(apiKey) {
        if (!apiKey || !apiKey.startsWith('sk-ant-')) {
            throw new Error('Invalid API key format');
        }

        const expireDate = new Date();
        expireDate.setTime(expireDate.getTime() + (this.cookieExpireDays * 24 * 60 * 60 * 1000));
        
        // Basic encoding (not encryption, but obfuscated)
        const encodedKey = btoa(apiKey);
        
        document.cookie = `${this.cookieName}=${encodeURIComponent(encodedKey)}; expires=${expireDate.toUTCString()}; path=/; SameSite=Strict; Secure`;
        
        console.log('✅ API key stored securely');
    }

    /**
     * Clear stored API key
     */
    clearApiKey() {
        document.cookie = `${this.cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; SameSite=Strict; Secure`;
        console.log('🗑️ API key cleared');
    }

    /**
     * Validate API key by making a test call
     */
    async validateApiKey(apiKey) {
        if (this.isValidating) return { valid: false, error: 'Validation already in progress' };
        this.isValidating = true;

        try {
            console.log(`🔍 Validating API key: ${apiKey.substring(0, 20)}...`);
            
            const response = await fetch('https://api.anthropic.com/v1/messages', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-api-key': apiKey,
                    'anthropic-version': '2023-06-01'
                },
                body: JSON.stringify({
                    model: 'claude-3-5-haiku-20241022',
                    max_tokens: 10,
                    messages: [{ role: 'user', content: 'Hello' }]
                })
            });

            this.isValidating = false;
            
            console.log(`📡 API Response Status: ${response.status}`);

            if (response.ok) {
                const data = await response.json();
                console.log('✅ API key validation successful', data);
                return { valid: true, error: null };
            } else if (response.status === 401) {
                const errorData = await response.text();
                console.error('❌ API key validation failed: 401 Unauthorized', errorData);
                return { valid: false, error: 'Invalid API key - please check your key is correct and active' };
            } else if (response.status === 400) {
                const errorData = await response.text();
                console.error('❌ API key validation failed: 400 Bad Request', errorData);
                return { valid: false, error: 'Bad request - API key format may be incorrect' };
            } else {
                const errorData = await response.text();
                console.error(`❌ API key validation failed: ${response.status}`, errorData);
                return { valid: false, error: `API error: ${response.status} ${response.statusText}` };
            }
        } catch (error) {
            this.isValidating = false;
            console.error('❌ API key validation error:', error);
            return { valid: false, error: `Network error: ${error.message}` };
        }
    }

    /**
     * Get API key with automatic prompting if needed
     */
    async getApiKey() {
        let apiKey = this.getStoredApiKey();
        
        if (!apiKey) {
            apiKey = await this.promptForApiKey();
            if (apiKey) {
                this.storeApiKey(apiKey);
            }
        }
        
        return apiKey;
    }

    /**
     * Show modal to prompt user for API key
     */
    async promptForApiKey() {
        return new Promise((resolve) => {
            // Create modal overlay
            const overlay = document.createElement('div');
            overlay.className = 'api-key-modal-overlay';
            overlay.innerHTML = `
                <div class="api-key-modal">
                    <div class="modal-header">
                        <h2>🤖 Enable AI Dungeon Master</h2>
                        <p>To unlock Claude AI responses, enter your Anthropic API key:</p>
                    </div>
                    <div class="modal-content">
                        <div class="api-key-info">
                            <h3>How to get your API key:</h3>
                            <ol>
                                <li>Visit <a href="https://console.anthropic.com/" target="_blank">console.anthropic.com</a></li>
                                <li>Sign up or log in to your account</li>
                                <li>Go to "API Keys" section</li>
                                <li>Create a new API key</li>
                                <li>Copy and paste it below</li>
                            </ol>
                            <div class="cost-info">
                                <strong>💰 Cost:</strong> ~$0.0008 per message with Claude 3.5 Haiku<br>
                                <strong>🔒 Privacy:</strong> Your key stays in your browser only
                            </div>
                        </div>
                        <div class="api-key-input-section">
                            <label for="apiKeyInput">Anthropic API Key:</label>
                            <input type="text" id="apiKeyInput" placeholder="sk-ant-api03-..." class="api-key-input" spellcheck="false">
                            <div class="input-hint">Your key will be stored securely in your browser</div>
                        </div>
                        <div class="modal-actions">
                            <button id="validateKeyBtn" class="btn-primary">✅ Validate & Save</button>
                            <button id="skipBtn" class="btn-secondary">Skip (Use Mock Responses)</button>
                            <button id="cancelBtn" class="btn-tertiary">Cancel</button>
                        </div>
                        <div id="validationStatus" class="validation-status"></div>
                    </div>
                </div>
            `;

            document.body.appendChild(overlay);

            const apiKeyInput = overlay.querySelector('#apiKeyInput');
            const validateBtn = overlay.querySelector('#validateKeyBtn');
            const skipBtn = overlay.querySelector('#skipBtn');
            const cancelBtn = overlay.querySelector('#cancelBtn');
            const statusDiv = overlay.querySelector('#validationStatus');

            // Focus input
            apiKeyInput.focus();

            // Handle input changes
            apiKeyInput.addEventListener('input', () => {
                const key = apiKeyInput.value.trim();
                validateBtn.disabled = key.length < 10; // Less strict initial check
                
                if (key.length > 0 && !key.startsWith('sk-ant-api')) {
                    statusDiv.innerHTML = '⚠️ API key should start with "sk-ant-api"';
                    statusDiv.className = 'validation-status warning';
                } else if (key.length > 0 && key.length < 50) {
                    statusDiv.innerHTML = '⚠️ Make sure you copied the complete API key';
                    statusDiv.className = 'validation-status warning';
                } else {
                    statusDiv.innerHTML = '';
                    statusDiv.className = 'validation-status';
                }
            });

            // Handle Enter key
            apiKeyInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !validateBtn.disabled) {
                    validateBtn.click();
                }
            });

            // Validate and save
            validateBtn.addEventListener('click', async () => {
                const apiKey = apiKeyInput.value.trim();
                
                // Basic format check
                if (!apiKey) {
                    statusDiv.innerHTML = '❌ Please enter your API key';
                    statusDiv.className = 'validation-status error';
                    return;
                }
                
                if (!apiKey.startsWith('sk-ant-api')) {
                    statusDiv.innerHTML = '❌ API key should start with "sk-ant-api"';
                    statusDiv.className = 'validation-status error';
                    return;
                }
                
                if (apiKey.length < 50) {
                    statusDiv.innerHTML = '❌ API key seems too short - make sure you copied the full key';
                    statusDiv.className = 'validation-status error';
                    return;
                }

                validateBtn.disabled = true;
                validateBtn.textContent = '🔄 Validating...';
                statusDiv.innerHTML = '🔄 Testing your API key with Claude API...';
                statusDiv.className = 'validation-status info';

                const result = await this.validateApiKey(apiKey);
                
                if (result.valid) {
                    statusDiv.innerHTML = '✅ API key validated successfully!';
                    statusDiv.className = 'validation-status success';
                    setTimeout(() => {
                        document.body.removeChild(overlay);
                        resolve(apiKey);
                    }, 1000);
                } else {
                    statusDiv.innerHTML = `❌ ${result.error}`;
                    statusDiv.className = 'validation-status error';
                    validateBtn.disabled = false;
                    validateBtn.textContent = '✅ Validate & Save';
                    
                    // Add debugging info
                    console.error('Validation failed:', result);
                }
            });

            // Skip - use mock responses
            skipBtn.addEventListener('click', () => {
                document.body.removeChild(overlay);
                resolve(null);
            });

            // Cancel
            cancelBtn.addEventListener('click', () => {
                document.body.removeChild(overlay);
                resolve(null);
            });

            // Close on overlay click
            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) {
                    document.body.removeChild(overlay);
                    resolve(null);
                }
            });
        });
    }

    /**
     * Show settings to manage stored API key
     */
    showApiKeySettings() {
        const currentKey = this.getStoredApiKey();
        const hasKey = !!currentKey;
        
        const overlay = document.createElement('div');
        overlay.className = 'api-key-modal-overlay';
        overlay.innerHTML = `
            <div class="api-key-modal">
                <div class="modal-header">
                    <h2>🔑 API Key Settings</h2>
                </div>
                <div class="modal-content">
                    <div class="current-status">
                        <strong>Status:</strong> ${hasKey ? '✅ API key configured' : '❌ No API key set'}
                        ${hasKey ? `<br><strong>Key:</strong> ${currentKey.substring(0, 12)}...` : ''}
                    </div>
                    <div class="modal-actions">
                        <button id="changeKeyBtn" class="btn-primary">🔄 ${hasKey ? 'Change' : 'Add'} API Key</button>
                        ${hasKey ? '<button id="removeKeyBtn" class="btn-danger">🗑️ Remove Key</button>' : ''}
                        <button id="closeSettingsBtn" class="btn-secondary">Close</button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(overlay);

        const changeKeyBtn = overlay.querySelector('#changeKeyBtn');
        const removeKeyBtn = overlay.querySelector('#removeKeyBtn');
        const closeBtn = overlay.querySelector('#closeSettingsBtn');

        changeKeyBtn.addEventListener('click', async () => {
            document.body.removeChild(overlay);
            const newKey = await this.promptForApiKey();
            if (newKey) {
                this.storeApiKey(newKey);
                // Refresh the page to use new key
                window.location.reload();
            }
        });

        if (removeKeyBtn) {
            removeKeyBtn.addEventListener('click', () => {
                this.clearApiKey();
                document.body.removeChild(overlay);
                // Refresh to use mock responses
                window.location.reload();
            });
        }

        closeBtn.addEventListener('click', () => {
            document.body.removeChild(overlay);
        });

        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                document.body.removeChild(overlay);
            }
        });
    }
}

// Global instance
window.apiKeyManager = new ApiKeyManager();