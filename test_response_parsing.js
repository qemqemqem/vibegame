/**
 * Tests for API response parsing logic
 * Run with: node test_response_parsing.js
 */

// Mock response parsing function (extracted from script.js)
function parseApiResponse(data) {
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
    return assistantMessage;
}

// Test data
const netlifyResponse = {
    choices: [{
        message: {
            content: "You enter a mysterious dungeon filled with ancient magic. What do you do?",
            role: 'assistant'
        }
    }],
    usage: {
        input_tokens: 15,
        output_tokens: 25,
        total_tokens: 40
    },
    model: 'claude-3-5-haiku-20241022'
};

const anthropicResponse = {
    content: [{
        text: "You find yourself in a dark cavern with glowing crystals. Which path do you choose?",
        type: "text"
    }],
    id: "msg_123",
    model: "claude-3-5-haiku-20241022",
    role: "assistant",
    usage: {
        input_tokens: 12,
        output_tokens: 18
    }
};

const invalidResponse = {
    error: "Something went wrong",
    message: "Invalid format"
};

// Run tests
function runTests() {
    console.log('🧪 Testing API Response Parsing Logic...\n');
    
    let passed = 0;
    let failed = 0;
    
    // Test 1: Netlify function response format
    try {
        const result = parseApiResponse(netlifyResponse);
        if (result === "You enter a mysterious dungeon filled with ancient magic. What do you do?") {
            console.log('✅ Test 1 PASSED: Netlify function format');
            passed++;
        } else {
            console.log('❌ Test 1 FAILED: Wrong content extracted');
            console.log('Expected: "You enter a mysterious dungeon filled with ancient magic. What do you do?"');
            console.log('Got:', result);
            failed++;
        }
    } catch (error) {
        console.log('❌ Test 1 FAILED: Exception thrown');
        console.log('Error:', error.message);
        failed++;
    }
    
    // Test 2: Direct Anthropic API response format
    try {
        const result = parseApiResponse(anthropicResponse);
        if (result === "You find yourself in a dark cavern with glowing crystals. Which path do you choose?") {
            console.log('✅ Test 2 PASSED: Direct Anthropic API format');
            passed++;
        } else {
            console.log('❌ Test 2 FAILED: Wrong content extracted');
            console.log('Expected: "You find yourself in a dark cavern with glowing crystals. Which path do you choose?"');
            console.log('Got:', result);
            failed++;
        }
    } catch (error) {
        console.log('❌ Test 2 FAILED: Exception thrown');
        console.log('Error:', error.message);
        failed++;
    }
    
    // Test 3: Invalid response format should throw error
    try {
        const result = parseApiResponse(invalidResponse);
        console.log('❌ Test 3 FAILED: Should have thrown an error');
        console.log('Got result:', result);
        failed++;
    } catch (error) {
        if (error.message === 'Unexpected response format from API') {
            console.log('✅ Test 3 PASSED: Invalid format correctly rejected');
            passed++;
        } else {
            console.log('❌ Test 3 FAILED: Wrong error message');
            console.log('Expected: "Unexpected response format from API"');
            console.log('Got:', error.message);
            failed++;
        }
    }
    
    // Test 4: Edge case - empty choices array
    try {
        const result = parseApiResponse({ choices: [] });
        console.log('❌ Test 4 FAILED: Should have thrown an error');
        failed++;
    } catch (error) {
        console.log('✅ Test 4 PASSED: Empty choices array correctly rejected');
        passed++;
    }
    
    // Test 5: Edge case - missing message in choice
    try {
        const result = parseApiResponse({ choices: [{ role: 'assistant' }] });
        console.log('❌ Test 5 FAILED: Should have thrown an error');
        failed++;
    } catch (error) {
        console.log('✅ Test 5 PASSED: Missing message correctly rejected');
        passed++;
    }
    
    console.log(`\n📊 Test Results: ${passed} passed, ${failed} failed`);
    
    if (failed === 0) {
        console.log('🎉 All tests passed! Response parsing logic is working correctly.');
        process.exit(0);
    } else {
        console.log('💥 Some tests failed. Please fix the parsing logic.');
        process.exit(1);
    }
}

runTests();