# AI Project Generator

# repo
https://github.com/pleabargain/auto-idea-generator



A fork of the DDS AI Project Assistant, enhanced with Ollama integration and improved logging. This interactive web application helps developers brainstorm and implement Generative AI projects using either OpenAI's GPT-4 or local Ollama models.

## Attribution

- Original Project: DDS AI Project Assistant
- Enhanced by: Dennis Daniels
- Improvements:
  - Added Ollama local model support
  - Implemented comprehensive logging system
  - Added API configuration management
  - Enhanced error handling and model switching

## Features

- 🎯 Pre-defined Generative AI project templates
- 💡 Custom project brainstorming
- 💻 Code generation and suggestions
- 🎨 Modern, intuitive web interface
- 🤖 Dual AI provider support (OpenAI and Ollama)
- 📊 Comprehensive logging system
- ⚙️ API configuration management

## Project Options

- Text-to-Image Generation
- GPT Chatbot Assistant
- AI Story Generator
- Voice Cloning AI
- AI Music Composer
- Text-to-Video Generation
- AI Code Generator
- AI Art Style Transfer
- AI Content Summarizer
- Virtual Avatar Creator

## Setup

1. Clone the repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up AI providers:
   
   ### OpenAI (Optional)
   Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

   ### Ollama (Optional)
   1. Install Ollama from [ollama.ai](https://ollama.ai)
   2. Start the Ollama service
   3. The application will automatically detect available models

4. Run the application:
   ```bash
   python app.py
   ```

5. Access the web interface at http://localhost:7860

## Usage

1. Configure AI Providers:
   - Go to the "API Configuration" tab
   - Verify the connection status of OpenAI and Ollama
   - Follow the provided instructions to set up missing providers

2. Generate Project Ideas:
   - Select your preferred AI provider and model
   - Choose the type of assistance (brainstorm or code)
   - Either:
     - Select from predefined project options
     - Enter your own project idea or code request
   - Click "Get AI Assistance" to receive detailed suggestions

3. Monitor Progress:
   - Check the status field for operation results
   - View detailed logs in `logs/app.log`

## Architecture

- `app.py`: Main application file with Gradio interface
- `ai_wrapper.py`: AI provider wrapper supporting both OpenAI and Ollama
- `logs/`: Directory containing application logs

## Requirements

- Python 3.8 or higher
- Gradio 4.0.0 or higher
- OpenAI Python SDK 1.0.0 or higher (for OpenAI integration)
- Ollama (for local model support)
- See `requirements.txt` for a complete list of dependencies

## Logging

The application maintains detailed logs in the `logs/app.log` file, including:
- API calls and responses
- User interactions
- System status and errors
- Model operations

## Note

This application can function with either OpenAI or Ollama as the AI provider. At least one provider must be properly configured for the application to be useful.

## License

Original project licensed under the terms that apply to the DDS AI Project Assistant.
Modifications and improvements are provided under the same terms.
