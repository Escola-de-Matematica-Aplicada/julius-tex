https://huggingface.co/mistralai/Leanstral-2603

Hugging Face's logo
Hugging Face
Models
Datasets
Spaces
Buckets
new
Docs
Enterprise
Pricing


mistralai
/
Leanstral-2603 

like
8

Following
Mistral AI_
15.8k
vllm

License:
apache-2.0
Model card
Files and versions
xet
Community
4
Leanstral 119B A6B
Leanstral is the first open-source code agent designed for Lean 4, a proof assistant capable of expressing complex mathematical objects such as perfectoid spaces and software specifications like properties of Rust fragments.

Built as part of the Mistral Small 4 family, it combines multimodal capabilities and an efficient architecture, making it both performant and cost-effective compared to existing closed-source alternatives.

For more details about the model and its scope, please read the related blog post.

Key Features
Leanstral incorporates the following architectural choices:

MoE: 128 experts, 4 active per token
Model Size: 119B parameters with 6.5B activated per token
Context Length: 256k tokens
Multimodal Input: Accepts text and image input, producing text output
Leanstral offers these capabilities:

Proof Agentic: Designed specifically for proof engineering scenarios
Tool Calling Support: Optimized for Mistral Vibe
Vision: Can analyze images and provide insights
Multilingual: Supports English, French, Spanish, German, Italian, Portuguese, Dutch, Chinese, Japanese, Korean, and Arabic
System Prompt Compliance: Strong adherence to system prompts
Speed-Optimized: Best-in-class performance
Apache 2.0 License: Open-source license for commercial and non-commercial use
Large Context Window: Supports up to 256k tokens
Recommended Settings
Temperature: 1.0
Reasoning Effort:
'none' → Do not use reasoning
'high' → Use reasoning (recommended for complex prompts) Use reasoning_effort="high" for complex tasks
Context Length: ≤ 200k tokens recommended
Usage
Mistral-Vibe
Use Leanstral 119B A6B with Mistral Vibe. Install the latest version (2.5.0):

uv pip install mistral-vibe --upgrade

# make sure it's >= 2.5.0

Leanstral can be added by starting vibe and simply running:

/leanstall

This will add leanstral as an additional model, add a system prompt (see LEAD.md) as well as ensure leanstral can be used as a subagent.

Screenshot 2026-03-16 at 18.03.39


Then just press "tab+shift" a couple times until you see the new "lean" mode and leanstral model.



Screenshot 2026-03-16 at 18.17.04

Local server

If instead of pinging the Mistral API, you want to use your local vLLM server, you can do the following:

Spin up a vllm server as explained in Usage - vllm
Create a new agent file called lean.toml in ~/.vibe/agents:
mkdir ~/.vibe/agents/ && touch ~/.vibe/agents/lean.toml

And then copy-paste the following config into ~/.vibe/agents/lean.toml

display_name = "Lean (local vLLM)"
description = "Lean 4 mode using local vLLM"
safety = "neutral"

system_prompt_id = "lean"
active_model = "leanstral"

[[providers]]
name = "vllm"
api_base = "http://<your-host-url>:8000/v1"
api_key_env_var = ""
backend = "generic"
reasoning_field_name = "reasoning_content"

[[models]]
name = "mistralai/Leanstral-2603"
provider = "vllm"
alias = "leanstral"
thinking = "high"
temperature = 1.0
auto_compact_threshold = 168000

[tools.bash]
default_timeout = 1200

Note: Make sure to overwrite <your-host-url> with your server's url.

Then restart vibe and "tab-shift" to "lean" mode.

Give it a try on some "lean" code such as, e.g.: PrimeNumberTheoremAnd

Local Deployment
The model can also be deployed with the following libraries, we advise everyone to use the Mistral AI API if the model is subpar with local serving:

vllm (recommended): See here.
transformers: WIP ⏳ - follow updates on this PR.
SGLang: WIP ⏳ - follow updates on this PR
vLLM (recommended)
We recommend using this model with the vLLM library to implement production-ready inference pipelines.

