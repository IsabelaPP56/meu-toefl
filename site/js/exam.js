(function () {
  const { esc } = Widgets;
  let timerHandle = null;

  function byPool(list, pool) {
    return (list || []).filter((x) => x.pool === pool);
  }

  function assemble(bank, mockId) {
    const p = "m" + mockId;
    const tag = "mock" + mockId;
    return {
      reading: {
        m1: blocksReading(bank, p),
        upper: blocksReading(bank, p + "u"),
        lower: blocksReading(bank, p + "l")
      },
      listening: {
        m1: blocksListening(bank, p),
        upper: blocksListening(bank, p + "u"),
        lower: blocksListening(bank, p + "l")
      },
      bas: byPool(bank.bas, tag).slice(0, 10),
      email: byPool(bank.email, tag)[0],
      discussion: byPool(bank.discussion, tag)[0],
      repeat: byPool(bank.repeat, tag)[0],
      interview: byPool(bank.interview, tag)[0]
    };
  }

  function blocksReading(bank, pool) {
    return []
      .concat(byPool(bank.ctw, pool).map((item) => ({ type: "ctw", item })))
      .concat(byPool(bank.daily, pool).map((item) => ({ type: "daily", item })))
      .concat(byPool(bank.academic, pool).map((item) => ({ type: "academic", item })));
  }
  function blocksListening(bank, pool) {
    return []
      .concat(byPool(bank.choose, pool).map((item) => ({ type: "choose", item })))
      .concat(byPool(bank.conversation, pool).map((item) => ({ type: "conversation", item })))
      .concat(byPool(bank.announcement, pool).map((item) => ({ type: "announcement", item })))
      .concat(byPool(bank.talk, pool).map((item) => ({ type: "talk", item })));
  }

  function countReading(blocks) {
    return blocks.reduce((n, b) => n + (b.type === "ctw" ? (b.item.gaps || []).length : b.item.questions.length), 0);
  }
  function countListening(blocks) {
    return blocks.reduce((n, b) => n + (b.type === "choose" ? 1 : b.item.questions.length), 0);
  }

  function flat(blocks) {
    const out = [];
    blocks.forEach((b, bi) => {
      if (b.type === "ctw") out.push({ bi, q: null, points: (b.item.gaps || []).length });
      else if (b.type === "choose") out.push({ bi, q: 0, points: 1 });
      else b.item.questions.forEach((_, q) => out.push({ bi, q, points: 1 }));
    });
    return out;
  }

  function fresh(mockId) {
    return {
      mockId,
      stage: "dir-read",
      cursor: 0,
      phase: "audio",
      deadline: null,
      answers: {},
      readingRoute: null,
      listeningRoute: null,
      sectionScores: {},
      speak: { repeat: [], interview: [] },
      index: 0
    };
  }

  function persist(run) {
    Store.get().mockRun = run;
    Store.save();
  }

  function stopTimer() {
    if (timerHandle) cancelAnimationFrame(timerHandle);
    timerHandle = null;
  }

  function startDeadline(run, seconds) {
    run.deadline = Date.now() + seconds * 1000;
    persist(run);
  }

  function remaining(run) {
    if (!run.deadline) return null;
    return Math.max(0, Math.ceil((run.deadline - Date.now()) / 1000));
  }

  function fmt(sec) {
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return String(m).padStart(2, "0") + ":" + String(s).padStart(2, "0");
  }

  function shell(title, timerText, low, body, foot) {
    return '<div class="exam-top"><div><b>TOEFL iBT</b> · ' + esc(title) + '</div><div class="timer' + (low ? " low" : "") + '">' + esc(timerText) + '</div></div><div class="exam-body">' + body + (foot || "") + "</div>";
  }

  function dir(title, english, pt, button) {
    return '<div class="dir-screen"><p class="kicker">Instruções</p><h1>' + esc(title) + "</h1><p>" + english + '</p><div class="note"><b>Em português.</b> ' + pt + '</div><p><button class="btn" id="begin">' + esc(button) + "</button></p></div>";
  }

  function scoreReadingBlocks(blocks, answers) {
    let hit = 0, total = 0;
    blocks.forEach((b) => {
      if (b.type === "ctw") {
        const got = answers["ctw:" + b.item.id] || [];
        const pieces = Widgets.ctwPieces(b.item).filter((p) => p.type === "gap");
        pieces.forEach((g, i) => {
          total += 1;
          if (String(got[i] || "").toLowerCase() === g.missing.toLowerCase()) hit += 1;
        });
      } else if (b.type === "choose") {
        total += 1;
        if (answers[b.item.id] === b.item.a) hit += 1;
      } else if (b.item.questions) {
        b.item.questions.forEach((q, i) => {
          total += 1;
          if (answers[b.item.id + ":" + i] === q.a) hit += 1;
        });
      }
    });
    return { hit, total, pct: total ? hit / total : 0 };
  }

  function scoreListening(blocks, answers) {
    return scoreReadingBlocks(blocks, answers);
  }

  function bandFromPct(pct, cap) {
    const table = [[0.92, 6], [0.85, 5.5], [0.78, 5], [0.7, 4.5], [0.62, 4], [0.54, 3.5], [0.46, 3], [0.38, 2.5], [0.3, 2], [0.2, 1.5], [0, 1]];
    let band = 1;
    for (const row of table) { if (pct >= row[0]) { band = row[1]; break; } }
    if (cap != null) band = Math.min(band, cap);
    return band;
  }

  function basScore(items, answers) {
    let hit = 0;
    items.forEach((item) => {
      const got = answers["bas:" + item.id] || [];
      if (item.answer.every((a, i) => got[i] === a)) hit += 1;
    });
    return { hit, total: items.length };
  }

  function render(root, bank) {
    stopTimer();
    AudioKit.stopSpeak();
    const state = Store.get();
    let run = state.mockRun;
    if (!run) {
      root.innerHTML = "<p>Nenhum simulado em andamento.</p>";
      return;
    }
    const form = assemble(bank, run.mockId);
    run.view = (run.view || 0) + 1;
    const view = run.view;
    const redraw = () => render(root, bank);

    function tick() {
      const left = remaining(run);
      const el = root.querySelector(".timer");
      if (el && left != null) {
        el.textContent = fmt(left);
        el.classList.toggle("low", left < 60);
        if (left <= 0) {
          stopTimer();
          onTimeUp();
          return;
        }
      }
      timerHandle = requestAnimationFrame(tick);
    }

    function onTimeUp() {
      if (run.stage === "read1") return finishRead1();
      if (run.stage === "read2") return go("vol-lis");
      if (run.stage === "lis1") return finishLis1();
      if (run.stage === "lis2") return go("dir-wri");
      if (run.stage === "bas") return go("email");
      if (run.stage === "email") return go("disc");
      if (run.stage === "disc") return go("dir-spk");
      if (run.stage === "repeat" || run.stage === "interview") return advanceSpeak(true);
    }

    function go(stage, extra) {
      run.token = (run.token || 0) + 1;
      run.stage = stage;
      run.cursor = 0;
      run.phase = "audio";
      run.index = 0;
      run.deadline = null;
      if (extra) Object.assign(run, extra);
      persist(run);
      redraw();
    }

    function finishRead1() {
      const sc = scoreReadingBlocks(form.reading.m1, run.answers);
      run.sectionScores.read1 = sc;
      run.readingRoute = sc.pct >= 0.65 ? "upper" : "lower";
      go("dir-read2");
    }
    function finishLis1() {
      const sc = scoreListening(form.listening.m1, run.answers);
      run.sectionScores.lis1 = sc;
      run.listeningRoute = sc.pct >= 0.65 ? "upper" : "lower";
      go("dir-lis2");
    }

    function abandon(next) {
      if (!confirm("Encerrar esta seção agora? O que ficou em branco entra como erro na estimativa. Na prova real não há pausa.")) return;
      next();
    }

    const foot = '<p class="muted"><button class="btn ghost small" id="abandon">Encerrar esta seção</button></p>';

    if (run.stage === "dir-read") {
      root.innerHTML = dir(
        "Reading Section",
        "In an actual test you answer questions about academic and non-academic texts. This section has two modules. You may move forward and back inside a module. You cannot return to Module 1 after Module 2 begins. The clock shows the time for the module.",
        "São dois módulos. Dá para voltar dentro do módulo. Depois que o módulo 2 começa, o módulo 1 fecha. O relógio é do módulo: 21:00 e depois 9:00. A soma é o tempo-base oficial de 30 minutos. O corte que escolhe o módulo 2 (65%) não é publicado pela ETS.",
        "Begin Reading"
      );
      root.querySelector("#begin").onclick = () => { go("read1"); startDeadline(run, 21 * 60); redraw(); };
      return;
    }

    if (run.stage === "read1" || run.stage === "read2") {
      const blocks = run.stage === "read1" ? form.reading.m1 : form.reading[run.readingRoute || "lower"];
      const units = flat(blocks);
      if (!units.length) {
        root.innerHTML = "<p>O banco deste módulo veio vazio. Confira os arquivos de dados.</p>";
        return;
      }
      if (run.cursor >= units.length) run.cursor = units.length - 1;
      const unit = units[run.cursor];
      const block = blocks[unit.bi];
      const left = remaining(run);
      let body = "";
      if (block.type === "ctw") {
        body += "<p class=\"kicker\">Complete the Words</p><h2>Fill in the missing letters in the paragraph.</h2>";
        body += '<div class="passage" id="ctw-host"></div>';
        body += '<p class="muted">Cada lacuna conta como um item. Primeira frase inteira, como na tarefa oficial.</p>';
      } else {
        const label = block.type === "daily" ? "Read in Daily Life" : "Read an Academic Passage";
        body += '<p class="kicker">' + label + "</p>";
        body += '<div class="passage">' + esc(block.item.text || "") + "</div>";
        const q = block.item.questions[unit.q];
        body += "<h3>" + esc(q.q) + "</h3>";
        body += q.options.map((op, i) => '<button class="q-option" data-a="' + i + '">' + esc(op) + "</button>").join("");
      }
      const answeredBefore = run.cursor;
      body += '<div class="row" style="margin-top:14px"><button class="btn secondary" id="back">Back</button><button class="btn" id="next">' + (run.cursor === units.length - 1 ? "Continue" : "Next") + "</button></div>";
      const totalPts = units.reduce((sum, u) => sum + (u.points || 1), 0);
      let seen = 0;
      for (let i = 0; i < run.cursor; i++) seen += units[i].points || 1;
      const here = unit.points || 1;
      const rangeLabel = here === 1 ? ("Item " + (seen + 1)) : ("Itens " + (seen + 1) + "–" + (seen + here));
      body += "<p class=\"muted\">" + rangeLabel + " de " + totalPts + " neste módulo. " + (run.stage === "read2" ? "Módulo 2 (" + (run.readingRoute === "upper" ? "mais difícil" : "mais fácil") + ")." : "Módulo 1.") + "</p>";
      root.innerHTML = shell("Reading", left == null ? "--:--" : fmt(left), left != null && left < 60, body, foot);
      if (block.type === "ctw") {
        const api = Widgets.mountCTW(root.querySelector("#ctw-host"), block.item, {
          initial: run.answers["ctw:" + block.item.id] || [],
          onChange: (vals) => { run.answers["ctw:" + block.item.id] = vals; persist(run); }
        });
        root.querySelector("#next").onclick = () => {
          run.answers["ctw:" + block.item.id] = api.read();
          step(1);
        };
      } else {
        const key = block.item.id + ":" + unit.q;
        const picked = run.answers[key];
        root.querySelectorAll(".q-option").forEach((btn) => {
          if (Number(btn.dataset.a) === picked) btn.classList.add("picked");
          btn.onclick = () => {
            run.answers[key] = Number(btn.dataset.a);
            persist(run);
            root.querySelectorAll(".q-option").forEach((b) => b.classList.remove("picked"));
            btn.classList.add("picked");
          };
        });
        root.querySelector("#next").onclick = () => step(1);
      }
      root.querySelector("#back").onclick = () => step(-1);
      root.querySelector("#abandon").onclick = () => abandon(() => run.stage === "read1" ? finishRead1() : go("vol-lis"));
      function step(d) {
        const nxt = run.cursor + d;
        if (nxt < 0) return;
        if (nxt >= units.length) {
          if (run.stage === "read1") finishRead1();
          else go("vol-lis");
          return;
        }
        run.cursor = nxt;
        persist(run);
        redraw();
      }
      timerHandle = requestAnimationFrame(tick);
      return;
    }

    if (run.stage === "dir-read2") {
      const hard = run.readingRoute === "upper";
      root.innerHTML = dir(
        "Reading, Module 2",
        "You will now begin Module 2. You cannot return to Module 1.",
        "Simulação adaptativa: o módulo 1 ficou em " + Math.round((run.sectionScores.read1.pct || 0) * 100) + "% . " + (hard ? "Você foi para o conjunto mais difícil." : "Você foi para o conjunto mais fácil, e a estimativa de Reading fica limitada a 4,0.") + " O corte real da ETS não é público. Relógio: 9:00.",
        "Begin Module 2"
      );
      root.querySelector("#begin").onclick = () => { go("read2"); startDeadline(run, 9 * 60); redraw(); };
      return;
    }

    if (run.stage === "vol-lis") {
      root.innerHTML = dir(
        "Listening volume",
        "You will hear a short sentence. Set your volume now. Section timing has not started. Official section estimates do not include adjusting the audio.",
        "Ajuste o volume. O tempo do módulo ainda não começou. A ETS diz que o tempo publicado não inclui esse ajuste.",
        "Play check"
      );
      root.querySelector("#begin").textContent = "Ouvir a frase de teste";
      root.querySelector("#begin").onclick = async () => {
        await AudioKit.speak("This is a volume check. Listening is about to begin.");
        const b = document.createElement("p");
        b.innerHTML = '<button class="btn" id="okvol">O volume está bom</button>';
        root.querySelector(".dir-screen").appendChild(b);
        root.querySelector("#okvol").onclick = () => go("dir-lis");
      };
      return;
    }

    if (run.stage === "dir-lis") {
      root.innerHTML = dir(
        "Listening Section",
        "You will hear each recording once. You cannot return to previous questions. Answer based on what the speakers say.",
        "Não dá para voltar. O áudio toca uma vez, pela voz do navegador, não pelo áudio da ETS. O relógio do módulo não pausa durante a fala: a ETS não publicou se o relógio de 2026 pausa. Módulo 1: 18:00.",
        "Begin Listening"
      );
      root.querySelector("#begin").onclick = () => { go("lis1"); startDeadline(run, 18 * 60); redraw(); };
      return;
    }

    if (run.stage === "lis1" || run.stage === "lis2") {
      const blocks = run.stage === "lis1" ? form.listening.m1 : form.listening[run.listeningRoute || "lower"];
      if (run.cursor >= blocks.length) {
        if (run.stage === "lis1") finishLis1(); else go("dir-wri");
        return;
      }
      const block = blocks[run.cursor];
      const left = remaining(run);
      const qCount = block.type === "choose" ? 1 : block.item.questions.length;
      if (run.phase === "audio") {
        const label = { choose: "Listen and choose a response.", conversation: "Listen to a conversation.", announcement: "Listen to an announcement.", talk: "Listen to a talk." }[block.type];
        root.innerHTML = shell("Listening", left == null ? "--:--" : fmt(left), left != null && left < 60,
          "<h2>" + esc(label) + '</h2><p id="status">Ouvindo… a transcrição fica escondida.</p><p class="muted">Questão seguinte: ' + (run.cursor + 1) + " de " + blocks.length + " estímulos.</p>", foot);
        const script = block.type === "choose"
          ? block.item.line
          : block.type === "conversation"
            ? block.item.lines.map((l) => l.text).join(" ")
            : block.item.script;
        const token = run.token || 0;
        AudioKit.speak(script, { rate: block.type === "talk" ? 0.94 : 1 }).then(() => {
          if (run.view !== view || run.phase !== "audio") return;
          run.phase = "question";
          run.index = 0;
          persist(run);
          redraw();
        });
        root.querySelector("#abandon").onclick = () => abandon(() => run.stage === "lis1" ? finishLis1() : go("dir-wri"));
        timerHandle = requestAnimationFrame(tick);
        return;
      }
      const qi = run.index || 0;
      const q = block.type === "choose"
        ? { q: "Choose the best response.", options: block.item.options, a: block.item.a }
        : block.item.questions[qi];
      const key = (block.type === "choose" ? block.item.id : block.item.id + ":" + qi);
      let body = "<p class=\"kicker\">Listening</p><h3>" + esc(q.q) + "</h3>";
      body += q.options.map((op, i) => '<button class="q-option" data-a="' + i + '">' + esc(op) + "</button>").join("");
      body += '<div class="row" style="margin-top:12px"><button class="btn" id="next">Next</button></div>';
      body += "<p class=\"muted\">Sem volta. Áudio deste estímulo já foi reproduzido. Pergunta " + (qi + 1) + " de " + qCount + ".</p>";
      root.innerHTML = shell("Listening", fmt(left || 0), left < 60, body, foot);
      root.querySelectorAll(".q-option").forEach((btn) => {
        btn.onclick = () => {
          run.answers[key] = Number(btn.dataset.a);
          persist(run);
          root.querySelectorAll(".q-option").forEach((b) => b.classList.remove("picked"));
          btn.classList.add("picked");
        };
      });
      root.querySelector("#next").onclick = () => {
        if (qi + 1 < qCount) { run.index = qi + 1; persist(run); redraw(); return; }
        run.cursor += 1;
        run.phase = "audio";
        run.index = 0;
        persist(run);
        if (run.cursor >= blocks.length) {
          if (run.stage === "lis1") finishLis1(); else go("dir-wri");
        } else redraw();
      };
      root.querySelector("#abandon").onclick = () => abandon(() => run.stage === "lis1" ? finishLis1() : go("dir-wri"));
      timerHandle = requestAnimationFrame(tick);
      return;
    }

    if (run.stage === "dir-lis2") {
      const hard = run.listeningRoute === "upper";
      const seconds = hard ? 11 * 60 : 7 * 60;
      root.innerHTML = dir(
        "Listening, Module 2",
        "You will now begin the next module. You cannot return to previous questions.",
        "Módulo 1: " + Math.round((run.sectionScores.lis1.pct || 0) * 100) + "%. " + (hard ? "Conjunto mais difícil, 11:00." : "Conjunto mais fácil, 7:00.") + " Esses dois tempos estão no blueprint de 2026. A página de conteúdo publica 29 minutos, que coincidem com 18 + 11.",
        "Begin Module 2"
      );
      root.querySelector("#begin").onclick = () => { go("lis2"); startDeadline(run, seconds); redraw(); };
      return;
    }

    if (run.stage === "dir-wri") {
      root.innerHTML = dir(
        "Writing Section",
        "There are three tasks: Build a Sentence, Write an Email, and Write for an Academic Discussion.",
        "Primeiro os 10 Build a Sentence num bloco de 5:50. Esse relógio é o que a TST Prep descreve; a ETS não publicou os segundos, só os 23 minutos da seção, 7 do e-mail e 10 da discussão.",
        "Begin Writing"
      );
      root.querySelector("#begin").onclick = () => { go("bas"); startDeadline(run, 5 * 60 + 50); redraw(); };
      return;
    }

    if (run.stage === "bas") {
      const items = form.bas;
      if (!items.length) { root.innerHTML = "<p>Faltam itens de Build a Sentence do simulado.</p>"; return; }
      const item = items[Math.min(run.cursor, items.length - 1)];
      const left = remaining(run);
      let body = '<p class="kicker">Build a Sentence · ' + (run.cursor + 1) + " / " + items.length + "</p>";
      body += "<h2>" + esc(item.prompt) + "</h2>";
      body += '<div id="bas-host"></div>';
      body += '<div class="row" style="margin-top:12px"><button class="btn secondary" id="back">Back</button><button class="btn" id="next">' + (run.cursor === items.length - 1 ? "Continue" : "Next") + "</button></div>";
      body += '<p class="muted">Dá para voltar só dentro destes 10 itens. A ETS não confirmou essa navegação. O relógio de 5:50 não é um número oficial da ETS.</p>';
      root.innerHTML = shell("Writing", fmt(left || 0), left < 60, body, foot);
      const api = Widgets.mountBAS(root.querySelector("#bas-host"), item, {
        initial: run.answers["bas:" + item.id],
        onChange: (vals) => { run.answers["bas:" + item.id] = vals; persist(run); }
      });
      root.querySelector("#next").onclick = () => {
        run.answers["bas:" + item.id] = api.read();
        if (run.cursor >= items.length - 1) go("email-dir");
        else { run.cursor += 1; persist(run); redraw(); }
      };
      root.querySelector("#back").onclick = () => {
        if (run.cursor === 0) return;
        run.answers["bas:" + item.id] = api.read();
        run.cursor -= 1; persist(run); redraw();
      };
      root.querySelector("#abandon").onclick = () => abandon(() => go("email-dir"));
      timerHandle = requestAnimationFrame(tick);
      return;
    }

    if (run.stage === "email-dir") {
      root.innerHTML = dir(
        "Write an Email",
        "You will have 7 minutes to write an email in complete sentences.",
        "Sete minutos oficiais. Cubra os três pontos. Não há mínimo de palavras publicado para o e-mail.",
        "Begin"
      );
      root.querySelector("#begin").onclick = () => { go("email"); startDeadline(run, 7 * 60); redraw(); };
      return;
    }

    if (run.stage === "email" || run.stage === "disc") {
      const task = run.stage === "email" ? form.email : form.discussion;
      const left = remaining(run);
      if (!task) { root.innerHTML = "<p>Falta o enunciado desta tarefa no banco.</p>"; return; }
      let body = "";
      if (run.stage === "email") {
        body += "<h2>Write an Email</h2><p><b>To:</b> " + esc(task.to) + "<br><b>Subject:</b> " + esc(task.subject) + "</p>";
        body += "<p>" + esc(task.scenario) + "</p><ul>" + task.bullets.map((b) => "<li>" + esc(b) + "</li>").join("") + "</ul>";
        body += "<p>Write as much as you can and in complete sentences.</p>";
      } else {
        body += "<h2>Write for an Academic Discussion</h2><p>" + esc(task.course) + "</p>";
        body += "<div class=\"passage\"><b>Professor:</b> " + esc(task.question) + "</div>";
        body += "<div class=\"passage\"><b>" + esc(task.s1.name) + ":</b> " + esc(task.s1.text) + "</div>";
        body += "<div class=\"passage\"><b>" + esc(task.s2.name) + ":</b> " + esc(task.s2.text) + "</div>";
        body += "<p>An effective response will contain at least 100 words. You have 10 minutes.</p>";
      }
      const key = run.stage === "email" ? "email" : "disc";
      body += '<textarea id="essay">' + esc(run.answers[key] || "") + "</textarea>";
      body += '<p><span id="wc">0</span> palavras</p><button class="btn" id="next">Continue</button>';
      root.innerHTML = shell("Writing", fmt(left || 0), left < 60, body, foot);
      const area = root.querySelector("#essay");
      const wc = root.querySelector("#wc");
      const update = () => {
        run.answers[key] = area.value;
        wc.textContent = AudioKit.tokenize(area.value).length;
        persist(run);
      };
      area.addEventListener("input", update);
      update();
      root.querySelector("#next").onclick = () => { update(); go(run.stage === "email" ? "disc-dir" : "dir-spk"); };
      root.querySelector("#abandon").onclick = () => abandon(() => go(run.stage === "email" ? "disc-dir" : "dir-spk"));
      timerHandle = requestAnimationFrame(tick);
      return;
    }

    if (run.stage === "disc-dir") {
      root.innerHTML = dir(
        "Write for an Academic Discussion",
        "You will have 10 minutes. An effective response will contain at least 100 words.",
        "Dez minutos oficiais. Posição, motivo, exemplo e uma referência a um colega, com as suas palavras.",
        "Begin"
      );
      root.querySelector("#begin").onclick = () => { go("disc"); startDeadline(run, 10 * 60); redraw(); };
      return;
    }

    if (run.stage === "dir-spk") {
      root.innerHTML = dir(
        "Speaking Section",
        "You will listen and repeat seven sentences. Then you will answer four interview questions. There is no preparation time.",
        "A seção oficial dura cerca de 8 minutos. Cada repetição tem de 8 a 12 segundos; os sete números exatos não foram publicados, então usamos 8, 9, 9, 10, 11, 12 e 12. Cada resposta de entrevista tem 45 segundos.",
        "Begin Speaking"
      );
      root.querySelector("#begin").onclick = () => go("repeat");
      return;
    }

    if (run.stage === "repeat") {
      const sc = form.repeat;
      if (!sc) { root.innerHTML = "<p>Falta o cenário de Listen and Repeat.</p>"; return; }
      const i = run.index || 0;
      if (i >= sc.sentences.length) { go("interview"); return; }
      const sentence = sc.sentences[i];
      const seconds = [8, 9, 9, 10, 11, 12, 12][i] || 12;
      root.innerHTML = shell("Speaking · Listen and Repeat", "00:" + String(seconds).padStart(2, "0"), seconds < 10,
        "<p class=\"kicker\">Listen and repeat only once · " + (i + 1) + " / 7</p><h2>" + esc(sc.scenario) + "</h2><p id=\"status\">Ouça e repita. A frase não aparece agora.</p><p id=\"heard\" class=\"muted\"></p>", "");
      (async () => {
        await AudioKit.speak(sentence.text);
        if (run.view !== view) return;
        root.querySelector("#status").textContent = "Repita agora.";
        let left = seconds;
        const iv = setInterval(() => {
          left -= 1;
          const t = root.querySelector(".timer");
          if (t) t.textContent = "00:" + String(Math.max(0, left)).padStart(2, "0");
        }, 1000);
        try {
          const rec = await AudioKit.recordFor(seconds * 1000, (txt) => {
            const h = root.querySelector("#heard");
            if (h) h.textContent = txt;
          });
          clearInterval(iv);
          run.speak.repeat[i] = { transcript: rec.transcript, accuracy: AudioKit.align(sentence.text, rec.transcript).accuracy };
          persist(run);
        } catch (e) {
          clearInterval(iv);
          run.speak.repeat[i] = { transcript: "", accuracy: null, error: "microfone" };
          persist(run);
        }
        run.index = i + 1;
        persist(run);
        redraw();
      })();
      return;
    }

    if (run.stage === "interview") {
      const sc = form.interview;
      if (!sc) { root.innerHTML = "<p>Falta a entrevista.</p>"; return; }
      const i = run.index || 0;
      if (i >= sc.questions.length) { finishAll(); return; }
      const q = sc.questions[i];
      root.innerHTML = shell("Speaking · Take an Interview", "00:45", false,
        "<p class=\"kicker\">Question " + (i + 1) + " of 4 · no preparation</p><h2>" + esc(sc.scenario) + "</h2><div class=\"passage\" id=\"qtext\">" + esc(q.text) + "</div><p class=\"note\">Na prova a pergunta é falada. O texto fica aqui porque a voz do navegador não é o áudio oficial. Não confirmamos se a tela real mostra a pergunta.</p><p id=\"heard\"></p>", "");
      (async () => {
        await AudioKit.speak(q.text);
        if (run.view !== view) return;
        let left = 45;
        const iv = setInterval(() => {
          left -= 1;
          const t = root.querySelector(".timer");
          if (t) { t.textContent = "00:" + String(Math.max(0, left)).padStart(2, "0"); t.classList.toggle("low", left < 10); }
        }, 1000);
        try {
          const rec = await AudioKit.recordFor(45000, (txt) => {
            const h = root.querySelector("#heard");
            if (h) h.textContent = txt;
          });
          clearInterval(iv);
          const words = AudioKit.tokenize(rec.transcript);
          run.speak.interview[i] = { transcript: rec.transcript, words: words.length, pauses: rec.pauses, url: rec.url };
          persist(run);
        } catch (e) {
          clearInterval(iv);
          run.speak.interview[i] = { transcript: "", words: 0, error: "microfone" };
          persist(run);
        }
        run.index = i + 1;
        persist(run);
        redraw();
      })();
      return;
    }

    function finishAll() {
      const readBlocks = form.reading.m1.concat(form.reading[run.readingRoute || "lower"]);
      const lisBlocks = form.listening.m1.concat(form.listening[run.listeningRoute || "lower"]);
      const read = scoreReadingBlocks(readBlocks, run.answers);
      const lis = scoreListening(lisBlocks, run.answers);
      const bas = basScore(form.bas, run.answers);
      const emailText = run.answers.email || "";
      const discText = run.answers.disc || "";
      const emailScore = form.email ? Widgets.heuristicBand(Widgets.emailChecks(form.email, emailText)) : 0;
      const discScore = form.discussion ? Widgets.heuristicBand(Widgets.discussionChecks(form.discussion, discText)) : 0;
      const rawW = bas.hit + emailScore + discScore;
      const wBand = bandFromPct(rawW / 20, null);
      const readCap = run.readingRoute === "lower" ? 4 : null;
      const lisCap = run.listeningRoute === "lower" ? 4 : null;
      const rep = run.speak.repeat.filter((x) => x && x.accuracy != null);
      const repAvg = rep.length ? rep.reduce((s, x) => s + x.accuracy, 0) / rep.length : null;
      const interviews = run.speak.interview.filter(Boolean);
      const wordAvg = interviews.length ? interviews.reduce((s, x) => s + (x.words || 0), 0) / interviews.length : 0;
      let speakBand = null;
      if (repAvg != null) {
        const repPart = repAvg;
        const lenPart = wordAvg >= 70 ? 1 : wordAvg >= 45 ? 0.75 : wordAvg >= 25 ? 0.5 : 0.25;
        speakBand = bandFromPct(repPart * 0.55 + lenPart * 0.45, null);
      }
      const bands = {
        reading: bandFromPct(read.pct, readCap),
        listening: bandFromPct(lis.pct, lisCap),
        writing: wBand,
        speaking: speakBand
      };
      const nums = [bands.reading, bands.listening, bands.writing].concat(speakBand == null ? [] : [speakBand]);
      const overall = nums.length ? Math.round((nums.reduce((a, b) => a + b, 0) / nums.length) * 2) / 2 : null;
      const result = {
        when: new Date().toISOString(),
        mockId: run.mockId,
        bands, overall, read, lis, bas, emailScore, discScore, rawW,
        routes: { reading: run.readingRoute, listening: run.listeningRoute },
        speak: run.speak,
        emailText, discText
      };
      Store.get().mocks.push(result);
      Store.get().mockRun = null;
      Store.get().lastResult = result;
      Store.save();
      location.hash = "#/resultado";
    }

    if (run.stage === "results") location.hash = "#/resultado";
  }

  window.ExamKit = { assemble, countReading, countListening, render, fresh, bandFromPct };
})();
