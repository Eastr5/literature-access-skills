#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Zotero 7 本地 API 客户端：查重、建条目、挂 PDF 附件、归入分类、写备注。

前提（两项，缺一不可）：
  1. Zotero 桌面版正在运行（本机为免安装版 D:\\Zotero\\Zotero_win-x64\\zotero.exe）；
  2. 设置 → 高级 → 「允许其他应用与本机 Zotero 通信」已勾选
     （对应配置项 extensions.zotero.httpServer.localAPI.enabled = true，本机已开启）。

本地 API 形如 http://localhost:23119/api/users/0 ，路径与 Zotero Web API v3 一致，
但不经过云端、不需要 API key、不消耗同步流量。写完之后是否同步到 zotero.org
由桌面版自己的同步开关决定。

用法：
    python zotero.py ping
    python zotero.py collections
    python zotero.py has "<DOI>"
    python zotero.py add --doi 10.1000/x --title "标题" --journal "刊名" --date 2026 \
        --author "Yang,Shudan" --author "Liu,Xiaoyu" --collection "阅读文献-崔" \
        --tag 担保网络 --pdf "D:/papers/x.pdf"
    python zotero.py add --meta meta.json --pdf x.pdf     # 从 JSON 读元数据
    python zotero.py ris --meta meta.json --out x.ris     # 不依赖 Zotero 运行的兜底导出

设计约束：
- 只使用本地 API，不读取也不写入 zotero.sqlite（Zotero 运行时直接改库会损坏数据）。
- 所有写入前先按 DOI 查重，命中则默认跳过，避免重复条目。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "http://localhost:23119/api/users/0"
AUTHORIZE = "http://localhost:23119/api/local/authorize"
HEADERS = {"Zotero-API-Version": "3"}
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
KEY_FILE = DATA_DIR / "local_api_key.json"
APP_NAME = "WorkBuddy"

# Zotero 本地 API 的写操作有两道门，都必须过：
#   1. CSRF 防护 —— 请求头回送服务端在响应头给出的 Zotero-Server-ID，
#      否则返回 HTTP 428 "Zotero-Server-ID not provided"；
#   2. 密钥 —— 向 POST /api/local/authorize 申请（body {"appName": "..."}），
#      Zotero 会弹出授权对话框，允许后返回 key；之后以 Authorization: Bearer <key> 提交，
#      否则返回 HTTP 401 "API key required"。
# 两道门都靠首次请求自动完成，密钥缓存于 data/local_api_key.json。
_SERVER_ID: str | None = None
_KEY: str | None = None


class ZoteroError(RuntimeError):
    pass


def load_key() -> str | None:
    """从缓存读取密钥，不发起申请。"""
    global _KEY
    if _KEY:
        return _KEY
    if KEY_FILE.exists():
        try:
            _KEY = json.loads(KEY_FILE.read_text(encoding="utf-8")).get("key")
        except Exception:
            _KEY = None
    return _KEY


def authorize(app_name: str = APP_NAME, force: bool = False) -> str:
    """申请或复用本地 API 密钥。Zotero 会在首次申请时弹出授权对话框。"""
    global _KEY
    if _KEY and not force:
        return _KEY
    if not force and load_key():
        return _KEY
    _discover_server_id()
    # auth=False：申请密钥这一步本身不能要求密钥，否则无限递归
    st, data = _req("POST", AUTHORIZE, body=json.dumps({"appName": app_name}).encode(),
                    ctype="application/json", auth=False)
    key = (data or {}).get("key") if isinstance(data, dict) else None
    if not key:
        raise ZoteroError(
            f"未取得本地 API 密钥：{data}。请在 Zotero 弹出的授权对话框中选择允许；"
            "若没有弹窗，检查 设置 → 高级 → 允许其他应用与本机 Zotero 通信。"
        )
    _KEY = key
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    KEY_FILE.write_text(json.dumps({"key": key, "appName": app_name}, ensure_ascii=False),
                        encoding="utf-8")
    return key


