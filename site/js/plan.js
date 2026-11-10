(function () {
  const WD = ["domingo", "segunda", "terça", "quarta", "quinta", "sexta", "sábado"];

  function todaySP() {
    return new Intl.DateTimeFormat("en-CA", { timeZone: "America/Sao_Paulo" }).format(new Date());
  }
  function utc(iso) {
    const [y, m, d] = iso.split("-").map(Number);
    return Date.UTC(y, m - 1, d);
  }
  function addDays(iso, n) {
    return new Date(utc(iso) + n * 86400000).toISOString().slice(0, 10);
  }
  function weekday(iso) { return WD[new Date(utc(iso)).getUTCDay()]; }
  function fmt(iso) {
    const [y, m, d] = iso.split("-");
    return d + "/" + m;
  }
  function daysUntil(exam) {
    return Math.round((utc(exam) - utc(todaySP())) / 86400000);
  }
  function range(start, endExclusive) {
    const out = [];
    let d = start;
    while (d < endExclusive) { out.push(d); d = addDays(d, 1); }
    return out;
  }

  function build(state) {
    const exam = state.examDate || "2026-12-04";
    const today = todaySP();
    const dates = range(today, exam);
    const n = dates.length;
    const short = state.sessionLen === "curto";
    const pri = state.priorities || ["escrita", "fala", "leitura", "escuta"];
    const mockAt = new Set();
    if (n >= 12) { mockAt.add(dates[Math.max(3, Math.round(n * 0.42))]); mockAt.add(dates[n - 3]); }
    else if (n >= 7) { mockAt.add(dates[Math.max(1, n - 6)]); mockAt.add(dates[n - 2]); }
    else if (n >= 4) { mockAt.add(dates[n - 2]); }
    let mockNum = 0;
    const cycle = pri[0] === "leitura"
      ? ["leitura", "email", "escuta", "discussao"]
      : pri[0] === "escuta"
        ? ["escuta", "email", "leitura", "discussao"]
        : ["email", "leitura", "discussao", "escuta"];

    const videos = {
      leitura: { href: "https://www.youtube.com/watch?v=eKaVhOnMjm8", title: "Reading 2026 (TST Prep) — só a parte da tarefa do dia" },
      escuta: { href: "https://www.youtube.com/watch?v=C0_sud-fw0k", title: "Listening 2026 (TST Prep) — uma tarefa, não o vídeo inteiro" },
      email: { href: "https://www.youtube.com/watch?v=bPRfxgXBQAI", title: "Write an Email 2026 (TST Prep)" },
      discussao: { href: "https://www.youtube.com/watch?v=SGP2VAnC_1I", title: "Templates 2026: e-mail e discussão" },
      bas: { href: "https://www.youtube.com/watch?v=XYLHVFBFsDc", title: "Build a Sentence 2026 (TST Prep)" },
      fala: { href: "https://www.youtube.com/watch?v=iR529CoRuZo", title: "Listen and Repeat 2026 (TST Prep)" }
    };

    return dates.map((iso, idx) => {
      const eve = idx === n - 1 && n > 1;
      const afterMock = idx > 0 && mockAt.has(dates[idx - 1]);
      const isMock = mockAt.has(iso) && !eve;
      let whichMock = null;
      if (isMock) { mockNum += 1; whichMock = mockNum; }
      const blocks = [];
      if (eve) {
        blocks.push({ id: "sono", title: "Logística e sono, não conteúdo novo", minutes: 20, href: "#/prova", note: "Confira documento, tomada, sala e Equipment Check. No máximo 3 frases curtas de aquecimento se a prova for amanhã." });
        return { iso, label: weekday(iso) + " " + fmt(iso), light: true, mock: null, minutes: 20, blocks, eve: true };
      }
      if (isMock) {
        blocks.push({ id: "mock", title: "Simulado " + whichMock + " na ordem da prova", minutes: 120, href: "#/simulado/" + whichMock, note: "Sem dicionário e sem pausa. A revisão fica para o dia seguinte." });
        return { iso, label: weekday(iso) + " " + fmt(iso), light: false, mock: whichMock, minutes: 130, blocks };
      }
      if (afterMock) {
        blocks.push({ id: "autopsia", title: "Autópsia do simulado", minutes: 35, href: "#/erros", note: "Separe erro de conhecimento, de atenção e de tempo. Refaça só o que errou." });
        blocks.push({ id: "regrava", title: "Regrave 2 respostas de fala", minutes: 15, href: "#/coach-fala?mode=interview&n=2", note: "Uma tentativa, ouvir, uma segunda." });
        return { iso, label: weekday(iso) + " " + fmt(iso), light: true, mock: null, minutes: short ? 40 : 55, blocks };
      }
      const focus = cycle[idx % cycle.length];
      blocks.push({ id: "erros", title: "Erros que já venceram o prazo", minutes: short ? 6 : 8, href: "#/erros", note: "Recuperação ativa: responda de novo antes de ver a explicação." });
      blocks.push({ id: "bas", title: "Build a Sentence, " + (short ? "5" : "8") + " itens", minutes: short ? 8 : 12, href: "#/pratica/bas?n=" + (short ? 5 : 8), note: "Prioridade. Anote o padrão (indireta, auxiliar, relativa, passiva)." });
      blocks.push({ id: "repeat", title: "Listen and Repeat em blocos", minutes: short ? 10 : 14, href: "#/coach-fala?mode=repeat", note: "Primeiro no modo bloco se a frase some no meio. Depois a frase inteira, uma vez." });
      blocks.push({ id: "entrevista", title: "Entrevista, " + (short ? "1" : "2") + " pergunta(s) de 45 s", minutes: short ? 6 : 10, href: "#/coach-fala?mode=interview&n=" + (short ? 1 : 2), note: "Resposta direta, motivo, exemplo. Regrave a mais fraca." });
      if (focus === "email") {
        blocks.push({ id: "email", title: "Um e-mail em 7 minutos", minutes: 12, href: "#/coach-escrita?task=email", note: "1 min de plano dos 3 pontos, 5 de texto, 1 de revisão." });
      } else if (focus === "discussao") {
        blocks.push({ id: "disc", title: "Uma discussão em 10 minutos", minutes: 14, href: "#/coach-escrita?task=discussion", note: "Posição, um motivo, um exemplo, uma frase sobre o colega. Meta: 100 palavras." });
      } else if (focus === "leitura") {
        blocks.push({ id: "ler", title: "Leitura: lacunas + um texto curto", minutes: short ? 12 : 20, href: "#/pratica/daily?n=4", note: "Depois faça um Complete the Words. Evidência antes de marcar." });
      } else {
        blocks.push({ id: "ouvir", title: "Escuta sem transcrição", minutes: short ? 12 : 20, href: "#/pratica/choose?n=6", note: "Uma vez só. Em seguida uma conversa ou um anúncio." });
      }
      if (!short && idx % 3 === 0) {
        const v = videos[focus] || videos.bas;
        blocks.push({ id: "video", title: "Vídeo curto: " + v.title, minutes: 15, href: v.href, note: "Pause e responda antes de ver o modelo. Não assista a playlist inteira." });
      }
      blocks.push({ id: "vocab", title: "8 cartões", minutes: 8, href: "#/vocab", note: "Frase, não palavra solta. Os cartões vencidos vêm primeiro." });
      const minutes = blocks.reduce((s, b) => s + b.minutes, 0);
      return { iso, label: weekday(iso) + " " + fmt(iso), light: short, mock: null, minutes, blocks, focus };
    });
  }

  window.PlanKit = { todaySP, daysUntil, weekday, fmt, build, addDays };
})();
