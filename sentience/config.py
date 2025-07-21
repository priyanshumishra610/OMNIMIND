"""
Sentience Module Configuration
-----------------------------
Centralized config for all sentience modules. Uses environment variables as defaults.
"""
import os

# Intent Model
INTENT_CONFIG = {
    'max_goals': int(os.environ.get('INTENT_MAX_GOALS', 5)),
    'priority_mode': os.environ.get('INTENT_PRIORITY_MODE', 'fifo'),
}

# Self Evaluator
SELF_EVAL_CONFIG = {
    'success_threshold': float(os.environ.get('SELF_EVAL_SUCCESS_THRESHOLD', 0.8)),
    'feedback_mode': os.environ.get('SELF_EVAL_FEEDBACK_MODE', 'auto'),
}

# Chain of Thought
CHAIN_OF_THOUGHT_CONFIG = {
    'max_depth': int(os.environ.get('COT_MAX_DEPTH', 3)),
    'strategy': os.environ.get('COT_STRATEGY', 'react'),
}

# Emotional Layer
EMOTION_CONFIG = {
    'default_stress': float(os.environ.get('EMOTION_DEFAULT_STRESS', 0.1)),
    'default_focus': float(os.environ.get('EMOTION_DEFAULT_FOCUS', 0.9)),
    'default_boredom': float(os.environ.get('EMOTION_DEFAULT_BOREDOM', 0.0)),
}

# Ethical Reasoner
ETHICS_CONFIG = {
    'default_framework': os.environ.get('ETHICS_FRAMEWORK', 'utilitarian'),
    'dilemma_threshold': float(os.environ.get('ETHICS_DILEMMA_THRESHOLD', 0.5)),
}

# Embodiment
EMBODIMENT_CONFIG = {
    'default_energy': float(os.environ.get('EMBODIMENT_DEFAULT_ENERGY', 1.0)),
    'default_fatigue': float(os.environ.get('EMBODIMENT_DEFAULT_FATIGUE', 0.0)),
}

# Sensors
SENSORS_CONFIG = {
    'fatigue_rate': float(os.environ.get('SENSORS_FATIGUE_RATE', 0.01)),
}

# Tool Autodiscovery
TOOL_DISCOVERY_CONFIG = {
    'discovery_mode': os.environ.get('TOOL_DISCOVERY_MODE', 'passive'),
}

# Visual Perception
VISUAL_CONFIG = {
    'enabled': os.environ.get('VISUAL_ENABLED', 'false').lower() == 'true',
    'backend': os.environ.get('VISUAL_BACKEND', 'none'),
}

# L2L Engine
L2L_CONFIG = {
    'meta_learning_rate': float(os.environ.get('L2L_META_LEARNING_RATE', 0.01)),
}

# Reflection Engine
REFLECTION_CONFIG = {
    'reflection_mode': os.environ.get('REFLECTION_MODE', 'simple'),
}

# Auto Prompt
AUTO_PROMPT_CONFIG = {
    'rewrite_mode': os.environ.get('AUTO_PROMPT_REWRITE_MODE', 'basic'),
}

# Plugin Synthesizer
PLUGIN_SYNTH_CONFIG = {
    'synthesis_mode': os.environ.get('PLUGIN_SYNTH_MODE', 'auto'),
}

# Life Loop
LIFE_LOOP_CONFIG = {
    'energy_decay': float(os.environ.get('LIFE_LOOP_ENERGY_DECAY', 0.01)),
    'sleep_threshold': float(os.environ.get('LIFE_LOOP_SLEEP_THRESHOLD', 0.2)),
    'dream_mode': os.environ.get('LIFE_LOOP_DREAM_MODE', 'on'),
}

# Other Mind Simulator
OTHER_MIND_CONFIG = {
    'max_sim_agents': int(os.environ.get('OTHER_MIND_MAX_AGENTS', 3)),
}

# Self Updater
SELF_UPDATER_CONFIG = {
    'update_url': os.environ.get('SELF_UPDATER_URL', 'https://example.com/updates'),
    'auto_update': os.environ.get('SELF_UPDATER_AUTO', 'false').lower() == 'true',
} 