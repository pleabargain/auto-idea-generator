"""
AI Project Generator - Main Application
Original Project: DDS AI Project Assistant
Enhanced by: Dennis Daniels

Improvements:
- Added Ollama integration for local model support
- Implemented comprehensive logging
- Added API configuration tab
- Enhanced error handling and model switching
"""

import gradio as gr
from ai_wrapper import AIProjectAssistant
from typing import Tuple, Dict, Any
import os
import logging
from dotenv import load_dotenv
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

# Load environment variables
load_dotenv()

# Initialize AI Assistant
assistant = AIProjectAssistant()

# Updated project options focusing on Generative AI
PROJECT_OPTIONS = {
    "Text-to-Image Generation": "Create an AI system that generates images from text descriptions using models like DALL-E or Stable Diffusion",
    "GPT Chatbot Assistant": "Build a custom GPT-powered chatbot assistant for specific domain expertise",
    "AI Story Generator": "Develop a creative writing AI that generates stories based on prompts",
    "Voice Cloning AI": "Create a system that can clone and synthesize human voices",
    "AI Music Composer": "Build an AI system that composes original music in different styles",
    "Text-to-Video Generation": "Implement a system that creates short videos from text descriptions",
    "AI Code Generator": "Create a coding assistant that generates code from natural language descriptions",
    "AI Art Style Transfer": "Develop a system that applies artistic styles to images using AI",
    "AI Content Summarizer": "Build an AI that creates concise summaries of long-form content",
    "Virtual Avatar Creator": "Create an AI system that generates and animates virtual avatars"
}

# Custom CSS for better styling
CUSTOM_CSS = """
.container {
    max-width: 1200px;
    margin: auto;
    padding: 20px;
}
.title {
    text-align: center;
    color: #61dafb;
    padding: 20px;
    border-bottom: 3px solid #61dafb;
    margin-bottom: 30px;
}
.subtitle {
    color: #ffffff;
    text-align: center;
    font-style: italic;
}
.project-button {
    margin: 5px;
    border: 2px solid #61dafb;
    border-radius: 8px;
    background-color: rgba(97, 218, 251, 0.1);
    color: #ffffff;
}
.project-button:hover {
    background-color: rgba(97, 218, 251, 0.2);
    color: #61dafb;
}
.output-box {
    border: 2px solid #61dafb;
    border-radius: 10px;
    padding: 15px;
    background-color: rgba(97, 218, 251, 0.05);
}
.sidebar {
    background-color: rgba(97, 218, 251, 0.05);
    padding: 20px;
    border-radius: 10px;
    border: 2px solid #61dafb;
}
"""

def get_model_choices() -> Dict[str, list]:
    """Get available models from both providers."""
    logger.debug("Fetching available models")
    return assistant.get_available_models()

def update_model_choices(provider: str) -> Dict:
    """Update model choices based on selected provider."""
    logger.debug(f"Updating model choices for provider: {provider}")
    models = get_model_choices()
    
    # Set appropriate default model based on provider
    default_model = "gpt-4" if provider == "openai" else "llama3.2"
    
    return gr.Dropdown(
        choices=models.get(provider, []),
        value=default_model
    )

def process_input(input_type: str, query: str, provider: str, model: str) -> Tuple[str, str]:
    """Process user input and return AI response."""
    if not query.strip():
        logger.warning("Empty query received")
        return "", "Please enter a query"
    
    logger.info(f"Processing {input_type} request with {provider} using {model}")
    
    if input_type == "brainstorm":
        response = assistant.brainstorm_project(query)
    else:
        response = assistant.get_code_suggestion(query)
    
    if response["success"]:
        status = f"Success! Tokens used: {response.get('tokens_used', 'N/A')}"
        logger.info(f"Request successful: {status}")
        return response["content"], status
    else:
        error_msg = f"Error: {response.get('error', 'Unknown error occurred')}"
        logger.error(error_msg)
        return "", error_msg

def handle_project_click(project_name: str, provider: str, model: str) -> Tuple[str, str, str]:
    """Handle when a project option is clicked."""
    description = PROJECT_OPTIONS[project_name]
    response = assistant.brainstorm_project(description)
    
    if response["success"]:
        status = f"Success! Tokens used: {response.get('tokens_used', 'N/A')}"
        logger.info(f"Project click handled successfully: {status}")
        return "brainstorm", description, response["content"]
    else:
        error_msg = f"Error: {response.get('error', 'Unknown error occurred')}"
        logger.error(f"Error handling project click: {error_msg}")
        return "brainstorm", description, error_msg

