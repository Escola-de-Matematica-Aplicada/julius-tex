6/6/2026


Os limites de tokens (principalmente o context window, que é o máximo de tokens que o modelo aceita no prompt + histórico + imagens, etc.) para os modelos do Grok via API da xAI variam por modelo. A documentação oficial (docs.x.ai) lista os valores atuais em março de 2026.
Aqui está a lista principal dos modelos disponíveis via API e seus limites de contexto (context window em tokens):
	•	grok-4-1-fast-reasoning e grok-4-1-fast-non-reasoning → 2.000.000 tokens (2 milhões) → Um dos maiores disponíveis atualmente, otimizado para tarefas agentic e longas.

2.000.000

	•	grok-4-fast-reasoning e grok-4-fast-non-reasoning → 2.000.000 tokens
	•	grok-code-fast-1 → 256.000 tokens
	•	grok-4-0709 (também conhecido como grok-4 ou grok-4-latest) → 256.000 tokens → Nota: Preços mudam para contextos > 128K (cobrança “extended context”).
	•	grok-3 e grok-3-mini → 131.072 tokens (≈ 128K)
Outros detalhes importantes sobre limites de tokens
	•	O context window é o limite total para input (prompt + histórico + ferramentas + imagens).
	◦	Imagens consomem entre 256 a 1.792 tokens cada, dependendo do tamanho.
	◦	O total (texto + imagens) não pode exceder o context window do modelo.
	•	Output tokens (resposta gerada): Geralmente não tem limite fixo separado divulgado, mas na prática é limitado pelo context window restante (input + output ≤ context window). Alguns modelos antigos tinham caps explícitos (ex.: max_tokens em chamadas), mas a xAI foca no context total.
	•	Rate limits relacionados a tokens (TPM = tokens per minute):
	◦	Modelos fast (2M context): até 4.000.000 TPM (tokens por minuto).
	◦	Modelos como grok-4-0709: 2.000.000 TPM.
	◦	Isso é limite de throughput, não o context por chamada.
	•	Reasoning tokens (pensamento interno em modelos reasoning): São cobrados como output tokens, mas não contam no input context.
	•	Para ver os limites exatos do seu time/conta (pois podem variar por tier ou early access), acesse o xAI Console → Models Page (https://console.x.ai/team/default/models).
Exemplos de uso no código (Python com openai sdk compatível)
from openai import OpenAI

client = OpenAI(
    api_key="sua-chave-xai",
    base_url="https://api.x.ai/v1"  # ou o endpoint atual
)

response = client.chat.completions.create(
    model="grok-4-1-fast-reasoning",  # ou outro da lista
    messages=[{"role": "user", "content": "Seu prompt longo aqui..."}],
    max_tokens=8192  # você pode limitar o output se quiser, mas o context é 2M
)
Os modelos mais recentes (Grok 4.1 Fast family) chegam a 2 milhões de tokens, o que é excelente para RAG, análise de documentos longos ou agentes com muita memória. Modelos mais antigos como Grok 3 ficam em torno de 128K-131K.
Se você tiver acesso a um modelo específico ou quiser confirmar o pricing/extended context para o seu uso, me diga mais detalhes! A fonte principal é https://docs.x.ai/docs/models (atualizada em tempo real).

