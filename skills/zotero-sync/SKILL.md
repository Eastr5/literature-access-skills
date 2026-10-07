---
name: zotero-sync
description: 通过 Zotero 7 本地 API 把文献写入 Zotero 桌面版：按 DOI 查重、建条目、上传 PDF 附件、归入分类、打标签、写备注。当用户说"存到 Zotero""同步到 Zotero""加入我的文献库""这篇入库""挂个 PDF 到 Zotero"，或完成文献下载后需要归档时使用。不依赖 Zotero 云端账号与 API key；Zotero 未运行时改用 RIS 导出兜底。不负责文献检索与下载（分别属于 literature-search 与 paper-fulltext-harvest）。
agent_created: true
---

# Zotero 入库（本地 API）

写入走 Zotero 桌面版的**本地 HTTP API**（`http://localhost:23119/api/users/0`），路径与 Zotero Web API v3 一致，但不经云端、不需要 API key、不占用同步流量。

**本机环境（已核验）**

| 项 | 值 |
|---|---|
| 程序位置 | 免安装版 `D:\Zotero\Zotero_win-x64\zotero.exe` |
| 数据目录 | `~/Zotero` |
| 本地 API 开关 | `extensions.zotero.httpServer.localAPI.enabled = true`（已开启） |
| 已有内容 | 16 条顶层条目、15 个附件、10 个分类 |
| 分类 | 未命名、阅读文献-崔、papers、基于知识图谱——外汇市场风险研究_沈嘉贤2025、知识图谱综述_田玲2021、BPHD-2026、DGNN-SR、Hypergraph-金融三篇、Vipra-Korinek-2023、LLM_KG构建论文 |
| 同步账号 | `eastr5`（桌面版自行同步到 zotero.org） |

## §1. 前提条件

两项缺一不可：

1. **Zotero 桌面版正在运行。** 未运行时本地 API 端口不监听，脚本会明确报错，不会静默失败。
2. **「设置 → 高级 → 允许其他应用与本机 Zotero 通信」已勾选。** 本机已开启，换机器时需重设。

若 Zotero 未运行，先用 §4 的 RIS 导出兜底，不要试图直接读写 `zotero.sqlite`——**Zotero 运行时直接改库会造成数据损坏**。

## §2. 常用命令

```bash
PY="~/.workbuddy/binaries/python/versions/3.13.12/python.exe"

$PY scripts/zotero.py ping                        # 连通性
$PY scripts/zotero.py collections                 # 列出分类及 key
$PY scripts/zotero.py has 10.1007/s44443-026-00904-2   # 按 DOI 查重

$PY scripts/zotero.py add \
  --doi 10.1007/s44443-026-00904-2 \
  --title "Default prediction and contagion risk assessment..." \
  --author "Yang,Shudan" --author "Liu,Xiaoyu" \
  --journal "J. King Saud Univ. Comput. Inf. Sci." \
  --date 2026 --volume 38 --pages 495 \
  --collection "阅读文献-崔" --tag 担保网络 --tag 撞车 \
  --pdf "F:/2026年/阅读文献-崔/papers/xxx.pdf"

$PY scripts/zotero.py add --meta meta.json --pdf x.pdf --collection "阅读文献-崔"
```

`add` 返回 JSON，含条目 key、分类、附件 key，以及 `zotero://select/items/0_<key>` 跳转链接。

**作者名格式**：`"姓,名"`（`Yang,Shudan`）或 `"名 姓"`（`Shudan Yang`）都接受，脚本统一转成 Zotero 的 creator 结构。

**查重**：`add` 默认先按 DOI 精确查重，命中则跳过并返回 `status: "duplicate"`。需要强制新建时加 `--force`。

## §3. 编程调用

```python
import sys
sys.path.insert(0, r"~/.workbuddy\skills\zotero-sync\scripts")
from zotero import add, find_by_doi, ensure_collection
from pathlib import Path

add(
    {"title": "...", "doi": "...", "authors": ["Yang,Shudan"],
     "journal": "...", "date": "2026", "tags": ["担保网络"]},
    pdf=Path("D:/papers/x.pdf"),
    collection="阅读文献-崔",
    tags=["撞车"],
    note="撞车终判：披露日对齐条目已被占用。",
)
```