if __name__ == "__main__":
    logger.info("Starting application")
    
    # Create Gradio interface with custom theme and tabs
    with gr.Blocks(css=CUSTOM_CSS, title="DDS AI Project Assistant") as interface:
        with gr.Column(elem_classes="container"):
            gr.HTML("""
                <div class="title">
                    <h1>🤖 DDS AI Project Assistant 🚀</h1>
                    <p class="subtitle">Your Generative AI Project Development Companion</p>
                </div>
            """)
            
            # Create tabs for main interface and API configuration
            with gr.Tabs():
                # Main interface tab
                with gr.Tab("Project Assistant"):
                    with gr.Row():
                        # Left sidebar with project options
                        with gr.Column(scale=1, elem_classes="sidebar"):
                            gr.HTML("""
                                <h3 style="text-align: center; color: #61dafb;">
                                    🎯 Popular GenAI Projects
                                </h3>
                            """)
                            project_buttons = [
                                gr.Button(
                                    name,
                                    elem_classes="project-button"
                                ) for name in PROJECT_OPTIONS.keys()
                            ]
                        
                        # Main content area
                        with gr.Column(scale=3):
                            with gr.Row():
                                provider = gr.Radio(
                                    choices=["openai", "ollama"],
                                    label="🤖 AI Provider",
                                    value=assistant.current_provider
                                )
                                model = gr.Dropdown(
                                    choices=get_model_choices().get(assistant.current_provider, []),
                                    label="🔧 Model",
                                    value=assistant.default_model.split(":")[0] if assistant.current_provider == "ollama" else assistant.default_model
                                )
                            
                            input_type = gr.Radio(
                                choices=["brainstorm", "code"],
                                label="🤔 What kind of help do you need?",
                                value="brainstorm"
                            )
                            
                            query = gr.Textbox(
                                label="💭 Enter your topic or code request",
                                placeholder="e.g., 'text-to-image generation' or 'implement stable diffusion'",
                                elem_classes="output-box"
                            )
                            
                            submit_btn = gr.Button(
                                "🚀 Get AI Assistance",
                                elem_classes="project-button"
                            )
                            
                            with gr.Column(elem_classes="output-box"):
                                output = gr.Textbox(
                                    label="🤖 AI Response",
                                    lines=10
                                )
                                status = gr.Textbox(
                                    label="📊 Status"
                                )
                    
                            # Handle main submit button
                            submit_btn.click(
                                fn=process_input,
                                inputs=[input_type, query, provider, model],
                                outputs=[output, status]
                            )
                            
                            # Handle project option buttons
                            for btn in project_buttons:
                                btn.click(
                                    fn=handle_project_click,
                                    inputs=[btn, provider, model],
                                    outputs=[input_type, query, output]
                                )
                    
                    gr.HTML("""
                    <div style="text-align: center; margin-top: 20px; padding: 10px; border-top: 2px solid #61dafb;">
                        <p>Original Project by DDS Team | Enhanced by Dennis Daniels | Powered by OpenAI & Ollama</p>
                    </div>
                    """)
                
                # API Configuration tab
                with gr.Tab("API Configuration"):
                    gr.Markdown("""
                        ### 🔑 API Configuration
                        Configure your AI providers and models here.
                    """)
                    
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("### OpenAI Configuration")
                            openai_status = gr.Textbox(
                                label="OpenAI Status",
                                value="Checking...",
                                interactive=False
                            )
                            if assistant.openai_client:
                                openai_status.value = "✅ Connected"
                            else:
                                openai_status.value = "❌ Not Connected (Set OPENAI_API_KEY in .env)"
                        
                        with gr.Column():
                            gr.Markdown("### Ollama Configuration")
                            ollama_status = gr.Textbox(
                                label="Ollama Status",
                                value="Checking...",
                                interactive=False
                            )
                            if "ollama" in get_model_choices():
                                ollama_status.value = "✅ Connected"
                            else:
                                ollama_status.value = "❌ Not Connected (Install Ollama locally)"
                    
                    gr.Markdown("""
                        ### 📝 Instructions
                        - For OpenAI: Add your API key to the .env file
                        - For Ollama: Install Ollama locally and start the service
                    """)
            
            # Connect provider selection to model updates
            provider.change(
                fn=update_model_choices,
                inputs=[provider],
                outputs=[model]
            )
    
    interface.launch()
