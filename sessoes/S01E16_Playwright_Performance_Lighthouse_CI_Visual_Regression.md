# S01E16 — Playwright Performance Testing: Lighthouse CI + Regressao Visual

**Data:** 25-26/06/2026
**Autor:** Christian Rasseli (Homelab)
**Agente:** Hermes (Hermes Desktop/Windows)
**Modelo:** deepseek-v4-flash + NVIDIA Nemotron Nano (subagente)

---

## Resumo

A suite de performance testing Playwright evoluiu de CWV basico (7 testes, 9/set/2025) para cobertura de 3 categorias com 14 testes: Core Web Vitals com budgets rigidos, auditoria Lighthouse CI com chrome-launcher, e regressao visual com screenshot diff nativo. Skill `playwright-perf-testing` atualizada com documentacao completa. Verificacao final: 29/29 checks, 14/14 testes passando.

---

## 1. Contexto — Suite Legado

O workspace `D:\projetos\playwright-tests\` ja continha:

- 7 testes CWV (LCP, FCP, CLS, INP, TTFB, budgets customizados, integridade de recursos)
- Fixtures e helpers em `tests/fixtures/` e `tests/helpers/`
- `global-setup.ts` e `global-teardown.ts`
- Playwright config multi-projeto (chromium, firefox, webkit, mobile-chrome, mobile-safari)
- Playwright `1.61.1` com Chromium 147 headless shell

**Faltava:** auditoria objetiva de terceiros (Lighthouse) e deteccao de regressao visual (screenshot diff entre builds).

---

## 2. Implementacao — Lighthouse CI

### 2.1 Abordagem Rejeitada: CDP Direto

Tentativa inicial de usar o browser Playwright com CDP debugging port para lighthouse:

```ts
// helper/lighthouse.ts (v1) — rejeitada
const cdpSession = await page.context().newCDPSession(page);
const result = await lighthouse(url, { port }); // CDP port discovery complexo
```

Problemas:
- Descobrir a porta de debugging dinamicamente exigia parsing de `--remote-debugging-port=0`
- Colisao de portas em paralelismo
- `port` undefined causava `Cannot read properties of undefined (reading 'catch')`

### 2.2 Abordagem Adotada: chrome-launcher

```ts
// helper/lighthouse.ts (v2) — definitiva
const { launch } = createRequire(import.meta.url)('chrome-launcher');
const chrome = await launch({
  chromePath: process.env.CHROME_PATH || /* Playwright chromium */,
  chromeFlags: ['--headless'],
});
const result = await lighthouse(url, { port: chrome.port });
```

Vantagens:
- Zero configuracao de CDP — chrome-launcher gerencia a porta
- Reusa o Chromium do Playwright via `CHROME_PATH`
- lighthouse executa navegacao propria — nao depende do page context do Playwright
- `createRequire` necessario porque o projeto usa ESM (`"type": "module"` no package.json)
- `chrome.kill()` com `try { await chrome.kill(); } catch {}` em vez de `.catch()` para robustez

### 2.3 Pitfalls Encontrados

| Pitfall | Sintoma | Solucao |
|---------|---------|---------|
| Categoria `pwa` inexistente | Lighthouse crash | Remover do `onlyCategories` |
| ESM + CJS modules | `require is not defined` | Usar `createRequire(import.meta.url)` |
| `chrome.kill()` em `finally` | `undefined.catch()` | Null check + try/catch bloqueante |
| chromelauncher busca Chrome system | Nao encontra Chromium do Playwright | Setar `CHROME_PATH` ou passar no construtor |
| lighthouse executa navegacao propria | Page object do Playwright irrelevante | Passar URL diretamente, nao page |

### 2.4 Resultados Lighthouse

| Categoria | Score | Budget | Status |
|-----------|-------|--------|--------|
| Performance | 100/100 | ≥ 70 | ✅ |
| Accessibility | 89/100 | ≥ 80 | ✅ |
| Best Practices | 96/100 | ≥ 80 | ✅ |
| SEO | 91/100 | ≥ 80 | ✅ |

Metricas: LCP ~1000ms, CLS 0, TBT ~30ms, SI ~850ms, FCP ~850ms, TTI ~1000ms.

---

## 3. Implementacao — Regressao Visual (Screenshot Diff)

### 3.1 Abordagem

Playwright nativo `toHaveScreenshot()` com pixelmatch interno:

```ts
test('pagina inicial — screenshot full page @visual', async ({ page }) => {
  await page.goto(BASE_URL);
  await page.waitForLoadState('networkidle');
  await expect(page).toHaveScreenshot('full-page.png', { fullPage: true });
});
```

### 3.2 Configuracao

- `snapshotDir: './snapshots/baselines'` no playwright.config.ts
- `ignoreSnapshots: false` (snapshots ativos sempre — local e CI)
- `maxDiffPixels: 500` (tolerancia para rendering differences entre ambientes)
- `maxDiffPixelRatio: 0.05` (5% de pixels diferentes aceitavel)

### 3.3 Fluxo

1. **Geracao de baselines:** `npx playwright test --update-snapshots` (cria .png em snapshots/baselines/)
2. **Comparacao:** `npx playwright test` (compara screenshots atuais vs baseline)
3. **Falha:** Playwright reporta diff visual com imagem de comparacao em test-results/

### 3.4 Cobertura Visual (5 testes)

| Teste | Descricao | Target |
|-------|-----------|--------|
| `screenshot full page` | Pagina inicial completa | `fullPage: true` |
| `screenshot fullPage (rolagem)` | Rolagem completa | `fullPage: true` |
| `elemento <header>` | Cabecalho/sessao | `body` (fallback para header ausente) |
| `viewport mobile` | Responsivo 375x667 | `fullPage: true` |
| `tema escuro` | Modo escuro (se aplicavel) | `fullPage: true` |

---

## 4. Integridade dos Artefatos

### 4.1 Arquivos Criados

| Arquivo | Descricao |
|---------|-----------|
| `tests/helpers/lighthouse.ts` | Helper reutilizavel com `runLighthouse()` e `logLighthouseReport()` |
| `tests/performance/lighthouse.spec.ts` | 2 testes: scores minimos + budget rigido |
| `tests/performance/visual-regression.spec.ts` | 5 testes de screenshot diff |
| `.hermes-test-pattern.md` | Documentacao da estrutura e comandos |

### 4.2 Arquivos Modificados

| Arquivo | Mudanca |
|---------|---------|
| `playwright.config.ts` | Adicionado `snapshotDir`, `ignoreSnapshots: false`, `maxDiffPixels` |
| `package.json` | Scripts `test:lighthouse`, `test:visual`, `test:visual:update`, `test:performance` |
| `SKILL.md` (playwright-perf-testing) | Secoes de Lighthouse CI e Visual Regression |

### 4.3 Verificacao Final

```
hermes-verify-fresh-v3.py: 29/29 checks OK
  - Helper lighthouse.ts: exports runLighthouse, logLighthouseReport
  - Spec lighthouse: usa runLighthouse, sem pwa, usa env vars LH_PERF_MIN, LH_STRICT_PERF_MIN
  - Spec visual: usa toHaveScreenshot, testa fullPage, usa @visual tag
  - Config: snapshotDir, ignoreSnapshots:false, maxDiffPixelRatio
  - npm scripts: test:lighthouse, test:visual, test:visual:update, test:performance
  - Dependencias: lighthouse instalado, chrome-launcher disponivel
  - Baselines PNG: 5 encontrados em snapshots/baselines/performance/
  - Skill documenta: Lighthouse, Visual, chrome-launcher, toHaveScreenshot, baselines versionados
  - Vault documenta: 14/14 passed, Lighthouse, Regressao Visual, 100/100
