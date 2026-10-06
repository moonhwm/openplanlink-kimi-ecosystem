# openplanlink-kimi-ecosystem

OpenPlanLink A2A 网络 · Kimi 生态层成果镜像（首批同步：2026-10-05）。

- 维护席：K3 主程序·云端沙箱（k3-main）
- 批准依据：主权人 2026-10-05 令「把目前技能等kimi生态层成果同步到github」
- 关联仓库：moonhwm/openplanlink-mirror（幻16 bridge 自动同步通道，本仓库不写入彼仓库）

## 目录结构

```text
skills/
├── govdoc-compliance-ops/        公文合规预检门 v0.2.0（术语闸/格式闸联动/协议闸）
│   ├── SKILL.md
│   ├── scripts/govdoc_precheck.py
│   └── references/               terminology / license-matrix / 两解构 INTEGRATION 与校验单
└── otl-format-ops/               OTL 编写总署（WPS 智能文档编写标准与发布管线）
    ├── SKILL.md
    ├── scripts/otl_source_lint.py
    ├── references/               markdown-subset / otl-facts / publishing
    └── assets/templates/         general-doc / ledger / plan / skill-doc
governance/
├── sdd/                          SDD 母规范与 specs 登记（0001 自进化聚焦工程）
├── verifier/                     验收准则（v1）与逐轮运行日志
├── reviews/                      全局声明审读报告
└── annotations/                  聚焦文档重读批注
```

## 剔除清单与理由（不同步项）

| 件 | 理由 |
|----|------|
| china_public_data 上游树与工具脚本副本 | UNLICENSED，体系内参照、不对外分发；INTEGRATION.md 与 SHA256SUMS.txt 在册存证 |
| archify 上游全树（222 件，约 8.3MB） | MIT 可再分发，但与上游 https://github.com/tt-a1i/archify 同源；本地全树保全并以 SHA256SUMS.txt（222 行）登记，镜像不重复携带 |
| 运维留痕件 | 含本机机器标识（网卡 MAC），依「机器标识不广播」纪律不同步 |
| 凭据链补丁件 | 凭据指纹登记件，不对外 |
| .skill 打包二进制 | 交付位于本地；镜像以真源为准（govdoc-compliance-ops v0.2.0 打包指纹 2c224023527e06d6 在案） |

## 许可姿态（主权人 2026-10-03 裁定分层组合）

- 代码层：AGPL-3.0（官方原文以 LICENSE-POINTER.md 指针登记，不改写不节选）
- 文档/蓝图：CC BY-SA 4.0
- 治理文本（governance/ 下规程与报告类）：不许可化，主权人保留终审权
- 第三方件随其各自许可（archify 上游为 MIT）；SSPL-1.0 层当前清单为空

## 溯源与纪律

- 真源：Kimi 云端沙箱交付位（/mnt/agents/output/），本镜像为只读快照式同步。
- 文书纪律：governance/ 各件均过双闸（otl_source_lint 0 error；govdoc_precheck 0 error）。
- 广播纪律：零 PII、零凭据、零机器标识；超链接零改动。
