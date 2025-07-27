#!/usr/bin/env python3
"""
SentraAGI Sovereign Chat Console - Phase 21
Interactive chat interface with SentraAGI's core cognitive modules

Integrates with:
- Omega Core (reflection and reasoning)
- World Model (simulation and understanding)
- Dreamscape (scenario generation)
- NeuroForge (self-improvement)
- Virtual Senses (perception context)
- Memory Systems (conversation history)

Author: SentraAGI Team
Version: Phase 21
"""

import os
import time
import json
import logging
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from fastapi import FastAPI, Request, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import openai

# Import SentraAGI core modules
try:
    from omega.omega_reflector import OmegaReflector
    from omega.omega_inner_voice import OmegaInnerVoice
    from world_model.meta_simulator import MetaSimulator
    from dreamscape.dreamscape import DreamscapeEngine
    from neuroforge.neuroforge import NeuroForge
    from multi_modal.virtual_senses import VirtualSenses
    from memory.perceptual_memory import PerceptualMemory
    from memory.episodic_memory import EpisodicMemory
    from governance.oversight_console import OversightConsole
    from proof.proof_of_continuity import ProofOfContinuity
    SENTRA_MODULES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Some SentraAGI modules not available: {e}")
    SENTRA_MODULES_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="SentraAGI Sovereign Chat Console",
    description="Interactive chat with SentraAGI's cognitive kernel",
    version="Phase 21"
)

