#!/usr/bin/env python3
"""
Anthropic API Connection Test for Vibe Game
Tests the direct API connection using environment variables

Run this locally to verify your API key and connection work correctly!
"""

import os
import sys
import json
import time
import requests
from datetime import datetime

class AnthropicConnectionTester:
    def __init__(self):
        self.api_key = None
        self.base_url = "https://api.anthropic.com/v1"
        self.test_results = []
        
    def print_header(self):
        """Print test header with timestamp"""
        print("=" * 60)
        print("🤖 ANTHROPIC API CONNECTION TEST")
        print("=" * 60)
        print(f"⏰ Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

    def check_environment(self):
        """Check if API key is properly configured"""
        print("🔍 STEP 1: Checking Environment Configuration")
        print("-" * 40)
        
        # Check for .env file
        env_file_exists = os.path.exists('.env')
        print(f"📁 .env file exists: {'✅ Yes' if env_file_exists else '❌ No'}")
        
        if env_file_exists:
            try:
                with open('.env', 'r') as f:
                    env_content = f.read()
                    has_anthropic_key = 'ANTHROPIC_API_KEY' in env_content
                    print(f"🔑 ANTHROPIC_API_KEY in .env: {'✅ Yes' if has_anthropic_key else '❌ No'}")
            except Exception as e:
                print(f"❌ Error reading .env file: {e}")
        
        # Check environment variable
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        if self.api_key:
            print(f"🔑 API Key loaded: ✅ Yes (length: {len(self.api_key)} chars)")
            if self.api_key.startswith('sk-ant-api'):
                print(f"🔑 API Key format: ✅ Valid (starts with 'sk-ant-api')")
            else:
                print(f"🔑 API Key format: ❌ Invalid (should start with 'sk-ant-api')")
                print(f"   Your key starts with: '{self.api_key[:10]}...'")
                return False
        else:
            print("🔑 API Key loaded: ❌ No")
            print("\n🚨 API KEY NOT FOUND!")
            print("To fix this:")
            print("1. Create a .env file in the project root")
            print("2. Add this line: ANTHROPIC_API_KEY=sk-ant-api-your-key-here")  
            print("3. Get your key from: https://console.anthropic.com/")
            print("4. Run: export ANTHROPIC_API_KEY=$(cat .env | grep ANTHROPIC_API_KEY | cut -d'=' -f2)")
            return False
            
        print("✅ Environment configuration looks good!")
        return True

    def check_network_connectivity(self):
        """Test basic network connectivity to Anthropic"""
        print("\n🌐 STEP 2: Checking Network Connectivity")
        print("-" * 40)
        
        try:
            # Test basic connectivity
            print("📡 Testing connection to api.anthropic.com...")
            response = requests.get("https://api.anthropic.com", timeout=10)
            print(f"📡 Connection status: ✅ Connected (status: {response.status_code})")
            
            # Test if we can reach the messages endpoint
            print("📡 Testing messages endpoint accessibility...")
            headers = {
                'x-api-key': 'invalid-key-for-connectivity-test',
                'anthropic-version': '2023-06-01',
                'content-type': 'application/json'
            }
            
            test_response = requests.post(
                f"{self.base_url}/messages", 
                headers=headers,
                json={'model': 'claude-3-5-haiku-20241022', 'messages': [], 'max_tokens': 1},
                timeout=10
            )
            
            if test_response.status_code == 401:
                print("📡 Messages endpoint: ✅ Accessible (401 = auth required, as expected)")
            else:
                print(f"📡 Messages endpoint: ⚠️ Unexpected response ({test_response.status_code})")
                
            return True
            
        except requests.ConnectionError:
            print("❌ Connection failed: Cannot reach api.anthropic.com")
            print("Possible causes:")
            print("  - No internet connection")
            print("  - Firewall blocking HTTPS requests")
            print("  - VPN/proxy issues")
            print("  - Corporate network restrictions")
            return False
            
        except requests.Timeout:
            print("❌ Connection timeout: Request took too long")
            print("Possible causes:")
            print("  - Slow internet connection")
            print("  - Network congestion")
            print("  - Firewall deep packet inspection")
            return False
            
        except Exception as e:
            print(f"❌ Unexpected network error: {e}")
            return False

    def test_api_authentication(self):
        """Test API key authentication"""
        print("\n🔐 STEP 3: Testing API Authentication")
        print("-" * 40)
        
        headers = {
            'x-api-key': self.api_key,
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json'
        }
        
        # Minimal test request
        test_payload = {
            'model': 'claude-3-5-haiku-20241022',
            'max_tokens': 10,
            'messages': [{'role': 'user', 'content': 'Hello'}]
        }
        
        try:
            print("🔐 Testing API key authentication...")
            response = requests.post(
                f"{self.base_url}/messages",
                headers=headers,
                json=test_payload,
                timeout=30
            )
            
            if response.status_code == 200:
                print("🔐 Authentication: ✅ Success!")
                data = response.json()
                if 'content' in data and len(data['content']) > 0:
                    print(f"🔐 Response received: ✅ Valid ({len(data['content'][0]['text'])} chars)")
                    return True
                else:
                    print("🔐 Response format: ❌ Unexpected format")
                    print(f"Response: {json.dumps(data, indent=2)}")
                    return False
                    
            elif response.status_code == 401:
                print("❌ Authentication failed: Invalid API key")
                print("Troubleshooting steps:")
                print("1. Verify your API key is correct")
                print("2. Check if the key is active in console.anthropic.com")
                print("3. Ensure you haven't exceeded rate limits")
                print("4. Try regenerating your API key")
                return False
                
            elif response.status_code == 400:
                print("❌ Bad request: API request format issue")
                try:
                    error_data = response.json()
                    print(f"Error details: {json.dumps(error_data, indent=2)}")
                except:
                    print(f"Raw error: {response.text}")
                return False
                
            elif response.status_code == 429:
                print("❌ Rate limited: Too many requests")
                print("Possible solutions:")
                print("  - Wait a few minutes and try again")
                print("  - Check your rate limits in console.anthropic.com")
                print("  - Upgrade your Anthropic plan if needed")
                return False
                
            elif response.status_code == 500:
                print("❌ Server error: Anthropic API is having issues")
                print("This is likely temporary. Try again in a few minutes.")
                return False
                
            else:
                print(f"❌ Unexpected response: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except requests.Timeout:
            print("❌ Request timeout: API call took too long")
            print("Possible causes:")
            print("  - Slow internet connection")
            print("  - Anthropic API experiencing high load")
            print("  - Network firewall interference")
            return False
            
        except Exception as e:
            print(f"❌ Unexpected error during authentication test: {e}")
            return False

    def test_game_scenario(self):
        """Test a realistic game scenario"""
        print("\n🎮 STEP 4: Testing Game Scenario")
        print("-" * 40)
        
        game_system_prompt = """You are an expert Dungeon Master running an immersive fantasy RPG adventure. Your role is to:

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

The player has just entered your dungeon. Guide them on an epic adventure!"""

        headers = {
            'x-api-key': self.api_key,
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json'
        }
        
        test_payload = {
            'model': 'claude-3-5-haiku-20241022',
            'max_tokens': 200,
            'temperature': 0.8,
            'system': game_system_prompt,
            'messages': [
                {'role': 'user', 'content': 'I look around the dungeon entrance.'}
            ]
        }
        
        try:
            print("🎮 Testing game scenario with Claude 3.5 Haiku...")
            start_time = time.time()
            
            response = requests.post(
                f"{self.base_url}/messages",
                headers=headers,
                json=test_payload,
                timeout=30
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data['content'][0]['text']
                
                print(f"🎮 Game test: ✅ Success!")
                print(f"⏱️ Response time: {response_time:.2f} seconds")
                print(f"📊 Tokens used: {data.get('usage', {}).get('input_tokens', 'N/A')} input, {data.get('usage', {}).get('output_tokens', 'N/A')} output")
                
                # Calculate estimated cost
                if 'usage' in data:
                    input_tokens = data['usage'].get('input_tokens', 0)
                    output_tokens = data['usage'].get('output_tokens', 0)
                    cost = (input_tokens * 0.80 / 1000000) + (output_tokens * 4.00 / 1000000)
                    print(f"💰 Estimated cost: ${cost:.6f}")
                
                print("\n📝 Sample AI Response:")
                print("-" * 30)
                print(f'"{ai_response}"')
                print("-" * 30)
                
                # Quality checks
                if len(ai_response) > 50:
                    print("📏 Response length: ✅ Substantial")
                else:
                    print("📏 Response length: ⚠️ Short (may indicate issues)")
                    
                if ai_response.endswith('?'):
                    print("❓ Ends with question: ✅ Good DM practice")
                else:
                    print("❓ Ends with question: ⚠️ Missing (DM should ask questions)")
                
                return True
                
            else:
                print(f"❌ Game test failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Game scenario test failed: {e}")
            return False

    def test_cost_estimation(self):
        """Estimate costs for different usage patterns"""
        print("\n💰 STEP 5: Cost Estimation")
        print("-" * 40)
        
        # Claude 3.5 Haiku pricing (per million tokens)
        input_cost_per_million = 0.80
        output_cost_per_million = 4.00
        
        # Typical game message estimates
        avg_input_tokens = 150  # User message + system prompt + conversation history
        avg_output_tokens = 120  # DM response
        
        cost_per_message = (
            (avg_input_tokens * input_cost_per_million / 1000000) + 
            (avg_output_tokens * output_cost_per_million / 1000000)
        )
        
        print(f"🎲 Estimated cost per message: ${cost_per_message:.6f}")
        print()
        
        usage_patterns = [
            ("Casual player", "5 messages/week", 5 * 4),
            ("Regular player", "20 messages/week", 20 * 4), 
            ("Heavy player", "100 messages/week", 100 * 4),
            ("Daily player", "10 messages/day", 10 * 30)
        ]
        
        for pattern_name, pattern_desc, monthly_messages in usage_patterns:
            monthly_cost = monthly_messages * cost_per_message
            print(f"👤 {pattern_name:<15} ({pattern_desc:<20}): ${monthly_cost:.2f}/month")
        
        print()
        print("💡 Cost-saving tips:")
        print("  - Monitor usage in console.anthropic.com")
        print("  - Set usage limits in your Anthropic account")
        print("  - Game provides fallback mock responses if API fails")
        print("  - Users can remove API key anytime to use only mock responses")

    def run_all_tests(self):
        """Run complete test suite"""
        self.print_header()
        
        # Test results tracking
        tests = [
            ("Environment Check", self.check_environment),
            ("Network Connectivity", self.check_network_connectivity), 
            ("API Authentication", self.test_api_authentication),
            ("Game Scenario", self.test_game_scenario)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
                    self.test_results.append((test_name, "PASS"))
                else:
                    self.test_results.append((test_name, "FAIL"))
                    # If a critical test fails, stop here
                    if test_name in ["Environment Check", "Network Connectivity"]:
                        break
            except Exception as e:
                print(f"❌ {test_name} crashed: {e}")
                self.test_results.append((test_name, "CRASH"))
        
        # Always run cost estimation (doesn't require API)
        self.test_cost_estimation()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        for test_name, result in self.test_results:
            status_icon = "✅" if result == "PASS" else "❌"
            print(f"{status_icon} {test_name}: {result}")
        
        print()
        if passed == total:
            print("🎉 ALL TESTS PASSED! Your Anthropic API integration is ready!")
            print()
            print("🚀 Next steps:")
            print("  1. Your API key is working correctly")
            print("  2. Deploy your game to GitHub Pages")
            print("  3. Users can add their own API keys for real Claude AI")
            print("  4. Start vibecoding epic adventures!")
            
        elif passed > 0:
            print(f"⚠️ PARTIAL SUCCESS: {passed}/{total} tests passed")
            print("   Fix the failing tests above, then try again.")
            
        else:
            print("❌ ALL TESTS FAILED")
            print("   Check the error messages above and fix issues before deploying.")
        
        print()
        print(f"⏰ Test completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

if __name__ == "__main__":
    print("🎲 Vibe Game - Anthropic API Connection Test")
    print()
    
    # Check if required packages are installed
    try:
        import requests
    except ImportError:
        print("❌ Error: 'requests' package not found")
        print("Install with: pip install requests")
        sys.exit(1)
    
    tester = AnthropicConnectionTester()
    tester.run_all_tests()