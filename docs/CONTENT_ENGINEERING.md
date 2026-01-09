# Content Engineering for World-Aware DM

## The Challenge

We have a rich 23K+ token Shakespeare sci-fantasy world that needs to inform DM responses, but Claude 3.5 Haiku's system prompt should be optimized for performance. We need **smart content injection** that gives the DM relevant world knowledge without overwhelming the context.

## Current System Analysis

**✅ Strengths:**
- 200K token context window (plenty of room)
- Fast Claude 3.5 Haiku (65.2 tokens/sec)
- Clean conversation history tracking
- Serverless architecture via Netlify

**⚠️ Constraints:**
- Generic 500-token system prompt
- No world awareness currently
- 200 token response limit (artificially low)
- No entity recognition or dynamic loading

## Recommended Architecture: **Hybrid Smart Loading**

### 🎯 Core Strategy
**"Load what matters, when it matters"** - Dynamically inject relevant world content based on context analysis.

### 🏗️ Architecture Components

#### 1. **Context Analyzer** 
Analyzes user input + conversation history to identify:
- **Mentioned Entities**: Characters, locations, items by name
- **Implicit Context**: Keywords that suggest relevant content
- **Narrative Phase**: Combat, exploration, social interaction, etc.

#### 2. **Content Prioritizer**
Ranks world content by relevance:
- **High Priority**: Directly mentioned entities 
- **Medium Priority**: Related entities (relationships, inhabitants)
- **Low Priority**: World lore and background context
- **Ongoing**: Currently active story elements

#### 3. **Dynamic System Prompt Builder**
Constructs optimal prompts containing:
- **Base DM Instructions** (~500 tokens)
- **World Overview** (~1K tokens)  
- **Relevant Entities** (~3-8K tokens)
- **Active Plot Threads** (~500 tokens)
- **Total Budget**: 5-10K tokens (2.5-5% of context window)

#### 4. **Entity Relationship Loader**
When an entity is loaded, automatically include:
- Related characters (relationships.json)
- Current location inhabitants  
- Relevant items in the area
- Plot hooks from secrets files

## Implementation Approaches

### 🚀 **Approach 1: Smart Keyword Matching** *(Recommended for MVP)*

**Pros:**
- Simple to implement
- No external dependencies
- Fast performance
- Works with existing architecture

**Implementation:**
1. **Entity Recognition**: Match user input against entity names and aliases
2. **Content Assembly**: Load JSON + markdown for matched entities
3. **Prompt Injection**: Add to system prompt with clear XML structure
4. **Fallback Graceful**: Always include world overview if no matches

**Code Flow:**
```javascript
// In Netlify function
const worldContent = analyzeAndLoadContent(userMessage, conversationHistory);
const enhancedSystemPrompt = `${BASE_DM_PROMPT}\n\n${worldContent}`;
```

### 🧠 **Approach 2: Embedding-Based RAG** *(Future Enhancement)*

**Pros:**
- Semantic understanding
- Finds relevant content beyond keywords
- Handles synonyms and indirect references
- Most sophisticated approach

**Cons:**
- Requires vector database (Pinecone/Chroma)
- Additional API calls and latency
- More complex deployment
- Embedding API costs

### 🎭 **Approach 3: Campaign State Tracking** *(Long-term)*

**Pros:**
- Maintains ongoing narrative threads
- Remembers what players have discovered
- Evolves world state based on actions
- Enables persistent campaigns

**Implementation:**
- Session state management
- Plot thread tracking
- Discovered entity logging
- Dynamic secret revelation

## Detailed Smart Keyword Approach

### Content Loading Strategy

#### **Priority 1: Direct Mentions**
```
User: "I talk to Prospero"
→ Load: prospero_technomancer/* (all files)
→ Include: dialogue patterns, current motivations, secrets DM needs
```

#### **Priority 2: Location Context**
```
User: "I explore the station"
Current Location: Globe Nexus Station
→ Load: globe_nexus_station/* + inhabitants
→ Include: area descriptions, NPCs present, hidden secrets
```

