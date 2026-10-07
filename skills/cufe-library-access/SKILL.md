---
name: cufe-library-access
description: 中央财经大学图书馆电子资源的定位与访问。回答"学校有没有 XX 数据库""从学校怎么下载这篇文献""知网/万方/Web of Science 怎么进"，解析图书馆三条访问通道（校内 IP、WebVPN、Shibboleth/CARSI 联邦登录），按 DOI 或刊名找到对应资源入口。当用户提到学校图书馆、电子资源、数据库导航、知网、万方、维普、Web of Science、ScienceDirect、Springer、EBSCO、JSTOR、CSMAR，或问"这篇能不能下""校外怎么访问""我们学校订了没有"时使用。不负责检索接口层面的文献发现（那属于 literature-search），也不负责批量全文收割（那属于 paper-fulltext-harvest）。
agent_created: true
---

# 中央财经大学图书馆电子资源访问

图书馆电子资源页（数据库导航）实际是一份**资源清单**，不是跨库检索平台。190 条数据库条目，每条指向一个独立检索界面。因此本技能负责的是"**去哪找、怎么进、能不能拿到全文**"这三件事，检索本身由各库自己的界面完成。

## §1. 三条访问通道

| 通道 | 判定特征 | 登录要求 | 本机实测 |
|---|---|---|---|
| 校内 IP 直连 | 图书馆接口判定 `intranet = true` | 不需要 | 客户端 IP 10.13.60.5，判定为内网 |
| WebVPN 代理 | 域名含 `webvpn.cufe.edu.cn` | **需统一身份认证** | `webvpn.cufe.edu.cn` 返回登录页，跳 `authserver.cufe.edu.cn`，支持账号密码与微信扫码 |
| Shibboleth / CARSI 联邦登录 | 域名含 `idp.cufe.edu.cn`、`shibboleth`、`carsi.edu.cn`、`fsso.cnki` | **需统一身份认证** | `idp.cufe.edu.cn/idp/shibboleth` 可达 |

**条目通道分布（190 条）**：WebVPN 代理 74、Shibboleth 联邦 38、直连 18、CNKI fsso 8、无直接地址 52。

**两条硬约束，先讲清楚：**

1. **索引里标"Shibboleth 联邦登录"不等于必须登录。** 2026-09-30 用真实文章 DOI 实测：
   Elsevier ScienceDirect、Wiley、Emerald、T&F、ProQuest、EBSCO、Web of Science、CNKI、万方
   **在校园网 IP 下都能直接下到全文，不需要登录**——索引给的是推荐路线，不是唯一路线。
   真正必须登录的是 **WebVPN 批次（74 条）**、**CARSI 批次（超星-百链／读秀、中经数据）**
   与 **CNKI fsso 批次（8 条）**。完整实测见 `references/platform-coverage.md`。
2. **本技能不接触账号凭据。** 登录动作由用户本人在 Chrome 里完成，技能通过驱动已登录的浏览器会话读取页面。不得要求用户提供学号密码，也不得代填登录表单。

## §1b. 平台可达性实测（2026-09-30）

判定方法**不是**看首页有没有机构横幅，而是**让 Chrome 直接下载该刊一篇真实文章的 PDF**
并以 `%PDF` 文件头校验。完整表格与陷阱清单见 `references/platform-coverage.md`，要点：

- 常用 8 个平台（ScienceDirect / Wiley / Emerald / T&F / ProQuest / EBSCO / WoS / CNKI+万方）
  全部校园 IP 直接可用。
- 现刊包只有 5 个：ScienceDirect、Wiley、T&F（商业管理与经济学科）、Emerald 管理学、CNKI 学术期刊。
  **Springer 只有电子书包、Cambridge 只有回溯库、OUP 只有过刊 + 专著** → 这三家的现刊取不到。
