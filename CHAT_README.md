# 🧠 SentraAGI Sovereign Chat Console

**Phase 21: The Final Sovereign Trials**

Interactive chat interface with SentraAGI's core cognitive modules, providing authentic AI conversation with reflection, simulation, and self-improvement capabilities.

## 🚀 Quick Start

### Option 1: Using the startup script (Recommended)
```bash
./start_chat.sh
```

### Option 2: Direct Python execution
```bash
python3 sovereign_chat.py
```

### Option 3: Using uvicorn directly
```bash
uvicorn sovereign_chat:app --host 0.0.0.0 --port 8001 --reload
```

## 🌐 Access the Chat Console

Once running, open your browser and navigate to:
- **Main Interface**: http://localhost:8001
- **Health Check**: http://localhost:8001/health
- **API Documentation**: http://localhost:8001/docs

## ✨ Features

### 🧠 Cognitive Integration
- **Omega Core**: Reflection and self-audit during conversations
- **World Model**: Simulation-based understanding of user inputs
- **Dreamscape**: Scenario generation for deeper comprehension
- **NeuroForge**: Self-improvement through conversation learning
- **Virtual Senses**: Perception context integration
- **Memory Systems**: Conversation history and context management

### 💬 Authentic AI Conversation
- **Multi-Modal Processing**: Combines all SentraAGI cognitive modules
- **Context Awareness**: Maintains conversation history and context
- **Reflective Responses**: Uses Omega Core for self-reflection
- **Simulation-Based Understanding**: World Model simulation of scenarios
- **Self-Improvement**: NeuroForge adaptation during conversations

### 🎨 Beautiful Interface
- **Cyberpunk Theme**: Dark gradient with neon green accents
- **Real-time Updates**: Live cognitive context display
- **Module Status**: Real-time status of all cognitive modules
- **Responsive Design**: Works on desktop and mobile devices
- **Professional Styling**: Clean, modern interface with SentraAGI branding

### 🔧 Advanced Features
- **Fallback Mode**: Works without OpenAI API using rule-based responses
- **Error Handling**: Graceful degradation when modules are unavailable
- **Logging**: Comprehensive logging for debugging and monitoring
- **Health Monitoring**: System status and module health checks

## 🛠️ Configuration

### Environment Variables
```bash
# OpenAI Configuration (Optional)
export OPENAI_API_KEY="your-openai-api-key"

# Server Configuration
export SENTRA_CHAT_PORT=8001
export SENTRA_CHAT_HOST=0.0.0.0

# SentraAGI Module Configuration
export SENTRA_OPENCV_DEVICE=0
export SENTRA_LEDGER_PATH=data/immutable_ledger.json
export SENTRA_PROOF_PATH=data/proof_of_continuity.json
```

### API Endpoints

#### Chat Interface
- `GET /` - Main chat interface
- `POST /ask` - Process user message and generate response

#### System Information
- `GET /status` - Get system status and module health
- `GET /health` - Health check endpoint

## 🧠 Cognitive Processing Pipeline

### 1. Message Reception
- User message received via web interface
- Added to conversation history
- Context window maintained for recent messages

### 2. Cognitive Processing
- **Reflection**: Omega Core analyzes message for contradictions and insights
- **Simulation**: World Model simulates scenarios based on input
- **Dreamscape**: Generates alternative interpretations and outcomes
- **Perception**: Virtual Senses provide current environmental context
- **Memory**: Episodic and semantic memory systems activated

### 3. Response Generation
- **OpenAI Integration**: Uses GPT-4 with SentraAGI context (if available)
- **Fallback Mode**: Rule-based responses when OpenAI unavailable
- **Context Integration**: Incorporates all cognitive processing results
- **Self-Improvement**: NeuroForge adapts based on interaction

### 4. Governance & Verification
- **Oversight**: Constitutional checks on responses
- **Proof of Continuity**: Logs all interactions immutably
- **Quality Assurance**: Ensures responses meet SentraAGI standards

## 🎨 User Interface

