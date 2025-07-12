#!/usr/bin/env python3
"""
Vibe Game Backend Server with LiteLLM Integration
Supports both real LLM calls and mocking for testing
"""

import os
import json
import asyncio
import re
from typing import Dict, List, Any, Optional
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import time

try:
    import litellm
    HAS_LITELLM = True
except ImportError:
    HAS_LITELLM = False
    print("Warning: litellm not installed. Install with: pip install litellm")

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    print("Warning: openai not installed. Install with: pip install openai")


class DalleImageGenerator:
    """Handles DALL-E 3 image generation for game scenarios"""
    
    def __init__(self, mock_mode: bool = False):
        self.mock_mode = mock_mode
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
        if not self.mock_mode and self.openai_api_key:
            try:
                self.client = openai.OpenAI(api_key=self.openai_api_key)
            except Exception as e:
                print(f"Warning: Could not initialize OpenAI client: {e}")
                self.client = None
        else:
            self.client = None
    
    def extract_visual_elements(self, text: str) -> List[str]:
        """Extract visual elements from game text for image generation"""
        # Common fantasy/RPG visual elements
        visual_keywords = [
            r'dark forest|mystical forest|enchanted forest|forest',
            r'dragon|dragons',
            r'castle|fortress|tower',
            r'dungeon|cave|cavern',
            r'ancient ruins|ruins|temple',
            r'magical sword|sword|weapon',
            r'glowing|magical glow|mystical light',
            r'stone walls|stone pillars|pillars',
            r'torch|torchlight|firelight',
            r'runes|mysterious symbols|carvings',
            r'starry sky|night sky|stars',
            r'crystal|crystalline|gems',
            r'portal|magical portal',
            r'wizard|sage|mage',
            r'creature|monster|beast',
            r'treasure|gold|jewels',
            r'mountain|cliff|valley',
            r'river|stream|waterfall',
            r'bridge|path|trail'
        ]
        
        elements = []
        text_lower = text.lower()
        
        for pattern in visual_keywords:
            matches = re.findall(pattern, text_lower)
            elements.extend(matches)
        
        # Remove duplicates and return unique elements
        return list(set(elements))
    
    def build_dalle_prompt(self, game_text: str, user_action: str = "") -> str:
        """Build a DALL-E prompt from game context"""
        visual_elements = self.extract_visual_elements(game_text + " " + user_action)
        
        # Base prompt structure
        prompt = "Fantasy RPG scene: "
        
        if visual_elements:
            # Use the most relevant visual elements
            main_elements = visual_elements[:3]  # Limit to avoid overly complex prompts
            prompt += ", ".join(main_elements)
        else:
            # Fallback to general adventure scene
            prompt += "an epic fantasy adventure scene"
        
        # Add style specifications
        prompt += ", digital art style, detailed illustration, cinematic lighting, high quality"
        
        return prompt
    
    def generate_mock_image(self, prompt: str) -> Dict[str, Any]:
        """Generate a mock image response for testing"""
        # Create a descriptive placeholder based on the prompt
        # Extract key words for the placeholder text
        words = prompt.replace(",", " ").split()
        key_words = [w for w in words if w.lower() in ['forest', 'dragon', 'castle', 'dungeon', 'magic', 'sword', 'adventure']]
        
        if key_words:
            placeholder_text = "+".join(key_words[:2])
        else:
            placeholder_text = "Fantasy+Adventure"
        
        mock_url = f"https://via.placeholder.com/1024x1024/4A5568/FFFFFF?text={placeholder_text}"
        
        return {
            "url": mock_url,
            "prompt": prompt,
            "revised_prompt": prompt  # In mock mode, we don't revise the prompt
        }
    
    def generate_image(self, game_text: str, user_action: str = "") -> Optional[Dict[str, Any]]:
        """Generate an image based on game context"""
        try:
            prompt = self.build_dalle_prompt(game_text, user_action)
            
            if self.mock_mode or not self.client:
                return self.generate_mock_image(prompt)
            
            # Real DALL-E API call
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            if response.data:
                image_data = response.data[0]
                return {
                    "url": image_data.url,
                    "prompt": prompt,
                    "revised_prompt": image_data.revised_prompt
                }
            
            return None
            
        except Exception as e:
            print(f"Image generation error: {e}")
            # Fallback to mock image if real API fails
            return self.generate_mock_image(self.build_dalle_prompt(game_text, user_action))


