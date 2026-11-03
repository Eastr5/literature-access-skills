# 文献获取技能集

WorkBuddy 技能仓库，收录文献与数据获取链路上自建的四个技能。

## 技能清单

| 技能 | 目录 | 作用 |
| --- | --- | --- |
| `cufe-library-access` | `skills/cufe-library-access/` | 中央财经大学图书馆电子资源的定位与访问。回答"学校有没有 XX 数据库""从学校怎么下载这篇文献"，解析三条访问通道（校内 IP / WebVPN / Shibboleth-CARSI），并内置 190 条数据库导航全量条目与下载节流参数。 |
| `literature-search` | `skills/literature-search/` | 多引擎学术检索。Semantic Scholar、arXiv、Tavily、Exa、AMiner、Google Scholar，按查询类型选择引擎，输出去重排序后的结构化元数据。 |
| `paper-fulltext-harvest` | `skills/paper-fulltext-harvest/` | 按 DOI 列表批量下载全文（PDF/XML）。按 25 个 DOI 前缀 / 19 个出版商家族分流到三条路径：出版商 TDM API、开放获取聚合源、浏览器兜底。 |
| `zotero-sync` | `skills/zotero-sync/` | 通过 Zotero 7 本地 API 把文献写入桌面版：DOI 查重、建条目、上传 PDF 附件、归入分类、打标签、写备注。 |

> `skills/literature-search/legacy/` 是早期同名的 `literature-search-skill` 仓库整体归档（含 agents / references / templates 设计稿），已被当前 `literature-search` 的脚本化实现取代，仅作参考留存。

## 链路关系

```
cufe-library-access   定位资源 + 确认访问通道
        ↓
literature-search      找到文献与元数据
        ↓
paper-fulltext-harvest 拿全文 PDF/XML
        ↓
zotero-sync            归档进 Zotero 库
```

前三个技能的浏览器兜底路径都依赖已登录的 Chrome 会话；`zotero-sync` 依赖 Zotero 桌面版处于运行状态。

## 安装

把对应技能目录放进 `~/.workbuddy/skills/`（Windows 为 `C:\Users\<用户名>\.workbuddy\skills\`），重启 WorkBuddy 即可被识别。

```bash
git clone <repo-url>
cp -r skills/* ~/.workbuddy/skills/
```

### 各技能的前置条件

- **cufe-library-access**：无需配置。`scripts/cufe_dbs.py update` 可重新抓取图书馆导航数据。
- **literature-search**：无需 key。脚本为 Node，直接调用公开 API。限流较严，脚本内已带 sleep。
- **paper-fulltext-harvest**：需要下载全文的出版商密钥。复制 `skills/paper-fulltext-harvest/scripts/.env.example` 为 `.env` 后填入手上有的项，缺项会自动禁用对应 provider。机构订阅的 TDM 还需要 `ELSEVIER_INSTTOKEN`。
- **zotero-sync**：需在 Zotero 里开启本地 API（设置 → 高级 → 允许本地 API 连接），并在 `extensions.zotero.httpServer.localAPI.enabled` 设为 `true`。首次写入时脚本自动申请本地 API key 并缓存到 `data/local_api_key.json`。

## 凭证处理

本仓库不含任何凭证。已做的处理：

- 移除 `zotero-sync/data/local_api_key.json`（本机 Zotero 本地 API key，首次使用时由脚本自动重新申请并生成，无需手动补）
- 所有绝对路径中的本机用户名替换为 `~`
- `.gitignore` 已屏蔽 `local_api_key.json`、`.env`、`config.json`、`__pycache__`、`node_modules` 等

## 来源说明

- `cufe-library-access` 与 `zotero-sync` 为本机自建，内容依据实际使用环境写成。
- `literature-search` 与 `paper-fulltext-harvest` 的初版来自外部开源项目（`paper-fulltext-harvest` 的出版商路由表与 `auto-paper-harvester` 共享，见其 `SKILL.md` 与 `references/tdm-apis.md` 中的上游链接）。二次分发前请自行确认上游许可。
- 部分技能文档中仍提到 `browser-cdp` 等 WorkBuddy 侧技能，跨环境使用时按本地实际情况调整。

## 使用边界

`paper-fulltext-harvest` 与 `cufe-library-access` 都涉及批量取全文。订购数据库的许可协议普遍禁止系统性下载，CNKI 与万方对连续快速下载有专门监测，触发后受影响的是**全校**的访问权限而非个人账号。取全文前先读 `skills/cufe-library-access/references/pacing.md` 与 `skills/paper-fulltext-harvest/references/` 下的节流参数说明。
