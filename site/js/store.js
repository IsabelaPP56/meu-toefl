(function () {
  const KEY = "meutoefl.v1";
  function blank() {
    return {
      examDate: "2026-12-04",
      sessionLen: "padrao",
      diagnostic: null,
      priorities: ["escrita", "fala", "leitura", "escuta"],
      stats: { answered: 0, correct: 0, byTask: {} },
      errors: [],
      vocab: {},
      checks: {},
      mocks: [],
      mockRun: null,
      api: {
        provider: "openai",
        baseUrl: "https://api.openai.com/v1",
        model: "gpt-4o-mini",
        geminiModel: "gemini-2.5-flash",
        key: ""
      },
      homeChecks: {}
    };
  }
  let state = blank();
  try {
    const raw = localStorage.getItem(KEY);
    if (raw) state = Object.assign(blank(), JSON.parse(raw));
  } catch (e) { /* keep blank */ }

  function save() {
    localStorage.setItem(KEY, JSON.stringify(state));
  }

  function bump(task, ok) {
    state.stats.answered += 1;
    if (ok) state.stats.correct += 1;
    const bag = state.stats.byTask[task] || { answered: 0, correct: 0 };
    bag.answered += 1;
    if (ok) bag.correct += 1;
    state.stats.byTask[task] = bag;
    save();
  }

  function gradeError(id, task, ok, payload) {
    let e = state.errors.find((x) => x.id === id);
    const now = Date.now();
    if (!e) {
      e = { id, task, ease: 2.3, interval: 0, reps: 0, due: now, lapses: 0, payload };
      state.errors.push(e);
    }
    if (payload) e.payload = payload;
    if (!ok) {
      e.reps = 0;
      e.interval = 0;
      e.due = now;
      e.lapses = (e.lapses || 0) + 1;
      e.ease = Math.max(1.3, (e.ease || 2.3) - 0.2);
    } else {
      e.reps = (e.reps || 0) + 1;
      if (e.reps === 1) e.interval = 1;
      else if (e.reps === 2) e.interval = 3;
      else e.interval = Math.max(1, Math.round((e.interval || 3) * (e.ease || 2.3)));
      e.due = now + e.interval * 86400000;
      e.ease = Math.min(2.6, (e.ease || 2.3) + 0.05);
    }
    save();
  }

  function gradeVocab(id, rating) {
    const now = Date.now();
    const v = state.vocab[id] || { ease: 2.3, interval: 0, reps: 0, due: now };
    if (rating === "again") {
      v.reps = 0; v.interval = 0; v.due = now; v.ease = Math.max(1.3, v.ease - 0.2);
    } else {
      v.reps += 1;
      const mult = rating === "hard" ? 1.2 : rating === "easy" ? v.ease + 0.15 : v.ease;
      if (v.reps === 1) v.interval = rating === "easy" ? 3 : 1;
      else v.interval = Math.max(1, Math.round((v.interval || 1) * mult));
      v.due = now + v.interval * 86400000;
      if (rating === "easy") v.ease = Math.min(2.7, v.ease + 0.08);
    }
    state.vocab[id] = v;
    save();
  }

  window.Store = {
    get: () => state,
    save,
    bump,
    gradeError,
    gradeVocab,
    set(patch) { Object.assign(state, patch); save(); },
    reset() { state = blank(); save(); },
    backup() {
      const copy = JSON.parse(JSON.stringify(state));
      copy.api = Object.assign({}, copy.api, { key: "" });
      return JSON.stringify(copy, null, 2);
    }
  };
})();