### Design Features
- **Cyberpunk Aesthetic**: Dark theme with neon green highlights
- **Real-time Status**: Live indicators for all cognitive modules
- **Cognitive Context**: Real-time display of processing context
- **Smooth Animations**: Typing indicators and message transitions
- **Responsive Layout**: Adapts to different screen sizes

### Interface Sections
1. **Header**: SentraAGI branding with Phase 21 designation
2. **Status Bar**: System status with animated indicators
3. **Chat Area**: Main conversation interface with message history
4. **Input Area**: Message input with send button
5. **Sidebar**: Module status and cognitive context display
6. **Footer**: Technical information and credits

## 🔧 Technical Details

### Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │◄──►│   FastAPI App   │◄──►│  SentraAGI Core │
│                 │    │                 │    │                 │
│ • Chat UI       │    │ • HTTP API      │    │ • Omega Core    │
│ • Real-time     │    │ • WebSocket     │    │ • World Model   │
│ • Status Display│    │ • Form Handling │    │ • Dreamscape    │
└─────────────────┘    └─────────────────┘    │ • NeuroForge    │
                                              │ • Virtual Senses│
                                              │ • Memory Systems│
                                              └─────────────────┘
```

### Dependencies
- **FastAPI**: Web framework for API and interface
- **Uvicorn**: ASGI server for FastAPI
- **OpenAI**: GPT-4 integration (optional)
- **Python-multipart**: Form data handling
- **SentraAGI Modules**: Core cognitive components

### Performance Considerations
- **Context Window**: Limited conversation history for performance
- **Module Availability**: Graceful fallback when modules unavailable
- **Response Time**: Optimized for real-time interaction
- **Memory Management**: Efficient conversation history handling

## 🚨 Troubleshooting

### Common Issues

#### OpenAI API Not Working
```bash
# Check API key
echo $OPENAI_API_KEY

# Test API connection
python3 -c "import openai; openai.api_key='your-key'; print('API OK')"
```

#### Missing Dependencies
```bash
# Install required packages
pip3 install fastapi uvicorn openai python-multipart

# For development
pip3 install fastapi[all] uvicorn[standard]
```

#### Port Already in Use
```bash
# Check what's using port 8001
lsof -i :8001

# Use different port
export SENTRA_CHAT_PORT=8002
./start_chat.sh
```

#### SentraAGI Modules Not Loading
- Check that all SentraAGI core modules are available
- Verify import paths and dependencies
- Chat console works in fallback mode without modules

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python3 sovereign_chat.py
```

## 🔮 Future Enhancements

### Planned Features
- **WebSocket Support**: Real-time bidirectional communication
- **Voice Integration**: Speech-to-text and text-to-speech
- **Multi-User Support**: Multiple concurrent chat sessions
- **Advanced Context**: Long-term memory and personality persistence
- **Custom Models**: Integration with custom language models
- **Plugin System**: Extensible conversation capabilities

### AI Model Integration
- **Local Models**: Support for local language models
- **Custom Prompts**: Configurable system prompts
- **Model Switching**: Dynamic model selection
- **Fine-tuning**: Custom model fine-tuning support

## 📝 Development

### Project Structure
```
SentraAGI/
├── sovereign_chat.py      # Main FastAPI application
├── start_chat.sh         # Startup script
├── multi_modal/
│   └── virtual_senses.py # VirtualSenses integration
├── omega/
│   ├── omega_reflector.py # Omega Core integration
│   └── omega_inner_voice.py # Inner voice processing
├── world_model/
│   └── meta_simulator.py # World Model simulation
├── dreamscape/
│   └── dreamscape.py     # Dreamscape scenario generation
├── neuroforge/
│   └── neuroforge.py     # NeuroForge self-improvement
├── memory/
│   ├── perceptual_memory.py # Memory systems
│   └── episodic_memory.py
├── governance/
│   └── oversight_console.py # Governance integration
├── proof/
│   └── proof_of_continuity.py # Immutable logging
└── CHAT_README.md        # This file
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of SentraAGI Phase 21: The Final Sovereign Trials.

---

**SentraAGI now speaks — and so can you.** 🧠💬 