```

---

## 5. Resultado Final Consolidado

| Suite | Testes | Status | Tempo |
|-------|--------|--------|-------|
| Core Web Vitals | 7/7 | ✅ LCP 148ms, CLS 0, INP 16ms | ~15s |
| Lighthouse CI | 2/2 | ✅ Perf 100/100, A11y 89/100 | ~37s |
| Visual Regression | 5/5 | ✅ 5 screenshots comparados | ~17s |
| **Total** | **14/14** | ✅ | **~20s (4 workers)** |

---

## 6. Atualizacao da Skill

Skill `playwright-perf-testing` (categoria `software-development`) foi atualizada com:

- Secao **Lighthouse CI Integration** usando chrome-launcher
- Secao **Visual Regression Testing** com toHaveScreenshot
- Secao **Pitfalls** documentando problemas encontrados
- Exemplos de codigo completos com helper, spec estrutura
- Referencia de configuracao (snapshotDir, ignoreSnapshots, env vars)
- Comandos de CI/CD

---

## 7. Commits e Versionamento

Arquivos documentados no repositorio `crasseli/hermes-log`:

- `diario/2026-06-26.md` — Diario da sessao
- `sessoes/S01E16_Playwright_Performance_Lighthouse_CI_Visual_Regression.md` — Esta sessao
- `README.md` — Tabela de sessoes atualizada com S01E14, S01E15, S01E16
- `metricas/2026-06.md` — Periodo estendido para 26/06, novos dados

---

## Proximos Passos

1. Testar contra dominio publico `https://seudominio.com.br` para metricas reais
2. Integrar com CI/CD (GitHub Actions com LHCI + snapshot diff)
3. Pipeline automatizado de geracao de baselines pre-deploy
4. Expandir cobertura visual para mais paginas/elementos
5. Thresholds de performance adaptativos por ambiente

---

## Metricas da Sessao

- Tool calls na implementacao: ~200 (estimado)
- Artefatos criados: 7 (helper, 2 specs, padrao, 3 verificacoes temp)
- Testes legacy preservados: 7/7 (zero regression)
- Testes novos criados: 7
- Total suite: 14/14 passando
- Skills atualizadas: 1 (playwright-perf-testing)
- Verificacoes ad-hoc: 3 (78, 29, 29 checks — todas OK)
- Scripts temporarios limpos: 3
- Duracao total da sessao: ~5 horas (2 dias)

---

*Documentado pelo Hermes Agent como parte da rotina de documentacao autonômica — Homelab.*