- **维普与 IEEE 本校未订购**（索引中 0 条）。
- ⚠️ 三个判定陷阱：① 正则会被"中央财经大学 WebVPN"登录页误命中，须排除
  `webvpn.cufe.edu.cn/` 且正文 < 1000 字符的页面；② 首页没有机构名 ≠ 没权限（Wiley、Emerald 都如此）；
  ③ `Rent`、`Sign in` 这类付费墙词在有权限的页面上同样出现，不能当判据。

## §2. 资源索引的用法

索引脚本：`scripts/cufe_dbs.py`，索引数据：`data/cufe_dbs.json`。

```bash
PY="~/.workbuddy/binaries/python/versions/3.13.12/python.exe"

$PY scripts/cufe_dbs.py where                        # 当前是否在校内网（含客户端 IP）
$PY scripts/cufe_dbs.py find 知网 --url               # 按名称/别名/学科模糊查库
$PY scripts/cufe_dbs.py find 经济学 --limit 20
$PY scripts/cufe_dbs.py url "Web of Science"          # 只看入口地址与通道判定
$PY scripts/cufe_dbs.py detail CSMAR                  # 输出图书馆详情页地址
$PY scripts/cufe_dbs.py list --lang 外文 --discipline 经济学
$PY scripts/cufe_dbs.py stats                         # 索引概览
$PY scripts/cufe_dbs.py update                        # 重新抓取（书目变动后刷新）
```

数据来自公开列表接口 `https://lib.cufe.edu.cn/db/api/newDbsList?intranet=0`，无需登录。

**索引覆盖范围的两点说明**（实测，别再重复踩）：

- 列表接口给出 190 条，其中 **138 条带直接入口地址**；其余 52 条只能从详情页人工确认（多为客户端软件类资源，如 Wind、CSMAR 客户端）。
- **资源类型与数据库简介在列表接口恒为空**（190/190），只在详情页由前端异步加载，因此索引不含这两项，**不能按"期刊/图书/文摘"筛选**。学科与语言字段完整可用，筛选走这两个维度。

索引只是本地缓存，**授权状态的最终依据是图书馆页面**。

## §3. 取全文的分工

本技能只负责"找到入口并把浏览器带到正确页面"，实际的 PDF 获取按文献类型分流：

| 文献类型 | 走哪里 | 说明 |
|---|---|---|
| 英文期刊（Elsevier / Wiley / Springer / T&F / Emerald） | `paper-fulltext-harvest` 技能 | 该技能已有 25 个 DOI 前缀的出版商路由、OA 兜底（Unpaywall / OpenAlex / Crossref）与浏览器兜底。**不要在本技能里重复实现** |
| 中文期刊（CNKI / 万方 / 维普） | 本技能的浏览器流程 | 无公开 API，只能走图书馆登录后的页面；CNKI 提供 CAJ 与 PDF 两种格式，优先选 PDF |
| 图书 / 年鉴 / 学位论文 | 本技能的浏览器流程 | 多为 WebVPN 代理类，需登录 |
| 只有题录、无全文 | 记录来源，入 Zotero 后标注"待补全文" | 不要伪造或拼凑 |

取到全文后交 `zotero-sync` 技能入库。驱动浏览器的动作交 `browser-cdp` 技能执行。

**脚本化取全文已实测不可行**（2026-09-30，校园网内）：ScienceDirect 返回 403、知网跳滑块验证码、Web of Science 跳登录页；只有 Crossref 这类元数据接口可脚本化访问。因此"下载"这一步必须借真实浏览器会话，不能靠 `curl` 或 `requests`。

**国外出版商的取全文命令对**（以 Elsevier 为例，机制说明见 `browser-cdp` §5）：

```bash
$PY browser-cdp/scripts/chrome_cdp.py prepare --dir "F:/.../tmp/cdp-dl"   # 一次性配置
$PY browser-cdp/scripts/chrome_cdp.py open "https://www.sciencedirect.com/science/article/pii/<PII>"
# 从 DOM 里按 PII 号筛出 /pdfft 直链，再：
$PY browser-cdp/scripts/chrome_cdp.py download "<直链>" "<目标路径>.pdf" --dir "F:/.../tmp/cdp-dl"
```

