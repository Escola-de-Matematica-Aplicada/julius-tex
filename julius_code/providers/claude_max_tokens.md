6/3/2026

Os modelos Claude atuais (linha 4.x, 3.x e 2.x) usam **janela padrão de 200 000 tokens (input + output)**, com extensões para **500 000** e até **1 000 000 tokens** em tiers avançados / beta para alguns modelos específicos. [platform.claude](https://platform.claude.com/docs/en/build-with-claude/context-windows)

Abaixo organizei por geração, como você pediu antes.

***

## Como a Anthropic define “context window”

A Anthropic define contexto como **todos os tokens no turno**: histórico da conversa, system prompt, ferramentas, anexos e a resposta gerada; tudo deve caber no limite de tokens da janela. [datastudios](https://www.datastudios.org/post/claude-ai-context-window-token-limits-and-memory-operational-boundaries-and-long-context-behavior)
Na documentação da plataforma consta que o limite padrão hoje é **200 000 tokens** para os modelos mais usados, com opções de contexto estendido (500k/1M) em planos Enterprise ou betas específicos. [aws.amazon](https://aws.amazon.com/bedrock/anthropic/)

***

## Claude 4.x (linha mais recente)

| Modelo | Notas | Contexto máximo |
|--------|-------|-----------------|
| **Claude Opus 4.6** | Flagship atual (razonamento máximo). [anthropic](https://www.anthropic.com/news/claude-opus-4-6) | **Padrão: 200k tokens**. [platform.claude](https://platform.claude.com/docs/en/build-with-claude/context-windows) **Beta: 1M tokens** em organizações com tier alto + header `anthropic-beta: context-1m-2025-08-07`. [platform.claude](https://platform.claude.com/docs/en/build-with-claude/context-windows) |
| **Claude Sonnet 4.6** | Modelo “equilíbrio” mais novo (velocidade × qualidade). [platform.claude](https://platform.claude.com/docs/en/about-claude/models/overview) | **Padrão: 200k tokens**; **1M tokens** em beta, mesma condição do Opus 4.6. [platform.claude](https://platform.claude.com/docs/en/build-with-claude/context-windows) |
| **Claude Sonnet 4.5** | Sonnet de geração anterior, ainda amplamente suportado. [platform.claude](https://platform.claude.com/docs/en/build-with-claude/context-windows) | **200k tokens** por padrão; suporte a **1M tokens** de contexto em beta/preview, inclusive citado em docs e AWS Bedrock. [platform.claude](https://platform.claude.com/docs/en/build-with-claude/context-windows) |
| **Claude Sonnet 4** | Sonnet 4 “base” (muito usado em apps e API). [platform.claude](https://platform.claude.com/docs/en/about-claude/models/overview) | **200k tokens** padrão; até **500k tokens** em Claude Enterprise; e **1M tokens** em preview em alguns ambientes (Bedrock/tiers avançados). [datastudios](https://www.datastudios.org/post/claude-context-window-token-limits-memory-policy-and-2025-rules) |
| **Claude Haiku 4.5** | Modelo pequeno/rápido mais novo, com “context awareness”. [platform.claude](https://platform.claude.com/docs/en/build-with-claude/context-windows) | **200k tokens** de contexto; não há ainda 1M oficial para Haiku 4.5, apenas os 200k padrão. [platform.claude](https://platform.claude.com/docs/en/build-with-claude/context-windows) |

***

## Claude 3.7 / 3.5 (linha “3.x” mais recente)

| Modelo | Notas | Contexto máximo |
|--------|-------|-----------------|
| **Claude Sonnet 3.7** | Sonnet com melhorias em ferramentas e “extended thinking”. | A documentação e artigos técnicos apontam **200k tokens** como janela padrão (mesmo patamar de 3.5). [datastudios](https://www.datastudios.org/post/claude-ai-context-window-token-limits-and-memory-operational-boundaries-and-long-context-behavior) |
| **Claude 3.5 Sonnet** | Modelo 3.5 principal (app/API, coding e RAG). [oreateai](https://www.oreateai.com/blog/unpacking-claude-35-sonnets-200k-token-context-window-what-it-means-for-you/735b365ddd6ca921438246190850e246) | **200k tokens** de contexto. [datastudios](https://www.datastudios.org/post/claude-ai-context-window-token-limits-and-memory-operational-boundaries-and-long-context-behavior) |
| **Claude 3.5 Haiku / Opus** (quando citados) | Variações 3.5 menores/maiores em alguns provedores. | Mesma família de **200k tokens**; docs e posts sobre 3.5 falam sempre em 200k como contexto “full”. [datastudios](https://www.datastudios.org/post/claude-ai-context-window-token-limits-and-memory-operational-boundaries-and-long-context-behavior) |

A doc de “Context windows” diz explicitamente que a **janela total disponível é de 200 000 tokens** para esses modelos, e que modelos a partir do Sonnet 3.7 passam a validar estritamente esse limite (erro se ultrapassar, em vez de truncar silenciosamente). [platform.claude](https://platform.claude.com/docs/en/build-with-claude/context-windows)

***

## Claude 3 (Opus, Sonnet, Haiku)

| Modelo | Notas | Contexto máximo |
|--------|-------|-----------------|
| **Claude 3 Opus** | Modelo topo de linha da geração 3. [anthropic](https://www.anthropic.com/news/claude-3-family) | **200k tokens** padrão; suporte a **1M tokens** para alguns clientes/tiers, segundo model card e guias externos. [platform.claude](https://platform.claude.com/docs/en/build-with-claude/context-windows) |
| **Claude 3 Sonnet** | Modelo intermediário 3. [anthropic](https://www.anthropic.com/news/claude-3-family) | **200k tokens** (docs e guias citam 200k; em algumas integrações há opção 1M para clientes selecionados). [encord](https://encord.com/blog/claude-3-explained/) |
| **Claude 3 Haiku** | Modelo pequeno/rápido. [anthropic](https://www.anthropic.com/news/claude-3-family) | **200k tokens** de contexto; não há 1M público como no Opus/Sonnet. [encord](https://encord.com/blog/claude-3-explained/) |

***

## Claude 2.x (2.1, 2.0) e Instant

| Modelo | Notas | Contexto máximo |
|--------|-------|-----------------|
| **Claude 2.1** | 2.x mais recente, com melhorias de confiança e ferramentas. [claude](https://claude.com/blog/claude-2-1-prompting) | **200k tokens** (artigo oficial “Long context prompting for Claude 2.1” reforça esse valor várias vezes). [claude](https://claude.com/blog/claude-2-1-prompting) |
| **Claude 2.0 / Claude 2** | Versão anterior com long‑context. [searchenginejournal](https://www.searchenginejournal.com/anthropic-launches-claude-2-with-100k-context-windows-file-uploads/491412/) | Model card indica **200k tokens** de contexto para Claude 2 (2.0). [anthropic](https://www.anthropic.com/claude-2-model-card) |
| **Claude Instant 1.2** | Modelo leve/rápido. [docsbot](https://docsbot.ai/models/claude-instant-1-2) | **100k tokens** de contexto (tanto em model listings de terceiros quanto em posts sobre “100k context window”). [docsbot](https://docsbot.ai/models/claude-instant-1-2) |

***

## Claude 1.x e primeiros long‑context

Antes de 2.x, o “Claude clássico” passou por dois patamares de contexto: [anthropic](https://www.anthropic.com/news/100k-context-windows)

| Modelo / era | Contexto máximo |
|--------------|-----------------|
| **Claude v1 inicial** | ~**9k tokens** de contexto. [anthropic](https://www.anthropic.com/news/100k-context-windows) |
| **Claude v1 com 100k** (inclui Instant v1/v1.1) | Atualização para **100k tokens** (post “Introducing 100K Context Windows”). [anthropic](https://www.anthropic.com/news/100k-context-windows?continueFlag=b1f3d285ec55b445f56f508334b2d067) |

***

## Resumo prático (para engenharia de contexto)

- Para **qualquer Claude “moderno” (2.x, 3.x, 4.x)**, você pode assumir **200k tokens (input + output)** como janela “normal” de API/app. [support.claude](https://support.claude.com/en/articles/8606394-how-large-is-the-context-window-on-paid-claude-plans)
- **Extensões maiores**:  
  - **500k tokens** em **Claude Enterprise** com Sonnet 4. [datastudios](https://www.datastudios.org/post/claude-context-window-token-limits-memory-policy-and-2025-rules)
  - **1M tokens** em beta/preview para **Opus 4.6, Sonnet 4.6, Sonnet 4.5 e Sonnet 4**, mediante header beta e tier alto. [anthropic](https://www.anthropic.com/news/claude-opus-4-6)
  - Alguns clientes enterprise também relatam **1M** em certas configurações de Claude 3 (especialmente Opus), mas isso aparece mais em materiais de parceiros do que em doc pública padrão. [www-cdn.anthropic](https://www-cdn.anthropic.com/de8ba9b01c9ab7cbabf5c33b80b7bbc618857627/Model_Card_Claude_3.pdf)

Se quiser, posso te montar uma tabela “one‑pager” com: modelo, contexto, limite de saída, preço relativo (por 1M tokens) e caso de uso típico — focada nas versões que você de fato consegue chamar hoje via API.