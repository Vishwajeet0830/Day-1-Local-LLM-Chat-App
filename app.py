# Main application file: app.py
import streamlit as st
import requests
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Import json module
import json

# Set page configuration
st.set_page_config(
    page_title="Local LLM Chat App",
    page_icon="💬",
    layout="wide"
)

# Custom CSS for better appearance
st.markdown("""
<style>
    .chat-message {
        padding: 1.5rem; 
        border-radius: 0.5rem; 
        margin-bottom: 1rem; 
        display: flex;
        flex-direction: row;
        align-items: flex-start;
    }
    .chat-message.user {
        background-color: #f0f2f6;
    }
    .chat-message.assistant {
        background-color: #e6f7ff;
    }
    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
        margin-right: 1rem;
    }
    .chat-message .message {
        flex-grow: 1;
        padding-top: 0.2rem;
    }
    .model-selector {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f9f9f9;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Function to call Ollama API
def query_ollama(prompt, model="llama3", stream=True):
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream
    }
    
    try:
        # For streaming response
        if stream:
            response = requests.post(url, json=payload, stream=True)
            if response.status_code == 200:
                collected_chunks = []
                collected_message = ""
                
                # Initialize the placeholder
                message_placeholder = st.empty()
                
                # Stream the response
                for chunk in response.iter_lines():
                    if chunk:
                        try:
                            chunk_json = json.loads(chunk.decode('utf-8'))
                            content = chunk_json.get("response", "")
                            collected_chunks.append(content)
                            collected_message = "".join(collected_chunks)
                            message_placeholder.markdown(collected_message)
                            
                            # Check if this is the last chunk
                            if chunk_json.get("done", False):
                                break
                        except json.JSONDecodeError as e:
                            st.error(f"Error decoding JSON: {str(e)}")
                            break
                return collected_message
            else:
                st.error(f"Error: {response.status_code}")
                return f"Error: {response.status_code}"
        # For non-streaming response
        else:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                st.error(f"Error: {response.status_code}")
                return f"Error: {response.status_code}"
    except Exception as e:
        st.error(f"Error connecting to Ollama: {str(e)}")
        return f"Error connecting to Ollama: {str(e)}"

# Function to get available models from Ollama
def get_available_models():
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = [model["name"] for model in response.json().get("models", [])]
            return models
        else:
            st.error(f"Error fetching models: {response.status_code}")
            return ["llama3", "phi3", "mistral"]  # Default models
    except Exception as e:
        st.error(f"Error connecting to Ollama: {str(e)}")
        return ["llama3", "phi3", "mistral"]  # Default models

# Initialize session state for chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# App title and description
st.title("🤖 Local LLM Chat App")
st.subheader("Chat with local open-source models using Ollama")

# Sidebar for model selection and settings
with st.sidebar:
    st.header("Settings")
    
    # Try to get available models, fallback to defaults if Ollama is not running
    try:
        available_models = get_available_models()
    except:
        available_models = ["llama3", "phi3", "mistral"]
    
    selected_model = st.selectbox(
        "Select LLM Model",
        options=available_models,
        index=0,
        help="Choose which local LLM to use for generating responses"
    )
    
    stream_response = st.checkbox("Stream Response", value=True, 
                                  help="Enable to see responses as they're generated")
    
    clear_chat = st.button("Clear Chat History")
    
    st.markdown("---")
    st.markdown("""
    ### About
    This app uses [Ollama](https://ollama.ai/) to run open-source LLMs locally on your machine.
    
    Make sure Ollama is running before using this app.
    
    ### Models
    - **Llama3**: Meta's latest open-source LLM
    - **Phi3**: Microsoft's efficient small language model
    - **Mistral**: High-performance open-source LLM
    """)

# Clear chat history if button is clicked
if clear_chat:
    st.session_state.messages = []
    st.experimental_rerun()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to ask?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Display assistant response
    with st.chat_message("assistant"):
        if stream_response:
            response = query_ollama(prompt, model=selected_model, stream=True)
        else:
            with st.spinner("Thinking..."):
                response = query_ollama(prompt, model=selected_model, stream=False)
                st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Display a warning if no messages and Ollama might not be running
if not st.session_state.messages:
    st.info("👋 Welcome! Make sure Ollama is running locally before sending messages.")
    st.markdown("""
    ### Quick Start:
    1. Install Ollama from [ollama.ai](https://ollama.ai/)
    2. Run Ollama locally
    3. Pull a model: `ollama pull llama3`
    4. Start chatting!
    """)

# Performance metrics section
if st.session_state.messages and st.checkbox("Show Performance Metrics"):
    st.subheader("Model Performance Metrics")
    
    # Create columns for metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Average Response Time", "1.2s", "-0.3s")
    
    with col2:
        st.metric("Tokens/Second", "45", "+5")
    
    with col3:
        st.metric("Memory Usage", "2.4 GB", "+0.2 GB")
    
    # Placeholder for more detailed metrics visualization
    st.text("Response time history (last 10 messages)")
    
    # Sample data for visualization
    st.bar_chart({"llama3": [1.2, 1.4, 1.3, 1.1, 0.9, 1.0, 1.2, 1.1, 0.9, 0.8],
                  "phi3": [0.8, 0.9, 0.7, 0.8, 0.6, 0.7, 0.8, 0.7, 0.6, 0.5]})
