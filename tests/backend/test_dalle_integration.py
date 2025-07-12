#!/usr/bin/env python3
"""
DALL-E 3 Integration Tests for Vibe Game
Tests image generation functionality with OpenAI API

Following TDD approach - tests written first!
"""

import os
import json
import unittest
from unittest.mock import patch, MagicMock
import sys
import requests
from datetime import datetime

# Add backend to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from server import VibeGameHandler, GameMockResponses


class TestDalleIntegration(unittest.TestCase):
    """Test DALL-E 3 integration for generating images"""
    
    def setUp(self):
        """Set up test environment"""
        # Don't instantiate handlers directly since they need HTTP context
        # We'll test the functionality through other means
        self.mock_mode = True
        self.real_mode = False
        
    def test_openai_api_key_environment_check(self):
        """Test that OPENAI_API_KEY can be loaded from environment"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'sk-test-key-123'}):
            # This should work when we implement the functionality
            self.assertEqual(os.getenv('OPENAI_API_KEY'), 'sk-test-key-123')
            
    def test_dalle_mock_response_generation(self):
        """Test that mock mode generates placeholder images"""
        # Mock scenario - should generate a placeholder image URL
        user_message = "I explore the mystical forest"
        game_text = "You venture into a dark forest with mystical creatures"
        
        # Test the DalleImageGenerator directly
        from server import DalleImageGenerator
        generator = DalleImageGenerator(mock_mode=True)
        
        result = generator.generate_image(game_text, user_message)
        
        # Check that we get a mock image response
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertIn('url', result)
        self.assertIn('prompt', result)
        self.assertIn('revised_prompt', result)
        self.assertTrue(result['url'].startswith('https://via.placeholder.com/'))
        
    def test_dalle_real_api_call_structure(self):
        """Test the structure of real DALL-E API calls"""
        # Test payload structure for DALL-E 3 API
        expected_payload = {
            "model": "dall-e-3",
            "prompt": "Fantasy RPG scene: A brave adventurer exploring a mystical forest filled with ancient trees and magical creatures, digital art style",
            "size": "1024x1024",
            "quality": "standard",
            "n": 1
        }
        
        # This test will fail until we implement the real API integration
        self.fail("DALL-E real API integration not implemented yet")
        
    def test_prompt_generation_from_game_context(self):
        """Test generating DALL-E prompts from game context"""
        from server import DalleImageGenerator
        generator = DalleImageGenerator(mock_mode=True)
        
        game_response = "You venture deeper into the dungeon. The torch light flickers across ancient stone walls carved with mysterious runes."
        user_action = "I examine the runes carefully"
        
        prompt = generator.build_dalle_prompt(game_response, user_action)
        
        # Expected prompt should combine game context with visual description
        expected_prompt_parts = [
            "Fantasy RPG scene:",
            "digital art style"
        ]
        
        # Check that the prompt includes expected parts
        for part in expected_prompt_parts:
            self.assertIn(part, prompt)
        
        # Check that some visual elements from the game context are included
        visual_elements = ["dungeon", "torch", "stone walls", "runes"]
        found_elements = [elem for elem in visual_elements if elem in prompt.lower()]
        self.assertGreater(len(found_elements), 0, f"No visual elements found in prompt: {prompt}")
        
    def test_chat_response_includes_image(self):
        """Test that chat responses now include generated images"""
        # Mock a chat request
        messages = [
            {"role": "user", "content": "I enter the magical castle"}
        ]
        
        # Expected response should include both text and image
        expected_response_structure = {
            "choices": [{
                "message": {
                    "content": "string",  # The DM's text response
                    "role": "assistant"
                }
            }],
            "image": {
                "url": "string",  # The generated image URL
                "prompt": "string",  # The prompt used to generate the image
                "revised_prompt": "string"  # OpenAI's revised prompt
            },
            "usage": {"total_tokens": "number"}
        }
        
        # This test will fail until we implement the enhanced response structure
        self.fail("Enhanced chat response with images not implemented yet")
        
    def test_image_generation_error_handling(self):
        """Test graceful handling of image generation failures"""
        # When DALL-E API fails, chat should still work with text-only response
        with patch('requests.post') as mock_post:
            # Mock DALL-E API failure
            mock_post.side_effect = requests.exceptions.RequestException("API Error")
            
            # Chat response should still work, just without image
            # This test will fail until we implement error handling
            self.fail("Image generation error handling not implemented yet")
            
    def test_cost_calculation_with_images(self):
        """Test cost calculation including both text and image generation"""
        # DALL-E 3 costs $0.040 per image (1024x1024 standard)
        # Should be added to existing text generation costs
        
        dalle_cost = 0.040  # Per image
        text_cost = 0.0005  # Approximate per message
        total_expected = dalle_cost + text_cost
        
        # This test will fail until we implement cost calculation
        self.fail("Cost calculation with images not implemented yet")
        
    def test_openai_api_key_validation(self):
        """Test OpenAI API key format validation"""
        valid_keys = [
            "sk-proj-1234567890abcdef",
            "sk-1234567890abcdef"
        ]
        
        invalid_keys = [
            "invalid-key",
            "sk-ant-api-123",  # Anthropic format
            "",
            None
        ]
        
        # This test will fail until we implement key validation
        self.fail("OpenAI API key validation not implemented yet")


class TestDallePromptGeneration(unittest.TestCase):
    """Test DALL-E prompt generation from game context"""
    
    def test_extract_visual_elements_from_text(self):
        """Test extracting visual elements from game text"""
        from server import DalleImageGenerator
        generator = DalleImageGenerator(mock_mode=True)
        
        test_cases = [
            {
                "text": "You enter a dark forest with twisted trees and glowing mushrooms",
                "expected_elements": ["forest", "glowing"]
            },
            {
                "text": "The dragon breathes fire as you raise your magical sword",
                "expected_elements": ["dragon", "sword"]
            },
            {
                "text": "Ancient stone pillars reach toward the starry sky",
                "expected_elements": ["stone pillars", "starry sky"]
            }
        ]
        
        for test_case in test_cases:
            with self.subTest(text=test_case["text"]):
                elements = generator.extract_visual_elements(test_case["text"])
                self.assertIsInstance(elements, list)
                # Check that at least some expected elements are found
                found_elements = [elem for elem in test_case["expected_elements"] if elem in elements]
                self.assertGreater(len(found_elements), 0, f"No expected elements found in {elements}")
        
    def test_build_dalle_prompt_from_elements(self):
        """Test building DALL-E prompts from visual elements"""
        from server import DalleImageGenerator
        generator = DalleImageGenerator(mock_mode=True)
        
        game_text = "You explore a mystical forest with ancient ruins and magical glow"
        user_action = "I investigate the ruins"
        
        prompt = generator.build_dalle_prompt(game_text, user_action)
        
        # Check that the prompt has the expected structure
        self.assertIsInstance(prompt, str)
        self.assertTrue(prompt.startswith("Fantasy RPG scene:"))
        self.assertIn("digital art style", prompt)
        # Check that some visual elements are included
        self.assertTrue(any(element in prompt.lower() for element in ["forest", "ruins", "magical"]))


if __name__ == '__main__':
    print("🎨 DALL-E Integration Tests")
    print("=" * 50)
    print("⚠️  These tests will fail until implementation is complete")
    print("   This is expected with TDD approach!")
    print()
    
    unittest.main(verbosity=2)