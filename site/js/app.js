(function () {
  const { esc } = Widgets;
  const root = document.getElementById("conteudo");
  const nav = document.getElementById("nav");
  let bank = null;
  const LINKS = [
    ["#/", "Início"],
    ["#/estudar", "Como estudar"],
    ["#/diagnostico", "Diagnóstico"],
    ["#/leitura", "Leitura"],
    ["#/escuta", "Escuta"],
    ["#/escrita", "Escrita"],
    ["#/fala", "Fala"],
    ["#/pratica", "Prática"],
    ["#/simulado", "Simulado"],
    ["#/vocab", "Vocabulário"],
    ["#/prova", "Dia da prova"]
  ];

  const VIDEOS = [
    { href: "https://www.youtube.com/watch?v=eKaVhOnMjm8", title: "TOEFL Reading 2026: Tips to Score Higher on the NEW Test", who: "TST Prep", task: "leitura", format: "2026" },
    { href: "https://www.youtube.com/watch?v=M5kTvJWIx8Q", title: "TOEFL Reading Practice Test 2026 (Answers Included)", who: "TST Prep", task: "leitura", format: "2026" },
    { href: "https://www.youtube.com/watch?v=C0_sud-fw0k", title: "TOEFL Listening 2026 Guide", who: "TST Prep", task: "escuta", format: "2026" },
    { href: "https://www.youtube.com/watch?v=Y9ztHoKJDxs", title: "TOEFL Listening Practice Test 2026", who: "TST Prep", task: "escuta", format: "2026" },
    { href: "https://www.youtube.com/watch?v=XYLHVFBFsDc", title: "Build a Sentence Training (2026)", who: "TST Prep", task: "escrita", format: "2026" },
    { href: "https://www.youtube.com/watch?v=bPRfxgXBQAI", title: "Write an Email Guide (2026)", who: "TST Prep", task: "escrita", format: "2026" },
    { href: "https://www.youtube.com/watch?v=SGP2VAnC_1I", title: "TOEFL 2026 Writing Templates — Email and Academic Discussion", who: "Test Resources", task: "escrita", format: "2026" },
    { href: "https://www.youtube.com/watch?v=MDR3k5nT5D8", title: "TOEFL Writing Practice Test 2026", who: "TST Prep", task: "escrita", format: "2026" },
    { href: "https://www.youtube.com/watch?v=iR529CoRuZo", title: "Listen and Repeat Training (2026)", who: "TST Prep", task: "fala", format: "2026" },
    { href: "https://www.youtube.com/watch?v=cktZfTZ9UXs", title: "Take an Interview Task (2026)", who: "TST Prep", task: "fala", format: "2026" },
    { href: "https://www.youtube.com/watch?v=YphRAv3fpMM", title: "TOEFL Speaking Practice Test 2026", who: "TST Prep", task: "fala", format: "2026" }
  ];

  function videosFor(task) {
    return '<div class="video-list">' + VIDEOS.filter((v) => v.task === task).map((v) =>
      '<a href="' + v.href + '" target="_blank" rel="noopener"><strong>' + esc(v.title) + '</strong><br><span class="muted">' + esc(v.who) + " · formato " + v.format + " · link verificado em 10/11/2026</span></a>"
    ).join("") + "</div>";
  }

  function route() {
    const raw = (location.hash || "#/").slice(1);
    const [path, qs] = raw.split("?");
    const parts = path.split("/").filter(Boolean);
    return { parts, q: Object.fromEntries(new URLSearchParams(qs || "")) };
  }

  function paintNav(active) {
    const exam = Store.get().mockRun;
    document.getElementById("site-header").classList.toggle("hidden", !!exam && (route().parts[0] === "simulado"));
    document.getElementById("site-footer").classList.toggle("hidden", !!exam && route().parts[0] === "simulado" && route().parts[1]);
    nav.innerHTML = LINKS.map(([href, label]) => '<a href="' + href + '"' + (active === href ? ' class="active"' : "") + ">" + label + "</a>").join("");
  }

  async function boot() {
    try {
      const files = ["ctw", "daily", "academic", "choose", "conversation", "announcement", "talk", "bas", "email", "discussion", "repeat", "interview", "vocab"];
      const pairs = await Promise.all(files.map(async (f) => {
        const res = await fetch("data/parts/" + f + ".json");
        if (!res.ok) throw new Error(f + " HTTP " + res.status);
        return [f, await res.json()];
      }));
      bank = Object.fromEntries(pairs);
    } catch (e) {
      root.innerHTML = '<div class="callout-bad"><b>Não achei o banco de prática.</b><p>' + esc(e.message) + "</p></div>";
      return;
    }
    window.addEventListener("hashchange", draw);
    draw();
  }

  function draw() {
    const r = route();
    const top = r.parts[0] || "";
    const map = { "": "#/", estudar: "#/estudar", diagnostico: "#/diagnostico", leitura: "#/leitura", escuta: "#/escuta", escrita: "#/escrita", fala: "#/fala", pratica: "#/pratica", simulado: "#/simulado", vocab: "#/vocab", erros: "#/erros", materiais: "#/materiais", prova: "#/prova", resultado: "#/simulado", "coach-fala": "#/fala", "coach-escrita": "#/escrita" };
    paintNav(map[top] || "#/");
    const page = {
      "": home,
      estudar: estudar,
      diagnostico: diagnostico,
      leitura: () => guia("leitura"),
      escuta: () => guia("escuta"),
      escrita: () => guia("escrita"),
      fala: () => guia("fala"),
      pratica: pratica,
      simulado: simulado,
      vocab: vocab,
      erros: erros,
      materiais: materiais,
      prova: prova,
      resultado: resultado,
      "coach-fala": coachFala,
      "coach-escrita": coachEscrita
    }[top] || home;
    if (Store.get().mockRun && top === "simulado" && r.parts[1]) {
      document.getElementById("site-header").classList.add("hidden");
      ExamKit.render(root, bank);
      return;
    }
    page(r);
    window.scrollTo(0, 0);
  }

  function counts() {
    const q = (list, field) => (list || []).reduce((n, item) => n + (item[field] ? item[field].length : 1), 0);
    const practice = (list) => (list || []).filter((x) => x.pool === "practice" || String(x.pool || "").startsWith("rep") || x.pool === "practice");
    function isPractice(x) { return x.pool === "practice"; }
    const gaps = (list) => list.filter(isPractice).reduce((n, item) => n + (item.gaps ? item.gaps.length : 0), 0);
    const qs = (list) => list.filter(isPractice).reduce((n, item) => n + (item.questions ? item.questions.length : 1), 0);
    return {
      ctw: gaps(bank.ctw),
      daily: qs(bank.daily),
      academic: qs(bank.academic),
      choose: bank.choose.filter(isPractice).length,
      conversation: qs(bank.conversation),
      announcement: qs(bank.announcement),
      talk: qs(bank.talk),
      bas: bank.bas.filter(isPractice).length,
      email: bank.email.filter(isPractice).length,
      discussion: bank.discussion.filter(isPractice).length,
      repeat: bank.repeat.filter(isPractice).length,
      repeatSentences: bank.repeat.filter(isPractice).reduce((n, s) => n + s.sentences.length, 0),
      interview: bank.interview.filter(isPractice).reduce((n, s) => n + s.questions.length, 0),
      vocab: bank.vocab.length
    };
  }

  function home() {
    const s = Store.get();
    const left = PlanKit.daysUntil(s.examDate);
    const plan = PlanKit.build(s);
    const today = plan[0];
    const c = counts();
    const pct = s.stats.answered ? Math.round(100 * s.stats.correct / s.stats.answered) : 0;
    root.innerHTML = `
      <section class="hero">
        <div class="card">
          <p class="kicker">TOEFL iBT em casa · fim de 2026</p>
          <h1>Um lugar só, até o dia da prova.</h1>
          <p class="lede">Formato de 21 de janeiro de 2026. A meta deste plano é banda 4 ou mais, o começo de B2. A aula de inglês continua; aqui entra o que a aula não cronometra: montar a frase, repetir sem perder o meio, e responder em 45 segundos.</p>
          <div class="row">
            <a class="btn" href="#/diagnostico">Começar pelo diagnóstico</a>
            <a class="btn secondary" href="#/simulado">Simulado na ordem da prova</a>
          </div>
        </div>
        <div class="card stack">
          <div>
            <p class="kicker">Contagem</p>
            <b style="font-family:var(--serif);font-size:2.4rem">${left < 0 ? "data passou" : left === 0 ? "é hoje" : left + " dias"}</b>
            <p class="muted">Fuso de Brasília. A data é sua e fica só neste navegador.</p>
          </div>
          <label class="field">Data da prova <input type="date" id="exam-date" value="${esc(s.examDate)}"></label>
          <label class="field">Tempo do dia
            <select id="session-len">
              <option value="padrao" ${s.sessionLen !== "curto" ? "selected" : ""}>Dia padrão, cerca de 75–90 min</option>
              <option value="curto" ${s.sessionLen === "curto" ? "selected" : ""}>Dia curto, cerca de 45 min</option>
            </select>
          </label>
        </div>
      </section>
      <section class="grid-2" style="margin-top:14px">
        <div class="card">
          <h2>Hoje</h2>
          ${today ? todayBlock(today) : '<p>A data da prova é hoje ou já passou. Abra <a href="#/prova">o dia da prova</a>.</p>'}
        </div>
        <div class="card">
          <h2>Progresso neste navegador</h2>
          <div class="grid-2">
            <div class="stat"><b>${s.stats.answered}</b> respostas</div>
            <div class="stat"><b>${pct}%</b> de acerto</div>
          </div>
          <p class="muted">Prioridade atual: ${esc((s.priorities || []).slice(0, 2).join(" e ") || "escrita e fala")}.</p>
          <p><a href="#/erros">Fila de erros (${s.errors.filter((e) => e.due <= Date.now()).length} para hoje)</a> · <a href="#/vocab">vocabulário</a></p>
          ${s.lastResult ? `<p>Último simulado ${s.lastResult.mockId}: estimativa geral <b>${s.lastResult.overall ?? "—"}</b>. <a href="#/resultado">Ver</a></p>` : ""}
        </div>
      </section>
      <section class="card" style="margin-top:14px">
        <h2>Estrutura que a página da ETS mostrava em 10/11/2026</h2>
        <table>
          <tr><th>Seção</th><th>Tarefas</th><th>Itens</th><th>Tempo-base</th></tr>
          <tr><td>Reading</td><td>Complete the Words, Read in Daily Life, Read an Academic Passage</td><td>50</td><td>30 min, em dois módulos</td></tr>
          <tr><td>Listening</td><td>Choose a Response, Conversation, Announcement, Academic Talk</td><td>47</td><td>29 min no caminho mais longo</td></tr>
          <tr><td>Writing</td><td>Build a Sentence, Write an Email, Academic Discussion</td><td>12</td><td>23 min (e-mail 7, discussão 10)</td></tr>
          <tr><td>Speaking</td><td>Listen and Repeat, Take an Interview</td><td>11</td><td>cerca de 8 min</td></tr>
        </table>
        <p class="muted">Ordem: Reading, Listening, Writing, Speaking. Sem intervalo programado. Reserve cerca de duas horas, porque as instruções não entram nesse relógio. Reading e Listening mudam no segundo módulo. A nota é de 1 a 6, de meio em meio; 4 a 4,5 é B2. <a href="#/materiais">Fontes e o que não foi possível confirmar</a>.</p>
      </section>
      <section class="card" style="margin-top:14px">
        <h2>O que tem para treinar aqui</h2>
        <div class="grid-4">
          ${stat("Lacunas", c.ctw)}
          ${stat("Cotidiano", c.daily)}
          ${stat("Acadêmica", c.academic)}
          ${stat("Escolha a resposta", c.choose)}
          ${stat("Conversas", c.conversation)}
          ${stat("Anúncios", c.announcement)}
          ${stat("Palestras", c.talk)}
          ${stat("Build a Sentence", c.bas)}
          ${stat("E-mails", c.email)}
          ${stat("Discussões", c.discussion)}
          ${stat("Frases para repetir", c.repeatSentences)}
          ${stat("Perguntas de entrevista", c.interview)}
        </div>
        <p class="muted">Contagem só do banco de prática, sem os dois simulados. Tudo é autoral. ${c.vocab} cartões de vocabulário.</p>
      </section>
      <section class="card" style="margin-top:14px">
        <h2>Plano até a prova</h2>
        <p>Cada dia começa pelo que você erra, depois Build a Sentence e fala. Leitura, escuta, e-mail e discussão se alternam. Os simulados entram no meio e perto do fim, com um dia de revisão depois. Se a prova for em menos de duas semanas, o plano comprime vídeo e mantém correção.</p>
        ${plan.map((d) => '<div class="day"><div class="when">' + esc(d.label) + "<br>" + d.minutes + ' min</div><div>' + d.blocks.map((b) => '<div class="checkline"><input type="checkbox" data-day="' + d.iso + '" data-id="' + b.id + '" ' + ((s.checks[d.iso] || {})[b.id] ? "checked" : "") + '><div><a href="' + esc(b.href) + '">' + esc(b.title) + "</a> · " + b.minutes + " min<div class=\"muted\">" + esc(b.note) + "</div></div></div>").join("") + "</div></div>").join("")}
      </section>`;
    root.querySelector("#exam-date").onchange = (e) => { Store.set({ examDate: e.target.value }); draw(); };
    root.querySelector("#session-len").onchange = (e) => { Store.set({ sessionLen: e.target.value }); draw(); };
    root.querySelectorAll("input[type=checkbox]").forEach((box) => {
      box.onchange = () => {
        const st = Store.get();
        st.checks[box.dataset.day] = st.checks[box.dataset.day] || {};
        st.checks[box.dataset.day][box.dataset.id] = box.checked;
        Store.save();
      };
    });
  }

  function stat(label, n) { return '<div class="stat"><b>' + n + "</b>" + esc(label) + "</div>"; }
  function todayBlock(d) {
    return "<p><b>" + esc(d.label) + "</b> · cerca de " + d.minutes + " min</p>" + d.blocks.map((b) => '<p><a href="' + esc(b.href) + '">' + esc(b.title) + "</a><br><span class=\"muted\">" + esc(b.note) + "</span></p>").join("");
  }

  function estudar() {
    root.innerHTML = `
      <p class="kicker">Método</p>
      <h1>Como estudar em poucas semanas</h1>
      <p class="lede">A aula de inglês cobre língua geral. Este plano cobre a prova: recuperar de memória, errar de propósito, e repetir o ponto fraco com relógio. Não dá para compensar um dia perdido com três horas de vídeo.</p>
      <div class="grid-2">
        <article class="card"><h2>Recuperação, não releitura</h2><p>Tentar responder antes de ver a explicação fixa mais do que reler o resumo. Por isso o diagnóstico vem primeiro, a fila de erros volta sozinha, e o cartão de vocabulário pede a resposta antes de virar.</p><p class="muted">Roediger e Karpicke, 2006, Psychological Science. Dunlosky e colegas, 2013, Psychological Science in the Public Interest: prática de teste e prática espaçada ficam entre as técnicas de maior utilidade.</p></article>
        <article class="card"><h2>Espaçar e intercalar</h2><p>Um erro de hoje volta amanhã, e de novo alguns dias depois. No mesmo dia você não faz só fala: Build a Sentence, uma repetição e um bloco de leitura ou escuta se alternam. Misturar assuntos parecidos demais piora a ilusão de fluência e melhora a prova.</p><p class="muted">Cepeda e colegas, 2006, Psychological Bulletin. Rohrer e Taylor, 2007, Instructional Science.</p></article>
        <article class="card"><h2>Prática deliberada</h2><p>Cada Build a Sentence errado vira um padrão com nome: pergunta indireta, auxiliar, oração relativa, passiva, preposição. Você refaz esse padrão, não “a seção de writing” inteira. O mesmo vale para a palavra que sumiu no meio da frase.</p><p class="muted">Ericsson, Krampe e Tesch-Römer, 1993, Psychological Review.</p></article>
        <article class="card"><h2>Sombra em blocos</h2><p>Listen and Repeat não é decorar tradução. É segurar um bloco de sentido, falar, e só então o próximo. O modo lento parte a frase. A transcrição mostra a palavra que caiu, em geral a, the, of, to, ou o verbo do meio.</p><p class="muted">Murphey, 2001, Language Teaching Research, sobre shadowing. O treino em blocos também é o que o vídeo de Listen and Repeat da TST Prep (2026) recomenda para quem esquece o meio da frase.</p></article>
      </div>
      <article class="card" style="margin-top:14px">
        <h2>O que entra em cada dia</h2>
        <ol>
          <li>Erros vencidos, sem olhar a resposta.</li>
          <li>Build a Sentence cronometrado, com correção do padrão.</li>
          <li>Sete frases de repetição: bloco se a precisão cair, frase inteira uma vez.</li>
          <li>Uma ou duas respostas de 45 segundos, ouvir, regravar a pior.</li>
          <li>Um bloco intercalado: e-mail de 7 min, discussão de 10, leitura ou escuta.</li>
          <li>Oito cartões. Uma linha no diário: qual regra falhou.</li>
        </ol>
        <p>Vídeo entra em alguns dias, 15 minutos, e você pausa antes do modelo. A TST Prep e a própria página de preparação da ETS pedem prática com o formato novo, não com o Integrated Writing antigo nem com as quatro tarefas velhas de Speaking.</p>
        <p>Fontes da prova, não do método: <a href="https://www.ets.org/toefl/test-takers/ibt/about/content.html">conteúdo e tempos</a>, <a href="https://www.ets.org/pdfs/toefl/toefl-ibt-test-overview.pdf">overview em PDF</a>, <a href="https://www.ets.org/toefl/test-takers/ibt/prepare.html">preparação</a>. O plano deste site adapta o roteiro de 6/11 a 4/12 que você já tinha, contado a partir de hoje e da data que você gravar.</p>
      </article>`;
  }

  const GUIAS = {
    leitura: {
      title: "Reading",
      body: `<p>Três tarefas. O texto fica na tela. Dentro do módulo dá para voltar; o módulo 1 fecha quando o 2 começa.</p>
        <h3>Complete the Words</h3><p>A primeira frase vem inteira. Depois faltam letras em 10 palavras. Leia a frase e decida a classe: verbo, nome, conector. O começo da palavra já está visível. Não chute letra por letra sem pronunciar a palavra inteira.</p>
        <h3>Read in Daily Life</h3><p>Aviso, e-mail, mensagem, agenda. Pergunte: quem quer o quê, até quando, com qual condição. Cuidado com unless, except, before e after.</p>
        <h3>Read an Academic Passage</h3><p>Cerca de 200 palavras e 5 questões. Não precisa saber a matéria. A resposta está no texto. Elimine o que é verdade no mundo, mas não no parágrafo, e o que troca causa e efeito.</p>
        <h3>Erro comum</h3><p>Gastar o módulo inteiro no primeiro texto. O relógio é do módulo, não de cada lacuna.</p>`,
      videos: "leitura"
    },
    escuta: {
      title: "Listening",
      body: `<p>Quatro tarefas. O áudio toca uma vez e, na prova, não se volta à questão anterior. Sotaques citados pela ETS: América do Norte, Reino Unido, Austrália e Nova Zelândia.</p>
        <h3>Choose a Response</h3><p>A frase não está escrita. Ouça a função: pedido, convite, desculpa, correção. Descarte a opção que repete uma palavra e responde outra pergunta.</p>
        <h3>Conversa e anúncio</h3><p>Anote problema → o que a pessoa vai fazer. No anúncio: evento, horário, lugar, ação.</p>
        <h3>Academic Talk</h3><p>Entre cerca de 100 e 250 palavras no material oficial. Aqui são quatro perguntas, como no Practice Test 1. Anote só o tema, duas relações e um exemplo.</p>`,
      videos: "escuta"
    },
    escrita: {
      title: "Writing",
      body: `<h3>Build a Sentence</h3><p>Há uma frase pronta e peças para a resposta. Sobram peças. Procure primeiro o verbo e o auxiliar. Pergunta indireta não inverte: Do you know where she went, não where did she go. Relativa cola no nome: the guide who showed us. Passiva: be + particípio + by. Este é o seu ponto fraco declarado: faça um bloco curto todo dia, não um mutirão no fim de semana.</p>
        <p><a class="btn small" href="#/pratica/bas?n=8">Treinar 8 frases</a></p>
        <h3>E-mail, 7 minutos</h3><p>Saudação, motivo na primeira ou segunda frase, os três tópicos, fecho. Frases completas. A ETS não publicou mínimo de palavras; a discussão, sim.</p>
        <h3>Discussão, 10 minutos</h3><p>Pelo menos 100 palavras. Posição, um motivo, um exemplo com nome ou situação, uma frase sobre o que o colega disse. Não escreva dois motivos rasos nem copie o post.</p>
        <p><a class="btn small" href="#/coach-escrita?task=email">E-mail com relógio</a> <a class="btn small secondary" href="#/coach-escrita?task=discussion">Discussão com relógio</a></p>`,
      videos: "escrita"
    },
    fala: {
      title: "Speaking",
      body: `<h3>Listen and Repeat</h3><p>Sete frases, cada vez mais longas, 8 a 12 segundos, sem preparação, uma tentativa. Se a frase some no meio, não recomece do zero em silêncio: segure o primeiro bloco (quem / o quê) como imagem e fale. As palavras que mais caem são a, the, of, to e o -s do verbo.</p>
        <p><a class="btn small" href="#/coach-fala?mode=repeat">Abrir o modo bloco</a></p>
        <h3>Take an Interview</h3><p>Quatro perguntas, 45 segundos, sem preparação. A primeira é fato ou experiência. As outras pedem opinião. Estrutura: resposta direta, motivo, exemplo. Fale até o relógio ficar baixo. Um um ou uh natural não derruba a nota 5 do exemplo oficial; muitos fillers e pausa longa, sim.</p>
        <p><a class="btn small" href="#/coach-fala?mode=interview">Treinar entrevista</a></p>`,
      videos: "fala"
    }
  };

  function guia(key) {
    const g = GUIAS[key];
    root.innerHTML = `<p class="kicker">Tarefa</p><h1>${esc(g.title)}</h1><article class="card">${g.body}<h3>Aulas em vídeo</h3>${videosFor(g.videos)}<p class="muted">Os vídeos são de terceiros. A estratégia deles não substitui o PDF da ETS quando os dois divergem.</p></article>`;
  }

  function pratica(r) {
    const task = r.parts[1];
    if (!task) {
      const items = [
        ["ctw", "Complete the Words"],
        ["daily", "Read in Daily Life"],
        ["academic", "Passagem acadêmica"],
        ["choose", "Choose a Response"],
        ["conversation", "Conversas"],
        ["announcement", "Anúncios"],
        ["talk", "Palestras"],
        ["bas", "Build a Sentence"]
      ];
      root.innerHTML = `<h1>Prática autoral</h1><p>Não são questões da ETS. A correção é na hora. Itens que você erra voltam em <a href="#/erros">Erros</a>.</p><div class="grid-2">${items.map(([id, name]) => '<a class="card" href="#/pratica/' + id + '"><h2>' + name + "</h2><span class=\"muted\">Abrir uma série</span></a>").join("")}</div>`;
      return;
    }
    runPractice(task, Number(r.q.n || 0) || defaultN(task));
  }

  function defaultN(task) {
    return { ctw: 1, daily: 2, academic: 1, choose: 6, conversation: 2, announcement: 2, talk: 1, bas: 8 }[task] || 5;
  }

  let practice = null;
  function runPractice(task, n) {
    const pool = (bank[task] || []).filter((x) => x.pool === "practice");
    const dueIds = new Set(Store.get().errors.filter((e) => e.task === task && e.due <= Date.now()).map((e) => e.id));
    const due = pool.filter((x) => dueIds.has(x.id));
    const rest = pool.filter((x) => !dueIds.has(x.id));
    shuffle(rest);
    const items = due.concat(rest).slice(0, Math.max(1, n));
    practice = { task, items, i: 0, revealed: false, picked: null };
    showPracticeItem();
  }
  function shuffle(a) { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } }

  function showPracticeItem() {
    const p = practice;
    if (!p || p.i >= p.items.length) {
      root.innerHTML = `<div class="card"><h1>Série fechada</h1><p>Os erros já estão na fila espaçada.</p><p><a class="btn" href="#/pratica">Outra tarefa</a> <a class="btn secondary" href="#/">Voltar ao plano</a></p></div>`;
      return;
    }
    const item = p.items[p.i];
    root.innerHTML = `<p class="kicker">Prática autoral · ${p.i + 1} / ${p.items.length}</p><div class="card" id="stage"></div><div id="feedback"></div>`;
    const stage = root.querySelector("#stage");
    if (p.task === "ctw") {
      stage.innerHTML = "<h2>Fill in the missing letters.</h2><div id=\"host\" class=\"passage\"></div><button class=\"btn\" id=\"go\">Corrigir</button>";
      const api = Widgets.mountCTW(stage.querySelector("#host"), item, {});
      stage.querySelector("#go").onclick = () => {
        const sc = api.score();
        sc.gaps.forEach((g, i) => {
          const ok = (sc.got[i] || "").toLowerCase() === g.missing.toLowerCase();
          Store.bump("ctw", ok);
        });
        Store.gradeError(item.id, "ctw", sc.hit === sc.total, {});
        api.score();
        Widgets.mountCTW(stage.querySelector("#host"), item, { initial: sc.got, locked: true, reveal: true });
        root.querySelector("#feedback").innerHTML = `<div class="note">${sc.hit} de ${sc.total}. ${esc(item.why || "")}</div><button class="btn" id="next">Próxima</button>`;
        root.querySelector("#next").onclick = () => { p.i += 1; showPracticeItem(); };
      };
      return;
    }
    if (p.task === "bas") {
      stage.innerHTML = `<p class="tag">${esc(item.pattern)}</p><h2>${esc(item.prompt)}</h2><div id="host"></div><button class="btn" id="go">Corrigir</button>`;
      const api = Widgets.mountBAS(stage.querySelector("#host"), item, {});
      stage.querySelector("#go").onclick = () => {
        const ok = api.correct();
        Store.bump("bas", ok);
        Store.gradeError(item.id, "bas", ok, {});
        root.querySelector("#feedback").innerHTML = `<div class="${ok ? "note" : "callout-bad"}">${ok ? "Ordem certa." : "A ordem do gabarito é: " + esc(item.answer.join(" "))}</div><p>${esc(item.why || "")}</p><button class="btn" id="next">Próxima</button>`;
        root.querySelector("#next").onclick = () => { p.i += 1; showPracticeItem(); };
      };
      return;
    }
    const listening = ["choose", "conversation", "announcement", "talk"].includes(p.task);
    if (listening && !p.heard) {
      const script = p.task === "choose" ? item.line : p.task === "conversation" ? item.lines.map((l) => l.who + ": " + l.text).join(". ") : item.script;
      stage.innerHTML = `<h2>${p.task === "choose" ? "Listen and choose a response" : "Listen. The transcript stays hidden."}</h2><p id="st">Preparando a voz do navegador…</p><button class="btn" id="play">Ouvir uma vez</button>`;
      stage.querySelector("#play").onclick = async () => {
        stage.querySelector("#play").disabled = true;
        stage.querySelector("#st").textContent = "Ouvindo…";
        await AudioKit.speak(script);
        p.heard = true;
        showPracticeItem();
      };
      return;
    }
    const questions = p.task === "choose" ? [{ q: "Choose the best response.", options: item.options, a: item.a, why: item.why }] : item.questions;
    const qi = p.qi || 0;
    const q = questions[qi];
    const passage = p.task === "daily" || p.task === "academic" ? `<div class="passage">${esc(item.text)}</div>` : "";
    stage.innerHTML = passage + `<h3>${esc(q.q)}</h3>` + q.options.map((op, i) => `<button class="q-option" data-a="${i}">${esc(op)}</button>`).join("") + `<p><button class="btn" id="go">Corrigir</button></p>`;
    let picked = null;
    stage.querySelectorAll(".q-option").forEach((btn) => btn.onclick = () => {
      picked = Number(btn.dataset.a);
      stage.querySelectorAll(".q-option").forEach((b) => b.classList.remove("picked"));
      btn.classList.add("picked");
    });
    stage.querySelector("#go").onclick = () => {
      const ok = picked === q.a;
      Store.bump(p.task, ok);
      Store.gradeError(item.id, p.task, ok, {});
      stage.querySelectorAll(".q-option").forEach((btn) => {
        const i = Number(btn.dataset.a);
        if (i === q.a) btn.classList.add("good");
        else if (i === picked) btn.classList.add("bad");
      });
      let extra = "";
      const lastQ = qi + 1 >= questions.length;
      if (listening && lastQ) {
        const script = p.task === "choose" ? item.line : p.task === "conversation" ? item.lines.map((l) => l.who + ": " + l.text).join("\n") : item.script;
        extra = `<h3>Transcrição, só agora</h3><div class="passage">${esc(script)}</div>`;
      }
      root.querySelector("#feedback").innerHTML = `<div class="${ok ? "note" : "callout-bad"}">${esc(q.why || "")}</div>${extra}<button class="btn" id="next">Continuar</button>`;
      root.querySelector("#next").onclick = () => {
        if (qi + 1 < questions.length) { p.qi = qi + 1; showPracticeItem(); }
        else { p.i += 1; p.qi = 0; p.heard = false; showPracticeItem(); }
      };
    };
  }

  function simulado(r) {
    const id = r.parts[1];
    if (id === "1" || id === "2") {
      if (r.q.novo === "1" || !Store.get().mockRun || String(Store.get().mockRun.mockId) !== id) {
        const run = ExamKit.fresh(Number(id));
        Store.get().mockRun = run;
        Store.save();
      }
      document.getElementById("site-header").classList.add("hidden");
      document.getElementById("site-footer").classList.add("hidden");
      ExamKit.render(root, bank);
      return;
    }
    const c1 = ExamKit.assemble(bank, 1);
    const c2 = ExamKit.assemble(bank, 2);
    const info = (c, n) => {
      const r1 = ExamKit.countReading(c.reading.m1), rU = ExamKit.countReading(c.reading.upper), rL = ExamKit.countReading(c.reading.lower);
      const l1 = ExamKit.countListening(c.listening.m1), lU = ExamKit.countListening(c.listening.upper);
      return `<p>Reading ${r1}+${rU} (fácil ${rL}). Listening ${l1}+${lU}. Build a Sentence: ${c.bas.length}. E-mail: ${c.email ? "sim" : "não"}. Discussão: ${c.discussion ? "sim" : "não"}. Repetir: ${c.repeat ? c.repeat.sentences.length : 0}. Entrevista: ${c.interview ? c.interview.questions.length : 0}.</p>`;
    };
    root.innerHTML = `<h1>Dois simulados</h1>
      <div class="warn"><b>Estimativa, não nota.</b> A ETS não publica a fórmula que transforma acertos em banda. O segundo módulo fica mais difícil se o primeiro passa de 65%. Esse corte é deste site. Itens em branco contam como erro. Não dá para voltar onde a prova não deixa.</div>
      <div class="grid-2" style="margin-top:12px">
        <article class="card"><h2>Simulado 1</h2>${info(c1, 1)}<a class="btn" href="#/simulado/1?novo=1">Começar</a></article>
        <article class="card"><h2>Simulado 2</h2>${info(c2, 2)}<a class="btn" href="#/simulado/2?novo=1">Começar</a></article>
      </div>
      <p class="muted">Se a contagem não for 50 de Reading e 47 de Listening, o banco não fechou o formulário. A tela mostra os números reais carregados.</p>`;
  }

  function resultado() {
    const res = Store.get().lastResult || Store.get().mocks[Store.get().mocks.length - 1];
    if (!res) { root.innerHTML = "<p>Nenhum resultado ainda.</p>"; return; }
    const b = res.bands;
    root.innerHTML = `<p class="kicker">Estimativa</p><h1>Simulado ${res.mockId}</h1>
      <div class="callout-bad"><b>Isto não é banda oficial.</b> Reading e Listening usam a porcentagem, com teto 4,0 se o módulo 2 foi o fácil. Writing soma acertos de Build a Sentence (0–10) e uma lista automática do e-mail e da discussão (0–5 cada). Speaking mistura a precisão da repetição e o tamanho da entrevista. A média segue o arredondamento para meia banda, no espírito do exemplo oficial, mas a escala não foi calibrada pela ETS.</div>
      <div class="grid-4" style="margin-top:12px">
        ${stat("Reading", b.reading)}
        ${stat("Listening", b.listening)}
        ${stat("Writing", b.writing)}
        ${stat("Speaking", b.speaking == null ? "sem áudio" : b.speaking)}
      </div>
      <p>Geral estimada: <b>${res.overall ?? "—"}</b>. B2 começa em 4. Rotas: Reading ${esc(res.routes.reading)}, Listening ${esc(res.routes.listening)}.</p>
      <div class="card"><h2>Contas</h2>
        <p>Reading ${res.read.hit}/${res.read.total}. Listening ${res.lis.hit}/${res.lis.total}. Build a Sentence ${res.bas.hit}/${res.bas.total}. Lista do e-mail ${res.emailScore}/5. Lista da discussão ${res.discScore}/5. Bruto de writing usado na conta: ${res.rawW}/20.</p>
      </div>
      <p><a class="btn" href="#/erros">Ver erros</a> <a class="btn secondary" href="#/">Plano</a></p>`;
  }

  let coach = null;
  function coachFala(r) {
    const mode = r.q.mode || "repeat";
    const scenarios = bank.repeat.filter((x) => x.pool === "practice");
    const interviews = bank.interview.filter((x) => x.pool === "practice");
    if (!coach || coach.kind !== mode) {
      coach = { kind: mode, si: 0, ii: 0, slow: false, chunk: false, chunkAt: 0 };
    }
    const sc = scenarios[coach.si % scenarios.length];
    const iv = interviews[coach.ii % interviews.length];
    root.innerHTML = `<p class="kicker">Coach de fala</p><h1>${mode === "interview" ? "Take an Interview" : "Listen and Repeat"}</h1>
      <div class="row">
        <a class="btn ${mode !== "interview" ? "" : "secondary"}" href="#/coach-fala?mode=repeat">Repetir</a>
        <a class="btn ${mode === "interview" ? "" : "secondary"}" href="#/coach-fala?mode=interview">Entrevista</a>
      </div>
      <div class="card" id="coach" style="margin-top:12px"></div>`;
    const host = root.querySelector("#coach");
    if (mode !== "interview") {
      const sent = sc.sentences[coach.chunkAt] || sc.sentences[0];
      host.innerHTML = `<p class="tag">${esc(sc.scenario)}</p>
        <p>Frase ${coach.chunkAt + 1} de ${sc.sentences.length}. Se o meio da frase some, ligue o modo bloco: cada pedaço de sentido toca e pausa.</p>
        <div class="row">
          <button class="btn" id="play">Ouvir frase inteira</button>
          <button class="btn secondary" id="chunks">Modo bloco</button>
          <button class="btn ghost" id="slow">Mais devagar</button>
        </div>
        <p id="live" class="muted"></p>
        <div id="diff"></div>
        <audio id="replay" controls class="hidden"></audio>
        <div class="note"><b>Como segurar a frase.</b> Não traduza. Olhe o cenário e quebre em quem / faz o quê / onde. Fale o primeiro bloco assim que ele acabar, mesmo no treino. Na prova há uma tentativa só. As palavras curtas são as que caem: marque-as no diff.</div>
        <p><button class="btn ghost small" id="another">Outro cenário</button></p>`;
      host.querySelector("#another").onclick = () => { coach.si += 1; coach.chunkAt = 0; coachFala(r); };
      host.querySelector("#play").onclick = () => doRepeat(sent, false);
      host.querySelector("#chunks").onclick = () => playChunks(sent);
      host.querySelector("#slow").onclick = () => doRepeat(sent, true);
    } else {
      const q = iv.questions[Math.min(coach.q || 0, 3)];
      const n = Number(r.q.n || 4);
      host.innerHTML = `<p>${esc(iv.scenario)}</p><h2>${esc(q.text)}</h2>
        <p class="muted">Foco: ${esc(q.focus)}. 45 segundos, sem preparação. Fale a resposta, o motivo e um exemplo.</p>
        <button class="btn" id="go">Ouvir e gravar 45 s</button>
        <p id="live"></p><audio id="replay" controls class="hidden"></audio><div id="metrics"></div>`;
      host.querySelector("#go").onclick = () => doInterview(q, iv, n);
    }
  }

  async function playChunks(sent) {
    for (const chunk of sent.chunks) {
      await AudioKit.speak(chunk, { rate: 0.86 });
      await new Promise((res) => setTimeout(res, 700));
    }
    const live = document.getElementById("live");
    if (live) live.textContent = "Agora a frase inteira, uma vez.";
    await doRepeat(sent, false);
  }
  async function doRepeat(sent, slow) {
    const live = document.getElementById("live");
    live.textContent = "Ouvindo…";
    await AudioKit.speak(sent.text, { rate: slow ? 0.78 : 0.96 });
    live.textContent = "Sua vez. Gravando 12 segundos.";
    try {
      const rec = await AudioKit.recordFor(12000, (t) => { live.textContent = t; });
      const diff = AudioKit.align(sent.text, rec.transcript);
      const box = document.getElementById("diff");
      box.innerHTML = `<p>Precisão: <b>${Math.round(diff.accuracy * 100)}%</b> (${diff.hit}/${diff.target}).</p><p class="diff">` + diff.tokens.map((tk) => `<span class="${tk.ok ? "ok" : tk.extra ? "extra" : "miss"}">${esc(tk.t)}</span>`).join(" ") + "</p><p class=\"muted\">Vermelho: faltou ou saiu diferente. Laranja: você acrescentou.</p>";
      const audio = document.getElementById("replay");
      audio.src = rec.url; audio.classList.remove("hidden");
      Store.bump("repeat", diff.accuracy >= 0.9);
      Store.gradeError("repeat:" + sent.text, "repeat", diff.accuracy >= 0.9, {});
      if (!rec.recognition) box.innerHTML += "<p>Este navegador não transcreveu. O áudio está aí para você ouvir.</p>";
    } catch (e) {
      live.textContent = "O microfone não abriu. Dá para ouvir e repetir mesmo assim; a nota automática precisa da permissão.";
    }
  }
  async function doInterview(q, iv, n) {
    const live = document.getElementById("live");
    await AudioKit.speak(q.text);
    live.textContent = "Gravando 45 segundos.";
    try {
      const rec = await AudioKit.recordFor(45000, (t) => { live.textContent = t; });
      const words = AudioKit.tokenize(rec.transcript);
      const fillers = (rec.transcript.match(AudioKit.FILLERS) || []).length;
      const wpm = Math.round(words.length / (45 / 60));
      const uniq = new Set(words).size;
      document.getElementById("metrics").innerHTML = `<div class="grid-3">
        <div class="stat"><b>${words.length}</b> palavras</div>
        <div class="stat"><b>${wpm}</b> palavras/min</div>
        <div class="stat"><b>${fillers}</b> fillers</div>
        <div class="stat"><b>${rec.pauses}</b> pausas longas</div>
        <div class="stat"><b>${uniq}</b> palavras diferentes</div>
        <div class="stat"><b>${words.length >= 60 ? "tamanho ok" : "curta"}</b> meta ~60–110</div>
      </div><p class="muted">Pausa longa aqui é silêncio de cerca de 0,7 s. O microfone do notebook conta ruído da sala, então o número é uma pista, não um laudo.</p>
      <button class="btn" id="copy">Copiar prompt de correção</button> <button class="btn secondary" id="ai">Pedir nota à API, se houver chave</button><pre id="out"></pre>`;
      const audio = document.getElementById("replay");
      audio.src = rec.url; audio.classList.remove("hidden");
      const prompt = buildPrompt("interview", q.text + "\n\nCenário: " + iv.scenario, rec.transcript);
      document.getElementById("copy").onclick = () => copyPrompt(prompt);
      document.getElementById("ai").onclick = () => callModel(prompt, document.getElementById("out"));
      coach.q = ((coach.q || 0) + 1) % Math.min(n, 4);
    } catch (e) {
      live.textContent = "Sem microfone nesta tentativa.";
    }
  }

  function coachEscrita(r) {
    const task = r.q.task === "discussion" ? "discussion" : "email";
    const list = bank[task].filter((x) => x.pool === "practice");
    const idx = Number(sessionStorage.getItem("widx") || 0) % list.length;
    const item = list[idx];
    const seconds = task === "email" ? 7 * 60 : 10 * 60;
    root.innerHTML = `<p class="kicker">Coach de escrita</p><h1>${task === "email" ? "Write an Email · 7 min" : "Academic Discussion · 10 min"}</h1>
      <div class="card" id="w"></div>`;
    const host = root.querySelector("#w");
    let html = "";
    if (task === "email") {
      html += `<p><b>To:</b> ${esc(item.to)} · <b>Subject:</b> ${esc(item.subject)}</p><p>${esc(item.scenario)}</p><ul>${item.bullets.map((b) => "<li>" + esc(b) + "</li>").join("")}</ul>`;
    } else {
      html += `<p>${esc(item.course)}</p><div class="passage"><b>Professor.</b> ${esc(item.question)}</div><div class="passage"><b>${esc(item.s1.name)}.</b> ${esc(item.s1.text)}</div><div class="passage"><b>${esc(item.s2.name)}.</b> ${esc(item.s2.text)}</div>`;
    }
    html += `<p class="timer" id="clock">${fmt(seconds)}</p><textarea id="essay"></textarea><p><span id="wc">0</span> palavras</p>
      <div class="row"><button class="btn" id="start">Começar o relógio</button><button class="btn secondary" id="check">Lista de checagem</button><button class="btn ghost" id="copy">Copiar prompt</button><button class="btn ghost" id="ai">API, se houver chave</button><button class="btn ghost" id="swap">Outro enunciado</button></div>
      <div id="list"></div><pre id="out"></pre>`;
    host.innerHTML = html;
    const area = host.querySelector("#essay");
    area.addEventListener("input", () => { host.querySelector("#wc").textContent = AudioKit.tokenize(area.value).length; });
    let left = seconds, iv = null;
    host.querySelector("#start").onclick = () => {
      if (iv) return;
      iv = setInterval(() => {
        left -= 1;
        host.querySelector("#clock").textContent = fmt(left);
        if (left <= 0) { clearInterval(iv); iv = null; }
      }, 1000);
    };
    function checks() {
      return task === "email" ? Widgets.emailChecks(item, area.value) : Widgets.discussionChecks(item, area.value);
    }
    host.querySelector("#check").onclick = () => {
      const c = checks();
      host.querySelector("#list").innerHTML = Widgets.renderChecks(c) + `<p>Lista automática: ${Widgets.heuristicBand(c)} / 5. Não é a rubrica humana da ETS.</p>`;
    };
    host.querySelector("#copy").onclick = () => copyPrompt(writingPrompt(task, item, area.value));
    host.querySelector("#ai").onclick = () => callModel(writingPrompt(task, item, area.value), host.querySelector("#out"));
    host.querySelector("#swap").onclick = () => { sessionStorage.setItem("widx", String(idx + 1)); coachEscrita(r); };
  }
  function fmt(sec) {
    sec = Math.max(0, sec);
    return String(Math.floor(sec / 60)).padStart(2, "0") + ":" + String(sec % 60).padStart(2, "0");
  }

  function rubricText(kind) {
    if (kind === "email") return "Rubrica da tarefa Write an Email, resumida do overview da ETS (0 a 5, não a banda 1–6): 5 = propósito bem elaborado, variedade sintática, vocabulário preciso, convenções sociais estáveis, quase sem erros além de deslize de tempo. 4 = claro, elaboração suficiente, poucas falhas. 3 = cumpre em parte, erros visíveis de forma ou tom. 2 = tentativa, elaboração fraca, erros acumulados. 1 = mensagem quase não sai. 0 = vazio, fora do tema ou copiado.";
    if (kind === "discussion") return "Rubrica da Academic Discussion (0 a 5): 5 = contribuição clara, exemplos e detalhes, variedade, quase sem erros de tempo. 4 = relevante e fácil de ler, elaboração adequada. 3 = em parte faltando exemplo ou clareza. 2 = pouco desenvolvido. 1 = sem ideia coerente ou cópia do enunciado. 0 = vazio ou fora de tema. A instrução pede pelo menos 100 palavras.";
    return "Rubrica de Take an Interview (0 a 5): 5 = no tema, elaborado, ritmo de conversa, pronúncia inteligível, gramática e vocabulário que precisem a ideia. 4 = claro, alguma pausa que não quebra o fluxo. 3 = elaboração curta, pausa e filler frequentes, vocabulário limitado. 2 = quase não desenvolve. 1 = frases soltas. 0 = mudo ou ininteligível. Para Listen and Repeat, 5 é repetição exata e inteligível; 4 admite troca pequena que não muda o sentido.";
  }
  function writingPrompt(task, item, text) {
    const stimulus = task === "email"
      ? `To: ${item.to}\nSubject: ${item.subject}\n${item.scenario}\nBullets:\n- ${item.bullets.join("\n- ")}`
      : `Course: ${item.course}\nProfessor: ${item.question}\n${item.s1.name}: ${item.s1.text}\n${item.s2.name}: ${item.s2.text}`;
    return buildPrompt(task, stimulus, text);
  }
  function buildPrompt(kind, stimulus, response) {
    return `Você é um avaliador do TOEFL iBT no formato de 2026. Responda em português, com exemplos em inglês.\n\n${rubricText(kind)}\n\nTarefa:\n${stimulus}\n\nResposta da candidata:\n${response || "(vazia)"}\n\nDevolva:\n1. Nota da tarefa de 0 a 5 e uma banda estimada de 1 a 6 para esta habilidade, deixando claro que é estimativa.\n2. O que a resposta cumpre e o que falta.\n3. Erros concretos de gramática, vocabulário e tarefa, com a forma corrigida.\n4. Uma versão melhorada, no nível B2, sem ficar artificialmente perfeita.\n5. Um único foco para o próximo treino de 10 minutos.`;
  }
  function copyPrompt(text) {
    navigator.clipboard.writeText(text).then(() => alert("Prompt copiado. Cole no ChatGPT, no Grok ou no Gemini.")).catch(() => {
      const ta = document.createElement("textarea");
      ta.value = text; document.body.appendChild(ta); ta.select();
      document.execCommand("copy"); ta.remove();
      alert("Prompt copiado.");
    });
  }
  async function callModel(prompt, out) {
    const api = Store.get().api;
    if (!api.key) {
      out.textContent = "Sem chave. Use Copiar prompt, ou grave uma chave na página Dia da prova → Ferramenta de correção. A chave fica só neste navegador.";
      return;
    }
    out.textContent = "Chamando o modelo a partir deste navegador…";
    try {
      let text = "";
      if (api.provider === "gemini") {
        const url = "https://generativelanguage.googleapis.com/v1beta/models/" + encodeURIComponent(api.geminiModel || "gemini-2.5-flash") + ":generateContent?key=" + encodeURIComponent(api.key);
        const res = await fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] }) });
        const data = await res.json();
        if (!res.ok) throw new Error(JSON.stringify(data).slice(0, 400));
        text = data.candidates?.[0]?.content?.parts?.map((p) => p.text).join("\n") || JSON.stringify(data).slice(0, 800);
      } else {
        const base = (api.baseUrl || "https://api.openai.com/v1").replace(/\/$/, "");
        const res = await fetch(base + "/chat/completions", {
          method: "POST",
          headers: { "Content-Type": "application/json", Authorization: "Bearer " + api.key },
          body: JSON.stringify({ model: api.model || "gpt-4o-mini", messages: [{ role: "user", content: prompt }] })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(JSON.stringify(data).slice(0, 400));
        text = data.choices?.[0]?.message?.content || JSON.stringify(data).slice(0, 800);
      }
      out.textContent = text;
    } catch (e) {
      out.textContent = "A chamada falhou. Muitos provedores bloqueiam o navegador (CORS). Nesse caso, use o prompt copiado. Detalhe: " + e.message;
    }
  }

  let card = null;
  function vocab() {
    const due = bank.vocab.filter((v) => ((Store.get().vocab[v.id] || {}).due || 0) <= Date.now());
    const pile = due.length ? due : bank.vocab;
    if (!card || !pile.find((v) => v.id === card.id)) card = pile[Math.floor(Math.random() * pile.length)];
    root.innerHTML = `<h1>Vocabulário</h1><p>${due.length} cartões para hoje, de ${bank.vocab.length}. Campus e texto acadêmico. A resposta fica só neste navegador.</p>
      <div class="card flash" id="flash"><div><p class="tag">${esc(card.topic)} · ${esc(card.pos)}</p><b>${esc(card.w)}</b><p id="back" class="hidden">${esc(card.pt)}<br><span class="muted">${esc(card.ex)}</span></p><p class="muted">Toque para virar</p></div></div>
      <div class="row" style="margin-top:10px">
        <button class="btn clay" id="again">De novo</button>
        <button class="btn secondary" id="hard">Difícil</button>
        <button class="btn" id="good">Lembrei</button>
        <button class="btn ghost" id="easy">Fácil</button>
      </div>`;
    root.querySelector("#flash").onclick = () => root.querySelector("#back").classList.toggle("hidden");
    ["again", "hard", "good", "easy"].forEach((id) => {
      root.querySelector("#" + id).onclick = () => { Store.gradeVocab(card.id, id); card = null; vocab(); };
    });
  }

  function erros() {
    const now = Date.now();
    const list = Store.get().errors.slice().sort((a, b) => a.due - b.due);
    root.innerHTML = `<h1>Fila de erros</h1><p>O que você errou volta no mesmo dia e, se acertar, vai para 1 dia, 3 dias e depois mais espaçado. Isso é recuperação ativa, não uma nota.</p>
      ${list.length ? "" : "<p>Nenhum erro guardado ainda. Faça uma série de prática.</p>"}
      <div class="stack">${list.slice(0, 40).map((e) => `<div class="card"><b>${esc(e.task)}</b> · ${esc(e.id)}<div class="muted">${e.due <= now ? "venceu" : "volta em " + Math.ceil((e.due - now) / 86400000) + " dia(s)"} · lapsos ${e.lapses || 0}</div></div>`).join("")}</div>
      <p><a class="btn" href="#/pratica/bas?n=8">Refazer Build a Sentence</a></p>`;
  }

  function materiais() {
    const rows = [
      ["2026", "Página de conteúdo, tempos e tarefas", "https://www.ets.org/toefl/test-takers/ibt/about/content.html", "Fonte dos 50/30, 47/29, 12/23, 11/8 e da regra de não pular seção."],
      ["2026", "Overview em PDF, tarefas, exemplos e rubricas", "https://www.ets.org/pdfs/toefl/toefl-ibt-test-overview.pdf", "Não baixamos o PDF para este site. Abra na ETS."],
      ["2026, com ressalva", "At a glance", "https://www.ets.org/pdfs/toefl/toefl-ibt-test-at-a-glance.pdf", "Ainda mostra faixas 35–48 e 35–45 e a nota de que os números podiam mudar antes de 21/01/2026."],
      ["2026, pré-lançamento", "Blueprint de especificações", "https://www.ets.org/pdfs/toefl/toefl-ibt-test-specifications-2026.pdf", "Tempos de módulo. O próprio PDF dizia que podia ser revisado até o lançamento."],
      ["2026", "Escala 1–6, CEFR", "https://www.ets.org/toefl/institutions/ibt/score-scale-update.html", "4 e 4,5 = B2 em todas as seções."],
      ["2026", "Relatório da escala", "https://www.ets.org/pdfs/toefl/score-scale-update-2026.pdf", "Tabela de concordância com 0–30 e 0–120."],
      ["2026", "Amostra interativa gratuita", "https://ibt2-toefl-pt.ets.org/dg?code=A01&tst=TELENKSAM", "Botão da página de preparação em 10/11/2026. Pode pedir cadastro."],
      ["2026", "Full-Length Practice Test 1", "https://www.ets.org/toefl/test-takers/ibt/prepare/sample-test-jan-2026-1.html", "Página oficial. O PDF em papel não é réplica adaptativa."],
      ["2026", "Full-Length Practice Test 2", "https://www.ets.org/toefl/test-takers/ibt/prepare/sample-test-jan-2026-2.html", "Guarde um teste para a reta final."],
      ["2026", "PDF Practice Test 1", "https://www.ets.org/pdfs/toefl/toefl-ibt-full-length-practice-test-1.pdf", "Papel. Para escuta, use a versão interativa se houver áudio."],
      ["2026", "PDF Practice Test 2", "https://www.ets.org/pdfs/toefl/toefl-ibt-full-length-practice-test-2.pdf", "Idem."],
      ["2026", "Preparação, produtos gratuitos", "https://www.ets.org/toefl/test-takers/ibt/prepare.html", "Em 10/11/2026 os grátis nomeados eram Interactive Sample e os dois full-length tests."],
      ["Home", "Requisitos de equipamento", "https://www.ets.org/toefl/test-takers/ibt/register/at-home-requirements.html", "Sem fone. Um monitor. Windows 11 ou macOS 10.13+."],
      ["Home", "Dia da prova em casa", "https://www.ets.org/toefl/test-takers/ibt/test-day/at-home-test-day.html", "Check-in, fiscal, o que cancela a nota."],
      ["Legado, conferir", "Writing rubrics PDF antigo", "https://www.ets.org/pdfs/toefl/writing-rubrics.pdf", "O arquivo existe. As rubricas novas de e-mail e discussão estão no overview de 2026."],
      ["Legado, conferir", "Lesson plan de writing", "https://www.ets.org/pdfs/toefl/toefl-ibt-lesson-plan-writing.pdf", "Material anterior. Não é o foco das tarefas novas."],
      ["Legado", "Free practice antigo", "https://www.ets.org/s/toefl/free-practice/index.html", "O endereço respondeu, mas o conteúdo útil não pôde ser lido daqui. Provável formato pré-2026."],
      ["Canal oficial", "TOEFL TV", "https://www.youtube.com/@TOEFLtv", "Canal da ETS. A playlist Inside the TOEFL vista em busca estava atualizada em 2023 e ensina tarefas antigas (prose summary, insert text). Serve para vocabulário e inferência, não para Listen and Repeat."],
      ["2026, não oficial", "TST Prep, prática", "https://tstprep.com/articles/toefl/complete-practice-test-for-the-toefl-test/", "Útil e alinhado ao formato novo. Não é ETS. É a fonte do relógio de 5:50 do Build a Sentence."]
    ];
    root.innerHTML = `<h1>Materiais oficiais, por link</h1><p>Nada disso foi copiado para este site. A lista separa formato 2026 e material anterior.</p>
      ${rows.map((r) => `<article class="card" style="margin-bottom:10px"><span class="tag">${esc(r[0])}</span><h3><a href="${esc(r[2])}" target="_blank" rel="noopener">${esc(r[1])}</a></h3><p>${esc(r[3])}</p><p class="muted">${esc(r[2])}</p></article>`).join("")}
      <p>O registro completo das fontes, inclusive o que não bate entre PDFs, está em <code>docs/format-sources.md</code> no repositório.</p>`;
  }

  function prova() {
    const s = Store.get();
    const items = [
      ["app", "App da ETS instalado e Equipment Check feito no mesmo dia da semana e horário da prova"],
      ["pc", "Notebook ou desktop na tomada, um monitor, um teclado, Windows 11+ ou macOS 10.13+"],
      ["audio", "Alto-falante e microfone que não sejam headset. Fone fica fora"],
      ["cam", "Câmera que gira 360°, inclusive embaixo da mesa"],
      ["cam2", "Segunda câmera conferida no seu agendamento: a ETS diz “se aplicável” nos requisitos e inclui o passo no check-in"],
      ["sala", "Sozinha, portas fechadas, vidro coberto, parede sem material de prova, cadeira comum"],
      ["notas", "Quadro branco pequeno ou folha dentro de plástico, com marcador apagável. Sem caneta"],
      ["id", "Passaporte ou documento aceito, e a verificação Entrust se a inscrição pedir"],
      ["net", "Apps, navegadores e acesso remoto fechados. Zoom e semelhantes não podem abrir sozinhos"],
      ["corpo", "Rosto e orelhas visíveis, sem máscara, sem relógio inteligente"]
    ];
    root.innerHTML = `<h1>Dia da prova em casa</h1>
      <div class="warn">Não há intervalo programado. Na Home Edition, “taking a break” está na lista de comportamentos que podem cancelar a nota. Se o equipamento falhar no dia, a ETS diz que não há reembolso nem remarcação gratuita.</div>
      <div class="card" style="margin-top:12px"><h2>Check-list</h2>
        ${items.map(([id, label]) => `<label class="checkline"><input type="checkbox" data-id="${id}" ${s.homeChecks[id] ? "checked" : ""}><span>${esc(label)}</span></label>`).join("")}
      </div>
      <article class="card" style="margin-top:12px"><h2>Na hora</h2>
        <ol>
          <li>Abra o teste pelo e-mail de confirmação ou pelo My TOEFL Home. O app entra numa sala de espera.</li>
          <li>Conecte a segunda câmera se for o seu caso, faça a identidade e mostre a sala.</li>
          <li>O fiscal fala por câmera e chat. Se precisar dele, fale ou abra o chat e espere.</li>
          <li>Reading e Listening: o tempo do módulo é contínuo. Não volte ao módulo anterior. Na escuta, não volte à questão.</li>
          <li>E-mail: 7 minutos, três pontos. Discussão: 10 minutos, 100 palavras ou mais.</li>
          <li>Repetição: comece a falar na hora. Entrevista: 45 segundos, sem preparação.</li>
          <li>No fim, Reading e Listening mostram uma nota não oficial e você pode reportar ou cancelar. Apague o quadro e mostre os dois lados.</li>
        </ol>
        <p>Última semana: um simulado, a autópsia no dia seguinte, e só erros recorrentes. Nas últimas 48 horas, nada de formulário novo. Na véspera, sono e a sala pronta.</p>
        <p><a href="https://www.ets.org/toefl/test-takers/ibt/register/at-home-requirements.html" target="_blank" rel="noopener">Requisitos</a> · <a href="https://www.ets.org/toefl/test-takers/ibt/test-day/at-home-test-day.html" target="_blank" rel="noopener">Dia da prova</a></p>
      </article>
      <article class="card" style="margin-top:12px"><h2>Correção por IA, opcional</h2>
        <p>O botão de copiar o prompt funciona sem chave. Se você colar uma chave, ela fica só no localStorage deste navegador. Este site estático não tem servidor e não envia a chave para lugar nenhum além do provedor que você escolher. Quem usar o computador pode ler a chave nas ferramentas do navegador. Não coloque a chave em nenhum arquivo do projeto.</p>
        <div class="grid-2">
          <label class="field">Provedor
            <select id="prov"><option value="openai" ${s.api.provider !== "gemini" ? "selected" : ""}>Compatível com OpenAI</option><option value="gemini" ${s.api.provider === "gemini" ? "selected" : ""}>Gemini</option></select>
          </label>
          <label class="field">Chave <input id="key" type="password" autocomplete="off" value="${esc(s.api.key || "")}"></label>
          <label class="field">URL base (OpenAI ou compatível) <input id="base" type="url" value="${esc(s.api.baseUrl)}"></label>
          <label class="field">Modelo OpenAI <input id="model" type="text" value="${esc(s.api.model)}"></label>
          <label class="field">Modelo Gemini <input id="gmodel" type="text" value="${esc(s.api.geminiModel)}"></label>
        </div>
        <p><button class="btn" id="saveapi">Guardar neste navegador</button> <button class="btn ghost" id="wipe">Apagar a chave</button></p>
        <p class="muted">Se o provedor bloquear CORS, a chamada direta falha e o prompt copiado continua valendo. O nome do modelo muda com o tempo; se a API recusar, troque o campo.</p>
      </article>
      <article class="card" style="margin-top:12px"><h2>Cópia de segurança do progresso</h2>
        <p>A cópia não inclui a chave.</p>
        <button class="btn secondary" id="exp">Baixar JSON</button>
        <label class="btn ghost">Trazer JSON <input id="imp" type="file" accept="application/json" class="hidden"></label>
      </article>`;
    root.querySelectorAll("input[type=checkbox]").forEach((box) => box.onchange = () => {
      Store.get().homeChecks[box.dataset.id] = box.checked; Store.save();
    });
    root.querySelector("#saveapi").onclick = () => {
      Store.get().api = {
        provider: root.querySelector("#prov").value,
        key: root.querySelector("#key").value.trim(),
        baseUrl: root.querySelector("#base").value.trim(),
        model: root.querySelector("#model").value.trim(),
        geminiModel: root.querySelector("#gmodel").value.trim()
      };
      Store.save();
      alert("Guardado só neste navegador.");
    };
    root.querySelector("#wipe").onclick = () => { Store.get().api.key = ""; Store.save(); root.querySelector("#key").value = ""; };
    root.querySelector("#exp").onclick = () => {
      const blob = new Blob([Store.backup()], { type: "application/json" });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob); a.download = "meu-toefl-progresso.json"; a.click();
    };
    root.querySelector("#imp").onchange = async (e) => {
      const file = e.target.files[0]; if (!file) return;
      const data = JSON.parse(await file.text());
      if (data.api) data.api.key = Store.get().api.key;
      Store.set(Object.assign(Store.get(), data));
      alert("Progresso restaurado.");
      draw();
    };
  }

  function diagnostico() {
    const d = Store.get().diagnostic;
    if (!window.diag) window.diag = null;
    if (!window.diag) {
      root.innerHTML = `<h1>Diagnóstico curto</h1>
        <p>Não é um simulado e não vira banda. Serve para ordenar o plano: lacunas, um texto do dia, uma passagem, seis respostas ouvidas, uma conversa, seis frases para montar e três repetições. Leva menos que uma seção oficial. O microfone é opcional; se não abrir, a fala fica sem porcentagem e o plano continua priorizando fala e escrita, que já são o seu ponto de partida.</p>
        <button class="btn" id="go">Começar</button>`;
      root.querySelector("#go").onclick = () => {
        window.diag = {
          steps: buildDiag(),
          i: 0,
          scores: { ctw: [], reading: [], listening: [], bas: [], repeat: [] }
        };
        diagnostico();
      };
      return;
    }
    const step = window.diag.steps[window.diag.i];
    if (!step) return finishDiag();
    root.innerHTML = `<p class="kicker">Diagnóstico · ${window.diag.i + 1} / ${window.diag.steps.length}</p><div class="card" id="d"></div>`;
    const host = root.querySelector("#d");
    if (step.kind === "ctw") {
      host.innerHTML = "<h2>Complete the Words</h2><div id=\"h\"></div><button class=\"btn\" id=\"ok\">Seguir</button>";
      const api = Widgets.mountCTW(host.querySelector("#h"), step.item, {});
      host.querySelector("#ok").onclick = () => {
        const sc = api.score();
        window.diag.scores.ctw.push(sc.hit / sc.total);
        window.diag.i += 1; diagnostico();
      };
    } else if (step.kind === "mc") {
      const q = step.q;
      host.innerHTML = (step.text ? `<div class="passage">${esc(step.text)}</div>` : "") + `<h3>${esc(q.q)}</h3>` + q.options.map((op, i) => `<button class="q-option" data-a="${i}">${esc(op)}</button>`).join("") + `<p><button class="btn" id="ok">Seguir</button></p>`;
      let picked = null;
      host.querySelectorAll(".q-option").forEach((b) => b.onclick = () => { picked = Number(b.dataset.a); host.querySelectorAll(".q-option").forEach((x) => x.classList.remove("picked")); b.classList.add("picked"); });
      host.querySelector("#ok").onclick = () => {
        const bag = step.area === "listening" ? window.diag.scores.listening : window.diag.scores.reading;
        bag.push(picked === q.a ? 1 : 0);
        window.diag.i += 1; diagnostico();
      };
    } else if (step.kind === "bas") {
      host.innerHTML = `<h2>${esc(step.item.prompt)}</h2><div id="h"></div><button class="btn" id="ok">Seguir</button>`;
      const api = Widgets.mountBAS(host.querySelector("#h"), step.item, {});
      host.querySelector("#ok").onclick = () => {
        window.diag.scores.bas.push(api.correct() ? 1 : 0);
        window.diag.i += 1; diagnostico();
      };
    } else if (step.kind === "repeat") {
      host.innerHTML = `<h2>Ouça e repita</h2><p id="st">${esc(step.item.scenario)}</p><button class="btn" id="ok">Ouvir e gravar</button><button class="btn ghost" id="skip">Pular a fala</button>`;
      host.querySelector("#skip").onclick = () => { window.diag.scores.repeat.push(null); window.diag.i += 1; diagnostico(); };
      host.querySelector("#ok").onclick = async () => {
        await AudioKit.speak(step.sentence.text);
        try {
          const rec = await AudioKit.recordFor(10000);
          window.diag.scores.repeat.push(AudioKit.align(step.sentence.text, rec.transcript).accuracy);
        } catch (e) {
          window.diag.scores.repeat.push(null);
        }
        window.diag.i += 1; diagnostico();
      };
    }
  }
  function buildDiag() {
    const steps = [];
    const ctw = bank.ctw.find((x) => x.pool === "practice");
    steps.push({ kind: "ctw", item: ctw });
    const daily = bank.daily.find((x) => x.pool === "practice");
    daily.questions.slice(0, 2).forEach((q) => steps.push({ kind: "mc", area: "reading", text: daily.text, q }));
    const ac = bank.academic.find((x) => x.pool === "practice");
    ac.questions.slice(0, 3).forEach((q) => steps.push({ kind: "mc", area: "reading", text: ac.text, q }));
    bank.choose.filter((x) => x.pool === "practice").slice(0, 4).forEach((item) => {
      steps.push({ kind: "mc", area: "listening", q: { q: item.line, options: item.options, a: item.a } });
    });
    const conv = bank.conversation.find((x) => x.pool === "practice");
    conv.questions.forEach((q) => steps.push({ kind: "mc", area: "listening", text: conv.lines.map((l) => l.who + ": " + l.text).join("\n"), q }));
    bank.bas.filter((x) => x.pool === "practice").slice(0, 6).forEach((item) => steps.push({ kind: "bas", item }));
    const rep = bank.repeat.find((x) => x.pool === "practice");
    rep.sentences.slice(0, 3).forEach((sentence) => steps.push({ kind: "repeat", item: rep, sentence }));
    return steps;
  }
  function avg(arr) {
    const nums = arr.filter((x) => typeof x === "number");
    if (!nums.length) return null;
    return nums.reduce((a, b) => a + b, 0) / nums.length;
  }
  function finishDiag() {
    const sc = window.diag.scores;
    const areas = {
      escrita: avg(sc.bas),
      leitura: avg([].concat(sc.ctw, sc.reading)),
      escuta: avg(sc.listening),
      fala: avg(sc.repeat)
    };
    const ranked = Object.entries(areas).filter((x) => x[1] != null).sort((a, b) => a[1] - b[1]).map((x) => x[0]);
    if (!ranked.includes("escrita")) ranked.push("escrita");
    if (!ranked.includes("fala")) ranked.splice(1, 0, "fala");
    Store.set({ diagnostic: areas, priorities: ranked });
    window.diag = null;
    root.innerHTML = `<h1>Prioridade do plano</h1><div class="grid-2">
      ${Object.entries(areas).map(([k, v]) => `<div class="stat"><b>${v == null ? "—" : Math.round(v * 100) + "%"}</b>${esc(k)}</div>`).join("")}
    </div><p>O plano passa a abrir pelo mais fraco: <b>${esc(ranked.slice(0, 2).join(" e "))}</b>. Isso não é banda. Se a fala ficou sem número, ela continua no topo junto com a escrita.</p><a class="btn" href="#/">Ver o plano de hoje</a>`;
  }

  boot();
})();
