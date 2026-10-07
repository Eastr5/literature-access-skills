#!/usr/bin/env node
// arXiv 检索：无需 key，稳定可用。适合找最新预印本。
// 用法：node scripts/search/arxiv.mjs "查询语句" -n 15 [--sort submittedDate] [--cat q-fin.RM]
// 常用分类：q-fin.RM 风险管理 / q-fin.CP 定价 / cs.LG 机器学习 / q-fin.GN 一般金融

const args = process.argv.slice(2);
if (!args.length || args[0] === "-h") {
  console.log("用法: node scripts/search/arxiv.mjs \"query\" -n 15 [--sort submittedDate] [--cat q-fin.RM]");
  process.exit(0);
}

const query = args[0];
const pick = (flag, dflt) => { const i = args.indexOf(flag); return i >= 0 ? args[i + 1] : dflt; };
const num = Number(pick("-n", "15"));
// 默认按相关度排序：arXiv 的 submittedDate 排序会把当天所有无关预印本排在前面。
const sort = pick("--sort", "relevance");
const cat = pick("--cat", "");

function parseXml(xml) {
  const out = [];
  const entries = xml.split("<entry>").slice(1);
  for (const e of entries) {
    const grab = (tag) => {
      const m = e.match(new RegExp(`<${tag}[^>]*>([\\s\\S]*?)</${tag}>`));
      return m ? m[1].replace(/\s+/g, " ").trim() : "";
    };
    out.push({
      id: grab("id"),
      title: grab("title"),
      published: grab("published").slice(0, 10),
      summary: grab("summary").slice(0, 200),
      authors: (e.match(/<name>([\s\S]*?)<\/name>/g) || []).length,
    });
  }
  return out;
}

(async () => {
  // 整句加引号在 arXiv 上过于严格（常返回 0 条）；改成取前 5 个实词用 AND 连接。
  const stop = new Set(["the", "a", "an", "of", "for", "in", "on", "and", "with", "via", "using", "to"]);
  const terms = query.replace(/"/g, "").split(/\s+/)
    .filter((w) => w && !stop.has(w.toLowerCase())).slice(0, 5);
  const phrase = terms.map((t) => `all:${encodeURIComponent(t)}`).join("+AND+");
  const q = cat ? `${phrase}+AND+cat:${cat}` : phrase;
  process.stderr.write(`检索式: ${decodeURIComponent(phrase)}\n`);
  const url = `http://export.arxiv.org/api/query?search_query=${q}&start=0&max_results=${num}&sortBy=${sort}&sortOrder=descending`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const xml = await res.text();
  const rows = parseXml(xml);
  console.log(`arXiv 返回 ${rows.length} 条：`);
  for (const r of rows) {
    console.log(`${r.published} | ${r.title.slice(0, 100)}`);
    console.log(`    ${r.id}`);
  }
})().catch((e) => { console.error("检索失败:", e.message); process.exit(1); });
