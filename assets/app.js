/* ==========================================================================
   PyPath — portal app
   Pure vanilla JS. No build step, no framework.
   ========================================================================== */

(() => {
  "use strict";

  const DATA = window.PYCOURSE;
  if (!DATA) {
    document.body.innerHTML =
      '<p style="padding:40px;font-family:sans-serif">data.js was not found. First run <code>python portal/build_portal.py</code>.</p>';
    return;
  }

  const chapters = DATA.chapters;
  const byNum = new Map(chapters.map((c) => [c.num, c]));
  const dsaChapters = DATA.dsaChapters || [];
  const dsaByNum = new Map(dsaChapters.map((c) => [c.num, c]));
  const STORAGE_KEY = "pypath.progress.v2";

  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));

  const SUN_SVG =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>';
  const MOON_SVG =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 12.8A8.5 8.5 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';

  /* ========================================================================
     Progress
     ======================================================================== */

  const DEFAULT_PROGRESS = {
    completed: [],
    dsaCompleted: [],
    quizTotal: 0,
    quizCorrect: 0,
    dsaQuizTotal: 0,
    dsaQuizCorrect: 0,
    streak: 0,
    lastDay: null,
    theme: "dark",
    kid: true,
  };

  function loadProgress() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        return {
          ...DEFAULT_PROGRESS,
          ...parsed,
          completed: Array.isArray(parsed.completed) ? parsed.completed : [],
          dsaCompleted: Array.isArray(parsed.dsaCompleted) ? parsed.dsaCompleted : [],
        };
      }
    } catch (error) {
      /* localStorage blocked - ignore */
    }
    return { ...DEFAULT_PROGRESS };
  }

  let progress = loadProgress();

  function saveProgress() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
    } catch (error) {
      /* ignore */
    }
    updateChrome();
  }

  function isDone(num) {
    return progress.completed.includes(num);
  }

  function isDsaDone(num) {
    return (progress.dsaCompleted || []).includes(num);
  }

  function todayISO() {
    const now = new Date();
    const local = new Date(now.getTime() - now.getTimezoneOffset() * 60000);
    return local.toISOString().slice(0, 10);
  }

  function updateStreak() {
    const today = todayISO();
    if (progress.lastDay === today) return;

    const yesterday = new Date(Date.now() - 86400000);
    const yLocal = new Date(yesterday.getTime() - yesterday.getTimezoneOffset() * 60000)
      .toISOString()
      .slice(0, 10);

    progress.streak = progress.lastDay === yLocal ? (progress.streak || 0) + 1 : 1;
    progress.lastDay = today;
    saveProgress();
  }

  /* ========================================================================
     Tiny utilities
     ======================================================================== */

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, (ch) => {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch];
    });
  }

  function shortTitle(chapter) {
    return chapter.title.replace(/^(Chapter|DSA)\s+\d+\s*-\s*/i, "");
  }

  function toast(message) {
    const el = $("#toast");
    if (!el) return;
    el.textContent = message;
    el.classList.add("show");
    clearTimeout(toast._timer);
    toast._timer = setTimeout(() => el.classList.remove("show"), 2200);
  }

  async function copyText(text, button) {
    try {
      await navigator.clipboard.writeText(text);
    } catch (error) {
      const helper = document.createElement("textarea");
      helper.value = text;
      helper.style.position = "fixed";
      helper.style.opacity = "0";
      document.body.appendChild(helper);
      helper.select();
      document.execCommand("copy");
      helper.remove();
    }
    if (button) {
      const original = button.textContent;
      button.textContent = "Copied!";
      setTimeout(() => {
        button.textContent = original;
      }, 1400);
    }
    toast("Code copied");
  }

  /* ========================================================================
     Markdown renderer (small, purpose-built)
     ======================================================================== */

  const PY_TOKEN =
    /(#[^\n]*)|("""[\s\S]*?"""|'''[\s\S]*?'''|"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*')|\b(def|class|return|if|elif|else|for|while|in|not|and|or|import|from|as|try|except|finally|raise|with|lambda|yield|pass|break|continue|global|nonlocal|assert|del|is|None|True|False|async|await|match|case)\b|\b(\d+(?:\.\d+)?)\b|(@[A-Za-z_]\w*)/g;

  function highlightPython(code) {
    let html = "";
    let lastIndex = 0;
    let match;
    PY_TOKEN.lastIndex = 0;

    while ((match = PY_TOKEN.exec(code)) !== null) {
      html += escapeHtml(code.slice(lastIndex, match.index));
      if (match[1]) html += `<span class="tok-com">${escapeHtml(match[1])}</span>`;
      else if (match[2]) html += `<span class="tok-str">${escapeHtml(match[2])}</span>`;
      else if (match[3]) html += `<span class="tok-kw">${escapeHtml(match[3])}</span>`;
      else if (match[4]) html += `<span class="tok-num">${escapeHtml(match[4])}</span>`;
      else if (match[5]) html += `<span class="tok-dec">${escapeHtml(match[5])}</span>`;
      lastIndex = match.index + match[0].length;
    }

    html += escapeHtml(code.slice(lastIndex));
    return html;
  }

  function renderCodeBlock(code, lang = "python", runnable = true) {
    const canRun = runnable && (lang === "python" || lang === "" || lang === "py");
    return `<div class="code-block">
      <div class="code-head">
        <span class="code-lang">${escapeHtml(lang || "python")}</span>
        <div class="code-actions">
          <button class="mini-btn" data-action="copy" type="button">Copy</button>
          ${canRun ? '<button class="mini-btn run" data-action="run" type="button">Run</button>' : ""}
        </div>
      </div>
      <pre><code>${highlightPython(code)}</code></pre>
      <pre class="console" hidden></pre>
    </div>`;
  }

  function inlineMarkdown(text) {
    const inlineCode = [];

    let output = text.replace(/`([^`]+)`/g, (match, code) => {
      inlineCode.push(code);
      return `\u0001IC${inlineCode.length - 1}\u0001`;
    });

    output = output.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    output = output.replace(/(^|[\s(])\*([^*\n]+)\*(?=[\s).,!?]|$)/g, "$1<em>$2</em>");
    output = output.replace(
      /\[([^\]]+)\]\(([^)\s]+)\)/g,
      '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>'
    );
    output = output.replace(/\u0001IC(\d+)\u0001/g, (match, index) => `<code>${inlineCode[Number(index)]}</code>`);

    return output;
  }

  function markdownToHtml(source) {
    if (!source) return "";

    const blocks = [];
    let text = String(source).replace(/\r\n/g, "\n");

    text = text.replace(/```([\w+-]*)\n([\s\S]*?)```/g, (match, lang, code) => {
      const index = blocks.length;
      blocks.push(renderCodeBlock(code.replace(/\n$/, ""), lang || "python"));
      return `\u0000CODE${index}\u0000`;
    });

    text = escapeHtml(text);

    const lines = text.split("\n");
    let html = "";
    let paragraph = [];
    let listType = null;
    let tableRows = [];

    const flushParagraph = () => {
      if (paragraph.length) {
        html += `<p>${inlineMarkdown(paragraph.join(" "))}</p>`;
        paragraph = [];
      }
    };

    const closeList = () => {
      if (listType) {
        html += `</${listType}>`;
        listType = null;
      }
    };

    const flushTable = () => {
      if (!tableRows.length) return;

      if (tableRows.length < 2) {
        html += tableRows.map((row) => `<p>${inlineMarkdown(row)}</p>`).join("");
        tableRows = [];
        return;
      }

      const cells = (row) =>
        row
          .replace(/^\|/, "")
          .replace(/\|$/, "")
          .split("|")
          .map((cell) => cell.trim());

      const head = cells(tableRows[0]);
      const body = tableRows.slice(2).map(cells);

      html += `<div class="table-wrap"><table><thead><tr>${head
        .map((cell) => `<th>${inlineMarkdown(cell)}</th>`)
        .join("")}</tr></thead><tbody>${body
        .map(
          (row) =>
            `<tr>${row.map((cell) => `<td>${inlineMarkdown(cell)}</td>`).join("")}</tr>`
        )
        .join("")}</tbody></table></div>`;
      tableRows = [];
    };

    for (const raw of lines) {
      const line = raw.trim();
      const codeMatch = line.match(/^\u0000CODE(\d+)\u0000$/);

      if (codeMatch) {
        flushParagraph();
        closeList();
        flushTable();
        html += blocks[Number(codeMatch[1])];
        continue;
      }

      if (!line) {
        flushParagraph();
        closeList();
        flushTable();
        continue;
      }

      const heading = line.match(/^(#{1,4})\s+(.*)$/);
      if (heading) {
        flushParagraph();
        closeList();
        flushTable();
        const level = heading[1].length;
        html += `<h${level}>${inlineMarkdown(heading[2])}</h${level}>`;
        continue;
      }

      if (/^(-{3,}|\*{3,})$/.test(line)) {
        flushParagraph();
        closeList();
        flushTable();
        html += "<hr>";
        continue;
      }

      if (line.startsWith("&gt; ")) {
        flushParagraph();
        closeList();
        flushTable();
        html += `<blockquote><p>${inlineMarkdown(line.slice(5))}</p></blockquote>`;
        continue;
      }

      const listItem = line.match(/^([-*]|\d+\.)\s+(.*)$/);
      if (listItem) {
        flushParagraph();
        flushTable();
        const wanted = /^\d/.test(listItem[1]) ? "ol" : "ul";
        if (listType !== wanted) {
          closeList();
          html += `<${wanted}>`;
          listType = wanted;
        }
        html += `<li>${inlineMarkdown(listItem[2])}</li>`;
        continue;
      }

      if (line.startsWith("|") && line.endsWith("|")) {
        flushParagraph();
        closeList();
        tableRows.push(line);
        continue;
      }

      flushTable();
      closeList();
      paragraph.push(line);
    }

    flushParagraph();
    closeList();
    flushTable();

    html = html.replace(/\u0000CODE(\d+)\u0000/g, (match, index) => blocks[Number(index)]);
    return html;
  }

  /* ========================================================================
     Pyodide (in-browser Python)
     ======================================================================== */

  let pyodideInstance = null;
  let pyodidePromise = null;

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const script = document.createElement("script");
      script.src = src;
      script.onload = resolve;
      script.onerror = () => reject(new Error("Pyodide could not be downloaded. Check your internet connection."));
      document.head.appendChild(script);
    });
  }

  async function getPyodide() {
    if (pyodideInstance) return pyodideInstance;

    if (!pyodidePromise) {
      pyodidePromise = (async () => {
        if (!window.loadPyodide) {
          await loadScript("https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js");
        }
        pyodideInstance = await window.loadPyodide({
          indexURL: "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/",
        });
        return pyodideInstance;
      })();
    }

    try {
      return await pyodidePromise;
    } catch (error) {
      pyodidePromise = null;
      throw error;
    }
  }

  async function executePython(code) {
    const pyodide = await getPyodide();
    let output = "";

    pyodide.setStdout({ batched: (line) => { output += line + "\n"; } });
    pyodide.setStderr({ batched: (line) => { output += line + "\n"; } });

    try {
      await pyodide.runPythonAsync(code);
      return { output, error: null };
    } catch (error) {
      return { output, error: error && error.message ? error.message : String(error) };
    }
  }

  async function runPython(code, outputEl) {
    if (!outputEl) return;

    outputEl.hidden = false;
    outputEl.classList.remove("error");
    outputEl.textContent = "Loading the Python engine... (first run ~10-20s, internet required)";

    try {
      outputEl.textContent = "Running...\n";
      const result = await executePython(code);
      if (result.error) {
        outputEl.classList.add("error");
        outputEl.textContent = "Error:\n" + result.error;
      } else {
        outputEl.textContent = result.output || "(no output)";
      }
    } catch (error) {
      outputEl.classList.add("error");
      outputEl.textContent = "Error:\n" + (error && error.message ? error.message : String(error));
    }
  }

  /* ========================================================================
     Chrome: sidebar, streak, theme
     ======================================================================== */

  function updateChrome() {
    const done = progress.completed.length;
    const percent = chapters.length ? (done / chapters.length) * 100 : 0;

    const navCount = $("#navChapterCount");
    if (navCount) navCount.textContent = chapters.length;

    const progressText = $("#sidebarProgressText");
    if (progressText) progressText.textContent = `${done}/${chapters.length}`;

    const progressBar = $("#sidebarProgressBar");
    if (progressBar) progressBar.style.width = `${percent}%`;

    const sidebarStreak = $("#sidebarStreak");
    if (sidebarStreak) sidebarStreak.textContent = progress.streak || 0;

    const topStreak = $("#topStreak");
    if (topStreak) topStreak.textContent = progress.streak || 0;

    const dsaNavCount = $("#navDsaCount");
    if (dsaNavCount) dsaNavCount.textContent = dsaChapters.length;

    const dsaDone = progress.dsaCompleted ? progress.dsaCompleted.length : 0;
    const dsaProgressText = $("#dsaProgressText");
    if (dsaProgressText) dsaProgressText.textContent = `${dsaDone}/${dsaChapters.length}`;

    const dsaChapterNav = $("#dsaChapterNav");
    if (dsaChapterNav) {
      dsaChapterNav.innerHTML = dsaChapters
        .map(
          (chapter) => `<a class="chapter-nav-item dsa-item ${isDsaDone(chapter.num) ? "done" : ""}" href="#/dsa/${chapter.num}">
            <span class="dot"></span>
            <span class="cn">${chapter.num.replace("D", "")}</span>
            <span class="ct">${escapeHtml(shortTitle(chapter))}</span>
          </a>`
        )
        .join("");
    }

    const chapterNav = $("#chapterNav");
    if (chapterNav) {
      chapterNav.innerHTML = chapters
        .map(
          (chapter) => `<a class="chapter-nav-item ${isDone(chapter.num) ? "done" : ""}" href="#/chapter/${chapter.num}">
            <span class="dot"></span>
            <span class="cn">${chapter.num}</span>
            <span class="ct">${escapeHtml(shortTitle(chapter))}</span>
          </a>`
        )
        .join("");
    }

    const accuracy = progress.quizTotal
      ? Math.round((progress.quizCorrect / progress.quizTotal) * 100)
      : 0;

    const quizTotalAll = (progress.quizTotal || 0) + (progress.dsaQuizTotal || 0);
    const quizCorrectAll = (progress.quizCorrect || 0) + (progress.dsaQuizCorrect || 0);
    const accuracyAll = quizTotalAll ? Math.round((quizCorrectAll / quizTotalAll) * 100) : 0;

    const footerStats = $("#footerStats");
    if (footerStats) {
      footerStats.textContent = `${done}/${chapters.length} chapters • ${
        quizTotalAll ? accuracyAll + "% quiz accuracy" : "no quiz yet"
      }`;
    }
  }

  function applyTheme(theme) {
    document.documentElement.dataset.theme = theme;
    progress.theme = theme;
    const button = $("#themeBtn");
    if (button) button.innerHTML = theme === "dark" ? SUN_SVG : MOON_SVG;
  }

  /* ========================================================================
     Kid mode - super simple explanations
     ======================================================================== */

  function isKid() {
    return Boolean(progress.kid);
  }

  function applyKidMode() {
    const on = isKid();
    document.body.classList.toggle("kid-mode", on);
    const button = $("#kidBtn");
    if (button) button.classList.toggle("active", on);
    const label = $("#kidLabel");
    if (label) label.textContent = on ? "Full notes" : "Kid mode";
  }

  function kidCard(chapter) {
    const kid = chapter.kid;
    if (!kid) return "";

    return `<section class="kid-card">
      <div class="kid-head">
        <span class="kid-badge">🧒 Kid version</span>
        <h2>${escapeHtml(kid.title)}</h2>
      </div>
      <p class="kid-story">${escapeHtml(kid.story)}</p>
      <ul class="kid-points">
        ${kid.points.map((point) => `<li>${escapeHtml(point)}</li>`).join("")}
      </ul>
      <h3 class="kid-try">Try it yourself 👇</h3>
      ${renderCodeBlock(kid.code, "python")}
      <p class="kid-win">🎉 <strong>Now you can:</strong> ${escapeHtml(kid.win)}</p>
    </section>`;
  }

  /* ========================================================================
     Router
     ======================================================================== */

  function getRoute() {
    const parts = location.hash.replace(/^#\/?/, "").split("/").filter(Boolean);
    return {
      view: parts[0] || "dashboard",
      param: parts[1] || null,
      tab: parts[2] || null,
    };
  }

  function navigate(hash) {
    if (location.hash === hash) render();
    else location.hash = hash;
  }

  function setActiveNav(view) {
    const key = view === "chapter" ? "chapters" : view;
    $$(".nav-item").forEach((item) => {
      item.classList.toggle("active", item.dataset.nav === key);
    });
  }

  function updateCrumbs(route) {
    const crumbs = $("#crumbs");
    if (!crumbs) return;

    if (route.view === "chapter" && byNum.has(route.param)) {
      const chapter = byNum.get(route.param);
      crumbs.innerHTML = `<a href="#/chapters">Chapters</a><span class="sep">/</span><span class="current">${escapeHtml(
        shortTitle(chapter)
      )}</span>`;
      return;
    }

    if (route.view === "dsa" && dsaByNum.has(route.param)) {
      const chapter = dsaByNum.get(route.param);
      crumbs.innerHTML = `<a href="#/dsa">DSA</a><span class="sep">/</span><span class="current">${escapeHtml(
        shortTitle(chapter)
      )}</span>`;
      return;
    }

    const labels = {
      dashboard: "Dashboard",
      chapters: "Python Chapters",
      projects: "Python Projects",
      dsa: "DSA Home",
      "dsa-quiz": "DSA Quiz",
      "dsa-cheatsheet": "DSA Cheatsheet",
      quiz: "Python Quiz",
      cheatsheet: "Python Cheatsheet",
      playground: "Python Playground",
    };

    crumbs.innerHTML = `<span class="current">${labels[route.view] || "PyPath"}</span>`;
  }

  function render() {
    const route = getRoute();
    const view = $("#view");
    if (!view) return;

    document.body.classList.remove("nav-open");
    view.innerHTML = "";

    switch (route.view) {
      case "dashboard":
        view.innerHTML = dashboardHTML();
        break;
      case "chapters":
        view.innerHTML = chaptersHTML();
        break;
      case "chapter":
        view.innerHTML = chapterHTML(route.param, route.tab);
        break;
      case "projects":
        view.innerHTML = projectsHTML();
        break;
      case "dsa":
        view.innerHTML = dsaByNum.has(route.param)
          ? dsaChapterHTML(route.param, route.tab)
          : dsaHTML();
        break;
      case "dsa-quiz":
        view.innerHTML = quizHTML("dsa");
        break;
      case "dsa-cheatsheet":
        view.innerHTML = `<div class="page-head"><h1>DSA Cheatsheet</h1><p>All the DSA templates in one place. Copy any template and change the names.</p></div><div class="prose">${markdownToHtml(
          DATA.dsa.cheatsheet || ""
        )}</div>`;
        break;
      case "quiz":
        view.innerHTML = quizHTML("python");
        break;
      case "cheatsheet":
        view.innerHTML = `<div class="page-head"><h1>Python Cheatsheet</h1><p>One-page revision. Copy the code blocks and run them in your editor.</p></div><div class="prose">${markdownToHtml(
          DATA.cheatsheet
        )}</div>`;
        break;
      case "playground":
        view.innerHTML = playgroundHTML();
        wirePlayground();
        break;
      case "game":
        view.innerHTML = gameHTML();
        wireGame();
        break;
      default:
        view.innerHTML = notFoundHTML();
    }

    setActiveNav(route.view);
    updateCrumbs(route);

    if (route.view === "chapter" && byNum.has(route.param)) {
      document.title = `${shortTitle(byNum.get(route.param))} — PyPath`;
    } else if (route.view === "dsa" && dsaByNum.has(route.param)) {
      document.title = `${shortTitle(dsaByNum.get(route.param))} — DSA — PyPath`;
    } else {
      document.title = "PyPath — Python from Zero to DSA";
    }

    window.scrollTo({ top: 0, behavior: "auto" });
  }

  /* ========================================================================
     Views: dashboard
     ======================================================================== */

  function greeting() {
    const hour = new Date().getHours();
    if (hour < 5) return "Late night";
    if (hour < 12) return "Good morning";
    if (hour < 17) return "Good afternoon";
    return "Good evening";
  }

  function chapterCard(chapter) {
    const done = isDone(chapter.num);
    const title = isKid() && chapter.kid ? chapter.kid.title : shortTitle(chapter);
    return `<a class="chapter-card ${done ? "done" : ""}" href="#/chapter/${chapter.num}">
      <div class="cc-top">
        <span class="cc-num">${chapter.num}</span>
        ${done ? '<span class="badge done">Done</span>' : `<span class="badge">${chapter.exercises.length} exercises</span>`}
      </div>
      <h3>${escapeHtml(title)}</h3>
      <p>${chapter.demos.length} demos • ${chapter.exercises.length} exercises</p>
      <div class="cc-foot"><span>~${chapter.minutes} min</span><span class="arrow">→</span></div>
    </a>`;
  }

  function dashboardHTML() {
    const done = progress.completed.length;
    const percent = Math.round((done / chapters.length) * 100);
    const next = chapters.find((chapter) => !isDone(chapter.num)) || chapters[chapters.length - 1];
    const quizTotalAll = (progress.quizTotal || 0) + (progress.dsaQuizTotal || 0);
    const quizCorrectAll = (progress.quizCorrect || 0) + (progress.dsaQuizCorrect || 0);
    const accuracyAll = quizTotalAll ? Math.round((quizCorrectAll / quizTotalAll) * 100) : 0;

    const radius = 52;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference * (1 - percent / 100);
    const kid = isKid();

    const heroTitle = kid
      ? `${greeting()}, coder! 👋<br><span class="grad">Let's play with Python.</span>`
      : `${greeting()}, coder.<br><span class="grad">Python from zero to DSA.</span>`;

    const heroText = kid
      ? `Every chapter is a small story with 5 easy points and a tiny program you can run right here. Start with Chapter ${next.num} and have fun!`
      : `${chapters.length} chapters, ${DATA.meta.demoCount} runnable demos, ${DATA.meta.exerciseCount} exercises and 3 projects. 45 minutes a day — solid Python in 20 days.`;

    const planCards = kid
      ? [
          ["1", "Read the story", "Each chapter starts with a fun story. Read it, it is only 5 minutes."],
          ["2", "Run the small program", "Press Run and watch the output. Change one number and run it again."],
          ["3", "Try the exercises", "Each one shows what the answer should look like. Then compare with the solution."],
        ]
      : [
          ["1", "Read the notes", "The chapter notes are in simple English. The concept becomes clear in 10 minutes."],
          ["2", "Solve the exercises", "Every exercise shows the expected output. Write it yourself, then compare with the solution."],
          ["3", "Quiz + revision", "Take 10 random questions to check if the concept really stuck."],
        ];

    return `
      <section class="hero">
        <div class="hero-copy">
          <span class="eyebrow">${kid ? "🧒 Simple mode • step by step" : "Python + DSA • daily practice"}</span>
          <h1>${heroTitle}</h1>
          <p>${heroText}</p>
          <div class="hero-actions">
            <a class="btn primary" href="#/chapter/${next.num}">
              ${done ? "Continue" : "Start"}: Chapter ${next.num}
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
            </a>
            <a class="btn ghost" href="#/chapters">All chapters</a>
          </div>
        </div>
        <div class="hero-ring" aria-label="${percent}% complete">
          <svg viewBox="0 0 120 120">
            <defs>
              <linearGradient id="ringGrad" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#22d3ee"/>
                <stop offset="100%" stop-color="#a3e635"/>
              </linearGradient>
            </defs>
            <circle class="ring-track" cx="60" cy="60" r="${radius}"/>
            <circle class="ring-value" cx="60" cy="60" r="${radius}"
              stroke-dasharray="${circumference.toFixed(1)}"
              stroke-dashoffset="${offset.toFixed(1)}"/>
          </svg>
          <div class="ring-label"><strong>${percent}%</strong><span>${done}/${chapters.length} chapters</span></div>
        </div>
      </section>

      <section class="stats">
        <div class="stat-card">
          <span class="label">Chapters</span>
          <strong>${done}<small> / ${chapters.length}</small></strong>
          <span class="sub">${percent}% complete</span>
        </div>
        <div class="stat-card">
          <span class="label">Exercises</span>
          <strong>${DATA.meta.exerciseCount}</strong>
          <span class="sub">auto-tested practice</span>
        </div>
        <div class="stat-card">
          <span class="label">Streak</span>
          <strong>${progress.streak || 0}<small> days</small></strong>
          <span class="sub">${progress.streak > 1 ? "stay consistent" : "start today"}</span>
        </div>
        <div class="stat-card">
          <span class="label">Quiz accuracy</span>
          <strong>${quizTotalAll ? accuracyAll + "%" : "—"}</strong>
          <span class="sub">${quizTotalAll ? quizCorrectAll + "/" + quizTotalAll + " correct" : "no quiz taken yet"}</span>
        </div>
      </section>

      <div class="section-head">
        <div><h2>Today's plan</h2><p>${kid ? "One chapter, three easy steps." : "One chapter, three simple steps."}</p></div>
      </div>
      <div class="plan-grid">
        ${planCards
          .map(
            ([step, title, text]) => `<div class="plan-card">
              <span class="step">${step}</span>
              <h3>${escapeHtml(title)}</h3>
              <p>${escapeHtml(text)}</p>
            </div>`
          )
          .join("")}
      </div>

      <div class="section-head">
        <div><h2>Chapters</h2><p>From zero to OOP, files and advanced topics.</p></div>
        <a href="#/chapters">View all →</a>
      </div>
      <div class="chapter-grid">${chapters.map(chapterCard).join("")}</div>

      <div class="dsa-banner">
        <div class="icon">⌘</div>
        <div>
          <h3>After Python: the full DSA core</h3>
          <p>${dsaChapters.length} chapters • ${DATA.meta.dsaExerciseCount || 0} auto-tested exercises • patterns to dynamic programming.</p>
        </div>
        <a class="btn ghost" href="#/dsa">Open DSA</a>
      </div>`;
  }

  /* ========================================================================
     Views: chapters list
     ======================================================================== */

  function chaptersHTML() {
    const done = progress.completed.length;
    const percent = Math.round((done / chapters.length) * 100);

    return `
      <div class="page-head">
        <h1>Chapters</h1>
        <p>Every chapter has notes, runnable demos, exercises with expected output and solutions. One chapter a day — that's it.</p>
      </div>

      <div class="course-progress">
        <span class="big">${percent}%</span>
        <div class="bar"><span style="width:${percent}%"></span></div>
        <span class="pct">${done} / ${chapters.length} complete</span>
      </div>

      <div class="filter-row">
        <button class="filter-btn active" data-action="filter" data-filter="all" type="button">All (${chapters.length})</button>
        <button class="filter-btn" data-action="filter" data-filter="pending" type="button">Pending (${chapters.length - done})</button>
        <button class="filter-btn" data-action="filter" data-filter="done" type="button">Done (${done})</button>
      </div>

      <div class="chapter-grid" id="chapterGrid">
        ${chapters
          .map(
            (chapter) => `<div data-done="${isDone(chapter.num)}">${chapterCard(chapter)}</div>`
          )
          .join("")}
      </div>`;
  }

  /* ========================================================================
     Views: single chapter
     ======================================================================== */

  function chapterHTML(num, tab) {
    const chapter = byNum.get(num);
    if (!chapter) return notFoundHTML();

    const active = ["notes", "demos", "exercises"].includes(tab) ? tab : "notes";
    const index = chapters.findIndex((item) => item.num === chapter.num);
    const previous = chapters[index - 1];
    const next = chapters[index + 1];
    const done = isDone(chapter.num);

    const kid = isKid();
    const kidBlock = kid ? kidCard(chapter) : "";

    let panel = "";
    if (active === "notes") {
      const notesHtml = `<article class="prose">${markdownToHtml(chapter.notes)}</article>
        <div class="explanation" style="max-width:880px;margin-top:22px">
          <strong>Practice tip:</strong> after reading the notes, open <code>${escapeHtml(chapter.file)}</code>
          and solve the exercises yourself. The portal is only for reading and revising.
        </div>`;

      panel = kid
        ? `${kidBlock}<details class="starter kid-full"><summary>Show the full notes (more detail)</summary>${notesHtml}</details>`
        : notesHtml;
    } else if (active === "demos") {
      panel = chapter.demos.length
        ? kidBlock +
          chapter.demos
            .map(
              (demo, demoIndex) => `<article class="demo-card">
                <div class="demo-head"><h3>${escapeHtml(demo.title)}</h3><span class="pill">demo ${demoIndex + 1}</span></div>
                ${renderCodeBlock(demo.code)}
              </article>`
            )
            .join("")
        : '<p class="prose">This chapter has no demos.</p>';
    } else {
      panel = kidBlock + chapter.exercises
        .map(
          (exercise) => `<article class="exercise-card">
            <div class="ex-head">
              <span class="ex-id">${escapeHtml(exercise.id)}</span>
              <h3>${escapeHtml(exercise.task)}</h3>
            </div>
            <div class="tests">
              <div class="mini-label">Expected output</div>
              <ul>${exercise.tests.map((test) => `<li>${escapeHtml(test)}</li>`).join("")}</ul>
            </div>
            ${
              exercise.starter
                ? `<details class="starter"><summary>View starter code</summary>${renderCodeBlock(exercise.starter)}</details>`
                : ""
            }
            <div class="ex-actions">
              <button class="btn ghost small" type="button" data-action="solution" data-target="sol-${exercise.id}">View solution</button>
              <button class="btn ghost small" type="button" data-action="practice">Try it in the Playground</button>
            </div>
            <div class="solution" id="sol-${exercise.id}" hidden>
              ${renderCodeBlock(exercise.solution)}
            </div>
          </article>`
        )
        .join("");
    }

    return `
      <div class="chapter-head">
        <div class="chapter-kicker">
          <a href="#/chapters">Chapters</a><span class="sep">/</span><span>Chapter ${chapter.num}</span>
        </div>
        <div class="chapter-title-row">
          <div>
            <h1>${escapeHtml(kid && chapter.kid ? chapter.kid.title : shortTitle(chapter))}</h1>
            ${kid && chapter.kid ? `<p class="kid-sub">${escapeHtml(shortTitle(chapter))}</p>` : ""}
            <div class="meta-row">
              <span>${chapter.demos.length} demos</span>
              <span>${chapter.exercises.length} exercises</span>
              <span>~${chapter.minutes} min</span>
              <span class="file-pill">${escapeHtml(chapter.file)}</span>
            </div>
          </div>
          <button class="btn ${done ? "success" : "primary"}" type="button" data-action="complete" data-num="${chapter.num}">
            ${done ? "✓ Complete" : "Mark complete"}
          </button>
        </div>
      </div>

      <div class="tabs">
        <a class="tab ${active === "notes" ? "active" : ""}" href="#/chapter/${chapter.num}/notes">Notes</a>
        <a class="tab ${active === "demos" ? "active" : ""}" href="#/chapter/${chapter.num}/demos">Demos <span class="count">${chapter.demos.length}</span></a>
        <a class="tab ${active === "exercises" ? "active" : ""}" href="#/chapter/${chapter.num}/exercises">Exercises <span class="count">${chapter.exercises.length}</span></a>
      </div>

      <div class="tab-panel">${panel}</div>

      <div class="chapter-pager">
        ${
          previous
            ? `<a class="pager-card" href="#/chapter/${previous.num}"><small>← Previous</small><strong>${escapeHtml(shortTitle(previous))}</strong></a>`
            : '<span class="pager-card disabled"><small>← Previous</small><strong>Start</strong></span>'
        }
        ${
          next
            ? `<a class="pager-card next" href="#/chapter/${next.num}"><small>Next →</small><strong>${escapeHtml(shortTitle(next))}</strong></a>`
            : '<a class="pager-card next" href="#/dsa"><small>Next →</small><strong>DSA Roadmap</strong></a>'
        }
      </div>`;
  }

  /* ========================================================================
     Views: projects + DSA
     ======================================================================== */

  function projectsHTML() {
    return `
      <div class="page-head">
        <h1>Projects</h1>
        <p>Three CLI projects — this is where real learning happens. Read the code, run it, then add your own features.</p>
      </div>
      <div class="project-grid">
        ${DATA.projects
          .map(
            (project) => `<article class="project-card">
              <h2>${escapeHtml(project.title)}</h2>
              <div class="project-meta">
                <span>${escapeHtml(project.file)}</span>
                <span>CLI</span>
                <span>Python 3.12</span>
              </div>
              <div class="prose">${markdownToHtml(project.notes)}</div>
              <details class="starter"><summary>View the full code (${project.code.split("\n").length} lines)</summary>
                ${renderCodeBlock(project.code, "python", false)}
              </details>
              <div class="project-actions">
                <button class="btn ghost small" type="button" data-action="practice">Open in Playground</button>
              </div>
            </article>`
          )
          .join("")}
      </div>

      <div class="explanation" style="margin-top:22px">
        <strong>How to run it:</strong> in the terminal, <code>python projects/02_todo_cli.py</code>.
        The portal Playground doesn't support <code>input()</code>, so run CLI projects in the terminal.
      </div>`;
  }

  function dsaChapterCard(chapter) {
    const done = isDsaDone(chapter.num);
    const title = isKid() && chapter.kid ? chapter.kid.title : shortTitle(chapter);
    return `<a class="chapter-card ${done ? "done" : ""}" href="#/dsa/${chapter.num}">
      <div class="cc-top">
        <span class="cc-num">${chapter.num}</span>
        ${done ? '<span class="badge done">Done</span>' : `<span class="badge">${chapter.exercises.length} exercises</span>`}
      </div>
      <h3>${escapeHtml(title)}</h3>
      <p>${chapter.demos.length} demos • ${chapter.exercises.length} exercises</p>
      <div class="cc-foot"><span>~${chapter.minutes} min</span><span class="arrow">→</span></div>
    </a>`;
  }

  function dsaHTML() {
    const done = progress.dsaCompleted ? progress.dsaCompleted.length : 0;
    const percent = dsaChapters.length ? Math.round((done / dsaChapters.length) * 100) : 0;

    return `
      <div class="page-head">
        <h1>DSA Course</h1>
        <p>The complete DSA core: ${dsaChapters.length} chapters with kid notes, full notes, runnable demos and auto-tested exercises. Start with DSA 01 and go in order.</p>
      </div>

      <div class="dsa-hero">
        <div class="big-icon">⌘</div>
        <div>
          <h2>${dsaChapters.length} chapters • ${DATA.meta.dsaExerciseCount || 0} exercises</h2>
          <p>Patterns → arrays → strings → two pointers → sliding window → sorting → hashing → stacks → queues → linked lists → recursion → trees → heaps → graphs → DP → binary search.</p>
        </div>
        <a class="btn ghost" style="margin-left:auto" href="${dsaChapters.length ? `#/dsa/${dsaChapters[0].num}` : "#/chapter/01"}">${
          dsaChapters.length ? "Start DSA" : "Start Python first"
        }</a>
      </div>

      <div class="course-progress">
        <span class="big">${percent}%</span>
        <div class="bar"><span style="width:${percent}%"></span></div>
        <span class="pct">${done} / ${dsaChapters.length} DSA chapters complete</span>
      </div>

      <div class="section-head">
        <div><h2>The DSA core</h2><p>Each chapter works exactly like the Python ones: read, run the demos, solve the exercises.</p></div>
      </div>
      <div class="chapter-grid">${dsaChapters.map(dsaChapterCard).join("")}</div>

      <div class="section-head">
        <div><h2>12-week plan</h2><p>How to spread these chapters over 12 weeks.</p></div>
      </div>
      <div class="prose">${markdownToHtml(DATA.dsa.roadmap)}</div>

      <div class="section-head">
        <div><h2>Starter code</h2><p>5 classic patterns — press Run and see the output.</p></div>
      </div>
      <article class="demo-card">
        <div class="demo-head"><h3>${escapeHtml(DATA.dsa.starter.title)}</h3><span class="pill">${escapeHtml(DATA.dsa.starter.file)}</span></div>
        <div class="prose">${markdownToHtml(DATA.dsa.starter.notes)}</div>
        ${renderCodeBlock(DATA.dsa.starter.code)}
      </article>

      ${
        DATA.dsa.cheatsheet
          ? `<div class="section-head">
               <div><h2>DSA cheat sheet</h2><p>All the templates you will use again and again.</p></div>
             </div>
             <details class="starter"><summary>Open the DSA cheat sheet (templates + complexity table)</summary>
               <div class="prose">${markdownToHtml(DATA.dsa.cheatsheet)}</div>
             </details>`
          : ""
      }`;
  }

  function dsaChapterHTML(num, tab) {
    const chapter = dsaByNum.get(num);
    if (!chapter) return dsaHTML();

    const active = ["notes", "demos", "exercises"].includes(tab) ? tab : "notes";
    const index = dsaChapters.findIndex((item) => item.num === chapter.num);
    const previous = dsaChapters[index - 1];
    const next = dsaChapters[index + 1];
    const done = isDsaDone(chapter.num);
    const kid = isKid();
    const kidBlock = kid ? kidCard(chapter) : "";

    let panel = "";
    if (active === "notes") {
      const notesHtml = `<article class="prose">${markdownToHtml(chapter.notes)}</article>
        <div class="explanation" style="max-width:880px;margin-top:22px">
          <strong>Practice tip:</strong> open <code>${escapeHtml(chapter.file)}</code> in your editor,
          solve every exercise, then run it again. The portal is for reading and revising.
        </div>`;

      panel = kid
        ? `${kidBlock}<details class="starter kid-full"><summary>Show the full notes (more detail)</summary>${notesHtml}</details>`
        : notesHtml;
    } else if (active === "demos") {
      panel = chapter.demos.length
        ? kidBlock +
          chapter.demos
            .map(
              (demo, demoIndex) => `<article class="demo-card">
                <div class="demo-head"><h3>${escapeHtml(demo.title)}</h3><span class="pill">demo ${demoIndex + 1}</span></div>
                ${renderCodeBlock(demo.code)}
              </article>`
            )
            .join("")
        : '<p class="prose">This chapter has no demos.</p>';
    } else {
      panel = kidBlock + chapter.exercises
        .map(
          (exercise) => `<article class="exercise-card">
            <div class="ex-head">
              <span class="ex-id">${escapeHtml(exercise.id)}</span>
              <h3>${escapeHtml(exercise.task)}</h3>
            </div>
            <div class="tests">
              <div class="mini-label">Expected output</div>
              <ul>${exercise.tests.map((test) => `<li>${escapeHtml(test)}</li>`).join("")}</ul>
            </div>
            ${
              exercise.starter
                ? `<details class="starter"><summary>View starter code</summary>${renderCodeBlock(exercise.starter)}</details>`
                : ""
            }
            <div class="ex-actions">
              <button class="btn ghost small" type="button" data-action="solution" data-target="dsol-${exercise.id}">View solution</button>
              <button class="btn ghost small" type="button" data-action="practice">Try it in the Playground</button>
            </div>
            <div class="solution" id="dsol-${exercise.id}" hidden>
              ${renderCodeBlock(exercise.solution)}
            </div>
          </article>`
        )
        .join("");
    }

    return `
      <div class="chapter-head">
        <div class="chapter-kicker">
          <a href="#/dsa">DSA</a><span class="sep">/</span><span>Chapter ${chapter.num}</span>
        </div>
        <div class="chapter-title-row">
          <div>
            <h1>${escapeHtml(kid && chapter.kid ? chapter.kid.title : shortTitle(chapter))}</h1>
            ${kid && chapter.kid ? `<p class="kid-sub">${escapeHtml(shortTitle(chapter))}</p>` : ""}
            <div class="meta-row">
              <span>${chapter.demos.length} demos</span>
              <span>${chapter.exercises.length} exercises</span>
              <span>~${chapter.minutes} min</span>
              <span class="file-pill">${escapeHtml(chapter.file)}</span>
            </div>
          </div>
          <button class="btn ${done ? "success" : "primary"}" type="button" data-action="dsa-complete" data-num="${chapter.num}">
            ${done ? "✓ Complete" : "Mark complete"}
          </button>
        </div>
      </div>

      <div class="tabs">
        <a class="tab ${active === "notes" ? "active" : ""}" href="#/dsa/${chapter.num}/notes">Notes</a>
        <a class="tab ${active === "demos" ? "active" : ""}" href="#/dsa/${chapter.num}/demos">Demos <span class="count">${chapter.demos.length}</span></a>
        <a class="tab ${active === "exercises" ? "active" : ""}" href="#/dsa/${chapter.num}/exercises">Exercises <span class="count">${chapter.exercises.length}</span></a>
      </div>

      <div class="tab-panel">${panel}</div>

      <div class="chapter-pager">
        ${
          previous
            ? `<a class="pager-card" href="#/dsa/${previous.num}"><small>← Previous</small><strong>${escapeHtml(shortTitle(previous))}</strong></a>`
            : '<a class="pager-card" href="#/dsa"><small>← Previous</small><strong>All DSA chapters</strong></a>'
        }
        ${
          next
            ? `<a class="pager-card next" href="#/dsa/${next.num}"><small>Next →</small><strong>${escapeHtml(shortTitle(next))}</strong></a>`
            : '<a class="pager-card next" href="#/dsa"><small>Next →</small><strong>All DSA chapters</strong></a>'
        }
      </div>`;
  }

  /* ========================================================================
     Views: quiz
     ======================================================================== */

  let quizState = null;
  let quizMode = "python";

  function quizBank(mode) {
    return mode === "dsa" ? DATA.dsaQuiz || [] : DATA.quiz || [];
  }

  function quizStats(mode) {
    if (mode === "dsa") {
      return { total: progress.dsaQuizTotal || 0, correct: progress.dsaQuizCorrect || 0 };
    }
    return { total: progress.quizTotal || 0, correct: progress.quizCorrect || 0 };
  }

  function shuffle(items) {
    const copy = [...items];
    for (let index = copy.length - 1; index > 0; index -= 1) {
      const swapIndex = Math.floor(Math.random() * (index + 1));
      [copy[index], copy[swapIndex]] = [copy[swapIndex], copy[index]];
    }
    return copy;
  }

  function startQuiz() {
    const bank = quizBank(quizMode);
    quizState = {
      mode: quizMode,
      questions: shuffle(bank).slice(0, Math.min(10, bank.length)),
      index: 0,
      score: 0,
      answered: false,
      selected: null,
      finished: false,
      recorded: false,
      answers: [],
    };
    render();
  }

  function answerQuiz(optionIndex) {
    if (!quizState || quizState.answered) return;
    const question = quizState.questions[quizState.index];
    quizState.answered = true;
    quizState.selected = optionIndex;
    const correct = optionIndex === question.answer;
    quizState.answers[quizState.index] = correct;
    if (correct) quizState.score += 1;
    render();
  }

  function nextQuiz() {
    if (!quizState) return;

    if (quizState.index + 1 >= quizState.questions.length) {
      quizState.finished = true;
      if (!quizState.recorded) {
        if (quizState.mode === "dsa") {
          progress.dsaQuizTotal = (progress.dsaQuizTotal || 0) + quizState.questions.length;
          progress.dsaQuizCorrect = (progress.dsaQuizCorrect || 0) + quizState.score;
        } else {
          progress.quizTotal += quizState.questions.length;
          progress.quizCorrect += quizState.score;
        }
        quizState.recorded = true;
        saveProgress();
      }
    } else {
      quizState.index += 1;
      quizState.answered = false;
      quizState.selected = null;
    }
    render();
  }

  function quizModeTabs(current) {
    return `<div class="tabs quiz-mode-tabs">
      <a class="tab ${current === "python" ? "active" : ""}" href="#/quiz">Python Quiz <span class="count">${(DATA.quiz || []).length}</span></a>
      <a class="tab ${current === "dsa" ? "active" : ""}" href="#/dsa-quiz">DSA Quiz <span class="count">${(DATA.dsaQuiz || []).length}</span></a>
    </div>`;
  }

  function quizHTML(mode) {
    quizMode = mode === "dsa" ? "dsa" : "python";
    if (quizState && quizState.mode !== quizMode) quizState = null;

    const bank = quizBank(quizMode);
    const stats = quizStats(quizMode);
    const accuracy = stats.total ? Math.round((stats.correct / stats.total) * 100) : 0;
    const isDsa = quizMode === "dsa";

    if (!quizState) {
      return `<div class="quiz-wrap">
        ${quizModeTabs(quizMode)}
        <div class="page-head" style="text-align:center">
          <h1>${isDsa ? "DSA Quiz" : "Python Quiz"}</h1>
          <p style="margin:0 auto">${
            isDsa
              ? "10 random questions — arrays, strings, stacks, trees, graphs, DP and more."
              : "10 random questions — output prediction, types, functions, OOP, files, stdlib."
          }</p>
        </div>
        <div class="quiz-card" style="text-align:center">
          <div class="quiz-result">
            <div class="score-big">${bank.length}</div>
            <h2>questions ready</h2>
            <p>${
              stats.total
                ? `So far: ${stats.correct}/${stats.total} correct (${accuracy}%).`
                : "First time here? You'll also get an explanation for each answer."
            }</p>
            <button class="btn primary" type="button" data-action="quiz-start">Start the quiz</button>
          </div>
        </div>
      </div>`;
    }

    if (quizState.finished) {
      const total = quizState.questions.length;
      const percent = Math.round((quizState.score / total) * 100);
      const message =
        percent === 100
          ? "Perfect! Today's revision is solid."
          : percent >= 70
          ? "Good job. Re-read the topics you got wrong."
          : "Do a little revision, then try the quiz again.";

      const review = quizState.questions
        .map((question, index) => {
          const correct = question.options[question.answer];
          const isCorrect = Boolean(quizState.answers[index]);
          return `<div class="review-item">
            <span class="mark ${isCorrect ? "ok" : "no"}">${isCorrect ? "✓" : "✗"}</span>
            <span><strong>${escapeHtml(question.q)}</strong><br>Answer: ${escapeHtml(correct)}</span>
          </div>`;
        })
        .join("");

      return `<div class="quiz-wrap">
        ${quizModeTabs(quizMode)}
        <div class="quiz-card">
        <div class="quiz-result">
          <div class="score-big">${quizState.score}/${total}</div>
          <h2>${percent}% • ${message}</h2>
          <p>Your score was saved in the browser. Streak: ${progress.streak} day(s).</p>
          <div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap">
            <button class="btn primary" type="button" data-action="quiz-restart">Play again</button>
            <a class="btn ghost" href="#/chapters">Go to Chapters</a>
          </div>
        </div>
        <div class="review">${review}</div>
      </div></div>`;
    }

    const question = quizState.questions[quizState.index];
    const total = quizState.questions.length;

    const options = question.options
      .map((option, index) => {
        let className = "option";
        if (quizState.answered) {
          if (index === question.answer) className += " correct";
          else if (index === quizState.selected) className += " wrong";
        }
        return `<button class="${className}" type="button" data-action="quiz-option" data-index="${index}" ${quizState.answered ? "disabled" : ""}>
          <span class="key">${String.fromCharCode(65 + index)}</span>
          <span>${escapeHtml(option)}</span>
        </button>`;
      })
      .join("");

      return `<div class="quiz-wrap">
        ${quizModeTabs(quizMode)}
        <div class="quiz-top">
          <span class="pill">Question ${quizState.index + 1} / ${total}</span>
          <span class="pill">Score ${quizState.score}</span>
          <span class="pill">${quizState.mode === "dsa" ? "DSA" : "Python"}</span>
        </div>
      <div class="quiz-progress"><span style="width:${((quizState.index + 1) / total) * 100}%"></span></div>
      <div class="quiz-card">
        <h2 class="quiz-q">${escapeHtml(question.q)}</h2>
        <div class="options">${options}</div>
        ${
          quizState.answered
            ? `<div class="explanation"><strong>Why:</strong> ${escapeHtml(question.explain)}</div>
               <div class="quiz-actions">
                 <button class="btn primary" type="button" data-action="quiz-next">
                   ${quizState.index + 1 === total ? "See result" : "Next question"}
                 </button>
               </div>`
            : ""
        }
      </div>
    </div>`;
  }

  /* ========================================================================
     Views: practice game
     ======================================================================== */

  const ROUND_SIZE = 10;

  let gameState = null;

  function newGame() {
    const bank = DATA.game || [];
    const puzzles = shuffle(bank).slice(0, Math.min(ROUND_SIZE, bank.length));

    gameState = {
      puzzles,
      index: 0,
      score: 0,
      streak: 0,
      bestStreak: 0,
      attempts: 0,
      solved: 0,
      revealed: false,
      finished: false,
      checked: false,
      lastResult: null,
      code: "",
      hintShown: false,
    };

    render();
  }

  function currentPuzzle() {
    if (!gameState || gameState.finished) return null;
    return gameState.puzzles[gameState.index] || null;
  }

  function gameCheck(code) {
    const puzzle = currentPuzzle();
    if (!puzzle || gameState.checked) return;

    gameState.attempts += 1;
    gameState.checked = true;
    gameState.lastResult = { got: "", expected: puzzle.expected, error: null, correct: false };

    const full = code + (puzzle.test ? "\n\n" + puzzle.test : "");
    const outputEl = $("#gameOutput");

    if (outputEl) {
      outputEl.hidden = false;
      outputEl.classList.remove("error");
      outputEl.textContent = "Checking...";
    }

    executePython(full)
      .then((result) => {
        const got = (result.output || "").trim();
        const expected = puzzle.expected.trim();
        const correct = !result.error && got === expected;

        gameState.lastResult = { got, expected, error: result.error, correct };

        if (correct) {
          const points = gameState.attempts === 1 ? 10 : 5;
          gameState.score += points;
          gameState.solved += 1;
          gameState.streak += 1;
          gameState.bestStreak = Math.max(gameState.bestStreak, gameState.streak);
          toast(correct ? `Correct! +${points} points 🎉` : "Wrong");
        } else {
          gameState.streak = 0;
          toast("Not yet - try again 💪");
        }

        render();
      })
      .catch((error) => {
        gameState.lastResult = {
          got: "",
          expected: puzzle.expected,
          error: error && error.message ? error.message : String(error),
          correct: false,
        };
        render();
      });
  }

  function gameNext() {
    if (!gameState) return;
    gameState.index += 1;
    gameState.attempts = 0;
    gameState.checked = false;
    gameState.revealed = false;
    gameState.lastResult = null;
    gameState.code = "";
    gameState.hintShown = false;

    if (gameState.index >= gameState.puzzles.length) {
      gameState.finished = true;
      if ((progress.gameBest || 0) < gameState.score) {
        progress.gameBest = gameState.score;
      }
      progress.gameRounds = (progress.gameRounds || 0) + 1;
      progress.gameSolved = (progress.gameSolved || 0) + gameState.solved;
      saveProgress();
    }

    render();
  }

  function gameHTML() {
    const bank = DATA.game || [];

    if (!bank.length) {
      return `<div class="page-head"><h1>Practice Game</h1><p>No puzzles found. Run <code>python portal/build_portal.py</code>.</p></div>`;
    }

    if (!gameState) {
      return `<div class="game-wrap">
        <div class="page-head" style="text-align:center">
          <h1>🎮 Practice Game</h1>
          <p style="margin:0 auto">${bank.length} small puzzles. Write Python code, press Check, and get points for every correct answer.</p>
        </div>
        <div class="game-stats">
          <div class="game-stat"><span class="gs-label">Puzzles</span><strong>${bank.length}</strong></div>
          <div class="game-stat"><span class="gs-label">Per round</span><strong>${Math.min(ROUND_SIZE, bank.length)}</strong></div>
          <div class="game-stat"><span class="gs-label">Your best</span><strong>${progress.gameBest || 0}</strong></div>
          <div class="game-stat"><span class="gs-label">Solved ever</span><strong>${progress.gameSolved || 0}</strong></div>
        </div>
        <div class="game-card center">
          <h2>Ready?</h2>
          <p>10 puzzles. 10 points for a first-try answer, 5 points if you needed a second try. Look at the hint if you are stuck - no shame in that.</p>
          <button class="btn primary" type="button" data-action="game-start">Start the game</button>
        </div>
      </div>`;
    }

    if (gameState.finished) {
      const score = gameState.score;
      const rating =
        score >= 90 ? "Champion! 🏆" : score >= 60 ? "Very good! 👏" : score >= 30 ? "Good try 💪" : "Keep practising 🌱";
      const isBest = score >= (progress.gameBest || 0);

      return `<div class="game-wrap">
        <div class="page-head" style="text-align:center">
          <h1>Round finished 🎉</h1>
        </div>
        <div class="game-card center">
          <div class="game-final-score">${score}</div>
          <h2>${rating}</h2>
          <p>You solved ${gameState.solved} of ${gameState.puzzles.length} puzzles. Best streak: ${gameState.bestStreak}.</p>
          ${isBest && score > 0 ? '<p class="game-best">🏅 New best score!</p>' : ""}
          <div class="game-actions center">
            <button class="btn primary" type="button" data-action="game-start">Play again</button>
            <a class="btn ghost" href="#/chapters">Back to chapters</a>
          </div>
        </div>
      </div>`;
    }

    const puzzle = currentPuzzle();
    const result = gameState.lastResult;
    const total = gameState.puzzles.length;

    let feedback = "";
    if (result && result.correct) {
      feedback = `<div class="game-feedback ok">🎉 Correct! That is the answer.</div>`;
    } else if (result && result.error) {
      feedback = `<div class="game-feedback bad">Your code gave an error:<br><code>${escapeHtml(result.error)}</code></div>`;
    } else if (result) {
      feedback = `<div class="game-feedback bad">
        Not the answer yet. Your output was:<br><code>${escapeHtml(result.got || "(nothing)")}</code>
        <br><small>(the answer is checked exactly, so watch the spaces and the words)</small>
      </div>`;
    }

    return `<div class="game-wrap">
      <div class="game-hud">
        <span class="pill">Puzzle ${gameState.index + 1} / ${total}</span>
        <span class="pill">Score ${gameState.score}</span>
        <span class="pill">Streak ${gameState.streak}</span>
        <span class="pill">Level ${puzzle.level} • ${escapeHtml(puzzle.tag)}</span>
      </div>
      <div class="game-progress"><span style="width:${((gameState.index + 1) / total) * 100}%"></span></div>

      <div class="game-card">
        <h2 class="game-title">${escapeHtml(puzzle.title)}</h2>
        <p class="game-story">${escapeHtml(puzzle.story).replace(/\n/g, "<br>")}</p>

        <div class="game-editor">
          <textarea id="gameCode" spellcheck="false" aria-label="Your Python code">${escapeHtml(gameState.code || puzzle.starter)}</textarea>
        </div>

        ${feedback}

        <div class="game-actions">
          <button class="btn primary" type="button" data-action="game-check" ${gameState.checked ? "disabled" : ""}>Check my answer</button>
          <button class="btn ghost small" type="button" data-action="game-hint">Hint</button>
          <button class="btn ghost small" type="button" data-action="game-solution">Show solution</button>
          ${gameState.checked && result && result.correct ? '<button class="btn success" type="button" data-action="game-next">Next puzzle →</button>' : ""}
          ${gameState.revealed ? '<button class="btn success" type="button" data-action="game-next">Next puzzle →</button>' : ""}
        </div>

        <div id="gameHint" class="game-hint" ${gameState.hintShown ? "" : "hidden"}>💡 ${escapeHtml(puzzle.hint)}</div>

        <div id="gameSolution" class="game-solution" ${gameState.revealed ? "" : "hidden"}>
          <div class="mini-label">Solution (no points for this one)</div>
          <div class="code-block">
            <div class="code-head"><span class="code-lang">python</span></div>
            <pre><code>${highlightPython(puzzle.solution)}</code></pre>
          </div>
        </div>

        <pre id="gameOutput" class="game-output" hidden></pre>
      </div>
    </div>`;
  }

  /* ========================================================================
     Views: playground
     ======================================================================== */

  let playgroundCode = `# Python Playground - try anything
