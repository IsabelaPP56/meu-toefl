(function () {
  function esc(s) {
    return String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  function ctwPieces(item) {
    const text = item.text || "";
    const dot = text.indexOf(".");
    if (dot < 0) return [{ type: "text", text }];
    const head = text.slice(0, dot + 1);
    const rest = text.slice(dot + 1);
    const pieces = [{ type: "text", text: head }];
    let cursor = 0;
    (item.gaps || []).forEach((word) => {
      const re = new RegExp("\\b" + word.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "\\b");
      const m = rest.slice(cursor).match(re);
      if (!m) return;
      const idx = cursor + m.index;
      pieces.push({ type: "text", text: rest.slice(cursor, idx) });
      const cut = Math.floor(word.length / 2);
      pieces.push({ type: "gap", prefix: word.slice(0, cut), missing: word.slice(cut), word });
      cursor = idx + word.length;
    });
    pieces.push({ type: "text", text: rest.slice(cursor) });
    return pieces;
  }

  function mountCTW(host, item, opts) {
    opts = opts || {};
    const pieces = ctwPieces(item);
    const gaps = pieces.filter((p) => p.type === "gap");
    host.innerHTML = "";
    let gi = 0;
    pieces.forEach((p) => {
      if (p.type === "text") {
        host.appendChild(document.createTextNode(p.text));
      } else {
        const wrap = document.createElement("span");
        wrap.className = "gap-word";
        wrap.appendChild(document.createTextNode(p.prefix));
        const input = document.createElement("input");
        input.className = "gap-input";
        input.maxLength = p.missing.length;
        input.size = Math.max(3, p.missing.length);
        input.setAttribute("aria-label", "letras que faltam em " + p.word);
        input.spellcheck = false;
        input.autocomplete = "off";
        input.dataset.i = String(gi);
        input.value = (opts.initial && opts.initial[gi]) || "";
        if (opts.locked) input.disabled = true;
        input.addEventListener("input", () => { if (opts.onChange) opts.onChange(read()); });
        wrap.appendChild(input);
        host.appendChild(wrap);
        gi += 1;
      }
    });
    function read() {
      return Array.from(host.querySelectorAll("input")).map((el) => el.value.trim());
    }
    function score() {
      const got = read();
      let hit = 0;
      gaps.forEach((g, i) => {
        const ok = (got[i] || "").toLowerCase() === g.missing.toLowerCase();
        if (ok) hit += 1;
        const input = host.querySelectorAll("input")[i];
        if (input && opts.reveal) {
          input.style.borderBottomColor = ok ? "#1d7a4d" : "#9d2c2c";
        }
      });
      return { hit, total: gaps.length, gaps, got };
    }
    return { read, score, gaps };
  }

  function mountBAS(host, item, opts) {
    opts = opts || {};
    const n = (item.template.match(/\{\d+\}/g) || []).length;
    let placed = Array.from({ length: n }, (_, i) => (opts.initial && opts.initial[i]) || null);
    const used = () => placed.filter(Boolean);
    function draw() {
      host.innerHTML = "";
      const line = document.createElement("div");
      line.className = "sentence-line";
      const parts = item.template.split(/(\{\d+\})/g);
      parts.forEach((part) => {
        const m = part.match(/^\{(\d+)\}$/);
        if (!m) { line.appendChild(document.createTextNode(part)); return; }
        const i = Number(m[1]);
        const slot = document.createElement("button");
        slot.type = "button";
        slot.className = "slot" + (placed[i] ? " filled" : "");
        slot.textContent = placed[i] || "···";
        slot.disabled = !!opts.locked;
        slot.addEventListener("click", () => {
          if (opts.locked || !placed[i]) return;
          placed[i] = null;
          draw();
        });
        slot.addEventListener("dragover", (e) => e.preventDefault());
        slot.addEventListener("drop", (e) => {
          e.preventDefault();
          const tile = e.dataTransfer.getData("text/plain");
          if (!tile || opts.locked) return;
          const from = placed.indexOf(tile);
          if (from >= 0) placed[from] = placed[i];
          placed[i] = tile;
          draw();
        });
        line.appendChild(slot);
      });
      const bank = document.createElement("div");
      bank.className = "tiles";
      item.tiles.forEach((tile) => {
        if (placed.includes(tile)) return;
        const b = document.createElement("button");
        b.type = "button";
        b.className = "tile";
        b.textContent = tile;
        b.draggable = !opts.locked;
        b.disabled = !!opts.locked;
        b.addEventListener("dragstart", (e) => e.dataTransfer.setData("text/plain", tile));
        b.addEventListener("click", () => {
          const hole = placed.findIndex((x) => !x);
          if (hole < 0 || opts.locked) return;
          placed[hole] = tile;
          draw();
        });
        bank.appendChild(b);
      });
      host.append(line, bank);
      if (opts.onChange) opts.onChange(placed.slice());
    }
    draw();
    return {
      read: () => placed.slice(),
      correct: () => placed.length === item.answer.length && placed.every((p, i) => p === item.answer[i])
    };
  }

  function emailChecks(item, text) {
    const raw = String(text || "");
    const low = raw.toLowerCase();
    const words = AudioKit.tokenize(raw);
    const checks = [];
    checks.push({
      ok: /^(hi|hello|dear|good morning|good afternoon|good evening)\b/i.test(raw.trim()),
      label: "Saudação",
      detail: "Comece com Dear, Hello ou Hi e o papel da pessoa."
    });
    item.keywords.forEach((group, i) => {
      const ok = (group || []).some((k) => low.includes(String(k).toLowerCase()));
      checks.push({ ok, label: "Ponto " + (i + 1), detail: item.bullets[i] });
    });
    checks.push({
      ok: /(best|regards|sincerely|thank|thanks|looking forward)/i.test(low),
      label: "Fecho",
      detail: "Uma linha de agradecimento ou Best regards fecha o e-mail."
    });
    checks.push({
      ok: words.length >= 80,
      label: "Elaboração (" + words.length + " palavras)",
      detail: "A ETS não publica mínimo para o e-mail. Pede frases completas. Meta de treino: 80 a 150."
    });
    const linkers = ["because", "however", "also", "could you", "please", "unfortunately", "in addition", "so that", "after"];
    const found = linkers.filter((l) => low.includes(l));
    checks.push({ ok: found.length >= 1, label: "Ligação entre ideias", detail: found.length ? found.join(", ") : "Inclua because, please, however ou could you." });
    return checks;
  }

  function discussionChecks(item, text) {
    const raw = String(text || "");
    const low = raw.toLowerCase();
    const words = AudioKit.tokenize(raw);
    const head = words.slice(0, 40).join(" ");
    const names = [item.s1.name, item.s2.name].filter(Boolean);
    const checks = [];
    checks.push({
      ok: /(i think|i believe|in my opinion|i agree|i disagree|should|shouldn't|should not)/i.test(head),
      label: "Posição cedo",
      detail: "A primeira ou segunda frase diz o que você acha."
    });
    checks.push({
      ok: /(because|since|the reason|this is)/i.test(low),
      label: "Motivo",
      detail: "Um motivo explícito vale mais do que dois motivos pela metade."
    });
    checks.push({
      ok: /(for example|for instance|such as|when i|last|once)/i.test(low),
      label: "Exemplo",
      detail: "Um caso concreto: quem, situação, resultado."
    });
    checks.push({
      ok: names.some((n) => low.includes(n.toLowerCase())) || /classmate|the point|the idea that|while .* said/i.test(low),
      label: "Colega",
      detail: "Cite " + names.join(" ou ") + " sem copiar a postagem."
    });
    checks.push({
      ok: words.length >= 100,
      label: "Pelo menos 100 palavras (" + words.length + ")",
      detail: "A instrução oficial da discussão pede uma resposta eficaz com pelo menos 100 palavras."
    });
    const copied = names.length && (item.s1.text + " " + item.s2.text).toLowerCase().split(/\s+/).filter((w, i, arr) => {
      const gram = arr.slice(i, i + 8).join(" ");
      return gram.length > 30 && low.includes(gram);
    }).length > 0;
    checks.push({ ok: !copied, label: "Palavras próprias", detail: copied ? "Há um trecho longo igual ao dos colegas." : "Não apareceu cópia longa do enunciado." });
    return checks;
  }

  function heuristicBand(checks) {
    if (!checks.length) return 0;
    const ratio = checks.filter((c) => c.ok).length / checks.length;
    const wordsOk = checks.some((c) => /palavras|100/.test(c.label) && c.ok);
    if (ratio >= 0.9 && wordsOk) return 5;
    if (ratio >= 0.75) return 4;
    if (ratio >= 0.55) return 3;
    if (ratio >= 0.35) return 2;
    if (ratio > 0) return 1;
    return 0;
  }

  function renderChecks(checks) {
    return checks.map((c) => '<div class="checkline"><span class="tag ' + (c.ok ? "ok" : "bad") + '">' + (c.ok ? "ok" : "rever") + "</span><div><b>" + esc(c.label) + "</b><div class=\"muted\">" + esc(c.detail) + "</div></div></div>").join("");
  }

  window.Widgets = { esc, ctwPieces, mountCTW, mountBAS, emailChecks, discussionChecks, heuristicBand, renderChecks };
})();