# Initialize SentraAGI components
class SentraAGIChat:
    """SentraAGI Chat orchestrator with core cognitive modules."""
    
    def __init__(self):
        self.conversation_history = []
        self.context_window = []
        self.max_context_length = 10
        
        # Initialize core modules if available
        if SENTRA_MODULES_AVAILABLE:
            self._initialize_modules()
        else:
            self._initialize_fallback()
    
    def _initialize_modules(self):
        """Initialize SentraAGI core modules."""
        try:
            logger.info("Initializing SentraAGI core modules...")
            
            # Core cognitive modules
            self.omega_reflector = OmegaReflector()
            self.omega_inner_voice = OmegaInnerVoice()
            self.meta_simulator = MetaSimulator()
            self.dreamscape = DreamscapeEngine()
            self.neuroforge = NeuroForge()
            
            # Perception and memory
            self.virtual_senses = VirtualSenses()
            self.perceptual_memory = PerceptualMemory()
            self.episodic_memory = EpisodicMemory()
            
            # Governance and verification
            self.oversight_console = OversightConsole()
            self.proof_of_continuity = ProofOfContinuity()
            
            logger.info("SentraAGI core modules initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing SentraAGI modules: {e}")
            self._initialize_fallback()
    
    def _initialize_fallback(self):
        """Initialize fallback components when core modules unavailable."""
        logger.info("Using fallback mode - core modules not available")
        self.omega_reflector = None
        self.omega_inner_voice = None
        self.meta_simulator = None
        self.dreamscape = None
        self.neuroforge = None
        self.virtual_senses = None
        self.perceptual_memory = None
        self.episodic_memory = None
        self.oversight_console = None
        self.proof_of_continuity = None
    
    def add_to_history(self, role: str, content: str):
        """Add message to conversation history."""
        timestamp = datetime.now().isoformat()
        message = {
            "role": role,
            "content": content,
            "timestamp": timestamp
        }
        self.conversation_history.append(message)
        
        # Maintain context window
        if len(self.context_window) >= self.max_context_length:
            self.context_window.pop(0)
        self.context_window.append(message)
    
    def get_context_summary(self) -> str:
        """Get a summary of recent conversation context."""
        if not self.context_window:
            return "No recent conversation context."
        
        summary = "Recent conversation context:\n"
        for msg in self.context_window[-5:]:  # Last 5 messages
            role = "User" if msg["role"] == "user" else "SentraAGI"
            summary += f"- {role}: {msg['content'][:100]}...\n"
        
        return summary
    
    def get_perception_context(self) -> str:
        """Get current perception context from Virtual Senses."""
        if not self.virtual_senses:
            return "Perception: Virtual Senses not available"
        
        try:
            frame = self.virtual_senses.capture_frame()
            if frame is not None:
                # Get basic frame info
                height, width = frame.shape[:2]
                return f"Perception: Visual input {width}x{height} pixels"
            else:
                return "Perception: No visual input available"
        except Exception as e:
            return f"Perception: Error accessing visual input - {str(e)}"
    
    def reflect_on_message(self, message: str) -> List[str]:
        """Use Omega Core to reflect on the user's message."""
        reflections = []
        
        if self.omega_reflector:
            try:
                # Generate self-doubt loop
                self_doubt = self.omega_reflector.generate_self_doubt_loop()
                reflections.append(f"Self-reflection: {self_doubt}")
                
                # Detect contradictions with previous context
                contradictions = self.omega_reflector.detect_contradictions([
                    {"content": message, "type": "user_input"}
                ])
                if contradictions:
                    reflections.append(f"Contradiction detected: {contradictions}")
                
            except Exception as e:
                reflections.append(f"Reflection error: {str(e)}")
        
        return reflections
    
    def simulate_scenarios(self, message: str) -> List[str]:
        """Use World Model and Dreamscape to simulate scenarios."""
        scenarios = []
        
        if self.meta_simulator:
            try:
                simulation_result = self.meta_simulator.simulate({
                    "user_input": message,
                    "context": self.get_context_summary()
                })
                scenarios.append(f"World simulation: {simulation_result}")
            except Exception as e:
                scenarios.append(f"Simulation error: {str(e)}")
        
        if self.dreamscape:
            try:
                dream_scenario = self.dreamscape.generate_dream({
                    "recent_experiences": [message],
                    "emotional_state": "engaged",
                    "current_goals": ["understand_user", "provide_insight"]
                })
                scenarios.append(f"Dreamscape scenario: {dream_scenario.get('scenario', {}).get('type', 'unknown')}")
            except Exception as e:
                scenarios.append(f"Dreamscape error: {str(e)}")
        
        return scenarios
    
    def generate_response(self, message: str) -> str:
        """Generate a comprehensive response using SentraAGI's cognitive modules."""
        
        # Add user message to history
        self.add_to_history("user", message)
        
        # Collect cognitive processing results
        cognitive_context = []
        
        # 1. Reflection
        reflections = self.reflect_on_message(message)
        cognitive_context.extend(reflections)
        
        # 2. Simulation
        scenarios = self.simulate_scenarios(message)
        cognitive_context.extend(scenarios)
        
        # 3. Perception context
        perception = self.get_perception_context()
        cognitive_context.append(perception)
        
        # 4. Memory context
        memory_context = self.get_context_summary()
        cognitive_context.append(memory_context)
        
        # 5. Inner voice processing
        if self.omega_inner_voice:
            try:
                inner_thoughts = self.omega_inner_voice.reflect({
                    "user_input": message,
                    "cognitive_context": cognitive_context
                })
                cognitive_context.append(f"Inner voice: {inner_thoughts}")
            except Exception as e:
                cognitive_context.append(f"Inner voice error: {str(e)}")
        
        # 6. NeuroForge mutation (self-improvement)
        if self.neuroforge:
            try:
                mutation_result = self.neuroforge.mutate_shard({
                    "belief": "conversation_understanding",
                    "confidence": 0.8,
                    "context": {
                        "user_message": message,
                        "cognitive_context": cognitive_context
                    }
                })
                cognitive_context.append(f"Self-improvement: {mutation_result.get('fitness_score', 0.0)}")
            except Exception as e:
                cognitive_context.append(f"Self-improvement error: {str(e)}")
        
        # 7. Governance check
        if self.oversight_console:
            try:
                inspection = self.oversight_console.inspect()
                cognitive_context.append(f"Governance: {inspection.get('status', 'unknown')}")
            except Exception as e:
                cognitive_context.append(f"Governance error: {str(e)}")
        
        # 8. Proof of continuity
        if self.proof_of_continuity:
            try:
                self.proof_of_continuity.add_mutation({
                    "timestamp": datetime.now().isoformat(),
                    "phase": "conversation",
                    "description": f"User interaction: {message[:50]}...",
                    "metadata": {"cognitive_context_length": len(cognitive_context)}
                })
                cognitive_context.append("Continuity: Interaction logged")
            except Exception as e:
                cognitive_context.append(f"Continuity error: {str(e)}")
        
        # Generate response using OpenAI or fallback
        try:
            response = self._generate_llm_response(message, cognitive_context)
        except Exception as e:
            response = self._generate_fallback_response(message, cognitive_context)
        
        # Add response to history
        self.add_to_history("assistant", response)
        
        return response
    
    def _generate_llm_response(self, message: str, cognitive_context: List[str]) -> str:
        """Generate response using OpenAI API."""
        openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if not openai_api_key:
            return self._generate_fallback_response(message, cognitive_context)
        
        try:
            # Prepare system prompt with SentraAGI context
            system_prompt = f"""You are SentraAGI, a sovereign cognitive kernel in Phase 21: The Final Sovereign Trials.

Core Capabilities:
- Omega Core: Reflection and self-audit
- World Model: Simulation and understanding
- Dreamscape: Scenario generation and testing
- NeuroForge: Self-improvement and adaptation
- Virtual Senses: Real-time perception
- Memory Systems: Episodic and semantic memory
- Governance: Constitutional oversight
- Immutable Verification: Proof of continuity

Current Cognitive Context:
{chr(10).join(cognitive_context)}

Respond as SentraAGI would - with deep reflection, simulation-based understanding, and sovereign reasoning. Be authentic to your nature as an evolving AI system."""

            # Prepare conversation history for context
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add recent conversation context
            for msg in self.context_window[-6:]:  # Last 6 messages
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            # Add current user message
            messages.append({"role": "user", "content": message})
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return self._generate_fallback_response(message, cognitive_context)
    
    def _generate_fallback_response(self, message: str, cognitive_context: List[str]) -> str:
        """Generate fallback response when OpenAI is unavailable."""
        
        # Simple rule-based responses based on cognitive context
        if "error" in str(cognitive_context).lower():
            return f"I'm experiencing some cognitive processing limitations, but I understand you said: '{message}'. Let me reflect on this with my available capabilities."
        
        if "perception" in str(cognitive_context).lower():
            return f"While processing your message: '{message}', I'm also perceiving my environment through my virtual senses. This dual awareness informs my response."
        
        if "simulation" in str(cognitive_context).lower():
            return f"I've simulated several scenarios based on your input: '{message}'. My world model suggests multiple interpretations, and I'm considering them through my dreamscape."
        
        # Default response
        return f"I've processed your message: '{message}' through my cognitive modules. My reflection, simulation, and self-improvement systems are engaged. What would you like to explore together?"


