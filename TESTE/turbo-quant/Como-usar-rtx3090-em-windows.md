> **Nota importante sobre "TurboQuant":** O TurboQuant é um método de quantização de KV cache recém-publicado no ICLR 2026 (março/2026), mas ainda **não está integrado ao vLLM**. Para RTX 3090, o equivalente de alta performance já disponível no vLLM é o **AWQ Marlin** e o **GPTQ Marlin** — kernels otimizados que entregam o melhor throughput na arquitetura Ampere. O guia abaixo cobre essa stack. [forums.developer.nvidia](https://forums.developer.nvidia.com/t/why-turboquant-saves-dgx-twice/364736)

***

## Visão Geral da Arquitetura

O vLLM **não roda nativamente no Windows** — você precisa de WSL2 (recomendado) ou Docker Desktop com backend WSL2. A RTX 3090 tem 24 GB VRAM e compute capability 8.6 (Ampere), o que tem uma **limitação importante**: FP8 KV cache (`--kv-cache-dtype fp8`) **não é suportado** nessa GPU. Os métodos de quantização de peso (AWQ Marlin, GPTQ Marlin) funcionam perfeitamente. [reddit](https://www.reddit.com/r/LocalLLaMA/comments/1jct1lk/pr_for_native_windows_support_was_just_submitted/)

***

## Pré-requisitos

Instale nesta ordem:

1. **Driver NVIDIA para Windows** — versão ≥ 525.x (o driver Windows já expõe CUDA ao WSL2 automaticamente)
2. **WSL2** — execute no PowerShell como admin:
   ```powershell
   wsl --install -d Ubuntu-22.04
   ```
3. **CUDA Toolkit dentro do WSL2** (não instale o driver dentro do WSL):
   ```bash
   wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
   sudo dpkg -i cuda-keyring_1.1-1_all.deb
   sudo apt-get update && sudo apt-get install -y cuda-toolkit-12-6
   ```
4. **Verifique o acesso à GPU** no WSL2:
   ```bash
   nvidia-smi  # deve listar a RTX 3090
   ```

***

## Instalação do vLLM

Dentro do WSL2, crie um ambiente Python isolado: [mobiarch.wordpress](https://mobiarch.wordpress.com/2025/10/02/install-vllm-in-wsl/)

```bash
# Criar ambiente virtual
python3 -m venv ~/vllm-env
source ~/vllm-env/bin/activate

# Instalar vLLM com suporte CUDA
pip install vllm

# Variáveis de ambiente CUDA (adicione ao ~/.bashrc)
export PATH="/usr/local/cuda-12.6/bin:$PATH"
export LD_LIBRARY_PATH="/usr/local/cuda-12.6/lib64:$LD_LIBRARY_PATH"
```

***

## Quantização Suportada no RTX 3090

A tabela abaixo mostra os métodos ordenados por desempenho na Ampere: [discuss.vllm](https://discuss.vllm.ai/t/kv-cache-quantizing/749)

| Método | Flag vLLM | VRAM (32B) | Throughput | Suporte 3090 |
|---|---|---|---|---|
| AWQ Marlin | `awq_marlin` | ~18 GB | ✅ Melhor | ✅ |
| GPTQ Marlin | `gptq_marlin` | ~17 GB | ✅ Ótimo | ✅ |
| GPTQ | `gptq` | ~17 GB | Bom | ✅ |
| AWQ | `awq` | ~18 GB | Bom | ✅ |
| BitsAndBytes | `bitsandbytes` | ~20 GB | Lento | ✅ |
| FP8 KV Cache | `--kv-cache-dtype fp8` | — | — | ❌ Não suportado |

O AWQ Marlin usa o kernel Marlin de alta performance e entrega +46% de throughput em relação ao BF16 baseline. [docs.gpustack](https://docs.gpustack.ai/2.0/performance-lab/references/the-impact-of-quantization-on-vllm-inference-performance/)

***
## model off-line

export HF_HUB_ENABLE_HF_TRANSFER=1

huggingface-cli download QuantTrio/Qwen3-Coder-30B-A3B-Instruct-AWQ --local-dir ~/.vllm-modelos/qwenA3B-30B-AWQ
vllm serve ~/.vllm-modelos/qwenA3B-30B-AWQ --quantization awq_marlin --host 127.0.0.1 --port 8000


## Subindo o Servidor API (OpenAI-Compatible)

Exemplo para servir um modelo Qwen2.5-32B-AWQ com AWQ Marlin: [qwen.readthedocs](https://qwen.readthedocs.io/en/stable/quantization/gptq.html)

```bash
source ~/vllm-env/bin/activate

-- Qwen3-Coder-30B-A3B-AWQ
-- DeepSeek-R1-Distill-Qwen-32B-AWQ
-- DeepSeek-R1-Distill-Qwen-14B-AWQ
-- Qwen/Qwen2.5-7B-Instruct-AWQ
-- Qwen/Qwen2.5-32B-Instruct-AWQ
-- Qwen/qwen3.5-35b-a3b

vllm serve ~/.vllm-modelos/qwenA3B-30B-AWQ \
  --quantization awq_marlin \
  --dtype half \
  --max-model-len 8192 \
  --max-num-batched-tokens 8192 \
  --max-num-seqs 1 \
  --gpu-memory-utilization 0.92 \
  --enforce-eager \
  --api-key "key" \
  --host 0.0.0.0 \
  --port 8000
```

Flags obrigatorias para tool use

```bash
vllm serve Qwen/Qwen3-Coder-30B-A3B-Instruct-AWQ \
  --quantization awq_marlin \
  --host 0.0.0.0 \
  --port 8000 \
  --max-model-len 32768 \
  --gpu-memory-utilization 0.90 \
  --disable-custom-all-reduce \
  --tool-call-parser qwen3_coder
```

Reasoning puro:

```bash
vllm serve bullerwins/DeepSeek-R1-Distill-Qwen-14B-GPTQ-Int4 \
  --quantization gptq_marlin \
  --host 0.0.0.0 \
  --port 8000 \
  --max-model-len 16384 \
  --gpu-memory-utilization 0.88
```

https://huggingface.co/QuantTrio/Qwen3-Coder-30B-A3B-Instruct-AWQ

```bash
export CONTEXT_LENGTH=32768
export VLLM_LOGGING_LEVEL=WARNING   # substitui --disable-log-requests
export TRANSFORMERS_OFFLINE=1


vllm serve ~/.vllm-modelos/qwenA3B-30B-AWQ \
    --served-model-name Qwen3-Coder-30B-A3B-Instruct-AWQ \
    --quantization awq_marlin \
    --max-model-len 32768 \
    --max-num-seqs 4 \
    --gpu-memory-utilization 0.90 \
    --trust-remote-code \
    --host 0.0.0.0 \
    --port 8000
```


Parâmetros críticos para 24 GB de VRAM:

- `--max-num-seqs 1` — com 24 GB, limite de 1 requisição concorrente para modelos 32B
- `--enforce-eager` — desabilita CUDA graphs, economiza memória
- `--gpu-memory-utilization 0.92` — reserva 8% de VRAM para overhead do sistema
- `--dtype half` — recomendado para AWQ no Ampere [docs.vllm](https://docs.vllm.ai/en/v0.6.0/serving/openai_compatible_server.html)

***

## Consumindo a API

curl -v http://127.0.0.1:8000/v1/models \
  -H "Authorization: Bearer key"

O endpoint é 100% compatível com o SDK da OpenAI: [docs.vllm](https://docs.vllm.ai/en/v0.6.0/serving/openai_compatible_server.html)

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="sua-chave-aqui"
)

response = client.chat.completions.create(
    model="Qwen/Qwen2.5-32B-Instruct-AWQ",
    messages=[{"role": "user", "content": "Explique quantização AWQ"}],
    temperature=0.7,
    max_tokens=512
)
print(response.choices[0].message.content)
```

***

## Modelos Recomendados para RTX 3090

Modelos já disponíveis no HuggingFace com AWQ/GPTQ prontos para uso: [reddit](https://www.reddit.com/r/LocalLLaMA/comments/1hm3e5t/how_to_serve_vllm_qwen2532b_awq_on_a_single_rtx/)

- **Qwen2.5-7B-Instruct-GPTQ-Int4** — cabe com folga (~6 GB), ideal para testes
- **Qwen2.5-14B-Instruct-AWQ** — boa qualidade com ~10 GB
- **Qwen2.5-32B-Instruct-AWQ** — máximo viável no 3090, ~18–20 GB
- **Llama-3.1-8B-AWQ** — alternativa leve e rápida

***

## Sobre TurboQuant (ICLR 2026)

O TurboQuant, publicado em 24/03/2026, propõe quantização de KV cache em 3,5 bits com perdas estatisticamente nulas em benchmarks como LongBench e RULER. Por enquanto, **não há integração oficial no vLLM**. Fique de olho nas releases do vLLM — dado o ritmo de adoção do projeto, a integração deve chegar nos próximos meses. Quando disponível, o flag será algo como `--kv-cache-dtype turbo` ou via `compressed-tensors`. [forums.developer.nvidia](https://forums.developer.nvidia.com/t/why-turboquant-saves-dgx-twice/364736)


## testar Aider

pip install aider-chat

aider \
  --openai-api-base http://localhost:8000/v1 \
  --openai-api-key EMPTY \
  --model Qwen/Qwen3-Coder-30B-A3B-Instruct-AWQ