前提是**代理 TUN 已关闭**；TUN 开着时出版商看到的是海外机房 IP，页面不会给出订阅全文（见 `browser-cdp` §2b）。

## §4. 操作纪律

**许可边界。** 所有订购数据库的许可协议都禁止系统性下载。CNKI 与万方对连续快速下载有专门监测，触发后暂停的是**全校**的访问权限，不是个人账号——代价是机构级的。完整参数、停止条件与升级规则见 `references/pacing.md`，**动手取全文前先读那一份**。摘要：

| 库 | 单篇间隔 | 单次会话上限 | 单日上限 |
|---|---|---|---|
| CNKI / 万方 | ≥ 30 秒 | 10 篇 | 30 篇 |
| Elsevier / Wiley / Emerald / T&F | ≥ 20 秒 | 20 篇 | 100 篇 |
| ProQuest / EBSCO（聚合库） | ≥ 30 秒 | 15 篇 | 50 篇 |
| OA 源（Unpaywall / OpenAlex / PMC） | ≥ 2 秒 | 100 篇 | 不限 |

每 10 篇插入一次 3–5 分钟的长暂停；串行、单标签页，不开多标签并行。

- 这些秒数**是自定的保守值**（厂商未公布阈值）→ 对外**不得**写成"官方限制"；
- 先取 1 篇验证链路，再放开批量；
- 出现验证码／滑块、跳登录页、403／429、"访问过于频繁"、或同一地址连续两次取回非 PDF → **停，冷却 ≥ 30 分钟，不重试**；同一平台触发两次则当日不再操作，把待取清单交用户手动处理；
- 不做整期、整刊、整个检索式结果集的拉取；
- 不绕验证码、不伪造 UA 规避检测；用户明确要求绕过时说明后果后由用户决定，不自行加码。

**浏览器会话。** 用 `browser-cdp` 技能驱动 Chrome。本机的浏览器自动化组件**不支持 Windows**，`browser-cdp` 走 Chrome 调试协议，是 Windows 上的实际通道。它使用独立配置目录（`~/.workbuddy\chrome-cdp-profile`），与日常 Chrome 隔离，因此**需要用户在该窗口内登录一次**统一身份认证；登录后 Cookie 长期保存在该目录，后续无需重复登录。

**登录态失效。** 出现登录页时停下，请用户本人完成登录，然后从当前步骤继续，不要重试同一请求。

## §5. 常见故障

| 现象 | 原因 | 处理 |
|---|---|---|
| 浏览器自动化组件报"不支持 Windows" | 该组件仅支持 macOS / Linux | 改用 `browser-cdp` 技能，走 Chrome 调试协议 |
| `curl` 访问出版商返回 403 | Cloudflare 拦截非浏览器请求 | 改用 `browser-cdp`，不要用命令行抓出版商页面 |
| WebVPN 域名打开是登录页 | 会话过期 | 请用户登录后重试 |
| 校内却拿不到全文 | 三种可能：未订阅该刊 / 需联邦登录 / 其实有权限但首页没显示机构名 | **先按 `references/platform-coverage.md` 的 DOI 直下法验证**，再判断是哪种；不要凭首页横幅就判"没权限" |
| 条目显示"无直接地址" | 图书馆未登记入口（如 Wind、CSMAR 客户端版） | 在图书馆详情页人工确认；这类多为客户端软件，非网页版 |
| 检索命中但没有下载按钮 | 未订阅该刊或仅订购题录 | 记录并转交题录，全文标注"待补" |

## §6. 文件布局

```
cufe-library-access/
├── SKILL.md
├── references/
│   ├── platform-coverage.md   平台可达性实测：通道归并、判定性表格、判定陷阱、复现命令
│   └── pacing.md             节流参数与停止条件：两套节奏、按库分档、触发信号、升级规则
├── scripts/
│   └── cufe_dbs.py     索引抓取、精简、查询与通道判定
└── data/
    └── cufe_dbs.json   190 条资源索引（可 update 刷新）
```