可用函数：`ping`、`collections`、`ensure_collection`、`find_by_doi`、`build_item`、`create_item`、`upload_pdf`、`add_note`、`add`、`to_ris`。

## §4. RIS 兜底

Zotero 没开、或本地 API 被防火墙挡住时：

```bash
$PY scripts/zotero.py ris --out "F:/.../tmp/x.ris" --doi ... --title ... --author "Yang,Shudan" \
    --journal ... --date 2026 --tag 担保网络
```

然后在 Zotero 中「文件 → 导入…」选中该 ris 文件。RIS 不含 PDF，全文需另行挂载。

## §5. 操作纪律

- **不直接读写 `zotero.sqlite`。** 所有写操作走本地 API。
- **入库前先查重**，避免同一 DOI 出现多条记录。
- **上传的 PDF 先校验**：文件存在、大小合理、前 4 字节为 `%PDF`。脚本会检查文件存在性；内容校验由上游下载环节负责。
- **分类名不擅自新建。** 目标分类不存在时 `ensure_collection` 会创建；不确定归到哪里时先列出现有分类问用户，不要凭猜测新建。
- **同步由桌面版决定。** 写完只在本地库可见，是否上传到 zotero.org 取决于桌面版的同步开关与账号状态，本技能不触发同步。

## §6. 文件布局

```
zotero-sync/
├── SKILL.md
└── scripts/
    └── zotero.py   本地 API 客户端（读、写、附件上传、RIS 兜底）
```

## §7. 排错

| 现象 | 原因 | 处理 |
|---|---|---|
| `无法连接 Zotero 本地 API（WinError 10061）` | Zotero 未运行 | 启动 Zotero 桌面版 |
| `HTTP 403` / `HTTP 400` | 本地 API 开关未勾选 | 设置 → 高级 → 允许其他应用通信 |
| 条目建好但附件缺失，返回 `pdf_error` | 文件上传端点不通 | 见 §8；若仍失败，用 RIS 兜底后手动拖入 PDF |
| `创建分类失败` | 同名分类已存在但字段异常 | 用 `collections` 查看现有分类名 |

## §8. PDF 附件上传：三段式流程与已证伪的做法

上传 PDF 要按申请、传字节、登记三步走，与 Zotero Web API 的文件上传流程一致，本地实现同样支持。

**① 申请上传**

```
POST /items/<附件key>/file
Content-Type: application/x-www-form-urlencoded
If-None-Match: *

md5=<文件 md5 的十六进制串>&filename=<文件名>&filesize=<字节数>&mtime=<毫秒时间戳>
```

`md5` 必须是 `hashlib.md5(data).hexdigest()`，且必须放在**表单体**里。放响应头（`MD5` / `Content-MD5` / `Zotero-MD5`）或放查询参数（`?md5=` / `?MD5=` / `?hash=`）都会被拒，返回 HTTP 400 `MD5 hash not provided` —— 这 8 种变体已逐一实测，全部失败。

响应形如：

```json
{"url": "http://localhost:23119/api/local/uploads/<key>", "uploadKey": "<key>",
 "contentType": "application/pdf", "prefix": "", "suffix": ""}
```

若服务器已存有同内容文件（md5 命中），返回 `{"exists": 1}`，跳过 ②③ 直接完成。

**② 上传字节** 把 `prefix + 文件字节 + suffix` 拼接后 POST 到响应给的 `url`，成功返回 201。

**③ 登记** 再 POST 一次申请端点，表单体 `upload=<uploadKey>`，成功返回 204。

完成后 Zotero 会把 `md5` 与 `mtime` 写回附件条目，可用 `GET /items/<key>` 复核；文件落在数据目录 `~/Zotero\storage\<附件key>\<文件名>`，应与源文件 md5 一致。

**不支持增量上传。** `PATCH /items/<key>/file` 在本地实现返回 405，每次都传完整文件。

**实测记录（2026-09-30）**：DHGN-Credit 条目 `ZAPPH6P5` 挂载 2.82 MB 的 `s44443-026-00904-2.pdf`（md5 `959651dc954644fa2cfb93fe7599e1e7`），申请返回 200、上传返回 201、登记返回 204，存储文件与源文件 md5 逐位一致。`GET /items/<key>/file` 会返回 302 跳转，属正常行为，不是错误。