name = "Ravi"
for i in range(1, 6):
    print(f"{name} -> {i} x {i} = {i * i}")

print("\\nList comprehension:", [n * n for n in range(1, 6)])
`;

  function playgroundHTML() {
    return `
      <div class="page-head">
        <h1>Python Playground</h1>
        <p>Run Python in your browser — it uses Pyodide (WebAssembly). The first run takes ~10-20 seconds and needs internet.</p>
      </div>
      <div class="playground">
        <div class="pg-panel pg-editor">
          <div class="pg-head"><span class="file">main.py</span><span>Python 3.12 (Pyodide)</span></div>
          <textarea id="pgCode" spellcheck="false" aria-label="Python code">${escapeHtml(playgroundCode)}</textarea>
          <div class="pg-actions">
            <button class="btn primary small" type="button" id="pgRun">▶ Run</button>
            <button class="btn ghost small" type="button" id="pgClear">Clear</button>
            <span class="pg-status" id="pgStatus">You can also run with Ctrl + Enter</span>
          </div>
        </div>
        <div class="pg-panel pg-output">
          <div class="pg-head"><span>Output</span><span>stdout / stderr</span></div>
          <pre id="pgOutput">Press Run and the output will appear here...</pre>
        </div>
      </div>
      <p class="pg-note">Note: <code>input()</code> doesn't work in the browser. Use the terminal for file/JSON examples.</p>`;
  }

  function wireGame() {
    const textarea = $("#gameCode");
    if (!textarea || !gameState) return;

    textarea.addEventListener("input", () => {
      gameState.code = textarea.value;
    });

    textarea.addEventListener("keydown", (event) => {
      if (event.key === "Tab") {
        event.preventDefault();
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        textarea.value = textarea.value.slice(0, start) + "    " + textarea.value.slice(end);
        textarea.selectionStart = textarea.selectionEnd = start + 4;
        gameState.code = textarea.value;
      }
      if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
        event.preventDefault();
        gameCheck(textarea.value);
      }
    });
  }

  function wirePlayground() {
    const textarea = $("#pgCode");
    const runButton = $("#pgRun");
    const clearButton = $("#pgClear");
    const output = $("#pgOutput");
    const status = $("#pgStatus");

    if (!textarea || !runButton || !output) return;

    textarea.addEventListener("input", () => {
      playgroundCode = textarea.value;
    });

    textarea.addEventListener("keydown", (event) => {
      if (event.key === "Tab") {
        event.preventDefault();
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        textarea.value = textarea.value.slice(0, start) + "    " + textarea.value.slice(end);
        textarea.selectionStart = textarea.selectionEnd = start + 4;
        playgroundCode = textarea.value;
      }
      if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
        event.preventDefault();
        runPython(textarea.value, output);
      }
    });

    runButton.addEventListener("click", () => {
      status.textContent = "Running...";
      runPython(textarea.value, output).finally(() => {
        status.textContent = "Done";
      });
    });

    clearButton.addEventListener("click", () => {
      textarea.value = "";
      playgroundCode = "";
      output.textContent = "Press Run and the output will appear here...";
      output.classList.remove("error");
      textarea.focus();
    });
  }

  /* ========================================================================
     Views: 404
     ======================================================================== */

  function notFoundHTML() {
    return `<div class="page-head" style="padding:60px 0;text-align:center">
      <h1>404 — page not found</h1>
      <p style="margin:0 auto 20px">The link may be old. Go back to the Dashboard.</p>
      <a class="btn primary" href="#/dashboard">Dashboard</a>
    </div>`;
  }

  /* ========================================================================
     Search
     ======================================================================== */

  const searchItems = [];

  function buildSearchIndex() {
    chapters.forEach((chapter) => {
      searchItems.push({
        type: "chapter",
        title: `Chapter ${chapter.num} — ${shortTitle(chapter)}`,
        sub: `${chapter.demos.length} demos • ${chapter.exercises.length} exercises`,
        href: `#/chapter/${chapter.num}`,
        text: `${chapter.num} ${shortTitle(chapter)} ${chapter.notes}`.toLowerCase(),
      });

      chapter.demos.forEach((demo) => {
        searchItems.push({
          type: "demo",
          title: demo.title,
          sub: `Chapter ${chapter.num} demo`,
          href: `#/chapter/${chapter.num}/demos`,
          text: `${demo.title} ${demo.code}`.toLowerCase(),
        });
      });

      chapter.exercises.forEach((exercise) => {
        searchItems.push({
          type: "exercise",
          title: `${exercise.id} — ${exercise.task}`,
          sub: `Chapter ${chapter.num} exercise`,
          href: `#/chapter/${chapter.num}/exercises`,
          text: `${exercise.id} ${exercise.task} ${exercise.tests.join(" ")}`.toLowerCase(),
        });
      });
    });

    DATA.projects.forEach((project) => {
      searchItems.push({
        type: "project",
        title: project.title,
        sub: project.file,
        href: "#/projects",
        text: `${project.title} ${project.notes}`.toLowerCase(),
      });
    });

    dsaChapters.forEach((chapter) => {
      searchItems.push({
        type: "chapter",
        title: `DSA ${chapter.num} — ${shortTitle(chapter)}`,
        sub: `${chapter.demos.length} demos • ${chapter.exercises.length} exercises`,
        href: `#/dsa/${chapter.num}`,
        text: `dsa ${chapter.num} ${shortTitle(chapter)} ${chapter.notes}`.toLowerCase(),
      });

      chapter.exercises.forEach((exercise) => {
        searchItems.push({
          type: "exercise",
          title: `DSA ${exercise.id} — ${exercise.task}`,
          sub: `DSA chapter ${chapter.num} exercise`,
          href: `#/dsa/${chapter.num}/exercises`,
          text: `dsa ${exercise.id} ${exercise.task} ${exercise.tests.join(" ")}`.toLowerCase(),
        });
      });
    });

    searchItems.push({
      type: "chapter",
      title: "DSA Roadmap",
      sub: "12-week plan",
      href: "#/dsa",
      text: `dsa roadmap arrays dp graph ${DATA.dsa.roadmap}`.toLowerCase(),
    });
    searchItems.push({
      type: "chapter",
      title: "Cheatsheet",
      sub: "Quick revision",
      href: "#/cheatsheet",
      text: `cheatsheet syntax ${DATA.cheatsheet}`.toLowerCase(),
    });
  }

  function searchResultsHTML(query) {
    const needle = query.trim().toLowerCase();

    let items;
    if (!needle) {
      items = searchItems.filter((item) => item.type === "chapter").slice(0, 8);
    } else {
      items = searchItems
        .filter((item) => item.title.toLowerCase().includes(needle) || item.text.includes(needle))
        .slice(0, 24);
    }

    if (!items.length) {
      return `<div class="search-empty">Nothing found. Try: "strings", "dict", "OOP", "decorator".</div>`;
    }

    return items
      .map(
        (item) => `<a class="search-result" href="${item.href}" data-search-link>
          <span class="type-badge ${item.type}">${item.type}</span>
          <span class="sr-main">
            <span class="sr-title">${escapeHtml(item.title)}</span>
            <span class="sr-sub">${escapeHtml(item.sub)}</span>
          </span>
        </a>`
      )
      .join("");
  }

  function openSearch() {
    const modal = $("#searchModal");
    const input = $("#searchInput");
    if (!modal || !input) return;

    modal.classList.add("open");
    modal.setAttribute("aria-hidden", "false");
    $("#searchResults").innerHTML = searchResultsHTML("");
    input.value = "";
    setTimeout(() => input.focus(), 40);
  }

  function closeSearch() {
    const modal = $("#searchModal");
    if (!modal) return;
    modal.classList.remove("open");
    modal.setAttribute("aria-hidden", "true");
  }

  /* ========================================================================
     Global events
     ======================================================================== */

  function toggleComplete(num) {
    const index = progress.completed.indexOf(num);
    if (index >= 0) {
      progress.completed.splice(index, 1);
      toast(`Chapter ${num} marked as pending`);
    } else {
      progress.completed.push(num);
      toast(`Chapter ${num} complete! Well done 🎉`);
    }
    saveProgress();
    render();
  }

  function toggleDsaComplete(num) {
    if (!progress.dsaCompleted) progress.dsaCompleted = [];
    const index = progress.dsaCompleted.indexOf(num);
    if (index >= 0) {
      progress.dsaCompleted.splice(index, 1);
      toast(`DSA chapter ${num} marked as pending`);
    } else {
      progress.dsaCompleted.push(num);
      toast(`DSA chapter ${num} complete! Nice work 🏆`);
    }
    saveProgress();
    render();
  }

  function bindEvents() {
    $("#menuBtn")?.addEventListener("click", () => document.body.classList.toggle("nav-open"));
    $("#scrim")?.addEventListener("click", () => document.body.classList.remove("nav-open"));

    $("#searchTrigger")?.addEventListener("click", openSearch);
    $("#searchPill")?.addEventListener("click", openSearch);
    $("#searchClose")?.addEventListener("click", closeSearch);

    $("#searchModal")?.addEventListener("click", (event) => {
      if (event.target.id === "searchModal") closeSearch();
    });

    $("#searchInput")?.addEventListener("input", (event) => {
      $("#searchResults").innerHTML = searchResultsHTML(event.target.value);
    });

    $("#searchResults")?.addEventListener("click", (event) => {
      if (event.target.closest("[data-search-link]")) closeSearch();
    });

    $("#kidBtn")?.addEventListener("click", () => {
      progress.kid = !isKid();
      applyKidMode();
      saveProgress();
      render();
      toast(progress.kid ? "Kid mode ON — super simple notes 🧒" : "Full notes ON");
    });

    $("#themeBtn")?.addEventListener("click", () => {
      const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
      applyTheme(next);
      saveProgress();
    });

    document.addEventListener("keydown", (event) => {
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        openSearch();
      }
      if (event.key === "Escape") {
        closeSearch();
        document.body.classList.remove("nav-open");
      }
    });

    document.addEventListener("click", (event) => {
      if (!(event.target instanceof Element)) return;
      const trigger = event.target.closest("[data-action]");
      if (!trigger) return;

      const action = trigger.dataset.action;

      if (action === "copy") {
        const block = trigger.closest(".code-block");
        const code = block?.querySelector("code");
        if (code) copyText(code.textContent, trigger);
      }

      if (action === "run") {
        const block = trigger.closest(".code-block");
        const code = block?.querySelector("code");
        const output = block?.querySelector(".console");
        if (code && output) runPython(code.textContent, output);
      }

      if (action === "complete") {
        toggleComplete(trigger.dataset.num);
      }

      if (action === "dsa-complete") {
        toggleDsaComplete(trigger.dataset.num);
      }

      if (action === "solution") {
        const box = document.getElementById(trigger.dataset.target);
        if (box) {
          box.hidden = !box.hidden;
          trigger.textContent = box.hidden ? "View solution" : "Hide solution";
        }
      }

      if (action === "practice") {
        const card = trigger.closest(".exercise-card, .project-card, .demo-card");
        let code = "";
        if (card) {
          code =
            card.querySelector("details.starter code")?.textContent ||
            card.querySelector("details code")?.textContent ||
            card.querySelector(".solution code")?.textContent ||
            "";
        }
        if (!code) {
          toast("Code not found");
          return;
        }
        playgroundCode = code;
        navigate("#/playground");
      }

      if (action === "filter") {
        const filter = trigger.dataset.filter;
        $$(".filter-btn").forEach((button) => button.classList.toggle("active", button === trigger));
        $$("#chapterGrid > div").forEach((wrapper) => {
          const done = wrapper.dataset.done === "true";
          wrapper.hidden = filter === "done" ? !done : filter === "pending" ? done : false;
        });
      }

      if (action === "quiz-start") startQuiz();
      if (action === "quiz-option") answerQuiz(Number(trigger.dataset.index));
      if (action === "quiz-next") nextQuiz();
      if (action === "quiz-restart") {
        quizState = null;
        render();
      }

      if (action === "game-start") newGame();
      if (action === "game-check") {
        const textarea = $("#gameCode");
        gameCheck(textarea ? textarea.value : "");
      }
      if (action === "game-hint") {
        if (!gameState) return;
        gameState.hintShown = true;
        render();
      }
      if (action === "game-solution") {
        if (!gameState) return;
        gameState.revealed = true;
        gameState.streak = 0;
        render();
      }
      if (action === "game-next") gameNext();
    });
  }

  /* ========================================================================
     Init
     ======================================================================== */

  function init() {
    applyTheme(progress.theme === "light" ? "light" : "dark");
    applyKidMode();
    updateStreak();
    buildSearchIndex();
    bindEvents();
    window.addEventListener("hashchange", render);
    updateChrome();
    render();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
