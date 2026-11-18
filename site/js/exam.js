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

  function adjustBand(band, flags) {
    if (band == null || !flags) return band;
    const n = ["points", "example", "grammar", "clear"].filter((k) => flags[k]).length;
    let b = band;
    if (n >= 4) b += 0.5;
    else if (n === 2) b -= 0.5;
    else if (n <= 1) b -= 1;
    return Math.max(1, Math.min(6, Math.round(b * 2) / 2));
  }

  function cefrOf(band) {
    if (band == null) return "—";
    if (band >= 6) return "C2";
    if (band >= 5) return "C1";
    if (band >= 4) return "B2";
    if (band >= 3) return "B1";
    if (band >= 2) return "A2";
    return "A1";
  }

  function overallOf(bands, keys) {
    const nums = keys.map((k) => bands[k]).filter((n) => n != null);
    if (!nums.length) return null;
    return Math.round((nums.reduce((a, b) => a + b, 0) / nums.length) * 2) / 2;
  }

  function skillBands(form, run) {
    const readBlocks = form.reading.m1.concat(form.reading[run.readingRoute || "lower"]);
    const lisBlocks = form.listening.m1.concat(form.listening[run.listeningRoute || "lower"]);
    const read = scoreReadingBlocks(readBlocks, run.answers);
    const lis = scoreListening(lisBlocks, run.answers);
    const bas = basScore(form.bas, run.answers);
    const emailScore = form.email ? Widgets.heuristicBand(Widgets.emailChecks(form.email, run.answers.email || "")) : 0;
    const discScore = form.discussion ? Widgets.heuristicBand(Widgets.discussionChecks(form.discussion, run.answers.disc || "")) : 0;
    const writingBase = bandFromPct((bas.hit + emailScore + discScore) / 20, null);
    const writing = adjustBand(writingBase, run.rubric && run.rubric.writing);
    const readCap = run.readingRoute === "lower" ? 4 : null;
    const lisCap = run.listeningRoute === "lower" ? 4 : null;
    const rep = (run.speak.repeat || []).filter((x) => x && x.accuracy != null);
    const repAvg = rep.length ? rep.reduce((s, x) => s + x.accuracy, 0) / rep.length : null;
    const interviews = (run.speak.interview || []).filter(Boolean);
    const wordAvg = interviews.length ? interviews.reduce((s, x) => s + (x.words || 0), 0) / interviews.length : 0;
    let speakingBase = null;
    if (repAvg != null || interviews.length) {
      const repPart = repAvg == null ? 0.4 : repAvg;
      const lenPart = wordAvg >= 70 ? 1 : wordAvg >= 45 ? 0.75 : wordAvg >= 25 ? 0.5 : 0.25;
      speakingBase = bandFromPct(repPart * 0.55 + lenPart * 0.45, null);
    }
    const speaking = adjustBand(speakingBase, run.rubric && run.rubric.speaking);
    return {
      reading: bandFromPct(read.pct, readCap),
      listening: bandFromPct(lis.pct, lisCap),
      writing, speaking, writingBase, speakingBase,
      read, lis, bas, emailScore, discScore
    };
  }

  function markPhrases(text, phrases) {
    let html = esc(text || "").replace(/\n/g, "<br>");
    (phrases || []).forEach((p) => {
      if (!p) return;
      const e = esc(p);
      html = html.split(e).join("<mark>" + e + "</mark>");
    });
    return html;
  }

  function modelHtml(m) {
    if (!m) return "<p class=\"muted\">Sem modelo para este item.</p>";
    return '<p class="tag">Banda 5–6</p><p>' + markPhrases(m.high, m.phrases) + '</p><p class="tag">B2 · banda 4, meta realista</p><p>' + markPhrases(m.b2, m.phrases) + '</p><p class="muted">' + esc(m.note) + "</p>";
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
      if (run.stage === "read2") return go("sec-read");
      if (run.stage === "lis1") return finishLis1();
      if (run.stage === "lis2") return go("sec-lis");
      if (run.stage === "bas") return go("email");
      if (run.stage === "email") return go("disc");
      if (run.stage === "disc") return go("sec-wri");
      if (run.stage === "repeat" || run.stage === "interview") {
        const i = run.index || 0;
        run.review = { kind: run.stage, i };
        return go("model", { index: i });
      }
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
      root.querySelector("#abandon").onclick = () => abandon(() => run.stage === "read1" ? finishRead1() : go("sec-read"));
      function step(d) {
        const nxt = run.cursor + d;
        if (nxt < 0) return;
        if (nxt >= units.length) {
          if (run.stage === "read1") finishRead1();
          else go("sec-read");
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
        await AudioKit.speak("This is a volume check. Listening is about to begin.", { rate: 1 });
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
        if (run.stage === "lis1") finishLis1(); else go("sec-lis");
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
        root.querySelector("#abandon").onclick = () => abandon(() => run.stage === "lis1" ? finishLis1() : go("sec-lis"));
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
          if (run.stage === "lis1") finishLis1(); else go("sec-lis");
        } else redraw();
      };
      root.querySelector("#abandon").onclick = () => abandon(() => run.stage === "lis1" ? finishLis1() : go("sec-lis"));
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
      root.querySelector("#next").onclick = () => { update(); go(run.stage === "email" ? "disc-dir" : "sec-wri"); };
      root.querySelector("#abandon").onclick = () => abandon(() => go(run.stage === "email" ? "disc-dir" : "sec-wri"));
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
        await AudioKit.speak(sentence.text, { rate: 1 });
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
        run.review = { kind: "repeat", i };
        go("model", { index: i });
      })();
      return;
    }

    if (run.stage === "interview") {
      const sc = form.interview;
      if (!sc) { root.innerHTML = "<p>Falta a entrevista.</p>"; return; }
      const i = run.index || 0;
      if (i >= sc.questions.length) { go("sec-spk"); return; }
      const q = sc.questions[i];
      root.innerHTML = shell("Speaking · Take an Interview", "00:45", false,
        "<p class=\"kicker\">Question " + (i + 1) + " of 4 · no preparation</p><h2>" + esc(sc.scenario) + "</h2><div class=\"passage\" id=\"qtext\">" + esc(q.text) + "</div><p class=\"note\">Na prova a pergunta é falada. O texto fica aqui porque a voz do navegador não é o áudio oficial. Não confirmamos se a tela real mostra a pergunta.</p><p id=\"heard\"></p>", "");
      (async () => {
        await AudioKit.speak(q.text, { rate: 1 });
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
        run.review = { kind: "interview", i };
        go("model", { index: i });
      })();
      return;
    }

    if (run.stage === "sec-read" || run.stage === "sec-lis" || run.stage === "sec-wri" || run.stage === "sec-spk") {
      const keys = run.stage === "sec-read" ? ["reading"]
        : run.stage === "sec-lis" ? ["reading", "listening"]
        : run.stage === "sec-wri" ? ["reading", "listening", "writing"]
        : ["reading", "listening", "writing", "speaking"];
      const partial = run.stage !== "sec-spk";
      const snap = skillBands(form, run);
      const cards = keys.map((k) => {
        const name = { reading: "Reading", listening: "Listening", writing: "Writing", speaking: "Speaking" }[k];
        const v = snap[k];
        const c = cefrOf(v);
        return '<div class="card stat"><b id="band-' + k + '">' + (v == null ? "—" : v.toFixed(1)) + "</b>" + name +
          '<div class="muted">CEFR <span class="' + (c === "B2" ? "cefr goal" : "cefr") + '" id="cefr-' + k + '">' + c + "</span>" +
          (c === "B2" ? " · sua meta" : "") + "</div></div>";
      }).join("");
      const ov = overallOf(snap, keys);
      const oc = cefrOf(ov);
      let body = "<h2>Estimativa da seção</h2><p class=\"muted\">Estimativa deste site, não é nota da ETS. B2 (banda 4 a 4,5) é a sua meta.</p><div class=\"grid-4\">" + cards + "</div>";
      body += "<p>Geral " + (partial ? "até aqui" : "") + ': <b id="band-overall">' + (ov == null ? "—" : ov.toFixed(1)) + '</b> · CEFR <span id="cefr-overall" class="' + (oc === "B2" ? "cefr goal" : "cefr") + '">' + oc + "</span></p>";
      if (run.stage === "sec-wri" || run.stage === "sec-spk") {
        const kind = run.stage === "sec-wri" ? "writing" : "speaking";
        const labels = kind === "writing"
          ? [["points", "Cobri o que a tarefa pediu"], ["example", "Dei um detalhe ou exemplo"], ["grammar", "Frases completas, com um conector"], ["clear", "Os erros não atrapalham a leitura"]]
          : [["points", "Respondi o que foi perguntado"], ["example", "Dei motivo e exemplo"], ["grammar", "Dá para me entender"], ["clear", "Falei com poucas pausas e poucos fillers"]];
        const cur = (run.rubric && run.rubric[kind]) || {};
        body += '<fieldset class="card"><legend>Autoavaliação · entra na estimativa</legend>' +
          labels.map(([k, lab]) => '<label class="checkline"><input type="checkbox" data-rub="' + k + '"' + (cur[k] ? " checked" : "") + "> " + lab + "</label>").join("") +
          '<p class="muted">Quatro marcas sobem 0,5. Duas descem 0,5. Uma ou nenhuma desce 1.</p></fieldset>';
      }
      if (run.stage === "sec-wri") {
        const models = window.MODELS || {};
        const em = form.email && models.email && models.email[form.email.id];
        const di = form.discussion && models.discussion && models.discussion[form.discussion.id];
        body += "<details class=\"card\"><summary>Respostas-modelo do e-mail e da discussão</summary>" + modelHtml(em) + "<hr>" + modelHtml(di) + "</details>";
      }
      const nextLabel = run.stage === "sec-read" ? "Continuar para Listening"
        : run.stage === "sec-lis" ? "Continuar para Writing"
        : run.stage === "sec-wri" ? "Continuar para Speaking"
        : "Ver resultado";
      body += '<p><button class="btn" id="next">' + nextLabel + "</button></p>";
      root.innerHTML = shell("Estimativa", "", false, body, "");
      root.querySelectorAll("[data-rub]").forEach((el) => {
        el.onchange = () => {
          const kind = run.stage === "sec-wri" ? "writing" : "speaking";
          run.rubric = run.rubric || {};
          run.rubric[kind] = run.rubric[kind] || {};
          run.rubric[kind][el.dataset.rub] = el.checked;
          persist(run);
          const again = skillBands(form, run);
          ["writing", "speaking"].forEach((k) => {
            const node = root.querySelector("#band-" + k);
            if (node) node.textContent = again[k] == null ? "—" : again[k].toFixed(1);
            const cf = root.querySelector("#cefr-" + k);
            if (cf) {
              cf.textContent = cefrOf(again[k]);
              cf.className = cefrOf(again[k]) === "B2" ? "cefr goal" : "cefr";
            }
          });
          const keysNow = run.stage === "sec-wri" ? ["reading", "listening", "writing"] : ["reading", "listening", "writing", "speaking"];
          const o2 = overallOf(again, keysNow);
          const ob = root.querySelector("#band-overall");
          if (ob) ob.textContent = o2 == null ? "—" : o2.toFixed(1);
          const oc2 = root.querySelector("#cefr-overall");
          if (oc2) { oc2.textContent = cefrOf(o2); oc2.className = cefrOf(o2) === "B2" ? "cefr goal" : "cefr"; }
        };
      });
      root.querySelector("#next").onclick = () => {
        if (run.stage === "sec-read") go("vol-lis");
        else if (run.stage === "sec-lis") go("dir-wri");
        else if (run.stage === "sec-wri") go("dir-spk");
        else finishAll();
      };
      return;
    }

    if (run.stage === "model") {
      const rev = run.review || { kind: "repeat", i: 0 };
      const models = window.MODELS || {};
      let body = "<h2>Depois da sua tentativa</h2>";
      if (rev.kind === "repeat" && form.repeat) {
        const sent = form.repeat.sentences[rev.i];
        const pack = models.repeat && models.repeat[form.repeat.id];
        const m = pack && pack[rev.i];
        const got = (run.speak.repeat[rev.i] && run.speak.repeat[rev.i].transcript) || "";
        body += "<p class=\"muted\">A frase só aparece agora, depois da tentativa.</p>";
        body += "<p>Você disse: " + esc(got || "(sem transcrição)") + "</p>";
        body += modelHtml(m || (sent ? { high: sent.text, b2: sent.text, phrases: [], note: "A meta alta é a frase exata." } : null));
      } else if (form.interview) {
        const q = form.interview.questions[rev.i];
        const pack = models.interview && models.interview[form.interview.id];
        const m = pack && pack[rev.i];
        body += "<p><b>" + esc(q ? q.text : "") + "</b></p>";
        body += modelHtml(m);
      }
      body += '<p><button class="btn" id="next">Continuar</button></p>';
      root.innerHTML = shell("Speaking", "", false, body, "");
      root.querySelector("#next").onclick = () => {
        const nextI = rev.i + 1;
        if (rev.kind === "repeat") {
          const len = form.repeat ? form.repeat.sentences.length : 0;
          if (nextI >= len) go("interview");
          else go("repeat", { index: nextI });
        } else {
          const len = form.interview ? form.interview.questions.length : 0;
          if (nextI >= len) go("sec-spk");
          else go("interview", { index: nextI });
        }
      };
      return;
    }

    function finishAll() {
      const snap = skillBands(form, run);
      const bands = {
        reading: snap.reading,
        listening: snap.listening,
        writing: snap.writing,
        speaking: snap.speaking
      };
      const overall = overallOf(bands, ["reading", "listening", "writing", "speaking"]);
      const result = {
        when: new Date().toISOString(),
        mockId: run.mockId,
        bands, overall,
        base: { writing: snap.writingBase, speaking: snap.speakingBase },
        rubric: run.rubric || {},
        read: snap.read, lis: snap.lis, bas: snap.bas,
        emailScore: snap.emailScore, discScore: snap.discScore,
        rawW: snap.bas.hit + snap.emailScore + snap.discScore,
        routes: { reading: run.readingRoute, listening: run.listeningRoute },
        speak: run.speak,
        emailText: run.answers.email || "",
        discText: run.answers.disc || "",
        prompts: {
          email: form.email && form.email.id,
          discussion: form.discussion && form.discussion.id,
          repeat: form.repeat && form.repeat.id,
          interview: form.interview && form.interview.id
        }
      };
      Store.get().mocks.push(result);
      Store.get().mockRun = null;
      Store.get().lastResult = result;
      Store.save();
      location.hash = "#/resultado";
    }

    if (run.stage === "results") location.hash = "#/resultado";
  }

  window.ExamKit = { assemble, countReading, countListening, render, fresh, bandFromPct, cefrOf, adjustBand, overallOf };
})();