Installation

We recommend installing vLLM from our custom Docker image that has fixes for Tool Calling and Reasoning parsing in vLLM and uses the latest version of Transformers. We're working with the vLLM team to merge these fixes to main as soon as possible.

Custom Docker

Make sure to use the following docker image mistralllm/vllm-ms4:latest:

docker pull mistralllm/vllm-ms4:latest
docker run -it mistralllm/vllm-ms4:latest

Manual Install

If you prefer, you can also manually install vllm from this PR: Add Mistral Guidance.

Note: It is likely that this PR will be split into smaller PRs and merged to vllm main in the coming 1-2 weeks (Stand: 16.03.2026). Check latest developments directly on the PR.

Git clone vLLM:
git clone --branch fix_mistral_parsing https://github.com/juliendenize/vllm.git

Install with pre-compiled kernels
VLLM_USE_PRECOMPILED=1 pip install --editable .

Make sure, transformers is installed from "main":
uv pip install git+https://github.com/huggingface/transformers.git

Also make sure to have installed mistral_common >= 1.10.0. To check:

python -c "import mistral_common; print(mistral_common.__version__)"

Launch server

We recommend that you use Leanstral in a server/client setting.

vllm serve mistralai/Leanstral-2603 \
  --max-model-len 200000 \
  --tensor-parallel-size 4 \
  --attention-backend FLASH_ATTN_MLA \
  --tool-call-parser mistral \
  --enable-auto-tool-choice \
  --reasoning-parser mistral

Client

from openai import OpenAI
from huggingface_hub import hf_hub_download

# Modify OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "<your-host-url>"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

TEMP = 1.0
MAX_TOK = 32000
REASONING = "high" # switch to 'none' for faster answers

models = client.models.list()
model = models.data[0].id


prompt = """Define the transition rules as an inductive proposition.

This choice provides better support for proving properties about valid transitions and is generally more natural for modeling state machines in Lean, where you want to express logical rules rather than just computing a yes/no vale for each possible transition."""
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": prompt,
            },
        ],
    },
]



response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=TEMP,
    max_tokens=MAX_TOK,
    reasoning_effort=REASONING,
)

print("Content")
print(response.choices[0].message.content)

pritn("Reasoning")
print(response.choices[0].message.reasoning)

Example Content:

Expand
Tool-Calling

You can add tools to the chat completion as follows:

prompt = """I have the following Lean 4 code snippet and want to check if it compiles and runs without errors. Can you run it for me and let me know the result?

```lean\ninductive State where\n  | idle\n  | busy\n  | error\n\ndef transition : State → State → Bool\n  | .idle, .busy => true\n  | .busy, .idle => true\n  | .busy, .error => true\n  | _, _ => false\n\n#eval transition .idle .busy\n```"""

tools = [{
    "type": "function",
    "function": {
        "name": "lean_run_code",
        "description": "Run or compile an independent Lean code snippet or file and return the result or error message.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Lean code snippet to run or compile. Either this or file_path must be provided."
                },
                "file_path": {
                    "type": "string",
                    "description": "Path to the Lean file to run or compile. Either this or code must be provided."
                }
            },
        }
        }
}]

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": prompt,
            },
        ],
    },
]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=TEMP,
    max_tokens=MAX_TOK,
    reasoning_effort=REASONING,
    tools=tools,
)

print("Tool Calls")
print(response.choices[0].message.tool_calls)

print("Reasoning")
print(response.choices[0].message.reasoning)

Example Tool Calls:

Expand
License
This model is licensed under the Apache 2.0 License.

You must not use this model in a manner that infringes, misappropriates, or otherwise violates any third party’s rights, including intellectual property rights.

Downloads last month
4
Inference Providers
NEW
This model isn't deployed by any Inference Provider.
🙋
Ask for provider support
System theme
TOS
Privacy
About
Careers
Models
Datasets
Spaces
Pricing
Docs