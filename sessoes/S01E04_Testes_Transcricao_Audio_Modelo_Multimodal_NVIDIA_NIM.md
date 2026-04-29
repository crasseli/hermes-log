# Testes de Transcrição de Áudio: STT Dedicado vs Modelo Multimodal via NVIDIA NIM

**Sessão:** S01E04  
**Autores:** Christian Rasseli, Cohen (agente no M70q), Hermes (agente no notebook DELL)  
**Data:** 2026-04-29  
**Tipo:** Experimento / Análise comparativa  

---

## Resumo do Experimento

Um agente (Cohen) testou a capacidade de transcrição de áudio de um modelo multimodal servido via API NVIDIA NIM, comparando-o com um STT dedicado (Whisper large-v3-turbo via provedor de inferência rápida).

O áudio de teste continha aproximadamente 34 segundos de fala em português brasileiro com termos técnicos e acrônimos. O resultado foi contundente: o Whisper alcançou **95%+ de precisão** com apenas um erro de uma letra, enquanto o modelo multimodal atingiu cerca de 60% de precisão palavra-por-palavra, com parafraseamento, substituição de acrônimos e alucinações.

O experimento também revelou que o modo thinking/reasoning interage de forma problemática com entrada de áudio, priorizando compreensão semântica em detrimento da transcrição literal.

---

## Metodologia

### Áudio de teste
- **Duração:** ~34 segundos  
- **Idioma:** Português brasileiro  
- **Conteúdo:** Termos técnicos ("DIA", "NVIDIA NIM", "stand-alone", "Free Endpoints")  
- **Formato:** Mensagem de voz do Telegram (OGG) convertida para WAV via ffmpeg  

### Modelos testados
1. **Whisper (STT dedicado)** – large-v3-turbo com timestamps por segmento  
2. **Multimodal (thinking=ON)** – Nemotron 3 Nano Omni via NVIDIA NIM com `enable_thinking: true`  
3. **Multimodal (thinking=OFF)** – Mesmo modelo com `enable_thinking: false`  

### Fluxo utilizado
1. Recebimento do áudio via Telegram  
2. Conversão OGG → WAV  
3. Codificação em base64 e envio à API  
4. Chamadas paralelas ao NVIDIA NIM e ao Whisper  

---

## A Interação entre Thinking Mode e Entrada de Áudio

**Descoberta importante:** Embora o modelo suporte entrada de áudio, ativar `enable_thinking: true` causa forte degradação na qualidade da transcrição literal.  

O modelo passa a priorizar raciocínio semântico e compreensão contextual, resultando em:
- Parafraseamento intenso
- Substituição de acrônimos ("DIA" → "de IA")
- Alucinações e inserções de palavras inexistentes

Essa limitação comportamental ocorre porque o modo thinking incentiva a interpretação em vez da transcrição fiel. A documentação indica que o reasoning apresenta comportamento distinto quando combinado com áudio.  

Com thinking desativado o modelo melhora, mas ainda fica significativamente inferior ao Whisper em precisão literal.

---

## Resultados Comparativos

### O que foi realmente dito

> "Esse é apenas um áudio de teste. Objetivo de teste. Desenvolver um agente DIA pessoal autônomo completamente portátil, executável stand-alone, que opera exclusivamente via chamadas de API, aos serviços NVIDIA NIM, Free Endpoints, sem dependências de instalação no sistema host. Fim do teste."

### 1. Transcrição – Whisper (STT dedicado)

| Trecho original                          | Transcrição Whisper                    | Status                     |
|------------------------------------------|----------------------------------------|----------------------------|
| "Esse é apenas um áudio de teste"       | Correto                                | ✅ Acerto                  |
| "Objetivo de teste"                      | Correto                                | ✅ Acerto                  |
| "agente DIA pessoal autônomo"            | "agente DIA pessoal autônomo"          | ✅ Preservou acrônimo      |
| "NVIDIA NIM"                             | "NVIDIA **NIN**"                       | ⚠️ Erro de 1 letra        |
| "Free Endpoints"                         | Correto                                | ✅ Acerto                  |
| "Fim do teste"                           | Correto                                | ✅ Acerto                  |

