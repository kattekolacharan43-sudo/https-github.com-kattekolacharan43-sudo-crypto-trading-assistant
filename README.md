# Personal AI Assistant

A versatile, extensible AI assistant built with Python that can be customized for various use cases including crypto trading analysis, personal productivity, coding help, and more.

## Features

- 🤖 **Multi-Purpose AI Integration** - Supports OpenAI, Claude, and other LLM providers
- 💾 **Memory Management** - Conversation history and context persistence
- 🔧 **Modular Architecture** - Easy to extend with custom tools and features
- ⚙️ **Configuration Management** - Environment-based settings
- 📝 **Logging & Monitoring** - Comprehensive logging for debugging
- 🔐 **Security** - Secure API key handling
- 🧠 **Smart Responses** - Context-aware, intelligent replies

## Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- OpenAI API key or other LLM provider credentials

### Installation

1. Clone the repository
```bash
git clone <repo-url>
cd ai-assistant
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. Run the assistant
```bash
python main.py
```

## Project Structure

```
ai-assistant/
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment config
├── config/
│   ├── __init__.py
│   └── settings.py        # Configuration management
├── core/
│   ├── __init__.py
│   ├── assistant.py       # Main AI assistant class
│   ├── memory.py          # Conversation memory management
│   └── tools.py           # Custom tools and utilities
├── integrations/
│   ├── __init__.py
│   ├── openai_api.py      # OpenAI integration
│   ├── llm_provider.py    # LLM provider abstraction
│   └── crypto_api.py      # Crypto data integration (optional)
├── utils/
│   ├── __init__.py
│   ├── logger.py          # Logging setup
│   └── validators.py      # Input validation
└── tests/
    ├── __init__.py
    ├── test_assistant.py
    └── test_memory.py
```

## Usage

### Basic Chat
```python
from core.assistant import PersonalAssistant

assistant = PersonalAssistant()
response = assistant.chat("What is the current Bitcoin price?")
print(response)
```

### With Custom Tools
```python
assistant = PersonalAssistant()
assistant.add_tool(custom_tool_function)
response = assistant.chat("Use the tool to help me")
```

## Configuration

Edit `.env` file with your settings:
```
OPENAI_API_KEY=your_api_key_here
ASSISTANT_NAME=YourAssistantName
LOG_LEVEL=INFO
MAX_MEMORY=50
```

## API Providers Supported

- OpenAI (GPT-3.5, GPT-4)
- Anthropic Claude
- HuggingFace Inference API
- Local LLMs (via Ollama)

## Extending the Assistant

### Add a Custom Tool
```python
from core.tools import register_tool

@register_tool("my_tool")
def my_custom_tool(input_data):
    # Your implementation
    return result
```

### Add a New LLM Provider
1. Create a new file in `integrations/`
2. Implement the provider interface
3. Register in `llm_provider.py`

## Examples

- Crypto trading analysis and alerts
- Personal productivity assistant
- Code review and debugging helper
- Educational tutor
- Customer support chatbot
- And more...

## Contributing

Contributions are welcome! Please follow:
1. Create a feature branch
2. Write tests for new functionality
3. Submit a pull request

## License

MIT License

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Built with ❤️ for extensibility and ease of use**
