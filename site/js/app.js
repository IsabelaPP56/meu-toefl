(function () {
  const { esc } = Widgets;
  const root = () => document.getElementById("conteudo");
  let bank = null;
  const SKILL = {
    reading: ["ctw", "daily", "academic"],
    listening: ["choose", "conversation", "announcement", "talk"],
    writing: ["bas", "email", "discussion"],
    speaking: ["repeat", "interview"]
  };
  const TASK_NAME = {
    ctw: "Complete the Words", daily: "Read in Daily Life", academic: "Read an Academic Passage",
    choose: "Listen and Choose a Response", conversation: "Listen to a Conversation",
    announcement: "Listen to an Announcement", talk: "Listen to an Academic Talk",
    bas: "Build a Sentence", email: "Write an Email", discussion: "Write for an Academic Discussion",
    repeat: "Listen and Repeat", interview: "Take an Interview"
  };
  const VIDEOS = {
    reading: [
      ["https://www.youtube.com/watch?v=eKaVhOnMjm8", "Reading 2026: três tarefas (TST Prep)"],
      ["https://www.youtube.com/watch?v=M5kTvJWIx8Q", "Reading Practice Test 2026 (TST Prep)"]
    ],
    listening: [
      ["https://www.youtube.com/watch?v=C0_sud-fw0k", "Listening 2026: quatro tarefas (TST Prep)"],
      ["https://www.youtube.com/watch?v=Y9ztHoKJDxs", "Listening Practice Test 2026 (TST Prep)"]
    ],
    writing: [
      ["https://www.youtube.com/watch?v=XYLHVFBFsDc", "Build a Sentence 2026 (TST Prep)"],
      ["https://www.youtube.com/watch?v=bPRfxgXBQAI", "Write an Email 2026 (TST Prep)"],
      ["https://www.youtube.com/watch?v=SGP2VAnC_1I", "Templates 2026: e-mail e discussão (Test Resources)"],
      ["https://www.youtube.com/watch?v=MDR3k5nT5D8", "Writing Practice Test 2026 (TST Prep)"]
    ],
    speaking: [
      ["https://www.youtube.com/watch?v=iR529CoRuZo", "Listen and Repeat 2026 (TST Prep)"],
      ["https://www.youtube.com/watch?v=cktZfTZ9UXs", "Take an Interview 2026 (TST Prep)"],
      ["https://www.youtube.com/watch?v=YphRAv3fpMM", "Speaking Practice Test 2026 (TST Prep)"]
    ]
  };

  function route() {
    const raw = (location.hash || "#/").slice(1);
    const [path, qs] = raw.split("?");
    return { parts: path.split("/").filter(Boolean), q: Object.fromEntries(new URLSearchParams(qs || "")) };
  }
  function go(hash) { location.hash = hash; }

  const NAV = [
    { href: "#/", label: "Início", ico: "I", color: "#7c3aed" },
    { href: "#/estrutura", label: "Estrutura da prova", ico: "E", color: "#4f46e5" },
    { group: "Estudar", ico: "A", color: "#0ea5e9", items: [
      ["#/estudar/reading", "Reading"],
      ["#/estudar/listening", "Listening"],
      ["#/estudar/writing", "Writing"],
      ["#/estudar/speaking", "Speaking"],
      ["#/bas", "Build a Sentence"]
    ]},
    { group: "Simulados", ico: "S", color: "#7c3aed", items: [
      ["#/simulados", "Os 10 simulados"],
      ["#/historico", "Histórico"]
    ]},
    { href: "#/vocab", label: "Vocabulário", ico: "V", color: "#16a34a" },
    { href: "#/erros", label: "Caderno de erros", ico: "C", color: "#e11d48" },
    { href: "#/metodo", label: "Como estudar", ico: "M", color: "#d97706" },
    { href: "#/materiais", label: "Materiais oficiais", ico: "O", color: "#0891b2" },
    { href: "#/prova", label: "Dia da prova", ico: "D", color: "#be123c" }
  ];

  function paintChrome(crumb) {
    const r = route();
    const here = "#" + (location.hash.slice(1).split("?")[0] || "/");
    const open = JSON.parse(sessionStorage.getItem("navopen") || '{"Estudar":true,"Simulados":true}');
    const side = document.getElementById("sidebar");
    const theme = Store.get().theme || "light";
    document.documentElement.dataset.theme = theme;
    side.innerHTML = `
      <a class="brand" href="#/"><div class="brand-mark">T</div><div><b>Meu TOEFL</b><span>Home Edition · 2026</span></div></a>
      <div class="navscroll">${NAV.map((item) => {
        if (item.href) {
          const active = here === item.href ? " active" : "";
          return `<a class="nav-item${active}" href="${item.href}"><span class="ico" style="background:${item.color}">${item.ico}</span>${item.label}</a>`;
        }
        const on = open[item.group] ? " open" : "";
        const kids = item.items.map(([href, label]) => `<a href="${href}" class="${here === href ? "active" : ""}">${label}</a>`).join("");
        return `<button class="group-btn${on}" data-g="${item.group}"><span class="ico" style="background:${item.color}">${item.ico}</span>${item.group}</button><div class="nav-sub${on}">${kids}</div>`;
      }).join("")}</div>
      <div class="side-foot">
        <div class="toggle"><span>Modo escuro</span><button class="switch ${theme === "dark" ? "on" : ""}" id="theme" aria-label="Modo escuro"><i></i></button></div>
        <p>Dados neste navegador. Data da prova, progresso e chave de API ficam só aqui.</p>
      </div>`;
    side.querySelectorAll(".group-btn").forEach((b) => b.onclick = () => {
      open[b.dataset.g] = !open[b.dataset.g];
      sessionStorage.setItem("navopen", JSON.stringify(open));
      paintChrome(crumb);
    });
    side.querySelector("#theme").onclick = () => {
      Store.set({ theme: theme === "dark" ? "light" : "dark" });
      paintChrome(crumb);
    };
    document.getElementById("crumb").textContent = crumb || "Meu TOEFL";
    document.body.classList.remove("nav-open");
  }

  function head(eyebrow, title, lede) {
    return `<p class="eyebrow">${esc(eyebrow)}</p><h1 class="page">${esc(title)}</h1>${lede ? `<p class="lede">${lede}</p>` : ""}`;
  }

  async function boot() {
    const files = ["ctw","daily","academic","choose","conversation","announcement","talk","bas","email","discussion","repeat","interview","vocab"];
    bank = {};
    for (const f of files) {
      const res = await fetch("data/parts/" + f + ".json");
      if (!res.ok) throw new Error(f);
      bank[f] = await res.json();
    }
    const extra = await fetch("data/parts/scale.json");
    if (extra.ok) {
      const scale = await extra.json();
      Object.keys(scale).forEach((k) => { if (Array.isArray(scale[k])) bank[k] = (bank[k] || []).concat(scale[k]); });
    }
    document.getElementById("hamburger").onclick = () => document.body.classList.toggle("nav-open");
    document.getElementById("scrim").onclick = () => document.body.classList.remove("nav-open");
    window.addEventListener("hashchange", draw);
    draw();
  }

  function draw() {
    const r = route();
    const top = r.parts[0] || "";
    if (top === "simulado" && r.parts[1]) {
      const id = r.parts[1];
      if (r.q.novo === "1") {
        Store.get().mockRun = ExamKit.fresh(Number(id));
        Store.save();
        history.replaceState(null, "", "#/simulado/" + id);
      } else if (!Store.get().mockRun || String(Store.get().mockRun.mockId) !== id) {
        Store.get().mockRun = ExamKit.fresh(Number(id));
        Store.save();
      }
      document.body.classList.add("exam-mode");
      ExamKit.render(root(), bank);
      return;
    }
    document.body.classList.remove("exam-mode");
    const pages = {
      "": home, estrutura, estudar, bas: basPage, simulados, historico, vocab, erros, metodo, materiais, prova,
      pratica: pratica, resultado, diagnostico, "coach-fala": coachFala, "coach-escrita": coachEscrita
    };
    const crumb = {
      "": "Início", estrutura: "Meu TOEFL / Estrutura da prova", estudar: "Meu TOEFL / Estudar",
      bas: "Meu TOEFL / Build a Sentence", simulados: "Meu TOEFL / Simulados", historico: "Meu TOEFL / Histórico",
      vocab: "Meu TOEFL / Vocabulário", erros: "Meu TOEFL / Caderno de erros", metodo: "Meu TOEFL / Como estudar",
      materiais: "Meu TOEFL / Materiais", prova: "Meu TOEFL / Dia da prova", pratica: "Meu TOEFL / Prática"
    }[top] || "Meu TOEFL";
    paintChrome(crumb);
    (pages[top] || home)(r);
  }

  function skillPct(name) {
    const tasks = SKILL[name] || [];
    let a = 0, c = 0;
    const bag = Store.get().stats.byTask || {};
    tasks.forEach((t) => { const b = bag[t]; if (!b) return; a += b.answered; c += b.correct; });
    return a ? Math.round(100 * c / a) : null;
  }

  function home() {
    const s = Store.get();
    const left = PlanKit.daysUntil(s.examDate);
    const plan = PlanKit.build(s);
    const today = plan[0];
    const streak = s.streak || { count: 0, last: "" };
    root().innerHTML = head("Seu ritmo, sua prova", "Meu plano · TOEFL iBT", "Uma rotina curta, no feminino e no seu fuso. A meta é banda 4 ou mais, o começo de B2. A aula de inglês continua; aqui entra o que a prova cronometra.") + `
      <div class="pills">
        <button class="pill active" data-tab="hoje">Hoje</button>
        <button class="pill" data-tab="semana">Semana</button>
        <button class="pill" data-tab="progresso">Progresso</button>
      </div>
      <div id="tab"></div>`;
    const tab = root().querySelector("#tab");
    function show(name) {
      root().querySelectorAll(".pill").forEach((p) => p.classList.toggle("active", p.dataset.tab === name));
      if (name === "hoje") {
        tab.innerHTML = `<div class="grid-2">
          <div class="card"><p class="eyebrow">Contagem</p><div class="stat"><b>${left < 0 ? "A data passou" : left === 0 ? "É hoje" : left + " dias"}</b></div>
            <label class="field">Data da prova<input type="date" id="exam" value="${esc(s.examDate)}"></label>
            <p class="muted">Fuso de Brasília. Só neste navegador.</p></div>
          <div class="card"><p class="eyebrow">Sequência</p><div class="stat"><b>${streak.count || 0}</b> dia(s) seguido(s)</div>
            <p class="muted">Último estudo registrado: ${esc(streak.last || "ainda não")}.</p>
            <p>Prioridade: <b>escrita e fala</b>. Build a Sentence e Listen and Repeat vêm primeiro.</p>
            <a class="btn" href="#/diagnostico">Fazer o diagnóstico</a></div>
        </div>
        <div class="card"><h2>Mapa das habilidades</h2><div class="grid-4">${["reading","listening","writing","speaking"].map((k) => {
          const p = skillPct(k);
          return `<div><b>${k}</b><div class="heat"><span style="width:${p == null ? 8 : p}%"></span></div><span class="muted">${p == null ? "sem dados" : p + "% de acerto"}</span></div>`;
        }).join("")}</div></div>
        <div class="card"><h2>Hoje</h2>${today ? today.blocks.map((b) => `<p><a href="${esc(b.href)}">${esc(b.title)}</a><br><span class="muted">${esc(b.note)}</span></p>`).join("") : "<p>Se a prova é hoje, abra o dia da prova e descanse.</p>"}</div>`;
        const input = tab.querySelector("#exam");
        if (input) input.onchange = (e) => { Store.set({ examDate: e.target.value }); home(); };
      } else if (name === "semana") {
        tab.innerHTML = `<div class="card">${plan.slice(0, 14).map((d) => `<p><b>${esc(d.label)}</b> · ${d.minutes} min<br>${d.blocks.map((b) => esc(b.title)).join(" · ")}</p>`).join("") || "<p>Escolha uma data futura.</p>"}</div>`;
      } else {
        const st = s.stats;
        tab.innerHTML = `<div class="grid-3"><div class="card stat"><b>${st.answered}</b>respostas</div><div class="card stat"><b>${st.answered ? Math.round(100 * st.correct / st.answered) : 0}%</b>acerto</div><div class="card stat"><b>${(s.mocks || []).length}</b>simulados salvos</div></div>`;
      }
    }
    root().querySelectorAll(".pill").forEach((p) => p.onclick = () => show(p.dataset.tab));
    show("hoje");
  }

  function estrutura() {
    root().innerHTML = head("Formato 2026", "Estrutura da prova", "Números da página de conteúdo da ETS e do overview com copyright 2026. O que a ETS não publicou está marcado como estimativa.") + `
      <div class="card"><table>
        <tr><th>Seção</th><th>Tarefas</th><th>Itens</th><th>Tempo-base</th></tr>
        <tr><td>Reading</td><td>Complete the Words; Read in Daily Life; Read an Academic Passage</td><td>50</td><td>30 min</td></tr>
        <tr><td>Listening</td><td>Choose a Response; Conversation; Announcement; Academic Talk</td><td>47</td><td>29 min</td></tr>
        <tr><td>Writing</td><td>Build a Sentence; Write an Email; Academic Discussion</td><td>12</td><td>23 min</td></tr>
        <tr><td>Speaking</td><td>Listen and Repeat; Take an Interview</td><td>11</td><td>cerca de 8 min</td></tr>
      </table>
      <p>Ordem: Reading, Listening, Writing, Speaking. Sem intervalo programado. Reserve cerca de duas horas, porque as instruções não entram no relógio. Reading e Listening são adaptativos em dois módulos. A página da ETS diz que, com a adaptação, tempo e itens podem variar.</p></div>
      <div class="grid-2">
        <div class="card"><h2>Por tarefa, no material de prática oficial</h2>
          <ul>
            <li>Complete the Words: parágrafo de cerca de 70–100 palavras, 10 lacunas, primeira frase inteira.</li>
            <li>Read in Daily Life: texto de cerca de 15–150 palavras, 2 ou 3 questões.</li>
            <li>Academic Passage: cerca de 200 palavras, 5 questões no Practice Test.</li>
            <li>Choose a Response: a fala não vem escrita; 4 opções.</li>
            <li>Conversa e anúncio: 2 questões no Practice Test. Talk: 4.</li>
            <li>Build a Sentence: 10 itens. E-mail: 7 min. Discussão: 10 min e pelo menos 100 palavras.</li>
            <li>Listen and Repeat: 7 frases, 8–12 segundos, uma vez. Entrevista: 4 perguntas, 45 segundos, sem preparação.</li>
          </ul>
          <p class="muted">A divisão 30+20 e 28+19, e o corte de 65% do módulo 2, são deste site. A ETS não publicou o corte nem a contagem exata por módulo.</p></div>
        <div class="card"><h2>Escala 1–6</h2>
          <p>A nota geral é a média das quatro seções, na meia banda mais próxima. Exemplo oficial: 5,125 vira 5.</p>
          <table>
            <tr><th>CEFR</th><th>Banda</th></tr>
            <tr><td>C2</td><td>6</td></tr>
            <tr><td>C1</td><td>5–5,5</td></tr>
            <tr style="background:var(--soft)"><td><b>B2, sua meta</b></td><td><b>4–4,5</b></td></tr>
            <tr><td>B1</td><td>3–3,5</td></tr>
            <tr><td>A2</td><td>2–2,5</td></tr>
            <tr><td>A1</td><td>1–1,5</td></tr>
          </table>
          <p class="muted">Não existe nota de aprovação universal. Cada instituição escolhe o corte.</p></div>
      </div>
      <div class="card"><h2>Home Edition</h2>
        <ul>
          <li>Computador de mesa ou notebook, na tomada, sobre a mesa. Não pode ser tablet nem celular como máquina da prova. Um monitor, um teclado. Windows 11+ ou macOS 10.13+.</li>
          <li>Alto-falante e microfone que não sejam headset. Fone de ouvido não é permitido.</li>
          <li>Câmera que gira 360°, inclusive embaixo da mesa.</li>
          <li>Segunda câmera: a ETS escreve “se aplicável” nos requisitos e inclui o passo no check-in. Confira o seu agendamento.</li>
          <li>Sozinha, portas fechadas, vidro coberto, parede sem material de prova, cadeira comum. Sem comida, sem bebida, sem pausa. “Taking a break” está na lista do que pode cancelar a nota.</li>
          <li>Documento oficial. Rosto e orelhas visíveis, sem máscara, sem relógio inteligente.</li>
          <li>Notas só em quadro branco pequeno ou folha dentro de plástico, com marcador apagável. Sem caneta. No fim, apague e mostre os dois lados.</li>
          <li>Feche Zoom e qualquer acesso remoto. Se o equipamento falhar no dia, a ETS diz que não há reembolso nem remarcação gratuita.</li>
          <li>O fiscal fala por câmera e chat. No fim, Reading e Listening mostram nota não oficial; você pode reportar ou cancelar. Notas oficiais: em 3 dias, segundo o overview de 2026.</li>
        </ul>
        <p><a href="https://www.ets.org/toefl/test-takers/ibt/register/at-home-requirements.html" target="_blank" rel="noopener">Requisitos oficiais</a> · <a href="https://www.ets.org/toefl/test-takers/ibt/test-day/at-home-test-day.html" target="_blank" rel="noopener">Dia da prova</a></p></div>`;
  }

  const GUIDE = {
    reading: {
      title: "Reading",
      lede: "Três tarefas. O texto fica na tela. Dentro do módulo você volta; o módulo 1 fecha quando o 2 começa.",
      blocks: [
        ["Complete the Words", "Recupera forma e sentido. Primeira frase inteira; depois, 10 palavras pela metade.", "Leia a frase, decida a classe da palavra e prove a palavra inteira antes de preencher.", "Chutar letra sem pronunciar a palavra.", "We mi___ → might."],
        ["Read in Daily Life", "Aviso, e-mail, mensagem, agenda. 2 ou 3 questões.", "Quem quer o quê, até quando, com qual condição. Cuidado com unless, except, before.", "Marcar um fato verdadeiro no mundo e ausente no texto.", "Closed Friday; return Monday without a fee."],
        ["Read an Academic Passage", "Cerca de 200 palavras e 5 questões no material oficial. Sem conhecimento prévio.", "Função de cada trecho: ideia, exemplo, contraste. Elimine always/never e causa trocada.", "Gastar o módulo inteiro no primeiro texto.", "Por que o autor cita o exemplo?"]
      ]
    },
    listening: {
      title: "Listening",
      lede: "Quatro tarefas. O áudio toca uma vez. Não se volta à questão anterior. Sotaques: América do Norte, Reino Unido, Austrália e Nova Zelândia.",
      blocks: [
        ["Listen and Choose a Response", "Uma fala curta, só em áudio, e quatro respostas escritas.", "Ouça a função: pedido, convite, correção, má notícia.", "Escolher a opção que repete uma palavra e responde outra coisa.", "Could you hold the door? → Sure, I'll hold it."],
        ["Listen to a Conversation", "Dois falantes. No Practice Test, 2 questões.", "Problema e próximo passo.", "Ouvir de novo. Não dá.", "She will ask the desk."],
        ["Listen to an Announcement", "Um falante, cerca de 40–85 palavras.", "Evento, horário, lugar, ação.", "Trocar a condição.", "Arrive early because copies are limited."],
        ["Listen to an Academic Talk", "Cerca de 100–250 palavras. No Practice Test, 4 questões.", "Tema, duas relações, um exemplo.", "Anotar frase inteira.", "Why this example?"]
      ]
    },
    writing: {
      title: "Writing",
      lede: "Seu ponto fraco declarado. Um bloco curto todo dia vale mais do que um mutirão.",
      blocks: [
        ["Build a Sentence", "10 itens. Há peças que sobram. A ETS não publicou os segundos; a TST Prep descreve 5:50 para o bloco.", "Ache o verbo e o auxiliar. Pergunta indireta não inverte. Relativa cola no nome. Passiva: be + particípio.", "Usar a ordem da pergunta direta dentro do if/whether.", "Do you know where she went?"],
        ["Write an Email", "7 minutos. Em geral três pedidos. Sem mínimo oficial de palavras.", "Saudação, motivo, os três pontos, fecho. 1 min de plano, 5 de texto, 1 de revisão.", "Esquecer um tópico.", "Dear …, I am writing because …"],
        ["Academic Discussion", "10 minutos. Pelo menos 100 palavras. Professor e dois colegas.", "Posição, um motivo, um exemplo, uma frase sobre um colega, com as suas palavras.", "Dois motivos rasos ou cópia do post.", "I agree with Helena because …"]
      ]
    },
    speaking: {
      title: "Speaking",
      lede: "Cerca de 8 minutos. Sem preparação. Se a frase some no meio, segure o primeiro bloco de sentido e fale.",
      blocks: [
        ["Listen and Repeat", "7 frases, cada vez mais longas, 8 a 12 segundos, uma tentativa.", "Modo bloco no treino. Na prova, uma vez. As palavras que caem são a, the, of, to e o -s.", "Traduzir antes de falar.", "The quiet floors / are upstairs."],
        ["Take an Interview", "4 perguntas, 45 segundos. A primeira é fato; as outras, opinião.", "Resposta direta, motivo, exemplo. Fale até o fim do tempo.", "Parar aos 15 segundos.", "I usually study alone because …"]
      ]
    }
  };

  function estudar(r) {
    const key = r.parts[1] || "reading";
    const g = GUIDE[key] || GUIDE.reading;
    root().innerHTML = head("Estudar", g.title, g.lede) + g.blocks.map((b) => `<article class="card"><h2>${esc(b[0])}</h2><p><b>O que cobra.</b> ${esc(b[1])}</p><p><b>Passo a passo.</b> ${esc(b[2])}</p><p><b>Armadilha.</b> ${esc(b[3])}</p><p><b>Exemplo.</b> ${esc(b[4])}</p><p><a class="btn" href="#/pratica/${taskKey(b[0])}">Praticar esta tarefa</a></p></article>`).join("") +
      `<div class="card"><h2>Vídeos</h2>${(VIDEOS[key] || []).map(([href, title]) => `<p><a href="${href}" target="_blank" rel="noopener">${esc(title)}</a></p>`).join("")}<p class="muted">Terceiros. Se divergirem da ETS, fique com a ETS. Links conferidos em 10/11/2026.</p></div>`;
  }
  function taskKey(title) {
    const map = {
      "Complete the Words": "ctw", "Read in Daily Life": "daily", "Read an Academic Passage": "academic",
      "Listen and Choose a Response": "choose", "Listen to a Conversation": "conversation",
      "Listen to an Announcement": "announcement", "Listen to an Academic Talk": "talk",
      "Build a Sentence": "bas", "Write an Email": "email", "Academic Discussion": "discussion",
      "Listen and Repeat": "repeat", "Take an Interview": "interview"
    };
    return map[title] || "bas";
  }

  function basPage() {
    const patterns = ["embedded-wh","indirect-question","auxiliary","relative-clause","passive","preposition","reported-speech","conditional","comparison","gerund-infinitive","word-order","agreement"];
    root().innerHTML = head("Sua tarefa mais frágil", "Build a Sentence", "Monte a resposta com as peças. Sobram palavras. A ordem da pergunta direta não entra depois de if, whether ou de um wh- embutido.") +
      `<div class="card"><p>Treino por padrão. Cada série puxa primeiro o que você errou.</p><div class="pills">${patterns.map((p) => `<a class="pill" href="#/pratica/bas?pattern=${p}&n=8">${p}</a>`).join("")}</div><p><a class="btn" href="#/pratica/bas?n=10&timer=1">Série cronometrada, 10 itens</a></p></div>`;
  }

  function simulados() {
    let cards = "";
    for (let n = 1; n <= 10; n++) {
      let info = "Banco incompleto.";
      try {
        const c = ExamKit.assemble(bank, n);
        const r1 = ExamKit.countReading(c.reading.m1);
        const ru = ExamKit.countReading(c.reading.upper);
        const rl = ExamKit.countReading(c.reading.lower);
        const l1 = ExamKit.countListening(c.listening.m1);
        const lu = ExamKit.countListening(c.listening.upper);
        info = `Reading ${r1}+${ru} (fácil ${rl}). Listening ${l1}+${lu}. Frases: ${c.bas.length}. E-mail: ${c.email ? "sim" : "não"}. Discussão: ${c.discussion ? "sim" : "não"}. Repetir: ${c.repeat ? 7 : 0}. Entrevista: ${c.interview ? 4 : 0}.`;
      } catch (e) { info = e.message; }
      cards += `<article class="card"><h2>Simulado ${n}</h2><p>${esc(info)}</p><a class="btn" href="#/simulado/${n}?novo=1">Começar</a></article>`;
    }
    root().innerHTML = head("Condições de prova", "Dez simulados", "Ordem oficial, relógios de módulo e módulo 2 adaptativo. A banda é estimativa. Itens em branco contam como erro.") +
      `<div class="warn">Relógios: Reading 21:00 + 9:00. Listening 18:00 + 11:00 ou 7:00. Build a Sentence 5:50, número da TST Prep, não da ETS. E-mail 7:00. Discussão 10:00. Repetição 8–12 s. Entrevista 45 s.</div>` + cards;
  }

  function historico() {
    const list = (Store.get().mocks || []).slice().reverse();
    root().innerHTML = head("O que você já fez", "Histórico", "Cada simulado salvo neste navegador.") +
      (list.length ? list.map((m, i) => `<article class="card"><b>Simulado ${m.mockId}</b> · geral ${m.overall ?? "—"} · R ${m.bands.reading} · L ${m.bands.listening} · W ${m.bands.writing} · S ${m.bands.speaking ?? "—"}<br><span class="muted">${esc(m.when || "")}</span> <button class="btn ghost" data-i="${list.length - 1 - i}">Abrir</button></article>`).join("") : `<p class="card">Nenhum simulado salvo ainda.</p>`);
    root().querySelectorAll("button[data-i]").forEach((b) => b.onclick = () => {
      Store.get().lastResult = Store.get().mocks[Number(b.dataset.i)];
      Store.save();
      go("#/resultado");
    });
  }

  function resultado() {
    const res = Store.get().lastResult || (Store.get().mocks || []).slice(-1)[0];
    if (!res) { root().innerHTML = head("Resultado", "Nenhum simulado ainda", "") ; return; }
    const b = res.bands || {};
    root().innerHTML = head("Estimativa, não nota ETS", "Simulado " + res.mockId, "A fórmula oficial que transforma acertos em banda não é pública. Se o módulo 2 foi o fácil, a estimativa de Reading ou Listening fica limitada a 4,0.") +
      `<div class="grid-4"><div class="card stat"><b>${b.reading}</b>Reading</div><div class="card stat"><b>${b.listening}</b>Listening</div><div class="card stat"><b>${b.writing}</b>Writing</div><div class="card stat"><b>${b.speaking == null ? "—" : b.speaking}</b>Speaking</div></div>
      <div class="card"><p>Geral estimada: <b>${res.overall ?? "—"}</b>. B2 começa em 4.</p><p>Reading ${res.read.hit}/${res.read.total}. Listening ${res.lis.hit}/${res.lis.total}. Build a Sentence ${res.bas.hit}/${res.bas.total}. Lista do e-mail ${res.emailScore}/5. Lista da discussão ${res.discScore}/5.</p><a class="btn" href="#/erros">Caderno de erros</a></div>`;
  }

  let practice = null;
  function pratica(r) {
    const task = r.parts[1];
    if (!task) {
      root().innerHTML = head("Prática autoral", "Escolha a tarefa", "Não são questões da ETS.") + `<div class="grid-2">${Object.keys(TASK_NAME).map((id) => `<a class="card" href="#/pratica/${id}"><b>${TASK_NAME[id]}</b></a>`).join("")}</div>`;
      return;
    }
    const n = Number(r.q.n || 0) || ({ ctw: 1, daily: 2, academic: 1, choose: 6, conversation: 2, announcement: 2, talk: 1, bas: 8 }[task] || 4);
    const pool = (bank[task] || []).filter((x) => x.pool === "practice" && (!r.q.pattern || x.pattern === r.q.pattern));
    const due = new Set(Store.get().errors.filter((e) => e.task === task && e.due <= Date.now()).map((e) => e.id));
    const items = pool.filter((x) => due.has(x.id)).concat(pool.filter((x) => !due.has(x.id)));
    for (let i = items.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [items[i], items[j]] = [items[j], items[i]]; }
    practice = { task, items: items.slice(0, n), i: 0, timer: r.q.timer === "1" ? 6 * 60 : 0, left: r.q.timer === "1" ? 6 * 60 : 0 };
    showPractice();
  }
  function mark(task, ok) {
    Store.bump(task, ok);
    Store.touchStreak(PlanKit.todaySP());
  }
  function showPractice() {
    const p = practice;
    if (!p || p.i >= p.items.length) {
      root().innerHTML = head("Prática", "Série fechada", "Os erros entraram na fila.") + `<p><a class="btn" href="#/pratica">Outra tarefa</a></p>`;
      return;
    }
    const item = p.items[p.i];
    root().innerHTML = head("Prática autoral", TASK_NAME[p.task] + " · " + (p.i + 1) + "/" + p.items.length, p.timer ? "Relógio da série ligado." : "") + `<div class="card" id="stage"></div><div id="feedback"></div>`;
    const stage = root().querySelector("#stage");
    if (p.task === "ctw") {
      stage.innerHTML = `<div id="host" class="passage"></div><button class="btn" id="go">Corrigir</button>`;
      const api = Widgets.mountCTW(stage.querySelector("#host"), item, {});
      stage.querySelector("#go").onclick = () => {
        const sc = api.score();
        sc.gaps.forEach((g, i) => mark("ctw", (sc.got[i] || "").toLowerCase() === g.missing.toLowerCase()));
        Store.gradeError(item.id, "ctw", sc.hit === sc.total, {});
        Widgets.mountCTW(stage.querySelector("#host"), item, { initial: sc.got, locked: true, reveal: true });
        root().querySelector("#feedback").innerHTML = `<div class="note">${sc.hit} de ${sc.total}.</div><button class="btn" id="next">Próxima</button>`;
        root().querySelector("#next").onclick = () => { p.i += 1; showPractice(); };
      };
      return;
    }
    if (p.task === "bas") {
      stage.innerHTML = `<p class="tag">${esc(item.pattern || "")}</p><h2>${esc(item.prompt)}</h2><div id="host"></div><button class="btn" id="go">Corrigir</button>`;
      const api = Widgets.mountBAS(stage.querySelector("#host"), item, {});
      stage.querySelector("#go").onclick = () => {
        const ok = api.correct();
        mark("bas", ok);
        Store.gradeError(item.id, "bas", ok, {});
        root().querySelector("#feedback").innerHTML = `<div class="${ok ? "note" : "warn"}">${ok ? "Ordem certa." : "Gabarito: " + esc(item.answer.join(" "))}</div><p>${esc(item.why || "")}</p><button class="btn" id="next">Próxima</button>`;
        root().querySelector("#next").onclick = () => { p.i += 1; showPractice(); };
      };
      return;
    }
    if (p.task === "email" || p.task === "discussion") {
      go(p.task === "email" ? "#/coach-escrita?task=email" : "#/coach-escrita?task=discussion");
      return;
    }
    if (p.task === "repeat" || p.task === "interview") {
      go(p.task === "repeat" ? "#/coach-fala?mode=repeat" : "#/coach-fala?mode=interview");
      return;
    }
    const listening = ["choose", "conversation", "announcement", "talk"].includes(p.task);
    if (listening && !p.heard) {
      const script = p.task === "choose" ? item.line : p.task === "conversation" ? item.lines.map((l) => l.text).join(". ") : item.script;
      stage.innerHTML = `<p>A transcrição fica escondida.</p><button class="btn" id="play">Ouvir uma vez</button>`;
      stage.querySelector("#play").onclick = async () => { stage.querySelector("#play").disabled = true; await AudioKit.speak(script); p.heard = true; showPractice(); };
      return;
    }
    const questions = p.task === "choose" ? [{ q: "Choose the best response.", options: item.options, a: item.a, why: item.why }] : item.questions;
    const qi = p.qi || 0;
    const q = questions[qi];
    const passage = (p.task === "daily" || p.task === "academic") ? `<div class="passage">${esc(item.text)}</div>` : "";
    stage.innerHTML = passage + `<h3>${esc(q.q)}</h3>` + q.options.map((op, i) => `<button class="q-option" data-a="${i}">${esc(op)}</button>`).join("") + `<p><button class="btn" id="go">Corrigir</button></p>`;
    let picked = null;
    stage.querySelectorAll(".q-option").forEach((btn) => btn.onclick = () => { picked = Number(btn.dataset.a); stage.querySelectorAll(".q-option").forEach((b) => b.classList.remove("picked")); btn.classList.add("picked"); });
    stage.querySelector("#go").onclick = () => {
      const ok = picked === q.a;
      mark(p.task, ok);
      Store.gradeError(item.id, p.task, ok, {});
      stage.querySelectorAll(".q-option").forEach((btn) => {
        const i = Number(btn.dataset.a);
        if (i === q.a) btn.classList.add("good");
        else if (i === picked) btn.classList.add("bad");
      });
      let extra = "";
      if (listening && qi + 1 >= questions.length) {
        const script = p.task === "choose" ? item.line : p.task === "conversation" ? item.lines.map((l) => l.who + ": " + l.text).join("\n") : item.script;
        extra = `<h3>Transcrição</h3><div class="passage">${esc(script)}</div>`;
      }
      root().querySelector("#feedback").innerHTML = `<div class="note">${esc(q.why || "")}</div>${extra}<button class="btn" id="next">Continuar</button>`;
      root().querySelector("#next").onclick = () => {
        if (qi + 1 < questions.length) { p.qi = qi + 1; showPractice(); }
        else { p.i += 1; p.qi = 0; p.heard = false; showPractice(); }
      };
    };
  }

  let coach = { si: 0, q: 0 };
  function coachFala(r) {
    const mode = r.q.mode || "repeat";
    const scenarios = bank.repeat.filter((x) => x.pool === "practice");
    const interviews = bank.interview.filter((x) => x.pool === "practice");
    const sc = scenarios[coach.si % scenarios.length];
    root().innerHTML = head("Fala", mode === "interview" ? "Take an Interview" : "Listen and Repeat", "Grave, ouça e veja a palavra que caiu.") +
      `<div class="pills"><a class="pill ${mode !== "interview" ? "active" : ""}" href="#/coach-fala?mode=repeat">Repetir</a><a class="pill ${mode === "interview" ? "active" : ""}" href="#/coach-fala?mode=interview">Entrevista</a></div><div class="card" id="coach"></div>`;
    const host = root().querySelector("#coach");
    if (mode !== "interview") {
      const sent = sc.sentences[coach.at || 0];
      host.innerHTML = `<p class="tag">${esc(sc.scenario)}</p><p>Frase ${(coach.at || 0) + 1} de 7. No modo bloco, cada pedaço de sentido pausa.</p>
        <div class="row"><button class="btn" id="play">Ouvir frase inteira</button><button class="btn secondary" id="chunks">Modo bloco</button></div>
        <p id="live" class="muted"></p><div id="diff"></div><audio id="replay" controls class="hidden"></audio>
        <div class="note">Não traduza. Segure quem faz o quê. As palavras curtas são as que somem.</div>
        <p><button class="btn ghost" id="another">Outro cenário</button></p>`;
      host.querySelector("#another").onclick = () => { coach.si += 1; coach.at = 0; coachFala(r); };
      const run = async (slow) => {
        document.getElementById("live").textContent = "Ouvindo…";
        await AudioKit.speak(sent.text, { rate: slow ? 0.8 : 0.96 });
        document.getElementById("live").textContent = "Sua vez. Gravando 12 segundos.";
        try {
          const rec = await AudioKit.recordFor(12000, (t) => { document.getElementById("live").textContent = t; });
          const diff = AudioKit.align(sent.text, rec.transcript);
          document.getElementById("diff").innerHTML = `<p>Precisão: <b>${Math.round(diff.accuracy * 100)}%</b></p><p class="diff">${diff.tokens.map((tk) => `<span class="${tk.ok ? "ok" : tk.extra ? "extra" : "miss"}">${esc(tk.t)}</span>`).join(" ")}</p>`;
          const audio = document.getElementById("replay");
          audio.src = rec.url; audio.classList.remove("hidden");
          mark("repeat", diff.accuracy >= 0.9);
          Store.gradeError("repeat:" + sent.text, "repeat", diff.accuracy >= 0.9, {});
        } catch (e) {
          document.getElementById("live").textContent = "O microfone não abriu. Dá para ouvir e repetir mesmo assim; a nota automática precisa da permissão.";
        }
      };
      host.querySelector("#play").onclick = () => run(false);
      host.querySelector("#chunks").onclick = async () => {
        for (const c of sent.chunks) { await AudioKit.speak(c, { rate: 0.86 }); await new Promise((res) => setTimeout(res, 600)); }
        run(false);
      };
    } else {
      const iv = interviews[coach.si % interviews.length];
      const q = iv.questions[coach.q % 4];
      host.innerHTML = `<p>${esc(iv.scenario)}</p><h2>${esc(q.text)}</h2><p class="muted">45 segundos. Resposta, motivo, exemplo.</p><button class="btn" id="go">Ouvir e gravar</button><p id="live"></p><div id="metrics"></div><audio id="replay" controls class="hidden"></audio>`;
      host.querySelector("#go").onclick = async () => {
        await AudioKit.speak(q.text);
        try {
          const rec = await AudioKit.recordFor(45000, (t) => { document.getElementById("live").textContent = t; });
          const words = AudioKit.tokenize(rec.transcript);
          const fillers = (rec.transcript.match(AudioKit.FILLERS) || []).length;
          document.getElementById("metrics").innerHTML = `<div class="grid-3"><div class="stat"><b>${words.length}</b>palavras</div><div class="stat"><b>${Math.round(words.length / 0.75)}</b>por minuto</div><div class="stat"><b>${fillers}</b>fillers</div><div class="stat"><b>${rec.pauses}</b>pausas</div></div><button class="btn" id="copy">Copiar prompt de correção</button>`;
          const audio = document.getElementById("replay"); audio.src = rec.url; audio.classList.remove("hidden");
          document.getElementById("copy").onclick = () => navigator.clipboard.writeText(promptFor("interview", q.text, rec.transcript));
          coach.q = (coach.q + 1) % 4;
          mark("interview", words.length >= 60);
        } catch (e) {
          document.getElementById("live").textContent = "Sem microfone nesta tentativa.";
        }
      };
    }
  }

  function coachEscrita(r) {
    const task = r.q.task === "discussion" ? "discussion" : "email";
    const list = bank[task].filter((x) => x.pool === "practice");
    const idx = Number(sessionStorage.getItem("widx") || 0) % list.length;
    const item = list[idx];
    const seconds = task === "email" ? 7 * 60 : 10 * 60;
    root().innerHTML = head("Escrita", task === "email" ? "E-mail · 7 min" : "Discussão · 10 min", "Lista automática, não a nota da ETS.") + `<div class="card" id="w"></div>`;
    const host = root().querySelector("#w");
    let html = task === "email"
      ? `<p><b>To:</b> ${esc(item.to)} · ${esc(item.subject)}</p><p>${esc(item.scenario)}</p><ul>${item.bullets.map((b) => "<li>" + esc(b) + "</li>").join("")}</ul>`
      : `<p>${esc(item.course)}</p><div class="passage">${esc(item.question)}</div><div class="passage"><b>${esc(item.s1.name)}.</b> ${esc(item.s1.text)}</div><div class="passage"><b>${esc(item.s2.name)}.</b> ${esc(item.s2.text)}</div>`;
    html += `<p id="clock"></p><textarea id="essay"></textarea><p><span id="wc">0</span> palavras</p>
      <div class="row"><button class="btn" id="start">Começar o relógio</button><button class="btn secondary" id="check">Lista</button><button class="btn ghost" id="copy">Copiar prompt</button><button class="btn ghost" id="swap">Outro</button></div><div id="list"></div>`;
    host.innerHTML = html;
    const area = host.querySelector("#essay");
    const tick = (sec) => { host.querySelector("#clock").textContent = String(Math.floor(sec / 60)).padStart(2, "0") + ":" + String(sec % 60).padStart(2, "0"); };
    tick(seconds);
    area.oninput = () => { host.querySelector("#wc").textContent = AudioKit.tokenize(area.value).length; };
    let left = seconds, iv = null;
    host.querySelector("#start").onclick = () => { if (iv) return; iv = setInterval(() => { left -= 1; tick(Math.max(0, left)); if (left <= 0) clearInterval(iv); }, 1000); };
    host.querySelector("#check").onclick = () => {
      const checks = task === "email" ? Widgets.emailChecks(item, area.value) : Widgets.discussionChecks(item, area.value);
      host.querySelector("#list").innerHTML = Widgets.renderChecks(checks) + `<p>Lista: ${Widgets.heuristicBand(checks)} / 5.</p>`;
      mark(task, Widgets.heuristicBand(checks) >= 4);
    };
    host.querySelector("#copy").onclick = () => {
      const stimulus = task === "email" ? item.scenario + "\n" + item.bullets.join("\n") : item.question + "\n" + item.s1.name + ": " + item.s1.text + "\n" + item.s2.name + ": " + item.s2.text;
      navigator.clipboard.writeText(promptFor(task, stimulus, area.value));
    };
    host.querySelector("#swap").onclick = () => { sessionStorage.setItem("widx", String(idx + 1)); coachEscrita(r); };
  }
  function promptFor(kind, stimulus, response) {
    return `Você avalia TOEFL iBT 2026. Responda em português.\nTarefa (${kind}):\n${stimulus}\n\nResposta:\n${response || "(vazia)"}\n\nDê nota 0–5 da tarefa, banda estimada 1–6, erros concretos e uma versão melhor no nível B2. Diga que é estimativa, não nota ETS.`;
  }

  function vocab(r) {
    const mode = r.q.mode || "cards";
    const theme = r.q.theme || "";
    const level = r.q.level || "";
    let list = bank.vocab.slice();
    if (theme) list = list.filter((v) => (v.theme || v.topic) === theme);
    if (level) list = list.filter((v) => v.level === level);
    const due = list.filter((v) => ((Store.get().vocab[v.id] || {}).due || 0) <= Date.now());
    const themes = [...new Set(bank.vocab.map((v) => v.theme || v.topic))];
    root().innerHTML = head("Palavras que a prova usa", "Vocabulário", `${due.length} para hoje, de ${list.length} neste filtro. Família, colocação, exemplo e sinônimo.`) +
      `<div class="pills">
        <a class="pill ${mode === "cards" ? "active" : ""}" href="#/vocab?mode=cards&theme=${theme}&level=${level}">Cartões</a>
        <a class="pill ${mode === "type" ? "active" : ""}" href="#/vocab?mode=type&theme=${theme}&level=${level}">Digitar</a>
        <a class="pill ${mode === "listen" ? "active" : ""}" href="#/vocab?mode=listen&theme=${theme}&level=${level}">Ouvir</a>
      </div>
      <div class="row"><select id="th"><option value="">Tema</option>${themes.map((t) => `<option ${t === theme ? "selected" : ""}>${esc(t)}</option>`).join("")}</select>
      <select id="lv"><option value="">Nível</option>${["B1","B2","C1"].map((t) => `<option ${t === level ? "selected" : ""}>${t}</option>`).join("")}</select></div>
      <div id="v"></div>`;
    root().querySelector("#th").onchange = (e) => go(`#/vocab?mode=${mode}&theme=${encodeURIComponent(e.target.value)}&level=${level}`);
    root().querySelector("#lv").onchange = (e) => go(`#/vocab?mode=${mode}&theme=${encodeURIComponent(theme)}&level=${e.target.value}`);
    const pile = (due.length ? due : list);
    const card = pile[Math.floor(Math.random() * pile.length)];
    const host = root().querySelector("#v");
    if (!card) { host.innerHTML = "<p>Nenhuma palavra nesse filtro.</p>"; return; }
    if (mode === "cards") {
      host.innerHTML = `<div class="card flash" id="flash"><div><p class="tag">${esc(card.level || "")} · ${esc(card.theme || card.topic || "")}</p><b>${esc(card.w)}</b><p class="muted">${esc(card.pos || "")} ${esc(card.ipa || "")}</p><div id="back" class="hidden"><p>${esc(card.pt)}</p><p>Família: ${esc(card.family || "—")}</p><p>Colocações: ${esc(card.colloc || "—")}</p><p>${esc(card.ex || "")}</p><p>Sinônimos: ${esc(card.syn || "—")}</p></div><p class="muted">Toque para virar</p></div></div>
        <div class="row"><button class="btn ghost" id="hear">Ouvir</button><button class="btn" id="again">De novo</button><button class="btn secondary" id="hard">Difícil</button><button class="btn secondary" id="good">Lembrei</button><button class="btn ghost" id="easy">Fácil</button></div>`;
      host.querySelector("#flash").onclick = () => host.querySelector("#back").classList.toggle("hidden");
      host.querySelector("#hear").onclick = (e) => { e.stopPropagation(); AudioKit.speak(card.w); };
      ["again","hard","good","easy"].forEach((id) => host.querySelector("#" + id).onclick = () => { Store.gradeVocab(card.id, id); Store.touchStreak(PlanKit.todaySP()); vocab(r); });
    } else {
      host.innerHTML = `<div class="card"><p>${mode === "listen" ? "Ouça e escreva a palavra." : esc(card.pt)}</p><button class="btn ghost" id="hear">Ouvir</button><input id="ans" placeholder="a palavra em inglês"><button class="btn" id="ok">Corrigir</button><p id="out"></p></div>`;
      const play = () => AudioKit.speak(mode === "listen" ? card.w : card.ex || card.w);
      if (mode === "listen") play();
      host.querySelector("#hear").onclick = play;
      host.querySelector("#ok").onclick = () => {
        const ok = host.querySelector("#ans").value.trim().toLowerCase() === card.w.toLowerCase();
        host.querySelector("#out").textContent = ok ? "Certa." : "Era " + card.w + ".";
        Store.gradeVocab(card.id, ok ? "good" : "again");
        setTimeout(() => vocab(r), 700);
      };
    }
  }

  function erros() {
    const now = Date.now();
    const list = Store.get().errors.slice().sort((a, b) => a.due - b.due);
    root().innerHTML = head("Recuperação", "Caderno de erros", "O que você errou volta hoje e, se acertar, espaça.") +
      (list.slice(0, 40).map((e) => `<div class="card"><b>${esc(e.task)}</b> · ${esc(e.id)}<div class="muted">${e.due <= now ? "para hoje" : "em " + Math.ceil((e.due - now) / 86400000) + " dia(s)"}</div><a href="#/pratica/${esc(e.task)}">Refazer a tarefa</a></div>`).join("") || `<p class="card">Nenhum erro guardado.</p>`);
  }

  function metodo() {
    root().innerHTML = head("Poucas semanas", "Como estudar", "A aula cobre língua geral. Aqui você recupera de memória, no relógio, o que a prova cobra.") + `
      <div class="grid-2">
        <article class="card"><h2>Recuperar, não reler</h2><p>Tente a resposta antes da explicação. Por isso o erro volta sozinho.</p><p class="muted">Roediger e Karpicke, 2006. Dunlosky e colegas, 2013.</p></article>
        <article class="card"><h2>Espaçar e intercalar</h2><p>No mesmo dia entram frase, repetição e um bloco de leitura ou escuta.</p><p class="muted">Cepeda e colegas, 2006. Rohrer e Taylor, 2007.</p></article>
        <article class="card"><h2>Um padrão por vez</h2><p>Build a Sentence errado vira nome: indireta, auxiliar, relativa, passiva.</p><p class="muted">Ericsson, Krampe e Tesch-Römer, 1993.</p></article>
        <article class="card"><h2>Blocos de sentido</h2><p>Não traduza a frase. Fale o primeiro bloco assim que ele acabar.</p><p class="muted">Murphey, 2001. TST Prep, Listen and Repeat 2026.</p></article>
      </div>
      <div class="card"><p>O plano de 9–12 semanas da ETS pede prova de prática, variação de seções e foco em Speaking. O seu calendário até o início de dezembro comprime isso: todo dia frase e fala, e um simulado no meio e outro perto do fim.</p>
      <p>Fontes da prova: <a href="https://www.ets.org/toefl/test-takers/ibt/about/content.html" target="_blank" rel="noopener">conteúdo</a>, <a href="https://www.ets.org/pdfs/toefl/toefl-ibt-test-overview.pdf" target="_blank" rel="noopener">overview</a>, <a href="https://tstprep.com/articles/toefl/complete-practice-test-for-the-toefl-test/" target="_blank" rel="noopener">TST Prep</a>.</p></div>`;
  }

  function materiais() {
    const rows = [
      ["2026", "Conteúdo e tempos", "https://www.ets.org/toefl/test-takers/ibt/about/content.html"],
      ["2026", "Overview em PDF", "https://www.ets.org/pdfs/toefl/toefl-ibt-test-overview.pdf"],
      ["2026", "Practice Test 1", "https://www.ets.org/pdfs/toefl/toefl-ibt-full-length-practice-test-1.pdf"],
      ["2026", "Practice Test 2", "https://www.ets.org/pdfs/toefl/toefl-ibt-full-length-practice-test-2.pdf"],
      ["2026", "Página do teste 1", "https://www.ets.org/toefl/test-takers/ibt/prepare/sample-test-jan-2026-1.html"],
      ["2026", "Página do teste 2", "https://www.ets.org/toefl/test-takers/ibt/prepare/sample-test-jan-2026-2.html"],
      ["2026", "Escala e CEFR", "https://www.ets.org/toefl/institutions/ibt/score-scale-update.html"],
      ["Home", "Requisitos", "https://www.ets.org/toefl/test-takers/ibt/register/at-home-requirements.html"],
      ["Home", "Dia da prova", "https://www.ets.org/toefl/test-takers/ibt/test-day/at-home-test-day.html"],
      ["2026, não oficial", "TST Prep", "https://tstprep.com/articles/toefl/complete-practice-test-for-the-toefl-test/"]
    ];
    root().innerHTML = head("Só links", "Materiais oficiais", "Nada da ETS foi copiado para este repositório.") +
      rows.map((r) => `<article class="card"><span class="tag">${esc(r[0])}</span> <a href="${esc(r[2])}" target="_blank" rel="noopener">${esc(r[1])}</a><p class="muted">${esc(r[2])}</p></article>`).join("");
  }

  function diagnostico() {
    root().innerHTML = head("Sem nota", "Diagnóstico curto", "Uma lacuna, um texto, seis respostas ouvidas e seis frases. Serve para lembrar onde dói. Não vira banda.") +
      `<p><a class="btn" href="#/pratica/ctw?n=1">Começar pelas lacunas</a> <a class="btn secondary" href="#/pratica/bas?n=6">Seis frases</a> <a class="btn secondary" href="#/pratica/choose?n=6">Seis falas</a></p>`;
  }
  function prova() {
    root().innerHTML = head("Logística", "Dia da prova", "Na véspera, sala e sono. Nada de formulário novo.") +
      `<div class="card"><ul>
        <li>App da ETS e Equipment Check no mesmo dia da semana e horário.</li>
        <li>Sem fone. Um monitor. Documento. Quadro apagável.</li>
        <li>Sozinha, sem pausa, sem comida.</li>
        <li>E-mail 7 min, discussão 10 min, entrevista 45 s.</li>
      </ul><a class="btn" href="#/estrutura">Ver todas as regras</a></div>`;
  }

  boot().catch((e) => { document.getElementById("conteudo").innerHTML = `<div class="warn">${esc(e.message)}</div>`; });
})();
