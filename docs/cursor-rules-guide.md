# 🎯 Cursor Rules Guide for Vibe Game Development

## Overview

This guide outlines the three levels of Cursor rules and how to use them effectively for our vibe game project. Based on extensive research and best practices, this will help you set up effective AI assistance for game development.

## The Three Levels of Cursor Rules

### 1. Global Rules (Cursor Settings)
**Location**: Cursor → Settings → Rules for AI
**Scope**: All projects
**Visibility**: Only you (local settings)

These are universal coding standards that apply to all your projects. Keep these focused on fundamental principles like code style, error handling, and general best practices.

### 2. Project-Specific Rules (.cursorrules file)
**Location**: `.cursorrules` file in project root
**Scope**: This repository only
**Visibility**: Entire team via repository

This is where our main game development rules live. The file we created contains:
- Test-driven development practices
- Game-specific architecture patterns
- AI/DM integration guidelines
- Mobile-first design principles

### 3. Context-Aware Rules (.cursor/rules/*.mdc files)
**Location**: `.cursor/rules/` directory
**Scope**: Specific tasks or contexts
**Visibility**: Entire team via repository

These would be specialized rules that only activate for specific contexts (not created yet, but useful for complex projects).

## Why These Rules Matter for Game Development

### 1. **Consistent Game Logic**
- AI generates code that follows our established patterns
- Game state management remains predictable
- Testing practices ensure reliability

### 2. **Mobile-First Focus**
- AI understands our mobile-first approach
- Touch interactions are properly considered
- Performance optimization for mobile devices

### 3. **AI/DM Integration**
- Proper handling of mock vs real LLM modes
- Context-aware responses for different game scenarios
- Error handling for API failures

### 4. **Testing Excellence**
- Prevents the "bat attack" cultural risk
- Ensures thorough testing of game mechanics
- Maintains high quality for vibe coding

## Best Practices for Using Cursor Rules

### 1. **Start with Tests**
```bash
# Always write tests first
# This is not just best practice, it's cultural protection!
pytest tests/backend/test_new_feature.py  # Should fail initially
```

### 2. **Reference Context When Needed**
When hitting context limits, reference key files:
```
@README.md @.cursorrules
Let's continue implementing the combat system...
```

### 3. **Keep Rules Updated**
- Update `.cursorrules` as the project evolves
- Document new patterns and practices
- Remove outdated rules

### 4. **Use Task-Specific Context**
For complex features, create specific context files:
```
@docs/combat-system.md @tests/backend/test_combat.py
Implement the spell casting mechanics...
```

## Common Pitfalls to Avoid

### 1. **Too Many Rules**
- Don't overwhelm the AI with excessive guidelines
- Focus on the most important patterns
- Keep rules concise and actionable

### 2. **Conflicting Rules**
- Ensure rules don't contradict each other
- Test rules with simple examples
- Resolve conflicts quickly

### 3. **Ignoring Context Limits**
- AI assistants have token limits
- Use file references to restore context
- Keep important context in easily referenceable files

### 4. **Forgetting the Cultural Practice**
- Always acknowledge the "bat attack" risk
- Write tests before implementation
- Respect the cultural importance of TDD

## Game-Specific Rule Categories

### 1. **Game State Management**
- Predictable state transitions
- Immutable patterns where possible
- Consistent frontend/backend sync

### 2. **AI/DM Interactions**
- Mock mode for testing
- Context-aware responses
- Error recovery patterns

### 3. **Mobile Gaming**
- Touch-friendly interfaces
- Performance considerations
- Battery usage awareness

### 4. **Testing Game Mechanics**
- Edge case coverage
- Player journey validation
- AI response consistency

## Implementation Checklist

- [x] Create `.cursorrules` file with game-specific rules
- [x] Include TDD practices and cultural considerations
- [x] Document game architecture patterns
- [x] Add mobile-first design principles
- [ ] Test rules with sample implementations
- [ ] Create context-aware rules if needed
- [ ] Update global settings for universal patterns
- [ ] Train team on rule usage

## Monitoring and Improvement

### 1. **Track Rule Effectiveness**
- Monitor code quality improvements
- Measure development speed
- Gather team feedback

### 2. **Iterate and Improve**
- Update rules based on experience
- Add new patterns as they emerge
- Remove outdated guidelines

### 3. **Team Alignment**
- Ensure all team members understand rules
- Review and update regularly
- Document rule changes

## Next Steps

1. **Test the Current Rules**
   - Create a simple feature using TDD
   - Verify AI follows the established patterns
   - Refine rules based on results

2. **Expand Context Files**
   - Create domain-specific documentation
   - Add architecture diagrams
   - Document game mechanics

3. **Team Training**
   - Share this guide with team members
   - Practice using rules in development
   - Establish review processes

## Resources and References

- [Cursor Rules Documentation](https://cursor.sh/docs/rules)
- [Game Development Best Practices](https://gamedev.stackexchange.com)
- [TDD for Game Development](https://testdrivendevjamesshore.com)
- [Mobile Game Performance](https://developer.mozilla.org/en-US/docs/Games/Performance)

Remember: The goal is not to constrain AI, but to guide it toward producing the high-quality, tested code that makes vibe coding a joy! 🎮✨