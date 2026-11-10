# Meu TOEFL

Site estático, em português do Brasil, para a prova **TOEFL iBT Home Edition** no formato em vigor desde **21 de janeiro de 2026**. As tarefas e os textos de prática são em inglês. Nada aqui é questão oficial da ETS, e a nota da tela é uma estimativa.

## Endereço previsto no GitHub Pages

https://isabelapp56.github.io/meu-toefl/

O repositório é `IsabelaPP56/meu-toefl`. O GitHub publica o endereço em minúsculas.

**Passo manual:** em **Settings → Pages → Build and deployment → Source**, escolha **GitHub Actions**. Sem isso o workflow não publica. O arquivo `.github/workflows/pages.yml` usa `actions/configure-pages`, `actions/upload-pages-artifact` (pasta `site/`) e `actions/deploy-pages`. Ele roda no push para `main`.

## O que tem no site

- Painel com a estrutura oficial (50 / 30 min, 47 / 29 min, 12 / 23 min, 11 / 8 min), contagem até a data da prova e plano diário que cabe nessa data. Tudo fica no `localStorage`.
- Página **Como estudar**, com recuperação, espaçamento, intercalação, prática deliberada e repetição em blocos, e as fontes.
- Diagnóstico curto que reordena o plano. O ponto de partida já privilegia Build a Sentence e Speaking.
- Guia de cada tarefa, com vídeo verificado (TST Prep e Test Resources, formato 2026) e a lista de links oficiais, separados em 2026 e legado.
- Prática autoral com correção na hora. Build a Sentence é montado com peças. Complete the Words esconde a segunda metade da palavra. A escuta usa a voz do navegador e só mostra a transcrição depois da resposta.
- Dois simulados na ordem Reading → Listening → Writing → Speaking, com módulos, relógio, sem volta onde a prova não deixa, e segundo módulo mais fácil ou mais difícil conforme o primeiro. A banda é estimativa.
- Coach de fala (repetir, modo bloco, transcrição, diff, gravador) e de escrita (relógio, contagem, lista, prompt para colar no ChatGPT/Grok/Gemini, ou API opcional).
- Vocabulário com repetição espaçada e fila de erros.

Os fatos da prova e o que **não** deu para confirmar estão em [docs/format-sources.md](docs/format-sources.md).

## Rodar na sua máquina

```bash
cd site
python3 -m http.server 8765
```

Abra http://127.0.0.1:8765 . Não abra o `index.html` direto no disco: o banco é carregado por `fetch`.

## Chave de API

Opcional, na página Dia da prova. Fica só no navegador. Não há chave no repositório. Se o provedor bloquear CORS, use o botão que copia o prompt.
