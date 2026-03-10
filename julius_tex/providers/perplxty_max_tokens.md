6/3/2026

Hoje a Perplexity não publica um limite de tokens diferente por modelo: a FAQ técnica diz explicitamente que **todos os modelos na plataforma usam janelas de contexto de cerca de 32 000 tokens**, independentemente de serem GPT, Claude, Sonar, etc. [perplexity](https://www.perplexity.ai/help-center/es/articles/10354919-que-modelos-de-lenguaje-avanzados-vienen-incluidos-en-la-subscripcion-de-perplexity-pro)

Ou seja, para fins práticos, dentro do Perplexity você pode assumir \( \text{prompt} + \text{resposta} \approx 32k \) tokens para todos os modelos disponíveis (o que é bem abaixo do máximo teórico de alguns modelos na API nativa, mas padronizado pela própria Perplexity). [perplexity](https://www.perplexity.ai/de/hub/technical-faq/what-advanced-ai-models-does-perplexity-pro-unlock)

## Como a Perplexity organiza os modelos

A Perplexity expõe modelos em dois níveis: [perplexity](https://www.perplexity.ai/help-center/en/articles/10354919-what-advanced-ai-models-are-included-in-my-subscription)

- Um **modelo padrão / Best mode**, otimizado e afinado pela Perplexity para busca rápida e navegação na web.  
- Uma lista de **modelos avançados**, que você escolhe no seletor de modelo (Pro Search, Reasoning Search/Reasoning mode, Research/Labs), todos com *“context windows of around 32 000 tokens”* segundo a documentação em vários idiomas. [perplexity](https://www.perplexity.ai/help-center/fr/articles/10354919-quels-sont-les-modeles-d-ia-avances-inclus-dans-un-abonnement-perplexity-pro)

## Modelos próprios da Perplexity

| Modelo na UI | Base / fornecedor | Contexto máximo dentro da Perplexity |
|--------------|-------------------|---------------------------------------|
| Default / Standard model | Modelo próprio, ajustado para buscas rápidas e web browsing. [perplexity](https://www.perplexity.ai/help-center/en/articles/10354930-what-is-perplexity-s-default-language-model-and-how-does-it-compare-to-pro-options) | ~32k tokens (mesmo limite informado para todos os modelos avançados). [perplexity](https://www.perplexity.ai/help-center/es/articles/10354919-que-modelos-de-lenguaje-avanzados-vienen-incluidos-en-la-subscripcion-de-perplexity-pro) |
| Best mode | “Meta‑modo” que escolhe automaticamente o modelo mais adequado para a consulta (pode ser Sonar, GPT, Claude etc.). [perplexity](https://www.perplexity.ai/help-center/en/articles/10354919-what-advanced-ai-models-are-included-in-a-perplexity-pro-subscription) | Efetivamente ~32k tokens, herdando o limite do modelo selecionado. [perplexity](https://www.perplexity.ai/help-center/es/articles/10354919-que-modelos-de-lenguaje-avanzados-vienen-incluidos-en-la-subscripcion-de-perplexity-pro) |
| Sonar / Sonar Large / Sonar 32k | Modelo interno baseado em Llama 3.1 70B, fine‑tuned pela Perplexity para search em tempo real. [perplexity](https://www.perplexity.ai/help-center/en/articles/10354919-what-advanced-ai-models-are-included-in-a-perplexity-pro-subscription) | ~32k tokens (o próprio nome “Sonar 32k” na doc antiga reforça esse limite, e a FAQ diz que todos os modelos usam ~32k). [perplexity](https://www.perplexity.ai/de/hub/technical-faq/what-advanced-ai-models-does-perplexity-pro-unlock) |

## Modelos OpenAI disponíveis na Perplexity

| Modelo na UI | Descrição na doc da Perplexity | Contexto máximo dentro da Perplexity |
|--------------|--------------------------------|---------------------------------------|
| GPT‑5 / GPT‑5.2 | “OpenAI’s most advanced model”, foco em reasoning, coding e criatividade. [perplexity](https://www.perplexity.ai/help-center/en/articles/10354919-what-advanced-ai-models-are-included-in-a-perplexity-pro-subscription) | ~32k tokens na Perplexity (a FAQ em ES/FR/DE diz que todos os modelos do Pro usam janelas ≈32k). [perplexity](https://www.perplexity.ai/help-center/es/articles/10354919-que-modelos-de-lenguaje-avanzados-vienen-incluidos-en-la-subscripcion-de-perplexity-pro) |
| o3‑pro | Modelo de *reasoning* mais poderoso da série “o”, disponível para assinantes Max. [perplexity](https://www.perplexity.ai/help-center/en/articles/10354919-what-advanced-ai-models-are-included-in-a-perplexity-pro-subscription) | ~32k tokens na Perplexity (mesmo limite geral). [perplexity](https://www.perplexity.ai/help-center/es/articles/10354919-que-modelos-de-lenguaje-avanzados-vienen-incluidos-en-la-subscripcion-de-perplexity-pro) |
| GPT‑4 Turbo / GPT‑4o (menções em docs mais antigas) | Geração anterior multimodal/textual da OpenAI, ainda citada na FAQ técnica. [perplexity](https://www.perplexity.ai/de/hub/technical-faq/what-advanced-ai-models-does-perplexity-pro-unlock) | ~32k tokens (explicitamente dito que “Alle Kontextfenster von etwa 32k Tokens sind für unsere Modelle gleich”). [perplexity](https://www.perplexity.ai/de/hub/technical-faq/what-advanced-ai-models-does-perplexity-pro-unlock) |

## Modelos Anthropic (Claude) na Perplexity

| Modelo na UI | Descrição | Contexto máximo dentro da Perplexity |
|--------------|-----------|---------------------------------------|
| Claude Sonnet 4.5 / 4.6 | Modelo “equilíbrio” da Anthropic, forte em coding e reasoning. [perplexity](https://www.perplexity.ai/help-center/en/articles/10354919-what-advanced-ai-models-are-included-in-a-perplexity-pro-subscription) | ~32k tokens na Perplexity. [perplexity](https://www.perplexity.ai/help-center/es/articles/10354919-que-modelos-de-lenguaje-avanzados-vienen-incluidos-en-la-subscripcion-de-perplexity-pro) |
| Claude Sonnet 4.5 / 4.6 Thinking | Variante com *reasoning* intensivo, voltada a tarefas complexas. [perplexity](https://www.perplexity.ai/help-center/en/articles/10354919-what-advanced-ai-models-are-included-in-a-perplexity-pro-subscription) | ~32k tokens na Perplexity. [perplexity](https://www.perplexity.ai/help-center/es/articles/10354919-que-modelos-de-lenguaje-avanzados-vienen-incluidos-en-la-subscripcion-de-perplexity-pro) |
| Claude 4.1 / 4.6 Opus (Thinking) | Flagship da Anthropic, disponível só para Max em modo reasoning. [perplexity](https://www.perplexity.ai/help-center/en/articles/10354919-what-advanced-ai-models-are-included-in-a-perplexity-pro-subscription) | ~32k tokens na Perplexity. [perplexity](https://www.perplexity.ai/help-center/es/articles/10354919-que-modelos-de-lenguaje-avanzados-vienen-incluidos-en-la-subscripcion-de-perplexity-pro) |
| Claude 3 Sonnet / Opus (geraç. anterior, citados em FAQ antigas) | Versões anteriores de Claude 3. [perplexity](https://www.perplexity.ai/de/hub/technical-faq/what-advanced-ai-models-does-perplexity-pro-unlock) | ~32k tokens (mesma regra geral). [perplexity](https://www.perplexity.ai/de/hub/technical-faq/what-advanced-ai-models-does-perplexity-pro-unlock) |

## Modelos Google (Gemini) na Perplexity

| Modelo na UI | Descrição | Contexto máximo dentro da Perplexity |
|--------------|-----------|---------------------------------------|
| Gemini 3.1 Pro | Modelo multimodal mais recente usado em Pro Search. [perplexity](https://www.perplexity.ai/help-center/en/articles/10354919-what-advanced-ai-models-are-included-in-my-subscription) | ~32k tokens na Perplexity. [perplexity](https://www.perplexity.ai/help-center/es/articles/10354919-que-modelos-de-lenguaje-avanzados-vienen-incluidos-en-la-subscripcion-de-perplexity-pro) |
| Gemini 2.5 Pro | Versão anterior citada na doc de modelos avançados. [perplexity](https://www.perplexity.ai/help-center/en/articles/10354919-what-advanced-ai-models-are-included-in-a-perplexity-pro-subscription) | ~32k tokens na Perplexity. [perplexity](https://www.perplexity.ai/help-center/es/articles/10354919-que-modelos-de-lenguaje-avanzados-vienen-incluidos-en-la-subscripcion-de-perplexity-pro) |

## Modelos xAI, Kimi e outros parceiros

| Modelo na UI | Fornecedor | Contexto máximo dentro da Perplexity |
|--------------|-----------|---------------------------------------|
| Grok 4 / Grok 4.1 | xAI; modelo de reasoning e conhecimento atualizado em tempo real, texto e imagens. [perplexity](https://www.perplexity.ai/help-center/en/articles/10354919-what-advanced-ai-models-are-included-in-a-perplexity-pro-subscription) | ~32k tokens na Perplexity. [perplexity](https://www.perplexity.ai/help-center/es/articles/10354919-que-modelos-de-lenguaje-avanzados-vienen-incluidos-en-la-subscripcion-de-perplexity-pro) |
| Kimi K2.5 Thinking | Kimi (Moonshot AI), focado em “privacy‑first, logic‑driven problem solving”. [perplexity](https://www.perplexity.ai/help-center/en/articles/10354919-what-advanced-ai-models-are-included-in-my-subscription) | ~32k tokens na Perplexity (segue a mesma política de contexto). [perplexity](https://www.perplexity.ai/help-center/es/articles/10354919-que-modelos-de-lenguaje-avanzados-vienen-incluidos-en-la-subscripcion-de-perplexity-pro) |

## Ponto importante para engenharia de prompts / RAG

- A documentação da Perplexity deixa claro que **ela padroniza o contexto por razões operacionais**, ainda que os modelos “puros” de cada provedor suportem janelas maiores nas APIs originais. [perplexity](https://www.perplexity.ai/hub/legal/third-party-models)
- Para uso dentro da UI do Perplexity (Search, Pro Search, Research, Labs), o que vale é esse teto ≈32k tokens por consulta; se você quiser explorar contextos maiores (p.ex. 128k+ do GPT‑5 na API da OpenAI ou 200k+ do Claude 4.x), precisa ir direto na API do provedor ou em outra plataforma que exponha o limite completo.