def _req(method: str, path: str, *, body: bytes | None = None, ctype: str | None = None,
         extra: dict | None = None, timeout: int = 30, auth: bool = True,
         _skip_sid: bool = False):
    global _SERVER_ID
    # Server-ID 是所有请求（含 DELETE）的通用要求，必须先取到；
    # 密钥只在写操作时需要，且 authorize() 自身以 auth=False 调用，避免递归。
    # _discover_server_id() 内部的探测请求以 _skip_sid=True 调用，否则会自我递归。
    if _SERVER_ID is None and not _skip_sid:
        _discover_server_id()
    if method != "GET" and auth:
        authorize()
    url = path if path.startswith("http") else (path if path.startswith("/api/") else BASE + path)
    headers = dict(HEADERS)
    if _SERVER_ID:
        headers["Zotero-Server-ID"] = _SERVER_ID
    if auth and _KEY:
        headers["Authorization"] = f"Bearer {_KEY}"
    if ctype:
        headers["Content-Type"] = ctype
    if extra:
        headers.update(extra)
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            sid = r.headers.get("Zotero-Server-ID")
            if sid:
                _SERVER_ID = sid
            raw = r.read()
            try:
                return r.status, json.loads(raw.decode("utf-8"))
            except Exception:
                return r.status, raw
    except urllib.error.HTTPError as e:
        sid = e.headers.get("Zotero-Server-ID") if e.headers else None
        if sid:
            _SERVER_ID = sid
        detail = e.read().decode("utf-8", "replace")[:400]
        raise ZoteroError(f"HTTP {e.code} {method} {path}\n{detail}") from None
    except urllib.error.URLError as e:
        raise ZoteroError(
            f"无法连接 Zotero 本地 API（{e.reason}）。请确认 Zotero 桌面版已启动，"
            "且「设置 → 高级 → 允许其他应用与本机 Zotero 通信」已勾选。"
        ) from None


def _discover_server_id() -> str:
    """以一次只读请求换取 Zotero-Server-ID，写操作前必须完成。"""
    global _SERVER_ID
    if _SERVER_ID:
        return _SERVER_ID
    _req("GET", "/items?limit=1", auth=False, _skip_sid=True)
    if not _SERVER_ID:
        raise ZoteroError(
            "未能从响应头取得 Zotero-Server-ID；本地 API 可能需要重新开启"
            "（设置 → 高级 → 允许其他应用与本机 Zotero 通信）。"
        )
    return _SERVER_ID


# ---------------------------------------------------------------- 读

def ping() -> dict:
    st, data = _req("GET", "/items?limit=1", auth=False)
    if st != 200:
        raise ZoteroError(f"本地 API 返回 {st}")
    sid = _discover_server_id()
    key = load_key()
    return {"ok": True, "base": BASE, "items_probe": st,
            "collections": len(collections()), "server_id": sid,
            "api_key": "已缓存" if key else "未申请（首次写入时自动申请，Zotero 会弹授权框）"}


def delete_item(key: str) -> dict:
    """删除条目。Zotero 要求带 If-Unmodified-Since-Version，先取版本号再删。"""
    st, data = _req("GET", f"/items/{key}")
    if st != 200 or not isinstance(data, dict):
        raise ZoteroError(f"取条目版本失败：HTTP {st} {str(data)[:200]}")
    version = data.get("version")
    if version is None:
        raise ZoteroError("条目响应中没有 version 字段，无法安全删除")
    st2, _ = _req("DELETE", f"/items/{key}", extra={"If-Unmodified-Since-Version": str(version)})
    return {"status": st2, "key": key, "deleted": st2 in (200, 204)}


def collections() -> list[dict]:
    st, data = _req("GET", "/collections?limit=100")
    return data if isinstance(data, list) else []


def ensure_collection(name: str) -> str | None:
    """按名称取分类 key，不存在则创建。空名返回 None（表示不归类）。"""
    if not name:
        return None
    for c in collections():
        if (c.get("data") or {}).get("name") == name:
            return c["key"]
    st, data = _req("POST", "/collections", body=json.dumps([{"name": name}]).encode(),
                    ctype="application/json")
    ok = (data or {}).get("successful") or {}
    if ok:
        return list(ok.values())[0].get("key")
    raise ZoteroError(f"创建分类失败：{data}")


