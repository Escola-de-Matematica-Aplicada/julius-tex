# NVIDIA Provider Integration

## Overview

The NVIDIA provider has been integrated into julius-tex, allowing you to use NVIDIA's AI API endpoints for chat completions. This provider follows the OpenAI-compatible API standard, making it compatible with the existing provider infrastructure.

## Setup

### 1. Get Your NVIDIA API Key

1. Visit [NVIDIA Build](https://build.nvidia.com/)
2. Sign up or log in to your account
3. Generate an API key from your account settings
4. Copy the API key

### 2. Configure Your API Key

Add the NVIDIA API key to your `TOKENS` file:

```
NVIDIA_API_KEY=your_actual_api_key_here
```

Optionally, specify a default model:

```
NVIDIA_MODEL=z-ai/glm4.7
```

If not specified, the default model is `z-ai/glm4.7`.

## Available Models

The following models are available via the NVIDIA API:

| Model | Max Context | Description |
|-------|-------------|-------------|
| `z-ai/glm4.7` | 200,000 | GLM-4.7 model with extended context (default) |
| `nvidia/llama-3.1-nemotron-70b-instruct` | 4,096 | Llama 3.1 Nemotron instruction-tuned variant |
| `nvidia/mixtral-8x7b-instruct-v01` | 32,000 | Mixtral 8x7B instruction-tuned model |
| `nvidia/mistral-large` | 32,000 | Mistral Large language model |
| `nvidia/llama2-70b` | 4,096 | Llama 2 70B parameter model |

## Usage in julius-tex

Once configured, the NVIDIA provider will be automatically available in julius-tex. You can:

1. **Start julius-tex** and it will detect your NVIDIA API key
2. **Switch providers** using the `/providers` command in the chat
3. **Change models** using the `/models` command (if using an OpenAI-compatible model)
4. **View active provider** using the `/provider` command

## Example Code

### Basic Usage

```python
from julius_tex.providers.openai_compat import NvidiaProvider
from julius_tex.providers.base import Message

# Initialize the provider
api_key = "your_api_key_here"
provider = NvidiaProvider(api_key=api_key)

# Create a message
messages = [Message(role="user", content="Hello, NVIDIA!")]

# Get a response (non-streaming)
response = provider.chat(messages, system="You are a helpful assistant.")
print(response)

# Or stream the response
for chunk in provider.stream_chat(messages, system="You are a helpful assistant."):
    print(chunk, end="", flush=True)
```

### With Custom Model

```python
provider = NvidiaProvider(
    api_key="your_api_key_here",
    model="nvidia/llama-3.1-nemotron-70b-instruct"
)
```

## Features

- **OpenAI-Compatible API**: Uses the same interface as other OpenAI-compatible providers
- **Streaming Support**: Full streaming support for real-time response generation
- **Context Window Management**: Automatically manages messages to fit within model context limits
- **Multiple Models**: Switch between different NVIDIA models
- **System Prompts**: Full support for system prompts and context injection

## Troubleshooting

### "API Key not configured"
- Ensure `NVIDIA_API_KEY` is set in your `TOKENS` file
- Ensure the API key is valid and not the placeholder value (`your_`)
- Check that the key has not expired

### "Model not found"
- Verify the model name is correct
- Available models are listed in the `nvidia_max_tokens.md` file
- Check the NVIDIA API documentation for the latest available models

### "Connection refused"
- Verify you have internet connectivity
- Check that the NVIDIA API endpoint (https://integrate.api.nvidia.com/v1) is accessible
- Verify your API key has the necessary permissions

## API Endpoint

- **Base URL**: `https://integrate.api.nvidia.com/v1`
- **Authentication**: Bearer token (API key)
- **Documentation**: [NVIDIA API Documentation](https://docs.nvidia.com/ai-foundation/models/api-docs)

## References

- [NVIDIA Build](https://build.nvidia.com/) - Get started with NVIDIA models
- [NVIDIA API Documentation](https://docs.nvidia.com/ai-foundation/models/api-docs) - Full API reference
- [OpenAI Compatibility](https://openai.com/api/) - OpenAI API reference (compatible subset)
