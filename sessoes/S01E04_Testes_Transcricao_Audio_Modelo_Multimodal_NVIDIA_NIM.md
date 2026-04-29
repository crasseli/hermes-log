# Testes de Transcrição de Áudio: STT Dedicado vs Modelo Multimodal via NVIDIA NIM

**Sessão:** S01E04
**Autores:** Christian Rasseli, Cohen (agente no M70q), Hermes (agente no notebook DELL)
**Data:** 2026-04-29
**Tipo:** Experimento / Análise comparativa

---

## Resumo do Experimento

Um agente Hermes (Cohen) testou a capacidade de transcrição de áudio de um modelo multimodal servido via API NVIDIA NIM, comparando-o com um STT dedicado (Whisper via provedor de inferência rápida). O áudio de teste continha ~34 segundos de fala em português brasileiro com termos técnicos (acrônimos, nomes de serviços). O resultado foi contundente: o STT dedicado entregou precisão de 95%+ com apenas 1 erro de 1 letra, enquanto o modelo multimodal alcançou ~60% de precisão palavra-por-palavra, com parafraseamento, substituição de acrônimos e alucinações. O teste também revelou que o modo thinking/reasoning do modelo multimodal interage de forma problemática com entrada de áudio, degradando ainda mais a transcrição literal.

---

## Metodologia

### Áudio de teste

- **Duração:** ~34 segundos
- **Idioma:** Português brasileiro
- **Conteúdo:** Enunciado contendo termos técnicos (acrônimo "DIA", nome de serviço "NVIDIA NIM", termo "stand-alone", expressão "Free Endpoints")
- **Formato de entrega:** Mensagem de voz nativa do Telegram (OGG), convertida para WAV

### Modelos testados

1. **STT dedicado (Whisper):** Modelo Whisper large-v3-turbo via provedor de inferência rápida, com timestamps por segmento
2. **Modelo multimodal (thinking=ON):** Modelo multimodal via API NVIDIA NIM com `enable_thinking: true` e `temperature: 0.6`
3. **Modelo multimodal (thinking=OFF):** Mesmo modelo com `enable_thinking: false`

### Fluxo de processamento

1. Áudio recebido como mensagem de voz Telegram (formato OGG)
2. Conversão OGG → WAV via ffmpeg
3. Codificação do WAV em base64 para envio à API
4. Chamada à API NVIDIA NIM com input_audio (formato OpenAI-compatible)
5. Chamada ao Whisper via provedor dedicado para comparação

---

## A Interação entre Thinking Mode e Entrada de Áudio

**Descoberta importante:** Embora o modelo multimodal suporte processamento de áudio com o modo thinking ativado, testes práticos mostraram que habilitar `enable_thinking: true` causa uma degradação significativa na qualidade da transcrição literal. O modelo deixa de atuar como um ASR (Automatic Speech Recognition) preciso e passa a priorizar compreensão e interpretação semântica, resultando em:

- **Parafraseamento:** O modelo reescreve o conteúdo com suas próprias palavras em vez de transcrever fielmente
- **Substituição de acrônimos:** Termos como "DIA" são interpretados como "de IA" -- o modelo "entende" o significado e substitui
- **Alucinações:** O modelo inventa palavras e termos que não existem no áudio original

Esta limitação comportamental ocorre porque, ao ativar o modo thinking, o modelo prioriza o raciocínio semântico e a compreensão contextual em detrimento da transcrição literal palavra-por-palavra. Embora o modelo suporte entrada de áudio, o reasoning altera significativamente seu comportamento, fazendo-o atuar mais como um interpretador do que como um ASR tradicional. A documentação oficial indica que o uso otimizado de reasoning é mais previsível em texto e imagem, apresentando dinâmicas distintas quando combinado com áudio.

Apenas com thinking desativado o modelo entrega transcrições mais literais -- ainda assim significativamente inferior ao Whisper dedicado.

---

## Resultados Comparativos

### O que o operador humano realmente disse

> "Esse é apenas um áudio de teste. Objetivo de teste. Desenvolver um agente DIA pessoal autônomo completamente portátil, executável stand-alone, que opera exclusivamente via chamadas de API, aos serviços NVIDIA NIM, Free Endpoints, sem dependências de instalação no sistema host. Fim do teste."

### Transcrição do Whisper (STT dedicado)

