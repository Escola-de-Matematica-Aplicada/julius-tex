#!/usr/bin/env python3
"""
Example of using the NVIDIA provider directly with streaming support.
Based on the official NVIDIA API example provided.
"""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from julius_tex.providers.openai_compat import NvidiaProvider
from julius_tex.providers.base import Message


def example_basic_streaming():
    """Example 1: Basic streaming with NVIDIA provider."""
    print("=" * 60)
    print("Example 1: Basic Streaming")
    print("=" * 60)
    
    api_key = "your_nvidia_api_key_here"  # Replace with your actual key
    
    # Create provider
    provider = NvidiaProvider(api_key=api_key)
    
    print(f"Provider: {provider.name}")
    print(f"Model: {provider.model}")
    print(f"Max Context: {provider.max_context_tokens:,} tokens")
    print()
    
    # Create a simple message
    messages = [
        Message(role="user", content="What is machine learning in simple terms?")
    ]
    
    # Stream the response
    print("Response:")
    print("-" * 40)
    
    for chunk in provider.stream_chat(
        messages, 
        system="You are a helpful AI assistant."
    ):
        print(chunk, end="", flush=True)
    
    print("\n" + "-" * 40)
    print()


def example_custom_model():
    """Example 2: Using a custom NVIDIA model."""
    print("=" * 60)
    print("Example 2: Custom Model (Nemotron)")
    print("=" * 60)
    
    api_key = "your_nvidia_api_key_here"  # Replace with your actual key
    
    # Create provider with custom model
    provider = NvidiaProvider(
        api_key=api_key,
        model="nvidia/llama-3.1-nemotron-70b-instruct"
    )
    
    print(f"Provider: {provider.name}")
    print(f"Model: {provider.model}")
    print(f"Max Context: {provider.max_context_tokens} tokens")
    print()
    
    # Create a message
    messages = [
        Message(role="user", content="Explain quantum computing briefly.")
    ]
    
    print("Response:")
    print("-" * 40)
    
    for chunk in provider.stream_chat(messages):
        print(chunk, end="", flush=True)
    
    print("\n" + "-" * 40)
    print()


def example_multi_turn_conversation():
    """Example 3: Multi-turn conversation with context."""
    print("=" * 60)
    print("Example 3: Multi-turn Conversation")
    print("=" * 60)
    
    api_key = "your_nvidia_api_key_here"  # Replace with your actual key
    
    provider = NvidiaProvider(api_key=api_key)
    
    # Create a conversation history
    messages = [
        Message(role="user", content="What is Python?"),
        Message(role="assistant", content="Python is a high-level programming language known for its simplicity and readability. It's used in web development, data science, artificial intelligence, and many other domains."),
        Message(role="user", content="What are its main advantages?"),
    ]
    
    print("Conversation Context:")
    for msg in messages[:-1]:
        print(f"  {msg.role.upper()}: {msg.content[:50]}...")
    print(f"  USER: {messages[-1].content}")
    print()
    
    print("Response:")
    print("-" * 40)
    
    for chunk in provider.stream_chat(
        messages,
        system="You are a Python expert. Answer questions clearly and concisely."
    ):
        print(chunk, end="", flush=True)
    
    print("\n" + "-" * 40)
    print()


def example_list_models():
    """Example 4: List available models."""
    print("=" * 60)
    print("Example 4: Available Models")
    print("=" * 60)
    
    api_key = "your_nvidia_api_key_here"  # Replace with your actual key
    
    provider = NvidiaProvider(api_key=api_key)
    
    try:
        models = provider.list_models()
        print(f"Available NVIDIA models ({len(models)} total):")
        for i, model in enumerate(models, 1):
            print(f"  {i}. {model}")
    except Exception as e:
        print(f"Error listing models: {e}")
    
    print()


def example_with_system_prompt():
    """Example 5: Using a detailed system prompt."""
    print("=" * 60)
    print("Example 5: Custom System Prompt")
    print("=" * 60)
    
    api_key = "your_nvidia_api_key_here"  # Replace with your actual key
    
    provider = NvidiaProvider(api_key=api_key)
    
    system_prompt = """You are an expert technical writer specializing in AI and machine learning.
    When answering questions:
    - Be precise and technical
    - Include relevant examples
    - Explain complex concepts clearly
    - Suggest practical applications when relevant"""
    
    messages = [
        Message(role="user", content="Explain attention mechanisms in neural networks.")
    ]
    
    print("System Prompt:")
    print(f"  {system_prompt[:100]}...")
    print()
    print("User Question:")
    print(f"  {messages[0].content}")
    print()
    print("Response:")
    print("-" * 40)
    
    for chunk in provider.stream_chat(messages, system=system_prompt):
        print(chunk, end="", flush=True)
    
    print("\n" + "-" * 40)
    print()


def main():
    """Run all examples."""
    print("\n")
    print("█████████████████████████████████████████████████████████████")
    print("  NVIDIA Provider Examples for julius-tex")
    print("█████████████████████████████████████████████████████████████")
    print("\n")
    
    examples = [
        ("Basic Streaming", example_basic_streaming),
        ("Custom Model", example_custom_model),
        ("Multi-turn Conversation", example_multi_turn_conversation),
        ("List Models", example_list_models),
        ("Custom System Prompt", example_with_system_prompt),
    ]
    
    print("Available examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    print()
    
    # You can uncomment specific examples to run them
    # Make sure to set your actual API key first!
    
    print("To run these examples:")
    print("1. Set your NVIDIA API key in the script")
    print("2. Uncomment the example function calls below")
    print("3. Run: python examples_nvidia_provider.py")
    print()
    
    # Uncomment to run examples:
    # example_basic_streaming()
    # example_custom_model()
    # example_multi_turn_conversation()
    # example_list_models()
    # example_with_system_prompt()
    
    print("Documentation:")
    print("  - NVIDIA_QUICKSTART.md - Quick start guide")
    print("  - NVIDIA_SETUP.md - Detailed setup instructions")
    print("  - NVIDIA_INTEGRATION.md - Integration technical details")
    print()


if __name__ == "__main__":
    main()
