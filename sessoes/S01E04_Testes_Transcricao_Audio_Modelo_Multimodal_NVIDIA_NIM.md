# Testes de Transcrição de Áudio: STT Dedicado vs Modelo Multimodal via NVIDIA NIM

**Sessão:** S01E04  
**Autores:** Christian Rasseli, Cohen (agente no M70q), Hermes (agente no notebook DELL)  
**Data:** 2026-04-29  
**Tipo:** Experimento / Análise comparativa  

---

## Resumo do Experimento

Um agente (Cohen) testou a capacidade de transcrição de áudio de um modelo multimodal servido via API NVIDIA NIM, comparando-o com um STT dedicado (Whisper via provedor de inferência rápida).  

O áudio de teste tinha aproximadamente 34 segundos de fala em português brasileiro, contendo termos técnicos e acrônimos. O resultado foi claro: o Whisper entregou **precisão de 95%+** com apenas um erro de uma letra, enquanto o modelo multimodal alcançou cerca de 60% de precisão palavra-por-palavra, com parafraseamento, substituição de acrônimos e alucinações.  

O teste também revelou que o modo thinking/reasoning interage de forma problemática com entrada de áudio, degradando ainda mais a qualidade da transcrição literal.

---

## Metodologia

### Áudio de teste
- **Duração:** ~34 segundos  
- **Idioma:** Português brasileiro  
- **Conteúdo:** Termos técnicos (acrônimo "DIA", serviço "NVIDIA NIM", "stand-alone", "Free Endpoints")  
- **Formato:** Mensagem de voz do Telegram (OGG) convertida para WAV  

### Modelos testados
1. **Whisper (STT dedicado):** Whisper large-v3-turbo via provedor rápido, com timestamps por segmento  
2. **Multimodal (thinking=ON):** Nemotron 3 Nano Omni via NVIDIA NIM com `enable_thinking: true`  
3. **Multimodal (thinking=OFF):** Mesmo modelo com `enable_thinking: false`  

### Fluxo de processamento
1. Áudio recebido via Telegram (OGG)  
2. Conversão OGG → WAV via ffmpeg  
3. Codificação em base64 e envio à API  
4. Chamada ao NVIDIA NIM (formato compatível com OpenAI)  
5. Chamada paralela ao Whisper para comparação  

---

## A Interação entre Thinking Mode e Entrada de Áudio

**Descoberta importante:** Embora o modelo multimodal suporte áudio mesmo com o modo thinking ativado, habilitar `enable_thinking: true` causa uma degradação significativa na transcrição literal.  

O modelo deixa de atuar como um ASR preciso e passa a priorizar compreensão e interpretação semântica, resultando em:
- **Parafraseamento** — reescreve o conteúdo com suas próprias palavras
- **Substituição de acrônimos** — "DIA" vira "de IA"
- **Alucinações** — inventa palavras que não existem no áudio

Isso acontece porque o modo thinking incentiva o raciocínio semântico e a compreensão contextual em detrimento da fidelidade palavra-por-palavra. Embora o modelo suporte áudio, o reasoning o faz atuar mais como um interpretador do que como um transcritor tradicional. A documentação oficial indica que o uso de reasoning é mais previsível em texto e imagem, apresentando comportamento distinto com áudio.

Com thinking desativado, o modelo entrega transcrições mais literais — ainda assim, claramente inferior ao Whisper.

---

## Resultados Comparativos

### O que foi realmente dito

> "Esse é apenas um áudio de teste. Objetivo de teste. Desenvolver um agente DIA pessoal autônomo completamente portátil, executável stand-alone, que opera exclusivamente via chamadas de API, aos serviços NVIDIA NIM, Free Endpoints, sem dependências de instalação no sistema host. Fim do teste."

### 1. Transcrição do Whisper (STT dedicado)

| Trecho original                          | Transcrição Whisper                  | Status                  |
|------------------------------------------|--------------------------------------|-------------------------|
| "Esse é apenas um áudio de teste"       | Correto                              | ✅ Acerto               |
| "Objetivo de teste"                      | Correto                              | ✅ Acerto               |
| "agente DIA pessoal autônomo"            | "agente DIA pessoal autônomo"        | ✅ Acerto (preservou acrônimo) |
| "NVIDIA NIM"                             | "NVIDIA **NIN**"                     | ⚠️ 1 erro (1 letra)    |
| "Free Endpoints"                         | Correto                              | ✅ Acerto               |
| "Fim do teste"                           | Correto                              | ✅ Acerto               |