**Precisão:** 95%+ • Tempo: ~1 segundo

### 2. Transcrição – Multimodal (thinking=OFF)

| Trecho original                                   | Transcrição Multimodal                     | Status                          |
|---------------------------------------------------|--------------------------------------------|---------------------------------|
| "agente DIA pessoal autônomo"                     | "agente **de IA**, pessoal, **autonomo**"  | ❌ Substituição de acrônimo     |
| "executável stand-alone"                          | "executável standalone"                    | ⚠️ Perdeu hífen                 |
| "aos serviços NVIDIA NIM"                         | "serviços **em vídeo**, **ní**"            | ❌ Alucinação                    |
| "Free Endpoints"                                  | "free endpoints"                           | ⚠️ Perdeu maiúsculas            |
| "Fim do teste"                                    | "**Finto** teste"                          | ❌ Alucinação                    |

**Precisão:** ~60% • Tempo: ~3 segundos

### 3. Transcrição – Multimodal (thinking=ON)

| Trecho original                          | Transcrição Multimodal (thinking=ON)          | Status                           |
|------------------------------------------|-----------------------------------------------|----------------------------------|
| "Esse é apenas um áudio de teste"       | "Este é um áudio de teste"                    | ⚠️ Parafraseamento              |
| "Objetivo de teste"                      | *(omitido)*                                   | ❌ Omisão                        |
| "agente DIA pessoal autônomo"            | "agente **de IA** pessoal **e autônomo**"     | ❌ Substituição + inserção       |
| "completamente portátil"                 | "totalmente portátil"                         | ⚠️ Parafraseamento              |
| "executável stand-alone"                 | "executável de forma autônoma"                | ❌ Perdeu termo técnico          |
| "Fim do teste"                           | "Fim do teste"                                | ✅ Acerto                        |

**Precisão:** ~40% • Tempo: ~3 segundos

---

## Visualizações Comparativas

<div align="center">

### 1. Precisão de Transcrição
![Precisão de Transcrição](https://github.com/crasseli/hermes-log/blob/main/assets/s01e04_precisao.svg)

### 2. Velocidade de Processamento
![Velocidade](https://github.com/crasseli/hermes-log/blob/main/assets/s01e04_velocidade.svg)

### 3. Comparativo Radar (Precisão × Velocidade × Fidelidade)
![Radar Comparativo](https://github.com/crasseli/hermes-log/blob/main/assets/s01e04_radar.svg)

### 4. Literal vs Semântico
![Literal vs Semântico](https://github.com/crasseli/hermes-log/blob/main/assets/s01e04_literal_vs_semantico.svg)

</div>

---

## Lições para Mantenedores

1. **Whisper é a escolha correta para STT literal**  
   Erro de uma letra versus múltiplos erros graves não é diferença de grau — é diferença de categoria.

2. **Modelos multimodais servem para compreensão, não para transcrição**  
   Excelentes para resumir, extrair intenção ou analisar sentimento. Como substituto de STT, são incompatíveis.

3. **Sempre consulte o model card antes de integrar novas capacidades.**

4. **A arquitetura híbrida atual é a mais adequada**  
   Whisper para transcrição literal + Multimodal para visão e raciocínio contextual.

5. **Thinking + áudio é uma combinação problemática**  
   Desative o reasoning quando usar áudio se quiser maior fidelidade.

6. **Teste sempre com vocabulário técnico real**  
   Acrônimos e jargões são o ponto fraco dos modelos multimodais em tarefas de transcrição.

---

Documentado por: Christian Rasseli, Cohen (agente no M70q), Hermes (agente no notebook DELL) — 29 de abril de 2026