def find_by_doi(doi: str) -> list[dict]:
    if not doi:
        return []
    norm = doi.strip().lower()
    q = urllib.parse.quote(norm)
    st, data = _req("GET", f"/items?q={q}&qmode=everything&limit=25")
    hits = []
    for it in data or []:
        d = it.get("data") or {}
        if (d.get("DOI") or "").strip().lower() == norm:
            hits.append(it)
    return hits


# ---------------------------------------------------------------- 写

def _creators(authors: list[str]) -> list[dict]:
    """把 "Yang,Shudan" / "Shudan Yang" 统一成 Zotero 的 creator 结构。"""
    out = []
    for a in authors or []:
        a = (a or "").strip()
        if not a:
            continue
        if "," in a:
            last, first = [x.strip() for x in a.split(",", 1)]
        else:
            parts = a.split()
            last, first = (parts[-1], " ".join(parts[:-1])) if len(parts) > 1 else (a, "")
        c = {"creatorType": "author", "lastName": last}
        if first:
            c["firstName"] = first
        out.append(c)
    return out


def build_item(meta: dict, collection_key: str | None = None) -> dict:
    it = {
        "itemType": meta.get("itemType") or "journalArticle",
        "title": meta.get("title") or "",
    }
    if meta.get("authors"):
        it["creators"] = _creators(meta["authors"])
    if meta.get("journal"):
        it["publicationTitle"] = meta["journal"]
    if meta.get("date"):
        it["date"] = str(meta["date"])
    for src, dst in (("volume", "volume"), ("issue", "issue"), ("pages", "pages"),
                     ("doi", "DOI"), ("url", "url"), ("abstract", "abstractNote"),
                     ("publisher", "publisher"), ("language", "language")):
        if meta.get(src):
            it[dst] = meta[src]
    if meta.get("tags"):
        it["tags"] = [{"tag": t} for t in meta["tags"]]
    if collection_key:
        it["collections"] = [collection_key]
    return it


def create_item(item: dict) -> dict:
    st, data = _req("POST", "/items", body=json.dumps([item]).encode(), ctype="application/json")
    ok = (data or {}).get("successful") or {}
    bad = (data or {}).get("failed") or {}
    if not ok:
        raise ZoteroError(f"创建条目失败：{json.dumps(bad, ensure_ascii=False)}")
    return list(ok.values())[0]


def upload_pdf(parent_key: str, pdf_path: Path, title: str = "Full Text PDF") -> str:
    """建附件条目并把 PDF 传进 Zotero 存储。返回附件条目 key。

    上传是三段式（与 Zotero Web API 的文件上传流程一致，本地实现同样支持）：

      ① 申请上传：POST /items/<attKey>/file
         Content-Type: application/x-www-form-urlencoded
         If-None-Match: *
         表单字段 md5=<hex>、filename、filesize、mtime（毫秒）
         —— md5 必须放在**表单体**里。放响应头（MD5 / Content-MD5）或查询参数都会
            返回 HTTP 400 "MD5 hash not provided"。
         服务器若已存有同内容文件，返回 {"exists": 1}，跳过 ② ③ 直接完成。

      ② 上传字节：把响应里的 prefix + 文件字节 + suffix 拼起来 POST 到响应给的 url。
      ③ 登记：再 POST 一次申请端点，表单字段 upload=<uploadKey>。

    本地实现不支持增量（binary diff）上传：PATCH /items/<key>/file 会返回 405，
    每次都传完整文件。
    """
    data = pdf_path.read_bytes()
    md5_hex = hashlib.md5(data).hexdigest()
    stat = pdf_path.stat()
    att = {
        "itemType": "attachment",
        "parentItem": parent_key,
        "linkMode": "imported_file",
        "title": title,
        "filename": pdf_path.name,
        "contentType": "application/pdf",
    }
    created = create_item(att)
    att_key = created["key"]

    form = urllib.parse.urlencode({
        "md5": md5_hex,
        "filename": pdf_path.name,
        "filesize": len(data),
        "mtime": int(stat.st_mtime * 1000),
    }).encode()
    st, auth = _req("POST", f"/items/{att_key}/file", body=form,
                    ctype="application/x-www-form-urlencoded",
                    extra={"If-None-Match": "*"}, timeout=120)
    if not isinstance(auth, dict):
        raise ZoteroError(f"申请上传返回非结构化响应：HTTP {st} {str(auth)[:200]}")
    if auth.get("exists"):
        return att_key

    url, upload_key = auth.get("url"), auth.get("uploadKey")
    if not url or not upload_key:
        raise ZoteroError(f"申请上传响应缺少 url/uploadKey：{auth}")

    payload = (auth.get("prefix") or "").encode() + data + (auth.get("suffix") or "").encode()
    st2, _ = _req("POST", url, body=payload,
                  ctype=auth.get("contentType") or "application/octet-stream",
                  timeout=300)
    if st2 not in (200, 201, 204):
        raise ZoteroError(f"上传字节返回 HTTP {st2}")

    st3, _ = _req("POST", f"/items/{att_key}/file",
                  body=urllib.parse.urlencode({"upload": upload_key}).encode(),
                  ctype="application/x-www-form-urlencoded",
                  extra={"If-None-Match": "*"}, timeout=60)
    if st3 not in (200, 201, 204):
        raise ZoteroError(f"登记上传返回 HTTP {st3}")
    return att_key