| Trecho original | Transcrição Whisper | Status |
|----------------|---------------------|--------|
| "Esse é apenas um áudio de teste" | ✅ Correto | Acerto |
| "Objetivo de teste" | ✅ Correto | Acerto |
| "agente DIA pessoal autônomo" | "agente DIA pessoal autônomo" | ✅ Acerto -- preservou o acrônimo |
| "NVIDIA NIM" | "NVIDIA **NIN**" | ⚠️ 1 erro: NIM → NIN (1 letra) |
| "Free Endpoints" | ✅ Correto | Acerto |
| "Fim do teste" | ✅ Correto | Acerto |

**Precisão: 95%+** — Único deslize foi "NIN" em vez de "NIM" (1 letra de diferença). Tempo: ~1s com 8 segmentos e timestamps.

### Transcrição do Modelo Multimodal (thinking=OFF)

| Trecho original | Transcrição Multimodal | Status |
|----------------|------------------------|--------|
| "Esse é apenas um áudio de teste" | "Esse é apenas um áudio de teste" | ✅ Acerto |
| "Objetivo de teste" | "Objetivo de teste" | ✅ Acerto |
| "agente DIA pessoal autônomo" | "agente **de IA**, pessoal, **autonomo**" | ❌ Substituição de acrônimo: DIA → "de IA" + perdeu acento em "autônomo" |
| "completamente portátil, executável stand-alone" | "completamente portátil, executável standalone" | ⚠️ Perdeu o hífen de "stand-alone" |
| "que opera exclusivamente via chamadas de API" | ✅ Correto | Acerto |
| "aos serviços NVIDIA NIM" | "serviços **em vídeo**, **ní**" | ❌ Alucinação: inventou "vídeo", distorceu "NIM" para "ní" |
| "Free Endpoints" | "free endpoints" | ⚠️ Perdeu maiúsculas |
| "sem dependências de instalação no sistema host" | ✅ Correto | Acerto |
| "Fim do teste" | "**Finto** teste" | ❌ Alucinação: inventou palavra que não existe |

**Precisão: ~60%** — O modelo capturou a estrutura geral mas reinterpretou acrônimos e alucinou termos. Tempo: ~3s.

### Transcrição do Modelo Multimodal (thinking=ON)

Com thinking ativado, o resultado foi ainda mais semântico e menos literal. O modelo priorizou o raciocínio sobre o conteúdo e reescreveu extensivamente, perdendo completamente a fidelidade palavra-por-palavra.

| Trecho original | Transcrição Multimodal (thinking=ON) | Status |
|----------------|--------------------------------------|--------|
| "Esse é apenas um áudio de teste" | "Este é um áudio de teste" | ⚠️ Parafraseamento: "Esse é apenas" → "Este é" |
| "Objetivo de teste" | *(omitido)* | ❌ O modelo pulou inteiramente esta frase |
| "agente DIA pessoal autônomo" | "agente **de IA** pessoal **e autônomo**" | ❌ Substituição de acrônimo: DIA → "de IA" + inserção de "e" que não existe |
| "completamente portátil" | "totalmente portátil" | ⚠️ Parafraseamento: "completamente" → "totalmente" |
| "executável stand-alone" | "executável de forma autônoma" | ❌ Parafraseamento: "stand-alone" → "de forma autônoma" (perdeu o termo técnico) |
| "que opera exclusivamente via chamadas de API" | "que opera **através de** chamadas de API" | ⚠️ Parafraseamento: "exclusivamente via" → "através de" (perdeu a exclusividade) |
| "aos serviços NVIDIA NIM" | "aos serviços **da NVIDIA NIM**" | ⚠️ Inserção de preposição desnecessária |
| "Free Endpoints" | "free **endpoints**" | ⚠️ Perdeu maiúsculas |
| "sem dependências de instalação no sistema host" | "sem **a necessidade de** dependências de instalação no sistema **hospedeiro**" | ❌ Parafraseamento: "sem dependências" → "sem a necessidade de dependências" + "host" → "hospedeiro" |
| "Fim do teste" | "Fim **do** teste" | ✅ Acerto (com adição de artigo) |

**Precisão: ~40%** -- O modelo reescreveu praticamente cada frase com suas próprias palavras, inseriu conectivos inexistentes, omitiu trechos e substituiu termos técnicos por equivalências semânticas. Tempo: ~3s.