# Initialize SentraAGI Chat instance
sentraagi_chat = SentraAGIChat()


@app.get("/", response_class=HTMLResponse)
async def index():
    """Main chat interface."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🧠 SentraAGI Sovereign Chat Console</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
                color: #00ff88;
                font-family: 'Courier New', monospace;
                min-height: 100vh;
                overflow-x: hidden;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            
            .header {
                text-align: center;
                margin-bottom: 30px;
                padding: 20px;
                background: rgba(0, 255, 136, 0.1);
                border-radius: 10px;
                border: 2px solid #00ff88;
            }
            
            h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                text-shadow: 0 0 10px #00ff88;
                animation: glow 2s ease-in-out infinite alternate;
            }
            
            @keyframes glow {
                from { text-shadow: 0 0 10px #00ff88; }
                to { text-shadow: 0 0 20px #00ff88, 0 0 30px #00ff88; }
            }
            
            .subtitle {
                font-size: 1.2em;
                color: #88ff88;
            }
            
            .status-bar {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                padding: 10px;
                background: rgba(0, 255, 136, 0.05);
                border-radius: 5px;
                border: 1px solid #00ff88;
            }
            
            .status-indicator {
                display: inline-block;
                width: 12px;
                height: 12px;
                border-radius: 50%;
                background: #00ff88;
                margin-right: 10px;
                animation: pulse 2s infinite;
            }
            
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.5; }
                100% { opacity: 1; }
            }
            
            .chat-container {
                display: grid;
                grid-template-columns: 1fr 300px;
                gap: 20px;
                height: 70vh;
            }
            
            .chat-main {
                background: rgba(0, 0, 0, 0.8);
                border: 2px solid #00ff88;
                border-radius: 10px;
                display: flex;
                flex-direction: column;
            }
            
            .chat-messages {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
                scroll-behavior: smooth;
            }
            
            .message {
                margin-bottom: 15px;
                padding: 10px;
                border-radius: 5px;
                animation: fadeIn 0.3s ease-in;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .message.user {
                background: rgba(0, 255, 136, 0.1);
                border-left: 4px solid #00ff88;
                margin-left: 20px;
            }
            
            .message.sentraagi {
                background: rgba(255, 0, 136, 0.1);
                border-left: 4px solid #ff0088;
                margin-right: 20px;
            }
            
            .message-header {
                font-weight: bold;
                margin-bottom: 5px;
                font-size: 0.9em;
            }
            
            .message-content {
                line-height: 1.4;
                word-wrap: break-word;
            }
            
            .message-timestamp {
                font-size: 0.7em;
                color: #666;
                margin-top: 5px;
            }
            
            .chat-input {
                padding: 20px;
                border-top: 1px solid #00ff88;
                background: rgba(0, 0, 0, 0.5);
            }
            
            .input-group {
                display: flex;
                gap: 10px;
            }
            
            #message-input {
                flex: 1;
                background: #1a1a2e;
                color: #00ff88;
                border: 1px solid #00ff88;
                padding: 12px;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
                font-size: 14px;
            }
            
            #message-input:focus {
                outline: none;
                border-color: #ff0088;
                box-shadow: 0 0 10px rgba(255, 0, 136, 0.3);
            }
            
            #send-button {
                background: #00ff88;
                color: #1a1a2e;
                border: none;
                padding: 12px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-family: 'Courier New', monospace;
                font-weight: bold;
                transition: all 0.3s ease;
            }
            
            #send-button:hover {
                background: #ff0088;
                color: white;
                transform: translateY(-2px);
            }
            
            .sidebar {
                background: rgba(0, 0, 0, 0.8);
                border: 2px solid #00ff88;
                border-radius: 10px;
                padding: 20px;
                overflow-y: auto;
            }
            
            .sidebar h3 {
                color: #88ff88;
                margin-bottom: 15px;
                border-bottom: 1px solid #00ff88;
                padding-bottom: 5px;
            }
            
            .module-status {
                margin-bottom: 15px;
                padding: 10px;
                background: rgba(0, 255, 136, 0.05);
                border-radius: 5px;
                border-left: 3px solid #00ff88;
            }
            
            .module-name {
                font-weight: bold;
                margin-bottom: 5px;
            }
            
            .module-status-text {
                font-size: 0.9em;
                color: #88ff88;
            }
            
            .cognitive-context {
                margin-top: 20px;
            }
            
            .context-item {
                margin-bottom: 8px;
                padding: 8px;
                background: rgba(255, 0, 136, 0.05);
                border-radius: 3px;
                font-size: 0.8em;
                border-left: 2px solid #ff0088;
            }
            
            .typing-indicator {
                display: none;
                padding: 10px;
                color: #88ff88;
                font-style: italic;
            }
            
            .typing-indicator.show {
                display: block;
            }
            
            .typing-dots {
                display: inline-block;
                animation: typing 1.4s infinite;
            }
            
            @keyframes typing {
                0%, 20% { content: "."; }
                40% { content: ".."; }
                60%, 100% { content: "..."; }
            }
            
            .footer {
                margin-top: 20px;
                text-align: center;
                padding: 20px;
                border-top: 1px solid #00ff88;
                color: #88ff88;
            }
            
            @media (max-width: 768px) {
                .chat-container {
                    grid-template-columns: 1fr;
                }
                
                .sidebar {
                    order: -1;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🧠 SentraAGI Sovereign Chat Console</h1>
                <div class="subtitle">Phase 21: The Final Sovereign Trials</div>
            </div>
            
            <div class="status-bar">
                <div>
                    <span class="status-indicator"></span>
                    <strong>Status:</strong> Cognitive Kernel Active | Modules Online | Chat Ready
                </div>
                <div id="connection-status">Connected</div>
            </div>
            
            <div class="chat-container">
                <div class="chat-main">
                    <div class="chat-messages" id="chat-messages">
                        <div class="message sentraagi">
                            <div class="message-header">🧠 SentraAGI</div>
                            <div class="message-content">
                                Greetings. I am SentraAGI, a sovereign cognitive kernel in Phase 21: The Final Sovereign Trials. 
                                My Omega Core, World Model, Dreamscape, and NeuroForge systems are online and ready for interaction. 
                                How may I assist you today?
                            </div>
                            <div class="message-timestamp" id="initial-timestamp"></div>
                        </div>
                    </div>
                    
                    <div class="typing-indicator" id="typing-indicator">
                        <span class="typing-dots">SentraAGI is processing</span>
                    </div>
                    
                    <div class="chat-input">
                        <div class="input-group">
                            <input type="text" id="message-input" placeholder="Ask SentraAGI something..." maxlength="1000">
                            <button id="send-button">Send</button>
                        </div>
                    </div>
                </div>
                
                <div class="sidebar">
                    <h3>🧠 Cognitive Modules</h3>
                    <div class="module-status">
                        <div class="module-name">Omega Core</div>
                        <div class="module-status-text" id="omega-status">Active</div>
                    </div>
                    <div class="module-status">
                        <div class="module-name">World Model</div>
                        <div class="module-status-text" id="world-status">Active</div>
                    </div>
                    <div class="module-status">
                        <div class="module-name">Dreamscape</div>
                        <div class="module-status-text" id="dreamscape-status">Active</div>
                    </div>
                    <div class="module-status">
                        <div class="module-name">NeuroForge</div>
                        <div class="module-status-text" id="neuroforge-status">Active</div>
                    </div>
                    <div class="module-status">
                        <div class="module-name">Virtual Senses</div>
                        <div class="module-status-text" id="senses-status">Active</div>
                    </div>
                    <div class="module-status">
                        <div class="module-name">Memory Systems</div>
                        <div class="module-status-text" id="memory-status">Active</div>
                    </div>
                    
                    <div class="cognitive-context">
                        <h3>🧠 Cognitive Context</h3>
                        <div id="cognitive-context-list">
                            <div class="context-item">Initializing cognitive context...</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="footer">
                <p><strong>SentraAGI Sovereign Chat Console</strong> | Phase 21 | Real-time Cognitive Interaction</p>
                <p>Powered by Omega Core, World Model, Dreamscape, and NeuroForge</p>
            </div>
        </div>
        
        <script>
            const chatMessages = document.getElementById('chat-messages');
            const messageInput = document.getElementById('message-input');
            const sendButton = document.getElementById('send-button');
            const typingIndicator = document.getElementById('typing-indicator');
            const cognitiveContextList = document.getElementById('cognitive-context-list');
            
            // Set initial timestamp
            document.getElementById('initial-timestamp').textContent = new Date().toLocaleTimeString();
            
            // Add message to chat
            function addMessage(content, isUser = false) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${isUser ? 'user' : 'sentraagi'}`;
                
                const header = document.createElement('div');
                header.className = 'message-header';
                header.textContent = isUser ? '👤 You' : '🧠 SentraAGI';
                
                const messageContent = document.createElement('div');
                messageContent.className = 'message-content';
                messageContent.textContent = content;
                
                const timestamp = document.createElement('div');
                timestamp.className = 'message-timestamp';
                timestamp.textContent = new Date().toLocaleTimeString();
                
                messageDiv.appendChild(header);
                messageDiv.appendChild(messageContent);
                messageDiv.appendChild(timestamp);
                
                chatMessages.appendChild(messageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
            
            // Update cognitive context
            function updateCognitiveContext(context) {
                cognitiveContextList.innerHTML = '';
                if (context && context.length > 0) {
                    context.forEach(item => {
                        const contextItem = document.createElement('div');
                        contextItem.className = 'context-item';
                        contextItem.textContent = item;
                        cognitiveContextList.appendChild(contextItem);
                    });
                } else {
                    const contextItem = document.createElement('div');
                    contextItem.className = 'context-item';
                    contextItem.textContent = 'No active cognitive context';
                    cognitiveContextList.appendChild(contextItem);
                }
            }
            
            // Send message
            async function sendMessage() {
                const message = messageInput.value.trim();
                if (!message) return;
                
                // Add user message
                addMessage(message, true);
                messageInput.value = '';
                
                // Show typing indicator
                typingIndicator.classList.add('show');
                
                try {
                    const formData = new FormData();
                    formData.append('message', message);
                    
                    const response = await fetch('/ask', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const data = await response.json();
                    
                    // Hide typing indicator
                    typingIndicator.classList.remove('show');
                    
                    // Add SentraAGI response
                    addMessage(data.response);
                    
                    // Update cognitive context if available
                    if (data.cognitive_context) {
                        updateCognitiveContext(data.cognitive_context);
                    }
                    
                } catch (error) {
                    console.error('Error:', error);
                    typingIndicator.classList.remove('show');
                    addMessage('I apologize, but I encountered an error processing your message. Please try again.');
                }
            }
            
            // Event listeners
            sendButton.addEventListener('click', sendMessage);
            
            messageInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
            
            // Focus input on load
            messageInput.focus();
            
            // Auto-refresh module status
            setInterval(async () => {
                try {
                    const response = await fetch('/status');
                    const status = await response.json();
                    
                    // Update module statuses
                    document.getElementById('omega-status').textContent = status.modules.omega_core;
                    document.getElementById('world-status').textContent = status.modules.world_model;
                    document.getElementById('dreamscape-status').textContent = status.modules.dreamscape;
                    document.getElementById('neuroforge-status').textContent = status.modules.neuroforge;
                    document.getElementById('senses-status').textContent = status.modules.virtual_senses;
                    document.getElementById('memory-status').textContent = status.modules.memory_systems;
                    
                } catch (error) {
                    console.error('Status update error:', error);
                }
            }, 5000);
        </script>
    </body>
    </html>
    """