def add_note(parent_key: str, text: str) -> str:
    note = {"itemType": "note", "parentItem": parent_key,
            "note": f"<p>{text}</p>"}
    return create_item(note)["key"]


def add(meta: dict, pdf: Path | None, collection: str, tags: list[str], note: str,
        force: bool = False) -> dict:
    doi = (meta.get("doi") or "").strip()
    if doi and not force:
        existing = find_by_doi(doi)
        if existing:
            k = existing[0]["key"]
            return {"status": "duplicate", "key": k,
                    "title": (existing[0].get("data") or {}).get("title"),
                    "url": f"zotero://select/items/0_{k}"}

    ckey = ensure_collection(collection) if collection else None
    if tags:
        meta = {**meta, "tags": list(dict.fromkeys((meta.get("tags") or []) + tags))}
    created = create_item(build_item(meta, ckey))
    key = created["key"]

    result = {"status": "created", "key": key, "title": meta.get("title"),
              "collection": collection or None, "url": f"zotero://select/items/0_{key}"}
    if pdf:
        if not pdf.exists():
            result["pdf_error"] = f"文件不存在：{pdf}"
        else:
            try:
                result["attachment"] = upload_pdf(key, pdf)
                result["pdf"] = str(pdf)
            except ZoteroError as e:
                result["pdf_error"] = str(e)
    if note:
        try:
            result["note"] = add_note(key, note)
        except ZoteroError as e:
            result["note_error"] = str(e)
    return result


# ---------------------------------------------------------------- RIS 兜底

def to_ris(meta: dict) -> str:
    lines = ["TY  - JOUR"]
    for a in meta.get("authors") or []:
        if "," in a:
            last, first = [x.strip() for x in a.split(",", 1)]
        else:
            parts = a.split()
            last, first = (parts[-1], " ".join(parts[:-1])) if len(parts) > 1 else (a, "")
        lines.append(f"AU  - {last}, {first}".rstrip(", "))
    for tag, key in (("TI  - ", "title"), ("JO  - ", "journal"), ("PY  - ", "date"),
                     ("VL  - ", "volume"), ("IS  - ", "issue"), ("SP  - ", "pages"),
                     ("DO  - ", "doi"), ("UR  - ", "url"), ("AB  - ", "abstract")):
        if meta.get(key):
            lines.append(f"{tag}{meta[key]}")
    for t in meta.get("tags") or []:
        lines.append(f"KW  - {t}")
    lines.append("ER  - ")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- CLI

