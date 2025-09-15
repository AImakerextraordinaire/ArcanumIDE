#!/usr/bin/env python3
"""
Kokoro TTS Server for ArcanumIDE
Provides high-quality text-to-speech with magical character voices
"""

import asyncio
import json
import logging
import os
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional, Any

import torch
import torchaudio
import numpy as np
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pyttsx3
import threading
import queue
import io
import wave

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

class KokoroVoiceEngine:
    """Advanced TTS engine with character-specific voice synthesis"""
    
    def __init__(self):
        self.voice_configs = {
            'elvish_female': {
                'name': 'Arwen',
                'base_voice': 'female',
                'pitch_shift': 0.3,
                'speed_factor': 0.9,
                'emotion': 'gentle',
                'accent': 'british',
                'characteristics': {
                    'breathiness': 0.2,
                    'warmth': 0.8,
                    'clarity': 0.9
                }
            },
            'elvish_male': {
                'name': 'Legolas', 
                'base_voice': 'male',
                'pitch_shift': 0.1,
                'speed_factor': 0.85,
                'emotion': 'wise',
                'accent': 'british',
                'characteristics': {
                    'breathiness': 0.1,
                    'warmth': 0.7,
                    'clarity': 0.95
                }
            },
            'draconic_male': {
                'name': 'Smaug',
                'base_voice': 'male',
                'pitch_shift': -0.1,
                'speed_factor': 0.8,
                'emotion': 'powerful',
                'accent': 'deep',
                'characteristics': {
                    'breathiness': 0.0,
                    'warmth': 0.3,
                    'clarity': 0.8,
                    'reverb': 0.3
                }
            },
            'draconic_female': {
                'name': 'Tiamat',
                'base_voice': 'female',
                'pitch_shift': -0.05,
                'speed_factor': 0.75,
                'emotion': 'commanding',
                'accent': 'authoritative',
                'characteristics': {
                    'breathiness': 0.0,
                    'warmth': 0.4,
                    'clarity': 0.9,
                    'reverb': 0.2
                }
            },
            'orcish_male': {
                'name': 'Uruk',
                'base_voice': 'male',
                'pitch_shift': -0.4,
                'speed_factor': 1.1,
                'emotion': 'aggressive',
                'accent': 'rough',
                'characteristics': {
                    'breathiness': 0.0,
                    'warmth': 0.2,
                    'clarity': 0.7,
                    'gruffness': 0.8
                }
            },
            'orcish_female': {
                'name': 'Ghashak',
                'base_voice': 'female',
                'pitch_shift': -0.2,
                'speed_factor': 1.0,
                'emotion': 'fierce',
                'accent': 'commanding',
                'characteristics': {
                    'breathiness': 0.0,
                    'warmth': 0.3,
                    'clarity': 0.8,
                    'gruffness': 0.6
                }
            },
            'kiro_assistant': {
                'name': 'Kiro',
                'base_voice': 'female',
                'pitch_shift': 0.1,
                'speed_factor': 1.0,
                'emotion': 'friendly',
                'accent': 'neutral',
                'characteristics': {
                    'breathiness': 0.1,
                    'warmth': 0.9,
                    'clarity': 0.95,
                    'enthusiasm': 0.7
                }
            }
        }
        
        self.tts_engine = None
        self.audio_queue = queue.Queue()
        self.is_initialized = False
        self.temp_dir = Path(tempfile.gettempdir()) / "kokoro_tts"
        self.temp_dir.mkdir(exist_ok=True)
        
        # Initialize TTS engine
        self._initialize_engine()
    
    def _initialize_engine(self):
        """Initialize the TTS engine with optimal settings"""
        try:
            self.tts_engine = pyttsx3.init()
            
            # Get available voices
            voices = self.tts_engine.getProperty('voices')
            logger.info(f"Available voices: {len(voices) if voices else 0}")
            
            # Set default properties
            self.tts_engine.setProperty('rate', 200)
            self.tts_engine.setProperty('volume', 0.8)
            
            self.is_initialized = True
            logger.info("✨ Kokoro TTS Engine initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize TTS engine: {e}")
            self.is_initialized = False
    
    def get_voice_config(self, voice_id: str) -> Dict[str, Any]:
        """Get configuration for a specific voice"""
        return self.voice_configs.get(voice_id, self.voice_configs['kiro_assistant'])
    
    def apply_voice_characteristics(self, voice_config: Dict[str, Any]) -> None:
        """Apply voice characteristics to the TTS engine"""
        if not self.tts_engine:
            return
            
        try:
            # Adjust rate based on speed factor
            base_rate = 200
            adjusted_rate = int(base_rate * voice_config['speed_factor'])
            self.tts_engine.setProperty('rate', adjusted_rate)
            
            # Try to select appropriate system voice
            voices = self.tts_engine.getProperty('voices')
            if voices:
                target_voice = None
                
                # Voice selection logic
                if voice_config['base_voice'] == 'female':
                    target_voice = next((v for v in voices if 'female' in v.name.lower() or 'zira' in v.name.lower() or 'hazel' in v.name.lower()), None)
                else:
                    target_voice = next((v for v in voices if 'male' in v.name.lower() or 'david' in v.name.lower() or 'mark' in v.name.lower()), None)
                
                if target_voice:
                    self.tts_engine.setProperty('voice', target_voice.id)
                    logger.info(f"🎭 Selected voice: {target_voice.name} for {voice_config['name']}")
                    
        except Exception as e:
            logger.warning(f"Could not apply voice characteristics: {e}")
    
    def preprocess_text(self, text: str, voice_config: Dict[str, Any]) -> str:
        """Preprocess text based on character and language"""
        processed_text = text
        
        # Add character-specific speech patterns
        character_name = voice_config['name']
        
        if character_name == 'Smaug':
            # Add dramatic pauses and emphasis for dragon speech
            processed_text = processed_text.replace('.', '... ')
            processed_text = processed_text.replace('!', '! ')
            
        elif character_name in ['Arwen', 'Legolas']:
            # Add elvish elegance with slight pauses
            processed_text = processed_text.replace(',', ', ')
            
        elif character_name in ['Uruk', 'Ghashak']:
            # Make orcish speech more direct and forceful
            processed_text = processed_text.replace('?', '?!')
            
        elif character_name == 'Kiro':
            # Add friendly, enthusiastic tone
            processed_text = processed_text.replace('!', '! ')
            
        return processed_text
    
    async def synthesize_speech(self, text: str, voice_id: str, **kwargs) -> bytes:
        """Synthesize speech with the specified voice"""
        if not self.is_initialized:
            raise Exception("TTS engine not initialized")
        
        voice_config = self.get_voice_config(voice_id)
        processed_text = self.preprocess_text(text, voice_config)
        
        # Apply voice characteristics
        self.apply_voice_characteristics(voice_config)
        
        # Generate unique filename
        timestamp = int(time.time() * 1000)
        audio_file = self.temp_dir / f"kokoro_{voice_id}_{timestamp}.wav"
        
        try:
            # Synthesize to file
            self.tts_engine.save_to_file(processed_text, str(audio_file))
            self.tts_engine.runAndWait()
            
            # Wait for file to be created
            max_wait = 10  # seconds
            wait_time = 0
            while not audio_file.exists() and wait_time < max_wait:
                await asyncio.sleep(0.1)
                wait_time += 0.1
            
            if not audio_file.exists():
                raise Exception("Audio file was not created")
            
            # Read the audio file
            with open(audio_file, 'rb') as f:
                audio_data = f.read()
            
            # Clean up
            try:
                audio_file.unlink()
            except:
                pass
            
            logger.info(f"🎵 Generated {len(audio_data)} bytes of audio for {voice_config['name']}")
            return audio_data
            
        except Exception as e:
            logger.error(f"Speech synthesis failed: {e}")
            # Clean up on error
            try:
                if audio_file.exists():
                    audio_file.unlink()
            except:
                pass
            raise

