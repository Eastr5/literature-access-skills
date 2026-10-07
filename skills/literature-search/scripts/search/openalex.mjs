#!/usr/bin/env node
// OpenAlex 检索：无需 key，本机实测可用。限流很凶，务必带 sleep。
// 用法：node scripts/search/openalex.mjs "查询语句" -n 10 [--from 2018] [--to 2026] [--json]
// 说明：查询串宜用 3-5 个精确词，过长会命中大量无关结果。

const args = process.argv.slice(2);
if (!args.length || args[0] === "-h" || args[0] === "--help") {
  console.log("用法: node scripts/search/openalex.mjs \"query\" -n 10 [--from YYYY] [--to YYYY] [--json]");
  process.exit(0);
}

const query = args[0];
const num = (() => { const i = args.indexOf("-n"); return i >= 0 ? Number(args[i + 1]) : 10; })();
const from = (() => { const i = args.indexOf("--from"); return i >= 0 ? Number(args[i + 1]) : null; })();
const to = (() => { const i = args.indexOf("--to"); return i >= 0 ? Number(args[i + 1]) : null; })();
const asJson = args.includes("--json");

function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }

async function get(url, attempts = 4) {
  for (let i = 0; i < attempts; i += 1) {
    try {
      const res = await fetch(url, { headers: { "User-Agent": "lit-search/1.0 (mailto:research@example.org)" } });
      if (res.status === 429) {
        const wait = 12000 * (i + 1);
        process.stderr.write(`429 限流，等待 ${wait / 1000}s 后重试 (${i + 1}/${attempts})\n`);
        await sleep(wait);
        continue;
      }
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (err) {
      if (i === attempts - 1) throw err;
      await sleep(8000 * (i + 1));
    }
  }
  throw new Error("unreachable");
}

(async () => {
  const filters = [];
  if (from) filters.push(`from_publication_date:${from}-01-01`);
  if (to) filters.push(`to_publication_date:${to}-12-31`);
  const url = new URL("https://api.openalex.org/works");
  url.searchParams.set("search", query);
  url.searchParams.set("per_page", String(Math.min(num, 50)));
  if (filters.length) url.searchParams.set("filter", filters.join(","));
  url.searchParams.set("mailto", "research@example.org");

  const data = await get(url.toString());
  const rows = (data.results || []).map((w) => {
    const loc = w.primary_location?.source || {};
    return {
      year: w.publication_year,
      venue: loc.display_name || "NA",
      citations: w.cited_by_count,
      title: (w.title || "").replace(/\s+/g, " ").trim(),
      doi: w.doi || "",
      oa: w.open_access?.is_oa ? "OA" : "",
    };
  });

  if (asJson) {
    console.log(JSON.stringify({ total: data.meta?.count, results: rows }, null, 1));
    return;
  }
  console.log(`命中总数 ${data.meta?.count}，显示前 ${rows.length} 条：`);
  for (const r of rows) {
    console.log(`${r.year} | ${r.venue.slice(0, 40).padEnd(40)} | 被引 ${String(r.citations).padStart(5)} | ${r.oa.padEnd(2)} | ${r.title.slice(0, 100)}`);
  }
})().catch((e) => { console.error("检索失败:", e.message); process.exit(1); });
