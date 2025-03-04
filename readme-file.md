# Local LLM Chat App with Streamlit

![LLM Chat App](https://img.shields.io/badge/Project-LLM%20Chat%20App-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLMs-green)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Overview

This project is a real-time, user-friendly chat application using Streamlit and Ollama's local LLMs. It allows users to interact with various open-source large language models running locally on their machine, making it both private and flexible.

## Features

- 💬 Interactive chat interface with streaming responses
- 🔄 Support for multiple local LLM models (Llama3, Phi3, Mistral, etc.)
- 📊 Performance metrics comparison between models
- 🔒 Privacy-focused (all processing happens locally)
- 🎛️ Customizable settings (model selection, streaming toggle)
- 📱 Responsive design for various screen sizes

## Screenshot

(Add a screenshot of your application here when available)

## Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed locally

## Installation

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/local-llm-chat-app.git
cd local-llm-chat-app
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install and run Ollama:
- Download from [ollama.ai](https://ollama.ai/)
- Follow the installation instructions for your platform
- Pull a model: `ollama pull llama3`

## Usage

1. Ensure Ollama is running in the background
2. Start the Streamlit app:
```bash
streamlit run app.py
```
3. Open your browser at `http://localhost:8501`
4. Select your preferred model from the sidebar
5. Start chatting!

## Models

This app supports any model available through Ollama, including:

- **Llama3**: Meta's latest open-source LLM
- **Phi3**: Microsoft's efficient small language model
- **Mistral**: High-performance open-source LLM
- And many more!

## Project Structure

```
local-llm-chat-app/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Future Enhancements

- [ ] Add model parameter customization (temperature, max tokens)
- [ ] Implement chat history export/import
- [ ] Add support for RAG (Retrieval Augmented Generation)
- [ ] Integrate system prompts/personas
- [ ] Add benchmarking tools for model comparison

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the web app framework
- [Ollama](https://ollama.ai/) for making local LLMs accessible
- All the amazing open-source LLM projects
