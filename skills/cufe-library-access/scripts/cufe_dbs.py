#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""中央财经大学图书馆电子资源索引：抓取、精简、查询、访问通道判定。

数据来源：图书馆「数据库导航」页的列表接口
    https://lib.cufe.edu.cn/db/api/newDbsList?intranet=<0|1>
该接口为公开读取，返回全部订购/试用数据库条目（含名称、别名、学科、语言、资源类型、入口地址）。

用法：
    python cufe_dbs.py update                 # 重新抓取并刷新本地索引
    python cufe_dbs.py find <关键词>            # 按名称/别名/学科模糊查库
    python cufe_dbs.py list --lang 外文 --discipline 经济学
    python cufe_dbs.py url <关键词>             # 输出入口地址与通道判定
    python cufe_dbs.py detail <关键词>          # 输出图书馆详情页地址
    python cufe_dbs.py where                  # 判断当前是否在校内网
    python cufe_dbs.py stats                  # 索引概览

数据覆盖范围（实测）：
- 列表接口给出 190 条数据库条目，其中 138 条带直接入口地址；
- resTypeName（资源类型）与 dbIntro（简介）在列表接口恒为空，只在详情页由前端异步加载，
  因此本索引不含这两项；学科与语言字段可用。

设计说明：
- 索引落盘为 data/cufe_dbs.json，约 190 条，仅供本地查询，不替代图书馆页面。
- 通道判定基于入口 URL 的域名特征，只用于选择打开方式，不代表授权状态；
  真正的授权由图书馆的登录态决定，脚本不接触任何账号凭据。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://lib.cufe.edu.cn/db"
LIST_API = BASE + "/api/newDbsList?intranet={intranet}"
IP_API = BASE + "/cx/ipBlank"
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
DATA = Path(__file__).resolve().parent.parent / "data" / "cufe_dbs.json"

# 只保留查询与判定需要的字段，原始条目有 70 多个字段
# 注意：列表接口的 resTypeName 与 dbIntro 实测恒为空（190/190），资源类型与简介
# 只在详情页由前端异步加载，本索引不收录这两项。
KEEP = (
    "id",
    "dbName",
    "dbAliases",
    "firstLetter",
    "languagesNames",
    "disciplineNames",
    "newSign",
)

DETAIL_URL = BASE + "/detail?id={id}"


def _get(url: str, timeout: int = 30) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": BASE + "/"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _clean(text, limit: int = 300) -> str:
    """历史遗留：列表接口的 dbIntro 实测恒为空，本函数目前没有调用点，保留以便
    将来该字段有值时启用。"""
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", str(text))
    text = re.sub(r"&[a-z]+;", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]


def channel(url: str) -> tuple[str, str]:
    """按入口 URL 判定访问通道与是否需登录。返回 (通道, 登录要求)。"""
    u = (url or "").lower()
    if not u:
        return ("无直接地址", "需在图书馆详情页查看")
    if "webvpn.cufe.edu.cn" in u:
        return ("WebVPN 代理", "需统一身份认证")
    if "idp.cufe.edu.cn" in u or "shibboleth" in u:
        return ("Shibboleth 联邦登录", "需统一身份认证")
    if "carsi.edu.cn" in u:
        return ("CARSI 联邦登录", "需统一身份认证")
    if "fsso.cnki" in u:
        return ("CNKI 联邦登录 fsso", "需登录")
    if "sciencedirect" in u or "webofknowledge" in u or "onlinelibrary.wiley" in u:
        return ("出版商直连", "校内 IP 可能已授权，否则走 SSO")
    return ("直连", "视资源而定")


def fetch(intranet: int = 0) -> list[dict]:
    raw = json.loads(_get(LIST_API.format(intranet=intranet)).decode("utf-8"))
    if raw.get("code") != 1000:
        raise RuntimeError(f"接口返回异常：{raw.get('code')} {raw.get('message')}")
    return raw["data"]


def slim(rows: list[dict]) -> list[dict]:
    out = []
    for r in rows:
        urls = [d.get("dbUrl") for d in (r.get("dbps") or []) if d.get("dbUrl")]
        entry = {k: r.get(k) for k in KEEP}
        entry["dbUrl"] = urls[0] if urls else ""
        entry["altUrls"] = urls[1:]
        entry["detailUrl"] = DETAIL_URL.format(id=r.get("id"))
        entry["accessRoute"], entry["loginRequired"] = channel(entry["dbUrl"])
        out.append(entry)
    return out


def update() -> dict:
    rows = fetch()
    data = {
        "source": LIST_API.format(intranet=0),
        "note": "中央财经大学图书馆数据库导航全量条目；重新抓取请运行 cufe_dbs.py update",
        "count": len(rows),
        "items": slim(rows),
    }
    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    return data