def _load_meta(a) -> dict:
    if getattr(a, "meta", None):
        return json.loads(Path(a.meta).read_text(encoding="utf-8"))
    g = lambda k: getattr(a, k, None)  # noqa: E731  ris 子命令只定义了部分参数
    return {
        "title": g("title"), "authors": g("author") or [], "journal": g("journal"),
        "date": g("date"), "volume": g("volume"), "issue": g("issue"), "pages": g("pages"),
        "doi": g("doi"), "url": g("url"), "abstract": g("abstract"), "publisher": g("publisher"),
        "language": g("language"), "tags": g("tag") or [], "itemType": g("item_type"),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Zotero 本地 API 客户端")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("ping")
    sub.add_parser("collections")
    sub.add_parser("authorize", help="申请本地 API 密钥（Zotero 会弹授权框）")

    p_del = sub.add_parser("delete", help="按条目 key 删除")
    p_del.add_argument("key")

    p_att = sub.add_parser("attach", help="给已有条目补挂 PDF")
    p_att.add_argument("key")
    p_att.add_argument("pdf")
    p_att.add_argument("--title", default="Full Text PDF")

    p_has = sub.add_parser("has")
    p_has.add_argument("doi")

    p_add = sub.add_parser("add")
    p_add.add_argument("--meta", help="元数据 JSON 文件路径")
    p_add.add_argument("--doi")
    p_add.add_argument("--title")
    p_add.add_argument("--author", action="append")
    p_add.add_argument("--journal")
    p_add.add_argument("--date")
    p_add.add_argument("--volume")
    p_add.add_argument("--issue")
    p_add.add_argument("--pages")
    p_add.add_argument("--url")
    p_add.add_argument("--abstract")
    p_add.add_argument("--publisher")
    p_add.add_argument("--language")
    p_add.add_argument("--tag", action="append")
    p_add.add_argument("--item-type", default="journalArticle")
    p_add.add_argument("--pdf")
    p_add.add_argument("--collection", default="")
    p_add.add_argument("--note", default="")
    p_add.add_argument("--force", action="store_true", help="DOI 已存在时仍然新建")

    p_ris = sub.add_parser("ris")
    p_ris.add_argument("--meta")
    p_ris.add_argument("--out", required=True)
    p_ris.add_argument("--doi")
    p_ris.add_argument("--title")
    p_ris.add_argument("--author", action="append")
    p_ris.add_argument("--journal")
    p_ris.add_argument("--date")
    p_ris.add_argument("--url")
    p_ris.add_argument("--tag", action="append")
    p_ris.add_argument("--item-type", default="journalArticle")

    a = ap.parse_args()

    try:
        if a.cmd == "ping":
            print(json.dumps(ping(), ensure_ascii=False, indent=2))
        elif a.cmd == "authorize":
            print(f"密钥已就绪：{authorize(force=True)[:8]}…（已缓存至 {KEY_FILE}）")
        elif a.cmd == "delete":
            print(json.dumps(delete_item(a.key), ensure_ascii=False, indent=2))
        elif a.cmd == "attach":
            p = Path(a.pdf)
            if not p.exists():
                print(f"[错误] 文件不存在：{p}", file=sys.stderr)
                return 2
            att = upload_pdf(a.key, p, a.title)
            print(json.dumps({"status": "attached", "parent": a.key, "attachment": att,
                              "file": str(p)}, ensure_ascii=False, indent=2))
        elif a.cmd == "collections":
            for c in collections():
                d = c.get("data") or {}
                print(f"- {d.get('name')}  ({c['key']})")
        elif a.cmd == "has":
            hits = find_by_doi(a.doi)
            if hits:
                d = hits[0].get("data") or {}
                print(f"已存在：{d.get('title')}\nkey={hits[0]['key']}")
            else:
                print("未收录")
        elif a.cmd == "add":
            meta = _load_meta(a)
            res = add(meta, Path(a.pdf) if a.pdf else None, a.collection,
                      meta.get("tags") or [], a.note, a.force)
            print(json.dumps(res, ensure_ascii=False, indent=2))
        elif a.cmd == "ris":
            Path(a.out).write_text(to_ris(_load_meta(a)), encoding="utf-8")
            print(f"已写出 {a.out}（Zotero 中：文件 → 导入…）")
    except ZoteroError as e:
        print(f"[错误] {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
