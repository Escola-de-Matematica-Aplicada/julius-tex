# 🚀 NVIDIA Provider - Quick Start Guide

## O que foi feito?

O provider NVIDIA foi completamente integrado ao julius-tex com suporte para:
✅ Streaming de responses em tempo real
✅ Múltiplos modelos NVIDIA
✅ Gerenciamento automático de contexto
✅ Integração automática com a interface julius-tex

## Primeiros Passos

### 1. Obter sua API Key
1. Acesse https://build.nvidia.com/
2. Faça login (criar conta se necessário)
3. Gere uma nova API key nas configurações

### 2. Configurar no julius-tex
Adicione sua API key ao arquivo `TOKENS`:

```bash
# Abra/crie o arquivo TOKENS na raiz do projeto
NVIDIA_API_KEY=sua_chave_de_api_aqui

# Opcional: escolher um modelo específico
# NVIDIA_MODEL=z-ai/glm4.7
```

### 3. Pronto para usar!
```bash
# Simplesmente execute julius-tex normalmente
python -m julius_tex
```

O provider NVIDIA aparecerá automaticamente na lista de providers disponíveis.

## Comandos Úteis dentro do julius-tex

```
/providers    - Ver lista de providers e selecionar NVIDIA
/models       - Ver modelos disponíveis e trocar de modelo
/provider     - Ver qual provider está ativo
```

## Arquivos Principais Criados/Modificados

| Arquivo | O que mudou |
|---------|-----------|
| `julius_tex/providers/openai_compat.py` | Adicionado `NvidiaProvider` |
| `julius_tex/providers/__init__.py` | Registrado provider NVIDIA |
| `julius_tex/providers/nvidia_max_tokens.md` | Nova: lista de modelos |
| `TOKENS.example` | Adicionado `NVIDIA_API_KEY` |
| `NVIDIA_SETUP.md` | Nova: documentação detalhada |
| `tests/test_nvidia_provider.py` | Novo: testes do provider |

## Modelos Disponíveis

Por padrão, o modelo `z-ai/glm4.7` é usado (com suporte para 200k tokens!).

Outros modelos disponíveis:
- `nvidia/llama-3.1-nemotron-70b-instruct`
- `nvidia/mixtral-8x7b-instruct-v01`
- `nvidia/mistral-large`
- `nvidia/llama2-70b`

## Troubleshooting

**"No AI provider is configured"**
- Verifique se `NVIDIA_API_KEY` está no arquivo `TOKENS`
- Certifique-se de que não começa com `your_` (placeholder)

**"Model not found"**
- Confirme o nome do modelo
- Os modelos disponíveis estão em `julius_tex/providers/nvidia_max_tokens.md`

**"Connection refused"**
- Verifique sua conexão com a internet
- A API NVIDIA pode estar temporariamente indisponível

## Documentação Completa

Para mais detalhes, consulte:
- `NVIDIA_SETUP.md` - Guia de configuração detalhado
- `NVIDIA_INTEGRATION.md` - Resumo técnico da integração

---

**Pronto para começar!** 🎉

Sua integração NVIDIA está 100% funcional. Apenas configure sua API key e comece a usar!