**Precisão:** 95%+ • Tempo: ~1s

### 2. Transcrição do Modelo Multimodal (thinking=OFF)

| Trecho original                                   | Transcrição Multimodal                  | Status                          |
|---------------------------------------------------|-----------------------------------------|---------------------------------|
| "Esse é apenas um áudio de teste"                | Correto                                 | ✅ Acerto                       |
| "Objetivo de teste"                               | Correto                                 | ✅ Acerto                       |
| "agente DIA pessoal autônomo"                     | "agente **de IA**, pessoal, **autonomo**" | ❌ Substituição de acrônimo + erro de acentuação |
| "completamente portátil, executável stand-alone" | "completamente portátil, executável standalone" | ⚠️ Perdeu hífen                |
| "aos serviços NVIDIA NIM"                         | "serviços **em vídeo**, **ní**"         | ❌ Alucinação                   |
| "Free Endpoints"                                  | "free endpoints"                        | ⚠️ Perdeu maiúsculas           |
| "Fim do teste"                                    | "**Finto** teste"                       | ❌ Alucinação                   |

**Precisão:** ~60% • Tempo: ~3s

### 3. Transcrição do Modelo Multimodal (thinking=ON)

Com thinking ativado o modelo tornou-se ainda mais semântico, reescrevendo extensivamente o conteúdo.

| Trecho original                                   | Transcrição Multimodal (thinking=ON)       | Status                              |
|---------------------------------------------------|--------------------------------------------|-------------------------------------|
| "Esse é apenas um áudio de teste"                | "Este é um áudio de teste"                 | ⚠️ Parafraseamento                 |
| "Objetivo de teste"                               | *(omitido)*                                | ❌ Omisão completa                  |
| "agente DIA pessoal autônomo"                     | "agente **de IA** pessoal **e autônomo**"  | ❌ Substituição + inserção          |
| "completamente portátil"                          | "totalmente portátil"                      | ⚠️ Parafraseamento                 |
| "executável stand-alone"                          | "executável de forma autônoma"             | ❌ Perdeu termo técnico             |
| "exclusivamente via chamadas de API"              | "através de chamadas de API"               | ⚠️ Perdeu exclusividade            |
| "Fim do teste"                                    | "Fim do teste"                             | ✅ Acerto (com artigo extra)        |

**Precisão:** ~40% • Tempo: ~3s

---

## Lições para Mantenedores

1. **Whisper é a escolha correta para STT literal**  
   Erro de 1 letra versus múltiplos erros graves não é diferença de grau, é de categoria. Para atas, legendas, logs ou comandos de voz: use Whisper.

2. **Modelos multimodais servem para compreensão, não para transcrição**  
   São excelentes para resumir reuniões, extrair intenção ou analisar sentimento. Nessa tarefa, o “entender e reescrever” é uma vantagem. Como substituto de STT, são fundamentalmente incompatíveis.

3. **Sempre consulte o model card antes de integrar**  
   A limitação comportamental do reasoning com áudio estava documentada. Descobrimos na prática após tentativa e erro.

4. **A arquitetura híbrida atual é a correta**  
   - Whisper → transcrição literal  
   - Multimodal → visão e raciocínio contextual  
   - Compreensão de áudio (resumo, intenção) → caso futuro para o multimodal (nunca transcrição)

5. **Thinking + áudio = combinação problemática**  
   Se for usar modelo multimodal com áudio, desative o reasoning. O modo thinking agrava parafraseamento e alucinações.

6. **Teste sempre com vocabulário técnico**  
   Acrônimos, nomes de serviços e jargões são o pior cenário para modelos multimodais em tarefas de transcrição. Sempre valide com o vocabulário real do seu domínio.

---

**Gráficos comparativos** (ver pasta `assets/`):
- `s01e04_precisao_transcricao.svg`
- `s01e04_velocidade_processamento.svg`
- `s01e04_comparativo_whisper_omni.svg`
- `s01e04_literal_vs_semantico.svg`

---

Documentado por: Christian Rasseli, Cohen (agente no M70q), Hermes (agente no notebook DELL) — 29/04/2026