def load() -> dict:
    if not DATA.exists():
        return update()
    return json.loads(DATA.read_text(encoding="utf-8"))


def find(kw: str, limit: int = 25) -> list[dict]:
    data = load()
    k = kw.lower()
    hits = []
    for it in data["items"]:
        hay = " ".join(
            str(it.get(f) or "")
            for f in ("dbName", "dbAliases", "disciplineNames", "firstLetter")
        ).lower()
        if k in hay:
            # 名称命中排在别名/学科命中之前
            score = 0 if k in str(it.get("dbName") or "").lower() else 1
            hits.append((score, it))
    hits.sort(key=lambda x: (x[0], -int(x[1].get("id") or 0)))
    return [h[1] for h in hits[:limit]]


def where() -> dict:
    raw = json.loads(_get(IP_API).decode("utf-8"))
    # 注意：status 在 data 内，clientIP 在顶层，接口两处字段层级不一致
    d = raw.get("data") or {}
    return {"intranet": bool(d.get("status")), "clientIP": raw.get("clientIP")}


def _rows(items: list[dict]) -> list[list[str]]:
    return [
        [
            str(it.get("dbName") or ""),
            str(it.get("languagesNames") or ""),
            str(it.get("resTypeName") or ""),
            str(it.get("accessRoute") or ""),
            str(it.get("loginRequired") or ""),
        ]
        for it in items
    ]


def _print(items: list[dict], show_url: bool = False) -> None:
    if not items:
        print("未命中。可试试更短的关键词、数据库缩写（如 SCI / CNKI），或 list 看全量。")
        return
    for it in items:
        meta = " / ".join(
            x for x in (it.get("languagesNames"), it.get("disciplineNames")) if x
        )
        print(f"- {it['dbName']}" + (f"  [{meta}]" if meta else ""))
        if it.get("dbAliases") and it["dbAliases"] != it["dbName"]:
            print(f"    别名：{it['dbAliases']}")
        print(f"    通道：{it['accessRoute']}（{it['loginRequired']}）")
        if show_url and it.get("dbUrl"):
            print(f"    入口：{it['dbUrl']}")
        print(f"    详情页：{it.get('detailUrl')}")


def main() -> int:
    ap = argparse.ArgumentParser(description="中央财经大学图书馆电子资源索引")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("update", help="重新抓取索引")
    p_find = sub.add_parser("find", help="关键词查库")
    p_find.add_argument("keyword")
    p_find.add_argument("--url", action="store_true", help="同时打印入口地址")
    p_find.add_argument("--limit", type=int, default=25)

    p_list = sub.add_parser("list", help="列出全部（可筛）")
    p_list.add_argument("--lang", default="", help="中文 / 外文")
    p_list.add_argument("--discipline", default="", help="经济学 / 管理学 / 理学 / 综合 …")
    p_list.add_argument("--limit", type=int, default=0)

    p_url = sub.add_parser("url", help="输出入口地址与通道")
    p_url.add_argument("keyword")

    p_detail = sub.add_parser("detail", help="输出图书馆详情页地址")
    p_detail.add_argument("keyword")

    sub.add_parser("where", help="判断当前是否在校内网")
    sub.add_parser("stats", help="索引概览")

    a = ap.parse_args()

    if a.cmd == "update":
        d = update()
        print(f"索引已刷新：{d['count']} 条 → {DATA}")
        return 0

    if a.cmd == "where":
        w = where()
        print(f"客户端 IP：{w['clientIP']}")
        print("校内网：是（图书馆判定为内网，多数资源可直接访问）" if w["intranet"] else "校内网：否（需走 WebVPN 或 CARSI 登录）")
        return 0

    if a.cmd == "find":
        _print(find(a.keyword, a.limit), show_url=a.url)
        return 0

    if a.cmd == "list":
        items = load()["items"]
        if a.lang:
            items = [i for i in items if a.lang in str(i.get("languagesNames") or "")]
        if a.discipline:
            items = [i for i in items if a.discipline in str(i.get("disciplineNames") or "")]
        if a.limit:
            items = items[: a.limit]
        _print(items)
        print(f"\n共 {len(items)} 条")
        return 0

    if a.cmd == "detail":
        hits = find(a.keyword, limit=10)
        if not hits:
            print("未命中。")
            return 0
        for it in hits:
            print(f"{it['dbName']}\t{it.get('detailUrl')}")
        return 0

    if a.cmd == "url":
        hits = find(a.keyword, limit=10)
        _print(hits, show_url=True)
        return 0

    if a.cmd == "stats":
        d = load()
        items = d["items"]
        from collections import Counter

        print(f"条目总数：{d['count']}")
        print("语言：", dict(Counter(i.get("languagesNames") for i in items)))
        print("通道：", dict(Counter(i.get("accessRoute") for i in items)))
        print("有直接入口：", sum(1 for i in items if i.get("dbUrl")))
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