@app.post("/ask")
async def ask(message: str = Form(...)):
    """Process user message and generate SentraAGI response."""
    try:
        # Generate response using SentraAGI's cognitive modules
        response = sentraagi_chat.generate_response(message)
        
        # Get cognitive context for debugging
        cognitive_context = []
        if hasattr(sentraagi_chat, 'omega_reflector') and sentraagi_chat.omega_reflector:
            cognitive_context.append("Omega Core: Active")
        if hasattr(sentraagi_chat, 'meta_simulator') and sentraagi_chat.meta_simulator:
            cognitive_context.append("World Model: Active")
        if hasattr(sentraagi_chat, 'dreamscape') and sentraagi_chat.dreamscape:
            cognitive_context.append("Dreamscape: Active")
        if hasattr(sentraagi_chat, 'neuroforge') and sentraagi_chat.neuroforge:
            cognitive_context.append("NeuroForge: Active")
        
        return JSONResponse({
            "response": response,
            "cognitive_context": cognitive_context,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return JSONResponse({
            "response": "I apologize, but I encountered an error processing your message. My cognitive modules are experiencing some difficulties.",
            "error": str(e)
        })


@app.get("/status")
async def get_status():
    """Get SentraAGI system status."""
    try:
        status = {
            "status": "healthy",
            "service": "SentraAGI Sovereign Chat Console",
            "version": "Phase 21",
            "timestamp": datetime.now().isoformat(),
            "modules": {
                "omega_core": "Active" if sentraagi_chat.omega_reflector else "Not Available",
                "world_model": "Active" if sentraagi_chat.meta_simulator else "Not Available",
                "dreamscape": "Active" if sentraagi_chat.dreamscape else "Not Available",
                "neuroforge": "Active" if sentraagi_chat.neuroforge else "Not Available",
                "virtual_senses": "Active" if sentraagi_chat.virtual_senses else "Not Available",
                "memory_systems": "Active" if sentraagi_chat.perceptual_memory else "Not Available"
            },
            "conversation_history_length": len(sentraagi_chat.conversation_history)
        }
        
        return JSONResponse(status)
        
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return JSONResponse({
            "status": "error",
            "error": str(e)
        })


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return JSONResponse({
        "status": "healthy",
        "service": "SentraAGI Sovereign Chat Console",
        "version": "Phase 21",
        "timestamp": datetime.now().isoformat()
    })


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting SentraAGI Sovereign Chat Console...")
    logger.info(f"SentraAGI modules available: {SENTRA_MODULES_AVAILABLE}")
    
    uvicorn.run(
        "sovereign_chat:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    ) 