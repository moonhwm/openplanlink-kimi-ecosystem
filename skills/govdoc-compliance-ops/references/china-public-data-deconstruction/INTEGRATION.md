# china_public_data 解构集成注记

> 本注记由 k3-main 起草（2026-10-03），与上游原文分署；上游一切文件以 `upstream/` 内逐字副本为准，本注记不作替代。校验单：`SHA256SUMS.txt`（5 件，与 /app/.agents/plugins/china_public_data 源树逐字节一致）。

## 一、上游身份

| 项 | 值 |
|----|----|
| 插件 | china_public_data v0.1.12（kimi.plugin.json） |
| 作者 | Moonshot AI |
| 许可 | **UNLICENSED**（kimi.plugin.json 明示）——无再分发授权文 |
| 再分发姿态 | 按本体系许可纪律：**体系内参照使用，不对外再分发**，对外发布挂账候主权人裁定 |
| 数据源主页 | https://sjdj.nda.gov.cn/ （国家公共数据资源登记平台） |

## 二、能力解构（两 datasource × 六 API）

- **china_nda**（国家数据局体系）：
  - `china_nda_registry_search`：登记平台目录检索，结果落 CSV，返回行自带 `access_*` 四列（access_code/access_province_code/access_data_type/access_platform_code）；
  - `china_nda_registry_access`：获取方式解析（open 给 URL / authorized_operation 给机构 / apply 给用数申请指引）——入参即上一步 CSV 的 `access_*` 四列透传；
  - `china_nda_provinces` / `china_nda_province_search`：省级开放平台目录（限 13 区域码：海南/江西/山东/广东/北京/福建/安徽/湖南/湖北/内蒙古/四川/广西/哈尔滨市）。
- **china_nbs**（国家统计局）：
  - `china_nbs_indicators`：指标发现，11,789 个全国/省/市指标，按关键词检索名称/类别/路径，返回 scope 与 frequency；
  - `china_nbs_query`：语义查询，18 个精选指标（GDP/CPI/PPI/工业增加值/固投/社零/进出口/失业率/可支配收入/人口/M2/房地产投资/PMI/外汇储备/发电量/工业企业利润等）+ indicators 返回之任意指标，结果落 CSV。
- 命令面：`python3 scripts/china_public_data_tool.py describe`（聚合文档）与 `call --data-source <china_nda|china_nbs> --api-name <api> --params-json '{...}'`（或 `--params-file`）。

## 三、运行时与自包含性

- 脚本本体：`scripts/china_public_data_tool.py`（本技能内副本与上游逐字节一致，sha256=a31651dc45fb…4934）。
- 依赖：agent_gw Python SDK（缺时按其 Setup 节安装）+ 鉴权（`KIMI_API_KEY` 环境变量或 `~/.kimi/agent-gw.json` 其一）。
- 自包含结论：**代码自包含、取数依赖网关**——脚本为 agent-gw 薄转发层，不直连统计局/数据局；无网关鉴权时不得运行数据查询，且**严禁凭记忆编造指标数值**（上游 Compliance 节与本门红线同义）。

## 四、与公文合规预检门的衔接

1. **数据取证闸**：公文涉宏观经济数值（GDP/CPI/M2 等）时，以本解构件取证，CSV 落盘入附件；正文引用须注明来源（国家统计局/登记平台）、口径（同比=上年同月 100，涨幅=value−100）、地区与时间范围。
2. **先发现后查询**：非常用指标必先 `indicators` 确认 scope/frequency 再 `query`——与术语闸「先词表后行文」同构。
3. **口径红线**：指数类仅同比口径；环比须改用统计局发布稿并注明渠道差异；`registry_access` 结果必须注明「仅为获取指引，非原始数据」。
4. **重试纪律**：相同参数相同错误最多原样重试一次；EMPTY_DATA/NOT_FOUND 换关键词或如实标注来源更替。

## 五、边界

- 本席不改写上游任何字节；UNLICENSED 姿态下，本解构件不随技能对外发布——若技能需对外分发，先剔除本目录或取得授权，二选一候主权人裁。
- bundle.zip（14,723B）为上游自带包，原样保全不拆改。