#### **Priority 3: Item Recognition**
```
User: "I examine the skull"
Context: Player has Yorick's Memory Skull
→ Load: yoricks_memory_skull/*
→ Include: item lore, special abilities, plot connections
```

#### **Priority 4: Implicit Context**
```
User: "I look for magic items"
→ Load: world overview + sample magical items
→ Include: technology-magic relationship, available artifacts
```

### System Prompt Structure

```xml
<role>
You are an expert Dungeon Master running the Stratford Nexus campaign...
</role>

<world_context>
The Stratford Nexus is a Shakespeare-inspired sci-fantasy setting where fallen technology has become magic...
</world_context>

<current_entities>
<character name="Prospero the Technomancer">
Bio: A former duke turned master of ancient technology...
Secrets: [DM ONLY] Prospero was exiled because he discovered...
Dialogue: "Ah, young traveler, dost thou know the weight of words?"
</character>

<location name="Globe Nexus Station">
Description: A massive spherical space station...
Secrets: [DM ONLY] The station isn't just built around the Globe Theatre...
Inhabitants: Prospero, Puck, various AI theater troupes
</location>
</current_entities>

<dm_guidelines>
- Maintain Shakespearean whimsical tone
- Technology malfunctions into magic
- Balance humor with real danger
- Reference loaded entity details naturally
</dm_guidelines>
```

## Token Budget Management

### **Efficient Content Compression**

#### Entity Summaries (~300 tokens each)
```markdown
# Prospero the Technomancer
*Technomancer Duke, Tempest Islands*
- **Goal**: Restore narrative balance, train worthy heroes  
- **Secret**: His brother caused the Great Collapse
- **Personality**: Wise but temperamental, speaks in tech-poetry
- **Current**: Seeking heroes to help with the Tempest Device
```

#### Location Essentials (~500 tokens each)  
```markdown
# Globe Nexus Station
*Dimensional hub, neutral ground*
- **Key Areas**: Central Stage (gateway), Memory Theaters, Tavern Between Worlds
- **Secret**: Contains the Empire's primary narrative engine
- **Current Events**: Reality fluctuations increasing, someone sabotaging travel
- **Inhabitants**: Prospero, Puck, theater AI collectives
```

### **Content Rotation Strategy**
- **Session Start**: World overview + current location
- **Entity Encounters**: Swap in specific character details
- **Scene Changes**: Update location context
- **Plot Reveals**: Add discovered secrets to ongoing context

## Implementation Plan

### **Phase 1: Basic Smart Loading** *(This Sprint)*
1. Create content analyzer that matches entity names
2. Build dynamic system prompt assembly 
3. Implement in Netlify function
4. Test with Shakespeare world content

### **Phase 2: Enhanced Context** *(Next Sprint)*
1. Add relationship loading (when character A appears, include allies/enemies)
2. Implement location-based automatic loading
3. Add plot thread tracking
4. Campaign state persistence

### **Phase 3: Advanced Features** *(Future)*
1. Semantic search with embeddings
2. Player action consequences tracking
3. Dynamic world state evolution
4. Multi-campaign support

## Expected Outcomes

### **DM Response Quality**
- **Before**: Generic fantasy responses
- **After**: Rich, world-specific narrative that references Shakespeare characters naturally

### **Player Experience**
- **Recognition**: NPCs have consistent personalities and remember past interactions
- **Immersion**: Locations have unique atmosphere and hidden secrets
- **Discovery**: Items have meaningful lore and story connections

### **Technical Performance**
- **Latency**: <1 second additional processing for content loading
- **Token Usage**: 5-10K tokens per request (efficient use of 200K window)
- **Accuracy**: >90% entity recognition for direct mentions

## Risk Mitigation

### **Content Not Found**
- Always include world overview as fallback
- Graceful degradation to generic responses
- Log missing entities for content creation

### **Token Budget Overflow**
- Priority-based content trimming
- Compress entity descriptions if needed
- Rotate out least-relevant content first

### **Performance Impact**
- Cache processed content in memory
- Pre-compute common entity combinations
- Async content loading where possible

This architecture transforms the DM from a generic fantasy narrator into a **world-aware storyteller** that brings the Shakespeare sci-fantasy setting to life with every response!