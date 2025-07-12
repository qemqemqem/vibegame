const { createProxyServer } = require('litellm');

export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }
    
    const { messages, model = 'gpt-3.5-turbo', max_tokens = 200, temperature = 0.8 } = req.body;
    
    try {
        const response = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
            },
            body: JSON.stringify({
                model,
                messages,
                max_tokens,
                temperature,
            }),
        });
        
        if (!response.ok) {
            throw new Error(`OpenAI API error: ${response.status}`);
        }
        
        const data = await response.json();
        res.status(200).json(data);
    } catch (error) {
        console.error('Chat API Error:', error);
        res.status(500).json({ error: 'Failed to get response from AI' });
    }
}