(function () {
  function voices() {
    return window.speechSynthesis ? speechSynthesis.getVoices() : [];
  }
  function pickVoice() {
    const all = voices();
    return all.find((v) => /en-US/i.test(v.lang) && /female|samantha|aria|jenny/i.test(v.name))
      || all.find((v) => /^en-US/i.test(v.lang))
      || all.find((v) => /^en/i.test(v.lang))
      || null;
  }
  function speak(text, opts) {
    opts = opts || {};
    return new Promise((resolve) => {
      if (!window.speechSynthesis) { resolve({ ok: false }); return; }
      let done = false;
      const finish = (ok) => {
        if (done) return;
        done = true;
        resolve({ ok });
      };
      const u = new SpeechSynthesisUtterance(text);
      u.lang = opts.lang || "en-US";
      u.rate = opts.rate || 0.96;
      const v = pickVoice();
      if (v) u.voice = v;
      u.onend = () => finish(true);
      u.onerror = () => finish(false);
      speechSynthesis.cancel();
      speechSynthesis.speak(u);
      setTimeout(() => finish(false), Math.max(5000, String(text || "").length * 70));
    });
  }
  function stopSpeak() {
    if (window.speechSynthesis) speechSynthesis.cancel();
  }
  if (window.speechSynthesis) {
    speechSynthesis.onvoiceschanged = () => {};
  }

  function tokenize(s) {
    return String(s || "").toLowerCase().replace(/[^a-z0-9'\s]/g, " ").split(/\s+/).filter(Boolean);
  }

  function align(target, heard) {
    const a = tokenize(target);
    const b = tokenize(heard);
    const n = a.length, m = b.length;
    const dp = Array.from({ length: n + 1 }, () => Array(m + 1).fill(0));
    for (let i = n - 1; i >= 0; i--) {
      for (let j = m - 1; j >= 0; j--) {
        dp[i][j] = a[i] === b[j] ? dp[i + 1][j + 1] + 1 : Math.max(dp[i + 1][j], dp[i][j + 1]);
      }
    }
    const out = [];
    let i = 0, j = 0, hit = 0;
    while (i < n && j < m) {
      if (a[i] === b[j]) { out.push({ t: a[i], ok: true }); hit++; i++; j++; }
      else if (dp[i + 1][j] >= dp[i][j + 1]) { out.push({ t: a[i], miss: true }); i++; }
      else { out.push({ t: b[j], extra: true }); j++; }
    }
    while (i < n) out.push({ t: a[i++], miss: true });
    while (j < m) out.push({ t: b[j++], extra: true });
    return { tokens: out, accuracy: n ? hit / n : 0, target: n, hit };
  }

  const FILLERS = /\b(um+|uh+|er+|ah+|like|you know|kind of|sort of|actually|basically|i mean)\b/gi;

  async function recordFor(ms, onTick) {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const rec = new MediaRecorder(stream);
    const chunks = [];
    rec.ondataavailable = (e) => { if (e.data && e.data.size) chunks.push(e.data); };
    const stopped = new Promise((r) => { rec.onstop = r; });
    let transcript = "";
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recog = null;
    if (SR) {
      recog = new SR();
      recog.lang = "en-US";
      recog.continuous = true;
      recog.interimResults = true;
      recog.onresult = (ev) => {
        let finalTxt = "";
        let interim = "";
        for (let i = 0; i < ev.results.length; i++) {
          const piece = ev.results[i][0].transcript;
          if (ev.results[i].isFinal) finalTxt += piece + " ";
          else interim += piece + " ";
        }
        transcript = (finalTxt + interim).trim();
        if (onTick) onTick(transcript);
      };
      try { recog.start(); } catch (e) { recog = null; }
    }
    let pauses = 0;
    let silenceMs = 0;
    let inPause = false;
    let ctx = null;
    let timer = null;
    try {
      ctx = new AudioContext();
      const src = ctx.createMediaStreamSource(stream);
      const analyser = ctx.createAnalyser();
      analyser.fftSize = 2048;
      src.connect(analyser);
      const data = new Uint8Array(analyser.fftSize);
      timer = setInterval(() => {
        analyser.getByteTimeDomainData(data);
        let sum = 0;
        for (let i = 0; i < data.length; i++) {
          const v = (data[i] - 128) / 128;
          sum += v * v;
        }
        const rms = Math.sqrt(sum / data.length);
        if (rms < 0.02) {
          silenceMs += 100;
          if (silenceMs >= 700 && !inPause) { pauses += 1; inPause = true; }
        } else {
          silenceMs = 0;
          inPause = false;
        }
      }, 100);
    } catch (e) { ctx = null; }
    rec.start();
    await new Promise((r) => setTimeout(r, ms));
    if (recog) { try { recog.stop(); } catch (e) {} }
    if (rec.state !== "inactive") rec.stop();
    await stopped;
    if (timer) clearInterval(timer);
    if (ctx) { try { await ctx.close(); } catch (e) {} }
    stream.getTracks().forEach((t) => t.stop());
    const blob = new Blob(chunks, { type: rec.mimeType || "audio/webm" });
    return {
      blob,
      url: URL.createObjectURL(blob),
      transcript,
      pauses,
      recognition: Boolean(SR)
    };
  }

  window.AudioKit = { speak, stopSpeak, tokenize, align, FILLERS, recordFor };
})();
