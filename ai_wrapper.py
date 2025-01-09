"""
AI Project Generator - AI Provider Wrapper
Original Project: DDS AI Project Assistant
Enhanced by: Dennis Daniels

Improvements:
- Added Ollama integration for local model support
- Implemented comprehensive logging
- Enhanced error handling and model switching
- Added model detection and management
"""

import logging
import os
import requests
from openai import OpenAI
from typing import Dict, Any, Optional
from pathlib import Path

# Set up logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    filename=log_dir / "app.log",
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filemode='a'
)
logger = logging.getLogger(__name__)

class AIProjectAssistant:
    """Wrapper class for AI model interactions (OpenAI and Ollama) focused on Data Science and AI projects."""
    
    def __init__(self):
        """Initialize the AI assistant."""
        self.openai_client = None
        self.ollama_endpoint = "http://localhost:11434"
        self.current_provider = None
        self.default_temperature = 0.7
        
        # Try to initialize OpenAI from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                self.openai_client = OpenAI(api_key=api_key)
                self.current_provider = "openai"
                self.default_model = "gpt-4"
                logger.info("OpenAI client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
        
        # Check for Ollama availability
        try:
            response = requests.get(f"{self.ollama_endpoint}/api/version")
            if response.status_code == 200:
                self.current_provider = self.current_provider or "ollama"
                self.default_model = "llama3.2:latest"  # Include :latest suffix for Ollama
                logger.info(f"Ollama detected: {response.json().get('version')}")
        except Exception as e:
            logger.error(f"Failed to detect Ollama: {e}")
        
    def get_available_models(self) -> Dict[str, list]:
        """Get available models from both providers."""
        models = {"openai": [], "ollama": []}
        
        # Get OpenAI models
        if self.openai_client:
            models["openai"] = ["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"]
            logger.debug("Retrieved OpenAI models")
        
        # Get Ollama models
        try:
            response = requests.get(f"{self.ollama_endpoint}/api/tags")
            if response.status_code == 200:
                # Strip ":latest" suffix from model names for cleaner display
                models["ollama"] = [model["name"].split(":")[0] for model in response.json().get("models", [])]
                logger.debug(f"Retrieved Ollama models: {models['ollama']}")
        except Exception as e:
            logger.error(f"Failed to get Ollama models: {e}")
        
        return models

    def send_prompt(self, 
                   prompt: str, 
                   provider: Optional[str] = None,
                   model: Optional[str] = None,
                   temperature: Optional[float] = None) -> Dict[str, Any]:
        """
        Send a prompt to the selected AI provider and get the response.
        
        Args:
            prompt (str): The user's input prompt
            provider (str, optional): AI provider to use ('openai' or 'ollama')
            model (str, optional): Model to use
            temperature (float, optional): Response creativity (0-1)
            
        Returns:
            Dict[str, Any]: AI response
        """
        provider = provider or self.current_provider
        temp = temperature or self.default_temperature
        
        # Handle model selection based on provider
        if provider == "openai":
            model = model or "gpt-4"  # Default OpenAI model
        else:  # ollama
            if model and not ":" in model:
                model = f"{model}:latest"  # Add :latest suffix if not present
            else:
                model = self.default_model  # Use default Ollama model
        
        logger.info(f"Sending prompt using {provider} with model {model}")
        
        try:
            if provider == "openai" and self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model=model,  # OpenAI model name
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temp
                )
                logger.debug(f"OpenAI API response received for model {model}")
                result = {
                    "success": True,
                    "content": response.choices[0].message.content,
                    "tokens_used": response.usage.total_tokens
                }
            elif provider == "ollama":
                logger.debug(f"Sending request to Ollama with model {model}")
                response = requests.post(
                    f"{self.ollama_endpoint}/api/generate",
                    json={
                        "model": model,  # Ollama model name with :latest suffix
                        "prompt": prompt,
                        "temperature": temp
                    }
                )
                logger.debug(f"Ollama API response received for model {model}")
                response.raise_for_status()
                result = {
                    "success": True,
                    "content": response.json().get("response", ""),
                    "tokens_used": "N/A"  # Ollama doesn't provide token count
                }
            else:
                raise ValueError(f"Invalid or unavailable provider: {provider}")
            
            logger.debug(f"Successfully got response from {provider}")
            return result
            
        except Exception as e:
            logger.error(f"Error sending prompt to {provider}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def brainstorm_project(self, topic: str) -> Dict[str, Any]:
        """
        Generate AI project ideas based on a topic.
        
        Args:
            topic (str): The topic or field of interest
            
        Returns:
            Dict[str, Any]: Project suggestions and implementation details
        """
        prompt = f"""
        Help me brainstorm an AI/Data Science project related to {topic}. Please provide:
        1. Project title
        2. Problem statement
        3. Suggested approach
        4. Required technologies/libraries
        5. Potential challenges
        6. Expected outcomes
        """
        return self.send_prompt(prompt)
    
    def get_code_suggestion(self, description: str) -> Dict[str, Any]:
        """
        Get code suggestions for implementing specific functionality.
        
        Args:
            description (str): Description of the desired functionality
            
        Returns:
            Dict[str, Any]: Code suggestions and explanations
        """
        prompt = f"""
        Please provide Python code suggestions for the following functionality:
        {description}
        
        Include:
        1. Code implementation
        2. Required imports
        3. Brief explanation of the approach
        4. Any potential improvements
        """
        return self.send_prompt(prompt)
