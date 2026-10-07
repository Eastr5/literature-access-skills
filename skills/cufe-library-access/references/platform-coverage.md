# 央财图书馆：期刊类电子资源可达性实测

> 实测日期 2026-09-30。条件：校园网 IP（客户端 `10.13.60.5`，公网出口 `36.112.35.195`）、
> 代理 TUN 已关闭、未做任何登录。目的＝回答"哪些平台现在就能用，哪些要逐个过一遍"。

## 结论先行

- **190 条索引归到 5 条访问通道**，不是 190 个平台。
- **研究者常用的 8 个平台全部凭校园网 IP 直接可用，不需要登录**——已用真实文章 DOI 下到 PDF 验证，
  不是看首页横幅推断的。
- 需要一次性登录的只有三类：**WebVPN 批次**、**CARSI 批次**、**CNKI fsso**。
- 现刊包其实只有 5 个；索引里的多数条目是回溯库、电子书或数据库。

---

## 一、五条通道（静态，取自索引 `accessRoute` 字段）

| 通道 | 条数 | 前置条件 |
|---|---|---|
| WebVPN 代理 | 74 | 统一身份认证一次 |
| 无直接地址 | 52 | 索引未给直链，需看详情页；多为免费公开资源 |
| Shibboleth 联邦登录 | 38 | CUFE IdP 一次 |
| 直连 | 18 | 无 |
| CNKI 联邦登录 fsso | 8 | 选机构并登录一次 |

索引自带 `loginRequired` 分布：需统一身份认证 112 / 需在详情页查看 52 / 视资源而定 18 / 需登录 8。

按访问通道入口归并：

| 类别 | 代表资源 | 入口 |
|---|---|---|
| WebVPN | JSTOR、SAGE Deep Backfile、NSTL、HeinOnline、ACM Portal、剑桥回溯、牛津专著、CSMAR、CNRDS、J-STAGE、Bentham | `https://webvpn.cufe.edu.cn/` |
| CARSI | 超星-百链、超星-读秀、中经数据（教育版） | `https://ds.carsi.edu.cn/login/` |
| CNKI fsso | 知网总库／会议论文／学位论文／年鉴 | `https://fsso.cnki.net/`，机构列表里选"中央财经大学" |
| Shibboleth SSO | Wiley、Emerald、T&F、ProQuest、EBSCO、万方、BvD、RESSET | `idp=https://idp.cufe.edu.cn/idp/shibboleth` |

---

## 二、判定性实测（有全文权限的）

方法：**不看首页横幅，直接让 Chrome 下载该刊一篇真实文章的 PDF**，以 `%PDF` 文件头校验。

| 平台 | 判据 | 结果 |
|---|---|---|
| Elsevier ScienceDirect | IRFA `10.1016/j.irfa.2023.102635` → 1,878,398 B | ✅ 全文 |
| Wiley | CAR `10.1111/1911-3846.70083` → 695,242 B | ✅ 全文 |
| Emerald | MAJ `10.1108/maj-11-2024-4587` → 579,174 B | ✅ 全文 |
| Taylor & Francis | 首页 `Access provided by Central University of Finance & Economy` | ✅ 已识别 |
| ProQuest ABI/INFORM | 检索页出现机构名 | ✅ 已识别 |
| EBSCO | 携带 `shibtoken` 落地，显示"中央财经大学" | ✅ 已识别 |
| Web of Science | 落地 `webofscience.clarivate.cn`，显示机构名 | ✅ 已识别 |
| 中国知网 | `kns.cnki.net` 显示"中央财经大学图书馆" | ✅ 已识别 |
| 万方数据 | 显示"中央财经大学" | ✅ 已识别 |
| ACM Digital Library | 裸域名显示机构名 | ✅ 已识别 |
| Springer Link | 显示机构名（但订阅只有电子书包） | ✅ 已识别 |

---

## 三、判定陷阱（本次全部踩到，复用时先看这一节）

1. **正则会把 WebVPN 登录页当成"已授权"。**
   `中央财经大学 WebVPN` 这个标题命中了关键词 `中央财经`，导致 JSTOR／SAGE／NSTL／HeinOnline／
   ACM／剑桥回溯六个平台在脚本里被误报为"已授权"，实际都停在登录页。
   → 排除规则：URL 落在 `webvpn.cufe.edu.cn/` 且 `document.body.innerText.length < 1000` → 判为"未登录"。

2. **首页没有机构名 ≠ 没有权限。**
   Wiley、Emerald 首页都不显示机构名，但文章页的 PDF 直链可以直接下。
   → 首页横幅只能当粗筛，判据必须是"能不能下到 PDF"。

3. **索引的 `accessRoute` 是推荐路线，不是唯一路线。**
   ScienceDirect / WoS / ProQuest / T&F / Wiley / Emerald 在索引里都标"Shibboleth 联邦登录"，
   但校园 IP 下裸域名直接可用。索引**低估**了校园 IP 的可达范围。

4. **付费墙词不可靠。** `Rent`、`Sign in` 在有权限的 Elsevier／Emerald 页面上同样出现。

5. **SSO 深链未必能直达。** `shibboleth.ebscohost.com/...target=` 那种深链实测报
   `EBSCOhost System Error`；改用索引里正常的 `shibboleth-sp` 入口后正常。

---

## 四、没有订阅的

- **维普、IEEE**：索引中 0 条，本校未订购。
- **现刊包只有 5 个**：Elsevier ScienceDirect、Wiley、T&F（商业管理与经济学科）、
  Emerald 管理学、CNKI 学术期刊。
- **Springer 只有电子书包**（计算机科学学科包）、**Cambridge 只有回溯库**（国图来源）、
  **OUP 只有 1849–1995 过刊 + 在线专著** → 这三家的**现刊**不能直接取。
- JSTOR、SAGE Deep Backfile 也是过刊库，不是现刊。

---

## 五、复现命令

```bash
cd "F:/2026年/阅读文献-崔"
PY="~/.workbuddy/binaries/python/versions/3.13.12/python.exe"

"$PY" tmp/platform_check.py     # 第一轮：20 个平台首页扫描
"$PY" tmp/platform_check2.py    # 第二轮：用索引里的官方入口复测
"$PY" tmp/doi_check.py          # 第三轮：真实 DOI 落地页诊断
"$PY" tmp/pdf_probe.py          # 第四轮：判定性，直接下载 PDF
```

⚠️ `pdf_probe.py` 运行前必须调用 `chrome_cdp.prepare(dir)`（写入
`plugins.always_open_pdf_externally` 后重启实例），否则导航到 PDF 地址会被 Chrome 内置阅读器接管，
磁盘上不会出现文件，脚本只会报"等待 N 秒未发现下载文件"。

⚠️ `chrome_cdp.download(url, out, download_dir, wait)` 的 `out` 与 `download_dir`
**必须是 `Path` 对象**（传 `str` 会报 `'str' object has no attribute 'parent'`），
返回值是 `{"bytes", "path", "from"}` 而非路径字符串。
