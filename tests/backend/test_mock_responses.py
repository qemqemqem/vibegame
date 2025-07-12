#!/usr/bin/env python3
"""
Test suite for backend mock responses
This is our first line of defense - testing the fallback system!
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

import pytest
from server import GameMockResponses


class TestGameMockResponses:
    """Test our mock response system - our shield wall against API failures"""
    
    def test_get_random_response_returns_string(self):
        """Ensure we always get a valid response"""
        response = GameMockResponses.get_random_response()
        assert isinstance(response, str)
        assert len(response) > 0
        assert response in GameMockResponses.RESPONSES
    
    def test_contextual_response_combat(self):
        """Test combat-related responses"""
        combat_inputs = ['attack the dragon', 'I fight', 'draw sword', 'combat']
        
        for input_text in combat_inputs:
            response = GameMockResponses.get_contextual_response(input_text)
            assert isinstance(response, str)
            assert len(response) > 0
            # Should mention combat-related terms
            assert any(word in response.lower() for word in ['weapon', 'battle', 'fight', 'combat', 'attack'])
    
    def test_contextual_response_movement(self):
        """Test movement-related responses"""
        movement_inputs = ['go north', 'move forward', 'walk east', 'head south']
        
        for input_text in movement_inputs:
            response = GameMockResponses.get_contextual_response(input_text)
            assert isinstance(response, str)
            assert len(response) > 0
            # Should mention movement or direction
            assert any(word in response.lower() for word in ['move', 'forward', 'path', 'direction', 'ahead'])
    
    def test_contextual_response_investigation(self):
        """Test investigation-related responses"""
        investigation_inputs = ['look around', 'examine the room', 'search for clues', 'investigate']
        
        for input_text in investigation_inputs:
            response = GameMockResponses.get_contextual_response(input_text)
            assert isinstance(response, str)
            assert len(response) > 0
            # Should mention looking or examining
            assert any(word in response.lower() for word in ['examine', 'look', 'notice', 'see', 'observe'])
    
    def test_contextual_response_social(self):
        """Test social interaction responses"""
        social_inputs = ['talk to the guard', 'speak with NPC', 'ask about quest', 'say hello']
        
        for input_text in social_inputs:
            response = GameMockResponses.get_contextual_response(input_text)
            assert isinstance(response, str)
            assert len(response) > 0
            # Should mention communication
            assert any(word in response.lower() for word in ['voice', 'speak', 'response', 'words', 'say'])
    
    def test_contextual_response_fallback(self):
        """Test fallback for unrecognized inputs"""
        random_inputs = ['asdfghjkl', 'random nonsense', '12345', '']
        
        for input_text in random_inputs:
            response = GameMockResponses.get_contextual_response(input_text)
            assert isinstance(response, str)
            assert len(response) > 0
            # Should be one of our standard responses
            assert response in GameMockResponses.RESPONSES
    
    def test_all_responses_are_valid(self):
        """Ensure all mock responses meet quality standards"""
        for response in GameMockResponses.RESPONSES:
            assert isinstance(response, str)
            assert len(response) > 50  # Substantial responses
            assert response.endswith('?')  # Should end with a question
            assert not response.startswith(' ')  # No leading whitespace
            assert not response.endswith(' ')  # No trailing whitespace
    
    def test_response_variety(self):
        """Ensure we get different responses for different calls"""
        responses = [GameMockResponses.get_random_response() for _ in range(10)]
        # Should have some variety (not all the same)
        assert len(set(responses)) > 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])