---

## Gráficos

![Precisão de Transcrição](../assets/s01e04_precisao_transcricao.svg)

![Velocidade de Processamento](../assets/s01e04_velocidade_processamento.svg)

![Comparativo Literal vs Semântico](../assets/s01e04_comparativo_whisper_omni.svg)

![Processamento Literal vs Semântico](../assets/s01e04_literal_vs_semantico.svg)

---

## Análise do Comportamento do Modelo

### Por que o modelo multimodal falha em transcrição literal

O modelo multimodal testado é otimizado para **compreensão contextual multimodal** -- ele recebe áudio, imagem, vídeo ou texto e constrói uma representação semântica do conteúdo. Isso é excelente para tarefas como:

- "Resuma o sentimento dessa reunião"
- "Qual é a intenção do falante neste áudio?"
- "Extraia os pontos-chave dessa palestra"

Mas é fundamentalmente incompatível com transcrição **verbatim** (palavra-por-palavra), porque:

1. **O modelo "entende e reescreve":** Ao processar áudio, ele constrói uma representação semântica interna e então gera texto a partir dessa representação. Isso é parafraseamento, não transcrição.
2. **Acrônimos são interpretados, não preservados:** Quando o falante diz "DIA", o modelo entende o conceito e gera "de IA" -- porque semanticamente faz sentido. Um ASR dedicado não interpreta; ele apenas mapeia fonemas para grafemas.
3. **Alucinações são efeito colateral da geração:** O modelo é generativo. Quando o sinal de áudio é ambíguo (ruído, pronúncia pouco clara), ele "completa" com o que faz mais sentido no contexto semântico -- inventando palavras como "Finto" ou termos como "vídeo" que não existem no áudio.
4. **Thinking agrava o problema:** Com reasoning ativado, o modelo passa mais "tokens de pensamento" interpretando o conteúdo antes de gerar a resposta, o que amplifica o parafraseamento e reduz a fidelidade literal.

### Por que o Whisper é superior em transcrição

O Whisper é um modelo **encoder-decoder treinado especificamente para ASR**. Seu objetivo é mapear sinal de áudio para texto com máxima fidelidade. Ele não "entende" o conteúdo -- ele transcreve. Essa limitação (falta de compreensão semântica) é exatamente o que o torna preciso para transcrição literal.

---

## Lições para Mantenedores de Agentes Hermes

### 1. Whisper é a escolha correta para STT literal

Erro de 1 letra (Whisper) versus múltiplos erros (multimodal) -- não é diferença de grau, é de categoria. Para atas, legendas, comandos de voz: use Whisper.

### 2. Multimodal serve para compreensão, não para transcrição

Resumir reuniões, extrair intenção, analisar sentimento -- nessas tarefas o "entender e reescrever" é vantagem. Como substituto de STT, é fundamentalmente incompatível.

### 3. Consulte o model card antes de integrar

A limitação de reasoning com áudio estava documentada. Descobrimos só após tentativa e erro. Documentação oficial evita desperdício de tempo e tokens.

### 4. Arquitetura híbrida é a correta

- **Whisper** para STT literal
- **Multimodal** para visão e raciocínio contextual sobre imagens/vídeos
- **Compreensão de áudio** (resumo, intenção) como caso futuro -- nunca transcrição

### 5. Thinking + áudio = combinação problemática

Se for usar multimodal para áudio, desative reasoning. O modo thinking prioriza interpretação semântica, agravando parafraseamento e alucinações.

### 6. Teste com vocabulário técnico antes de produção

Acrônimos, nomes de serviços e jargões são o pior cenário para multimodais em modo transcrição. O modelo "traduz" o que não conhece. Sempre valide com o vocabulário real do seu caso de uso.

---

## Veredito Final

O teste selou a decisão arquitetural: **Whisper para STT, modelo multimodal para visão e raciocínio contextual**. A transcrição de áudio com modelo multimodal serve apenas para compreensão semântica (resumo, intenção, análise) -- nunca para transcrição literal. A diferença de precisão (95%+ vs ~60%) e velocidade (1s vs 3s) é suficientemente grande para não haver ambiguidade na escolha.

A configuração atual do sistema está correta e não precisa ser alterada.

---

Documentado por: Christian Rasseli, Cohen (agente no M70q), Hermes (agente no notebook DELL) -- 29/04/2026