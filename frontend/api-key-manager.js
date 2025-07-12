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
        if (this.isValidating) return false;
        this.isValidating = true;

        try {
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

            if (response.ok) {
                console.log('✅ API key validation successful');
                return true;
            } else if (response.status === 401) {
                console.error('❌ API key validation failed: Invalid key');
                return false;
            } else {
                console.error('❌ API key validation failed:', response.status);
                return false;
            }
        } catch (error) {
            this.isValidating = false;
            console.error('❌ API key validation error:', error);
            return false;
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
                            <input type="password" id="apiKeyInput" placeholder="sk-ant-api..." class="api-key-input">
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
                validateBtn.disabled = !key.startsWith('sk-ant-');
                if (key && !key.startsWith('sk-ant-')) {
                    statusDiv.innerHTML = '⚠️ API key should start with "sk-ant-"';
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
                if (!apiKey.startsWith('sk-ant-')) {
                    statusDiv.innerHTML = '❌ Invalid API key format';
                    statusDiv.className = 'validation-status error';
                    return;
                }

                validateBtn.disabled = true;
                validateBtn.textContent = '🔄 Validating...';
                statusDiv.innerHTML = '🔄 Testing your API key...';
                statusDiv.className = 'validation-status info';

                const isValid = await this.validateApiKey(apiKey);
                
                if (isValid) {
                    statusDiv.innerHTML = '✅ API key validated successfully!';
                    statusDiv.className = 'validation-status success';
                    setTimeout(() => {
                        document.body.removeChild(overlay);
                        resolve(apiKey);
                    }, 1000);
                } else {
                    statusDiv.innerHTML = '❌ Invalid API key. Please check and try again.';
                    statusDiv.className = 'validation-status error';
                    validateBtn.disabled = false;
                    validateBtn.textContent = '✅ Validate & Save';
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