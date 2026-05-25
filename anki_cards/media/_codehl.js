/* Автономная подсветка кода + нумерация строк для карточек Anki.
   Работает офлайн (без интернета) в Anki desktop и AnkiDroid.
   Универсальный токенайзер: ключевые слова, строки, комментарии,
   числа, вызовы функций. Номера строк рисуются через CSS-счётчик
   (см. .code-line в styling.css). Файл назван с «_», чтобы Anki
   не удалял его как «неиспользуемый» при проверке медиа. */
(function () {
  var KW = ("abstract and arguments as assert async await bool boolean break byte case catch char class const continue debugger def default del delete do double elif else enum except export extends false False final finally float fn for from func function global goto if impl implements import in include instanceof int interface is lambda let long match mut namespace native new nil None nonlocal not null or override package pass print private protected pub public raise return self short signed sizeof static struct super switch synchronized template this throw throws transient true True try typedef typename typeof union unsigned use var virtual void volatile where while with yield")
    .split(/\s+/);
  var KWSET = {};
  KW.forEach(function (k) { KWSET[k] = 1; });

  function esc(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function hlLine(line) {
    var out = "", i = 0, n = line.length;
    while (i < n) {
      var c = line.charAt(i);
      // комментарии //... и #...
      if (c === "/" && line.charAt(i + 1) === "/") {
        out += '<span class="tok-com">' + esc(line.slice(i)) + "</span>"; break;
      }
      if (c === "#") {
        out += '<span class="tok-com">' + esc(line.slice(i)) + "</span>"; break;
      }
      // строки в кавычках ' " `
      if (c === '"' || c === "'" || c === "`") {
        var q = c, j = i + 1, s = c;
        while (j < n) {
          var ch = line.charAt(j);
          s += ch;
          if (ch === "\\") { s += line.charAt(j + 1) || ""; j += 2; continue; }
          j++;
          if (ch === q) break;
        }
        out += '<span class="tok-str">' + esc(s) + "</span>"; i = j; continue;
      }
      // числа
      if (c >= "0" && c <= "9") {
        var m = line.slice(i).match(/^(0x[0-9a-fA-F]+|\d+\.?\d*([eE][+-]?\d+)?)/);
        if (m) { out += '<span class="tok-num">' + esc(m[0]) + "</span>"; i += m[0].length; continue; }
      }
      // идентификаторы / ключевые слова / вызовы функций
      if (/[A-Za-z_$]/.test(c)) {
        var w = line.slice(i).match(/^[A-Za-z_$][A-Za-z0-9_$]*/)[0];
        var after = line.charAt(i + w.length);
        if (KWSET[w]) out += '<span class="tok-kw">' + esc(w) + "</span>";
        else if (after === "(") out += '<span class="tok-fn">' + esc(w) + "</span>";
        else out += esc(w);
        i += w.length; continue;
      }
      out += esc(c); i++;
    }
    return out;
  }

  function process(pre) {
    if (pre.getAttribute("data-hl")) return;
    var code = pre.querySelector("code") || pre;
    var raw = (code.innerText != null ? code.innerText : code.textContent) || "";
    raw = raw.replace(/\r\n?/g, "\n").replace(/\n+$/, "");
    var lines = raw.split("\n");
    var html = "";
    for (var i = 0; i < lines.length; i++) {
      html += '<span class="code-line">' + (lines[i].length ? hlLine(lines[i]) : "&#8203;") + "</span>";
    }
    code.innerHTML = html;
    pre.setAttribute("data-hl", "1");
  }

  function run() {
    var pres = document.querySelectorAll("pre.code-block");
    for (var i = 0; i < pres.length; i++) process(pres[i]);
  }

  window.__codehl = run;
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