class GameMockResponses:
    """Mock responses for testing - our fallback battle plan"""
    
    RESPONSES = [
        "You venture deeper into the dungeon. The torch light flickers across ancient stone walls carved with mysterious runes. Ahead, you hear the distant sound of dripping water and something else... footsteps? What do you do?",
        
        "A cool breeze carries the scent of adventure from the passage ahead. The shadows dance as your torch illuminates a fork in the path - one way leads up toward distant light, the other down into echoing darkness. Which path calls to you?",
        
        "Your footsteps echo in the silence as you discover a chamber filled with glittering gems embedded in the walls. But wait - those aren't gems, they're eyes! Dozens of creatures watch you from hidden alcoves. How do you react?",
        
        "The dungeon floor suddenly gives way beneath your feet! You tumble into a hidden chamber where ancient magic still pulses through crystalline formations. As you dust yourself off, you notice three doorways marked with different symbols. Which one draws your attention?",
        
        "A wise old sage emerges from the shadows, his beard sparkling with stardust. 'Young adventurer,' he says, 'I sense great potential in you. But first, you must prove your worth.' Will you accept his challenge?",
        
        "The air shimmers and a magical portal opens before you, revealing glimpses of three different realms: a fiery volcanic landscape, a serene underwater kingdom, and a floating city among the clouds. Which realm calls to your adventurous spirit?"
    ]
    
    @classmethod
    def get_random_response(cls) -> str:
        import random
        return random.choice(cls.RESPONSES)
    
    @classmethod
    def get_contextual_response(cls, user_input: str) -> str:
        """Generate contextual mock responses based on user input"""
        input_lower = user_input.lower()
        
        if any(word in input_lower for word in ['attack', 'fight', 'combat', 'sword']):
            return "You draw your weapon and prepare for battle! The creature before you snarls and circles, looking for an opening. Roll for initiative - what's your strategy?"
            
        elif any(word in input_lower for word in ['look', 'examine', 'search', 'investigate']):
            return "As you carefully examine your surroundings, you notice intricate details previously hidden in shadow. Ancient carvings tell a story of heroes past, and you spot something glinting in a nearby alcove. What catches your attention?"
            
        elif any(word in input_lower for word in ['north', 'south', 'east', 'west', 'go', 'move']):
            return "You move cautiously in that direction, your footsteps echoing off the stone walls. The path ahead curves mysteriously, and you hear distant sounds that make your heart race with excitement. What do you do as you continue forward?"
            
        elif any(word in input_lower for word in ['talk', 'speak', 'say', 'ask']):
            return "Your words echo in the chamber, and to your surprise, you hear a response! A mysterious voice seems to come from everywhere and nowhere at once: 'Welcome, brave soul. Your journey has only just begun...' How do you respond?"
            
        else:
            return cls.get_random_response()


