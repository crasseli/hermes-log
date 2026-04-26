---
title: NPM Troubleshooting - MODULE_NOT_FOUND
date: 2026-04-23 13:40:34
updated: 2026-04-23 13:40:34
tags:
  - npm
  - nodejs
  - troubleshooting
  - MODULE_NOT_FOUND
  - devops
source: 
related: []
---

## Problema
NPM 10.9.7 funcionando, mas falha ao atualizar para 11.13.0 com erro MODULE_NOT_FOUND no promise-retry.

## Diagnostico
- promise-retry existe em node_modules/
- @npmcli/arborist nao encontra o modulo durante operacoes de install/update
- Problema de resolucao de dependencias na arvore do npm

## Solucoes Testadas
1. Criar symlink promise-retry em arborist/node_modules/ - parcialmente funciona para versoes, mas nao para update
2. Tentativa de reinstall manual do npm via tarball - bloqueado
3. Recomendacao: manter npm 10.9.7 (LTS estavel) ou reinstalar Node.js do zero

## Skill Criada
npm-troubleshooting em devops/