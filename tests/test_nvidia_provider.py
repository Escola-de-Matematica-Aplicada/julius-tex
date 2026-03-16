"""Test NVIDIA provider with streaming and reasoning content support."""

from julius_tex.providers.openai_compat import NvidiaProvider
from julius_tex.providers.base import Message


def test_nvidia_basic():
    """Test basic NVIDIA provider functionality."""
    # Initialize the provider with your NVIDIA API key
    api_key = "your_nvidia_api_key_here"
    provider = NvidiaProvider(api_key=api_key)
    
    print(f"Provider name: {provider.name}")
    print(f"Model: {provider.model}")
    print(f"Max context tokens: {provider.max_context_tokens}")
    

def test_nvidia_chat():
    """Test NVIDIA provider chat completion with streaming."""
    api_key = "your_nvidia_api_key_here"
    provider = NvidiaProvider(api_key=api_key, model="z-ai/glm4.7")
    
    # Create a simple message
    messages = [Message(role="user", content="What is the meaning of life?")]
    
    # Stream the response
    print("Streaming response from NVIDIA:")
    print("-" * 40)
    
    response = provider.stream_chat(messages, system="You are a helpful assistant.")
    for chunk in response:
        print(chunk, end="", flush=True)
    
    print("\n" + "-" * 40)


def test_nvidia_list_models():
    """Test listing available NVIDIA models."""
    api_key = "your_nvidia_api_key_here"
    provider = NvidiaProvider(api_key=api_key)
    
    try:
        models = provider.list_models()
        print("Available NVIDIA models:")
        for model in models:
            print(f"  - {model}")
    except Exception as e:
        print(f"Error listing models: {e}")


if __name__ == "__main__":
    test_nvidia_basic()
    print()
    # Uncomment to test with actual API:
    # test_nvidia_chat()
    # test_nvidia_list_models()
