O `grok-4.20-multi-agent-beta-0309` (ou simplesmente `grok-4.20-multi-agent`) é uma variante do Grok 4.20 da xAI que orquestra múltiplos agentes de IA em paralelo para resolver tarefas complexas de pesquisa e análise. A principal vantagem é a **validação cruzada entre agentes**, que reduz drasticamente a taxa de alucinação — de ~12% para ~4,2% comparado a modelos de agente único. [help.apiyi](https://help.apiyi.com/pt-pt/grok-4-20-beta-4-models-multi-agent-reasoning-api-guide-pt-pt.html)

## Arquitetura "Society of Mind"

O modelo lança um grupo de agentes que colaboram simultaneamente na sua query. Um **agente líder (Captain)** decompõe o problema, distribui subtarefas aos sub-agentes, arbitra divergências e sintetiza a resposta final. Apenas a saída do líder é retornada; o estado interno dos sub-agentes fica encriptado (acessível via `use_encrypted_content=True` no SDK se precisar de contexto multi-turn) . [codigosintetico.com](https://codigosintetico.com.br/posts/grok-4-20-sistema-multi-agente-xai)

Você pode configurar **4 agentes** (para queries focadas) ou **16 agentes** (para pesquisa profunda e multi-facetada) .

## Quando Usar

- Pesquisa acadêmica ou técnica com múltiplas fontes
- Análise de trade-offs complexos (ex: arquiteturas de sistemas, comparações de tecnologias)
- Automação de fluxos de trabalho multi-etapa
- Qualquer tarefa que exija perspectivas diversas e validação cruzada [cometapi](https://www.cometapi.com/pt/grok-4-2-feature-performance-benchmark-and-access/)

**Não use** para tarefas simples ou processamento em lote — prefira `grok-4.20-beta` (rápido e barato) ou `grok-4.20-beta-0309-non-reasoning` (baixa latência) nesses casos. [help.apiyi](https://help.apiyi.com/pt-pt/grok-4-20-beta-4-models-multi-agent-reasoning-api-guide-pt-pt.html)

## Como Usar via API

O modelo **não é compatível com o Chat Completions API** do OpenAI — use o **xAI SDK** ou o **Responses API** .

### Com xAI SDK (recomendado)

```python
import os
from xai_sdk import Client
from xai_sdk.chat import user
from xai_sdk.tools import web_search, x_search

client = Client(api_key=os.getenv("XAI_API_KEY"))

chat = client.chat.create(
    model="grok-4.20-multi-agent",
    agent_count=4,          # ou 16 para pesquisa profunda
    tools=[web_search(), x_search()],
    include=["verbose_streaming"],
)

chat.append(user("Compare as abordagens de consenso distribuído: Paxos, Raft e BFT."))

for response, chunk in chat.stream():
    if chunk.content:
        print(chunk.content, end="", flush=True)
```

### Com OpenAI SDK (via Responses API)

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),
    base_url="https://api.x.ai/v1",
)

response = client.responses.create(
    model="grok-4.20-multi-agent",
    reasoning={"effort": "high"},   # "low"/"medium" = 4 agentes | "high"/"xhigh" = 16
    input=[{"role": "user", "content": "Analise os trade-offs entre OLAP e OLTP..."}],
    tools=[{"type": "web_search"}, {"type": "x_search"}],
)
print(response.output_text)
```

## Configuração de Agentes

| SDK | Parâmetro | 4 Agentes | 16 Agentes |
|---|---|---|---|
| xAI SDK | `agent_count` | `4` | `16` |
| OpenAI SDK | `reasoning.effort` | `"low"` ou `"medium"` | `"high"` ou `"xhigh"` |
| REST API | `reasoning.effort` | `"low"` ou `"medium"` | `"high"` ou `"xhigh"` |


## Ferramentas Built-in Suportadas

As ferramentas nativas disponíveis são `web_search`, `x_search`, `code_execution` e `collections_search` . **Client-side tools (function calling) ainda não são suportados** nessa variante — apenas ferramentas built-in e MCP remotos são compatíveis .

## Pontos de Atenção

- **Custo elevado:** todos os tokens dos sub-agentes (input, output, reasoning) são cobrados, além das chamadas de ferramentas feitas por cada agente em paralelo 
- **`max_tokens` não é suportado** nesta variante 
- Ainda está em **beta** — a interface da API pode mudar 
- Para contexto em conversas multi-turn, passe `previous_response_id` da resposta anterior 

Dado o seu perfil com RAG, LangChain e integração de múltiplos provedores, esse modelo pode ser especialmente útil para tarefas de pesquisa profunda em pipelines onde a qualidade factual é crítica — vale testar no contexto de data governance ou análise de literatura acadêmica para seus projetos na FGV.