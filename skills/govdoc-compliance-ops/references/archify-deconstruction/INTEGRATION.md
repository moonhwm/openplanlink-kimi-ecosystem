# archify 解构集成注记

> 本注记由 k3-main 起草（2026-10-03），与上游原文分署；上游一切文件以 `upstream/` 内逐字副本为准，本注记不作替代。校验单：`SHA256SUMS.txt`（222 件，与 /app/.agents/plugins/archify 源树逐字节一致）。

## 一、上游身份

| 项 | 值 |
|----|----|
| 插件 | archify v0.2.3（kimi.plugin.json） |
| 技能 | archify v2.17.0-dev.1（skill-release.json，channel=development） |
| 作者 | tt-a1i；上游 https://github.com/tt-a1i/archify |
| 许可 | MIT（upstream/skills/archify/LICENSE 在案；THIRD_PARTY_NOTICES.md 在案）；基于 Cocoon-AI/architecture-diagram-generator（MIT v1.0） |
| 再分发姿态 | MIT 允许，条件=保留版权与许可声明——本副本全树含 LICENSE，条件自足 |

## 二、能力解构（五类图 × 三命令）

- 图型路由：architecture（组件/边界/基础设施）、workflow（流程/审批门/CI-CD）、sequence（API 调用链/请求生命周期）、dataflow（管道/ETL/血缘）、lifecycle（状态机/重试/终态）。
- 命令面（均在 `upstream/skills/archify/bin/archify.mjs`）：`validate <type> <spec.json> --quality showcase --json`（验收闸，9 项 artifact 检查）、`deliver <type> <spec.json> <out.html> --quality showcase --json`（终验，冻结规格快照+SHA-256 回执）、`visual-check <out.html> --json`（浏览器取证）、`doctor`/`demo`（环境自检）、`guide "<scenario>"`（图型导购）、`brands`（品牌标识）。
- 输入面：自有 JSON 规格（schemas/ 六件契约 + examples/ 范例）；Mermaid 三类（flowchart/sequenceDiagram/stateDiagram）读拓扑后重新创作，不机械转译。
- 输出面：自包含可交互 HTML（内嵌 SVG、深/浅主题、缩放搜索、导出 PNG/JPEG/WebP/SVG/WebM）。

## 三、运行时与自包含性

- 运行时：Node ≥18（本沙箱 v20.20.2 实证在位）；**运行期零 npm 依赖**（package.json 之 devDependencies 仅生成器/测试用）。
- 自包含结论：**完全自包含**——全树已在技能内，直接以 `node references/archify-deconstruction/upstream/skills/archify/bin/archify.mjs ...` 运行，无需插件在位、无需联网。
- 例外面：`scripts/check-update.mjs` 的更新检查需联网，按其自身契约「不能跑即静默继续」，不影响本体。

## 四、与公文合规预检门的衔接

1. **公文附图**：送审稿涉架构/流程/时序（如 A2A 网络拓扑、事件驱动补偿流程、凭据链生命周期）时，用本解构件出图；图之 JSON 规格视同文书附件，过术语闸（节点命名禁模糊术语、视角一致）。
2. **验收纪律同构**：archify 之 validate→deliver 两阶段与本门「先过闸再发布」同构；非零退出不得称成功（与「bad 自报=0」同理）。
3. **证据纪律**：deliver 回执（SHA-256+字节数）可入凭据链外台账，作附图之不变量登记。
4. **文体**：图内文字遵双框架词表；meta.locale 用 zh-CN。

## 五、边界

- 本席不改写上游任何字节；上游缺陷与版本演进挂账，升级须经主权人批准后再逐字覆盖并更新 SHA256SUMS。
- 图解构件仅作辅能；公文合规裁定权不因出图能力而扩张。