# Global voice engine instance
voice_engine = KokoroVoiceEngine()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Kokoro TTS Server',
        'version': '1.0.0',
        'initialized': voice_engine.is_initialized,
        'available_voices': list(voice_engine.voice_configs.keys())
    })

@app.route('/voices', methods=['GET'])
def get_voices():
    """Get available voice configurations"""
    voices = []
    for voice_id, config in voice_engine.voice_configs.items():
        voices.append({
            'id': voice_id,
            'name': config['name'],
            'language': config.get('accent', 'neutral'),
            'gender': config['base_voice'],
            'characteristics': config['characteristics']
        })
    
    return jsonify({'voices': voices})

@app.route('/synthesize', methods=['POST'])
async def synthesize():
    """Main TTS synthesis endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        text = data.get('text', '')
        voice_id = data.get('voice', 'kiro_assistant')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        logger.info(f"🎭 Synthesizing: '{text[:50]}...' with voice: {voice_id}")
        
        # Generate speech
        audio_data = await voice_engine.synthesize_speech(text, voice_id, **data)
        
        # Create temporary file for response
        temp_file = voice_engine.temp_dir / f"response_{int(time.time() * 1000)}.wav"
        with open(temp_file, 'wb') as f:
            f.write(audio_data)
        
        # Return audio file
        return send_file(
            str(temp_file),
            mimetype='audio/wav',
            as_attachment=False,
            download_name=f'{voice_id}_speech.wav'
        )
        
    except Exception as e:
        logger.error(f"Synthesis error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/test/<voice_id>', methods=['GET'])
async def test_voice(voice_id):
    """Test a specific voice"""
    try:
        test_text = f"Greetings! This is {voice_engine.get_voice_config(voice_id)['name']} speaking. How do I sound?"
        
        audio_data = await voice_engine.synthesize_speech(test_text, voice_id)
        
        # Create temporary file for response
        temp_file = voice_engine.temp_dir / f"test_{voice_id}_{int(time.time() * 1000)}.wav"
        with open(temp_file, 'wb') as f:
            f.write(audio_data)
        
        return send_file(
            str(temp_file),
            mimetype='audio/wav',
            as_attachment=False,
            download_name=f'test_{voice_id}.wav'
        )
        
    except Exception as e:
        logger.error(f"Voice test error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🎭 Starting Kokoro TTS Server...")
    print("🎵 Magical voices loading...")
    
    # Clean up old temp files on startup
    try:
        for old_file in voice_engine.temp_dir.glob("*.wav"):
            old_file.unlink()
    except:
        pass
    
    print("✨ Kokoro TTS Server ready!")
    print("🌟 Available at: http://localhost:5002")
    print("🎪 Available voices:")
    for voice_id, config in voice_engine.voice_configs.items():
        print(f"   🎭 {voice_id}: {config['name']} ({config['base_voice']})")
    
    app.run(host='0.0.0.0', port=5002, debug=False)