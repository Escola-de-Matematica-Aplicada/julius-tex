6/3/2026

Hoje a Mistral AI publica uma família grande de modelos; abaixo estão os principais modelos listados na página oficial de modelos e no índice de modelos, com suas respectivas janelas de contexto máximas (input + output) conforme documentação pública até março de 2026. [mistral](https://mistral.ai/models)

## Como ler “limite de tokens”

A Mistral define um limite de janela de contexto como o total de tokens do prompt + tokens gerados, ou seja, você deve garantir \(prompt\_tokens + max\_tokens \leq context\_length\). [datastudios](https://www.datastudios.org/post/mistral-le-chat-context-window-token-limits-memory-policy-and-2025-rules)
Em modelos especializados de OCR/Document AI, o limite é especificado em “páginas” (cada página representando cerca de 1 milhão de tokens de entrada e 1 milhão de saída, no caso da integração Vertex AI). [docs.cloud.google](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/mistral/mistral-ocr)

## Modelos gerais de texto / multimodais

Modelos de uso geral (chat, instruções, RAG, etc.), incluindo versões open‑weight e comerciais.

| Modelo | Tipo / geração | Contexto máximo |
|-------|----------------|-----------------|
| Mistral Large 3 (mistral-large-3-25-12) | Frontier multimodal, open‑weight [docs.mistral](https://docs.mistral.ai/models/mistral-large-3-25-12) | 256k tokens [docs.mistral](https://docs.mistral.ai/models/mistral-large-3-25-12) |
| Mistral Large 2.0 (mistral-large-2407) | Large open‑weight anterior [docs.mistral](https://docs.mistral.ai/models/mistral-large-2-0-24-07) | 128k tokens [docs.mistral](https://docs.mistral.ai/models/mistral-large-2-0-24-07) |
| Mistral Large 1.0 (mistral-large-2402) | Large enterprise original [docs.mistral](https://docs.mistral.ai/models/mistral-large-1-0-24-02) | 32k tokens [docs.mistral](https://docs.mistral.ai/models/mistral-large-1-0-24-02) |
| Mistral Medium 3.1 (mistral-medium-3-1-25-08) | Frontier multimodal [docs.mistral](https://docs.mistral.ai/models/mistral-medium-3-1-25-08) | 128k tokens [docs.mistral](https://docs.mistral.ai/models/mistral-medium-3-1-25-08) |
| Mistral Medium 3 (mistral-medium-3-25-05) | Frontier multimodal (versão anterior) | 128k tokens [docs.mistral](https://docs.mistral.ai/models/mistral-medium-3-25-05) |
| Mistral Medium 1.0 (mistral-medium-2312) | Medium enterprise original [docs.mistral](https://docs.mistral.ai/models/mistral-medium-1-0-23-12) | 32k tokens (model card/índice indicam 32k) [docs.mistral](https://docs.mistral.ai/models/mistral-medium-1-0-23-12) |
| Mistral Small 3.2 (mistral-small-3-2-25-06) | Small multimodal mais recente [docs.mistral](https://docs.mistral.ai/models/mistral-small-3-2-25-06) | 128k tokens [docs.mistral](https://docs.mistral.ai/models/mistral-small-3-2-25-06) |
| Mistral Small 3.1 (mistral-small-3-1-25-03) | Small multimodal anterior [docs.mistral](https://docs.mistral.ai/models/mistral-small-3-1-25-03) | 128k tokens [docs.mistral](https://docs.mistral.ai/models/mistral-small-3-1-25-03) |
| Mistral Small 3.0 (mistral-small-3-0-25-01) | Small 24B open‑weight [docs.mistral](https://docs.mistral.ai/models/mistral-small-3-0-25-01) | 32k tokens [docs.mistral](https://docs.mistral.ai/models/mistral-small-3-0-25-01) |
| Mistral Small 2.0 (mistral-small-2-0-24-09) | Small open‑weight anterior [docs.mistral](https://docs.mistral.ai/models/mistral-small-2-0-24-09) | 32k tokens [docs.mistral](https://docs.mistral.ai/models/mistral-small-2-0-24-09) |
| Mistral Small 1.0 (mistral-small-1-0-24-02) | Small enterprise inicial [docs.mistral](https://docs.mistral.ai/models/mistral-small-1-0-24-02) | 32k tokens (pelo modelo 2402 na AWS/Bedrock) [docs.mistral](https://docs.mistral.ai/models/mistral-small-1-0-24-02) |
| Mistral 7B (open-mistral-7b) | Primeiro modelo open‑weight [docs.mistral](https://docs.mistral.ai/models/mistral-7b-0-1) | 8k tokens [docs.mistral](https://docs.mistral.ai/models/mistral-7b-0-1) |
| Mixtral 8x7B (open-mixtral-8x7b) | MoE open‑weight [docs.mistral](https://docs.mistral.ai/getting-started/models) | 32k tokens [mistral](https://mistral.ai/news/mixtral-of-experts) |
| Mixtral 8x22B (open-mixtral-8x22b) | MoE open‑weight grande [docs.mistral](https://docs.mistral.ai/getting-started/models) | 64k tokens (≈64k–65k segundo model cards oficiais/3ºs) [promptingguide](https://www.promptingguide.ai/models/mixtral-8x22b) |
| Pixtral 12B (pixtral-12b-2409) | 12B multimodal (texto+imagem) [docs.mistral](https://docs.mistral.ai/getting-started/models) | 128k tokens [docs.mistral](https://docs.mistral.ai/models/pixtral-12b-24-09) |
| Ministral 3 14B (ministral-3-14b-25-12) | Edge 14B multimodal [docs.mistral](https://docs.mistral.ai/models/ministral-3-14b-25-12) | 256k tokens [docs.mistral](https://docs.mistral.ai/models/ministral-3-14b-25-12) |
| Ministral 3 8B (ministral-3-8b-25-12) | Edge 8B multimodal [docs.mistral](https://docs.mistral.ai/models/ministral-3-8b-25-12) | 256k tokens [docs.mistral](https://docs.mistral.ai/models/ministral-3-8b-25-12) |
| Ministral 3 3B (ministral-3-3b-25-12) | Edge 3B multimodal [docs.mistral](https://docs.mistral.ai/models/ministral-3-3b-25-12) | 256k tokens [docs.mistral](https://docs.mistral.ai/models/ministral-3-3b-25-12) |
| Ministral 8B v24.1 (ministral-8b-24-1) | Edge 8B geração anterior [docs.mistral](https://docs.mistral.ai/models/ministral-8b-24-1) | 128k tokens [docs.mistral](https://docs.mistral.ai/models/ministral-8b-24-1) |
| Ministral 3B v24.1 (ministral-3b-24-1) | Edge 3B geração anterior [docs.mistral](https://docs.mistral.ai/models/ministral-3b-24-1) | 128k tokens [docs.mistral](https://docs.mistral.ai/models/ministral-3b-24-1) |

Esses modelos são os que aparecem hoje como “Large 3”, “Medium 3.x”, “Small 3.x” e família “Ministral” na página oficial de modelos e no índice de versões. [docs.mistral](https://docs.mistral.ai/getting-started/models)

## Modelos de raciocínio (Magistral, Devstral)

Modelos voltados a chain‑of‑thought e uso como “reasoning LLM”.

| Modelo | Foco | Contexto máximo |
|--------|------|-----------------|
| Magistral Medium 1.x (magistral-medium-2507/2509) | Raciocínio frontier, multimodal [docs.mistral](https://docs.mistral.ai/models/magistral-medium-1-1-25-07) | 128k tokens (configuração atual em provedores e HF) [github](https://github.com/RooCodeInc/Roo-Code/issues/8362) |
| Magistral Small 1.x (magistral-small-2507/2509) | Raciocínio small open‑weight [docs.mistral](https://docs.mistral.ai/models/magistral-small-1-2-25-09) | 128k tokens (model card fala em janela de 128k, com melhor qualidade até ~40k) [simonwillison](https://simonwillison.net/2025/Jun/10/magistral/) |
| Devstral Small 1.0 (devstral-small-2505) | Engenharia de software / agentes de código [docs.mistral](https://docs.mistral.ai/getting-started/models) | 128k tokens [docs.mistral](https://docs.mistral.ai/getting-started/models) |

(A documentação oficial de Magistral não expõe o número na ficha resumida, mas issues de SDKs e o model card oficial no Hugging Face indicam 128k como limite de contexto.) [github](https://github.com/RooCodeInc/Roo-Code/issues/8362)

## Modelos de código (Codestral)

| Modelo | Foco | Contexto máximo |
|--------|------|-----------------|
| Codestral 25.01 (codestral-2501) | LLM de código (24B) open‑weight [docs.mistral](https://docs.mistral.ai/getting-started/models) | 128k tokens (model card Mistral indica 128k; alguns artigos mencionam 256k, mas os parceiros de nuvem usam 128k) [docs.cloud.google](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/mistral) |
| Codestral 2 (codestral-2) | Código de última geração, via Vertex AI [docs.cloud.google](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/mistral) | 128k tokens de contexto; 128k máx de saída [docs.cloud.google](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/mistral) |
| Codestral Mamba 7B (open-codestral-mamba) | Código com arquitetura Mamba‑2 [docs.mistral](https://docs.mistral.ai/getting-started/models) | 256k tokens (tabela de pesos indica context size 256k) [docs.mistral](https://docs.mistral.ai/models/codestral-mamba-7b-0-1) |

Quando você usa esses modelos via Vertex AI, Azure, etc., o limite de contexto do provedor é 128k (Codestral/Codestral 2) ou 256k (Codestral Mamba), respeitando também limites de tokens por minuto. [docs.cloud.google](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/mistral)

## Modelos de visão, áudio, OCR e Document AI

| Modelo | Tipo | Limite de contexto |
|--------|------|--------------------|
| Pixtral 12B (pixtral-12b-2409) | Multimodal texto+imagem [docs.mistral](https://docs.mistral.ai/models/pixtral-12b-24-09) | 128k tokens [docs.mistral](https://docs.mistral.ai/models/pixtral-12b-24-09) |
| Voxtral Small (voxtral-small-25-07) | Áudio + texto (instruções com voz) [docs.mistral](https://docs.mistral.ai/models/voxtral-small-25-07) | 32k tokens no canal textual, preço por minuto de áudio [docs.mistral](https://docs.mistral.ai/models/voxtral-small-25-07) |
| Voxtral Mini Transcribe (voxtral-mini-… realtime/transcribe) | ASR (transcrição) em tempo real [docs.mistral](https://docs.mistral.ai/capabilities/audio_transcription/realtime_transcription) | Limite prático dado por duração do stream; docs não especificam contexto em tokens, apenas parâmetros de streaming [docs.mistral](https://docs.mistral.ai/capabilities/audio_transcription/realtime_transcription) |
| Mistral OCR 25.05 (mistral-ocr-2505) | OCR especializado (Vertex AI) [docs.cloud.google](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/mistral/mistral-ocr) | 30 páginas por requisição; cada página = 1M tokens de entrada + 1M de saída; “context length” = 30 páginas [docs.cloud.google](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/mistral/mistral-ocr) |
| Mistral Document AI 25xx (mistral-document-ai-25xx) | OCR + Document AI empresarial (Azure/Foundry) [ai.azure](https://ai.azure.com/catalog/models/mistral-document-ai-2505) | Limite expresso em páginas/MB nos provedores (por ex., 30 páginas por chamada no backend OCR subjacente); número exato de tokens não é publicado nas fichas da Mistral [docs.cloud.google](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/mistral/mistral-ocr) |
| Mistral Embed (mistral-embed) | Embeddings de texto [docs.mistral](https://docs.mistral.ai/api/endpoint/embeddings) | Docs mostram uso com textos curtos a médios, mas não especificam formalmente um teto de tokens por requisição; o limite efetivo depende do provedor [docs.mistral](https://docs.mistral.ai/api/endpoint/embeddings) |
| Mistral Moderation | Moderação de conteúdo [mistral](https://mistral.ai/models) | A Mistral não publica um contexto máximo numérico separado; usualmente herda a janela do modelo subjacente (Small/Medium), tipicamente até 128k tokens nas gerações mais recentes [mistral](https://mistral.ai/models) |

## Modelos legados e de pesquisa

Além dos modelos acima, o índice de modelos da Mistral lista versões mais antigas e/ou puramente de pesquisa, como Mathstral 7B, Mistral Saba, Mistral Next e variantes antigas de Codestral, que seguem, em geral, os mesmos padrões de contexto da geração em que foram lançados (por exemplo, Small/Medium/ Large antigos em 32k–128k, Mixtral 8x7B em 32k, Mixtral 8x22B em 64k). [promptingguide](https://www.promptingguide.ai/models/mixtral-8x22b)
Para vários desses modelos experimentais, a Mistral não publica uma ficha detalhando explicitamente o limite máximo de tokens; quando o valor não consta em model cards oficiais ou em documentos de parceiros (Vertex, Azure, AWS), eu omiti o número em vez de inferir.