class VibeGameHandler(BaseHTTPRequestHandler):
    """HTTP request handler for our game server"""
    
    def __init__(self, *args, mock_mode=False, **kwargs):
        self.mock_mode = mock_mode
        self.image_generator = DalleImageGenerator(mock_mode=mock_mode)
        super().__init__(*args, **kwargs)
    
    def _set_cors_headers(self):
        """Set CORS headers for frontend access"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def do_OPTIONS(self):
        """Handle preflight CORS requests"""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        """Serve static files and game interface"""
        if self.path == '/' or self.path == '/index.html':
            self._serve_file('index.html', 'text/html')
        elif self.path == '/style.css':
            self._serve_file('style.css', 'text/css')
        elif self.path == '/script.js':
            self._serve_file('script.js', 'application/javascript')
        elif self.path == '/health':
            self._serve_json({'status': 'healthy', 'mock_mode': self.mock_mode})
        else:
            self.send_error(404, 'File not found')
    
    def do_POST(self):
        """Handle API requests"""
        if self.path == '/api/chat':
            self._handle_chat_request()
        else:
            self.send_error(404, 'API endpoint not found')
    
    def _serve_file(self, filename: str, content_type: str):
        """Serve a static file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self._set_cors_headers()
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
            
        except FileNotFoundError:
            self.send_error(404, f'File not found: {filename}')
        except Exception as e:
            self.send_error(500, f'Error serving file: {str(e)}')
    
    def _serve_json(self, data: Dict[str, Any]):
        """Send JSON response"""
        json_data = json.dumps(data)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self._set_cors_headers()
        self.end_headers()
        self.wfile.write(json_data.encode('utf-8'))
    
    def _handle_chat_request(self):
        """Handle chat API requests - the heart of our dungeon master"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            messages = request_data.get('messages', [])
            model = request_data.get('model', 'gpt-3.5-turbo')
            
            if not messages:
                self._serve_json({'error': 'No messages provided'})
                return
            
            # Get the last user message for context
            user_message = ""
            for msg in reversed(messages):
                if msg.get('role') == 'user':
                    user_message = msg.get('content', '')
                    break
            
            if self.mock_mode or not HAS_LITELLM:
                # Use mock responses for testing
                response_content = GameMockResponses.get_contextual_response(user_message)
                
                # Generate image based on the response
                image_data = self.image_generator.generate_image(response_content, user_message)
                
                response = {
                    'choices': [{
                        'message': {
                            'content': response_content,
                            'role': 'assistant'
                        }
                    }],
                    'usage': {'total_tokens': 50},  # Mock usage
                    'model': 'mock-dm'
                }
                
                # Add image data to response
                if image_data:
                    response['image'] = image_data
            else:
                # Use real LiteLLM call
                try:
                    response = litellm.completion(
                        model=model,
                        messages=messages,
                        max_tokens=request_data.get('max_tokens', 200),
                        temperature=request_data.get('temperature', 0.8)
                    )
                    # Convert to dict if needed
                    if hasattr(response, 'model_dump'):
                        response = response.model_dump()
                    elif hasattr(response, 'dict'):
                        response = response.dict()
                    
                    # Generate image based on the LLM response
                    if 'choices' in response and len(response['choices']) > 0:
                        ai_response = response['choices'][0]['message']['content']
                        image_data = self.image_generator.generate_image(ai_response, user_message)
                        
                        if image_data:
                            response['image'] = image_data
                    
                except Exception as e:
                    print(f"LiteLLM error: {e}")
                    # Fallback to mock response
                    response_content = GameMockResponses.get_contextual_response(user_message)
                    
                    # Generate image for fallback response too
                    image_data = self.image_generator.generate_image(response_content, user_message)
                    
                    response = {
                        'choices': [{
                            'message': {
                                'content': f"{response_content}\n\n*(Note: Using fallback response due to API error)*",
                                'role': 'assistant'
                            }
                        }],
                        'error': str(e)
                    }
                    
                    if image_data:
                        response['image'] = image_data
            
            self._serve_json(response)
            
        except json.JSONDecodeError:
            self._serve_json({'error': 'Invalid JSON in request'})
        except Exception as e:
            print(f"Chat request error: {e}")
            self._serve_json({'error': f'Server error: {str(e)}'})
    
    def log_message(self, format, *args):
        """Custom logging"""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {format % args}")


def create_handler_with_mock(mock_mode: bool):
    """Factory function to create handler with mock mode setting"""
    def handler(*args, **kwargs):
        return VibeGameHandler(*args, mock_mode=mock_mode, **kwargs)
    return handler


def run_server(port: int = 8000, mock_mode: bool = False):
    """Run the game server - our command center"""
    handler_class = create_handler_with_mock(mock_mode)
    
    server = HTTPServer(('localhost', port), handler_class)
    
    mode = "MOCK" if mock_mode else "LIVE"
    print(f"🎲 Vibe Game Server [{mode}] starting on http://localhost:{port}")
    print(f"   Frontend: http://localhost:{port}")
    print(f"   Health: http://localhost:{port}/health")
    print("   Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopping...")
        server.shutdown()


if __name__ == '__main__':
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Vibe Game Server')
    parser.add_argument('--port', type=int, default=8000, help='Port to run server on')
    parser.add_argument('--mock', action='store_true', help='Run in mock mode for testing')
    parser.add_argument('--test', action='store_true', help='Run quick test and exit')
    
    args = parser.parse_args()
    
    if args.test:
        print("🧪 Running quick test...")
        mock_response = GameMockResponses.get_contextual_response("I attack the dragon")
        print(f"Mock response: {mock_response}")
        print("✅ Test complete!")
    else:
        run_server(args.port, args.mock)