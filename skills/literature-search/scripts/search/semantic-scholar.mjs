#!/usr/bin/env node
// Semantic Scholar 检索：无需 key，但极易 429。失败时脚本会提示改用 openalex.mjs。
// 用法：node scripts/search/semantic-scholar.mjs "查询语句" -n 15 [--year 2020-2026]

const args = process.argv.slice(2);
if (!args.length || args[0] === "-h") {
  console.log("用法: node scripts/search/semantic-scholar.mjs \"query\" -n 15 [--year 2020-2026]");
  process.exit(0);
}

const query = args[0];
const pick = (flag, dflt) => { const i = args.indexOf(flag); return i >= 0 ? args[i + 1] : dflt; };
const num = Number(pick("-n", "15"));
const year = pick("--year", "");

function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }

(async () => {
  const url = new URL("https://api.semanticscholar.org/graph/v1/paper/search");
  url.searchParams.set("query", query);
  url.searchParams.set("limit", String(Math.min(num, 100)));
  url.searchParams.set("fields", "title,year,venue,citationCount,externalIds,abstract");
  if (year) url.searchParams.set("year", year);

  let data = null;
  for (let i = 0; i < 3; i += 1) {
    const res = await fetch(url.toString());
    if (res.status === 429) {
      process.stderr.write(`429 限流，等待 ${15 * (i + 1)}s 后重试\n`);
      await sleep(15000 * (i + 1));
      continue;
    }
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    data = await res.json();
    break;
  }
  if (!data) {
    console.error("Semantic Scholar 持续限流。请改用：node scripts/search/openalex.mjs \"" + query + "\" -n " + num);
    process.exit(2);
  }
  for (const p of data.data || []) {
    console.log(`${p.year} | ${(p.venue || "NA").slice(0, 38).padEnd(38)} | 被引 ${String(p.citationCount).padStart(5)} | ${(p.title || "").slice(0, 95)}`);
  }
})().catch((e) => { console.error("检索失败:", e.message); process.exit(1); });
