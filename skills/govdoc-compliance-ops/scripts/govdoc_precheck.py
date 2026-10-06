#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""govdoc_precheck.py — 公文合规预检门·术语闸机检 + 最小骨架检查。

用法:
  python3 govdoc_precheck.py <file.md>            # 术语闸全检
  python3 govdoc_precheck.py <file.md> --skeleton-only
  python3 govdoc_precheck.py <file.md> --json
  python3 govdoc_precheck.py --self-test

裁定依据: references/terminology.md（双框架词表/禁用清单/模糊术语裁定）。
纪律: 检出问题改文档不改闸；闸的误判修订走技能版本流。
"""
import json, re, sys

BANNED = {  # 词形: (类别, 裁定)
    "我觉得": ("个人视角口语", "error"), "我认为": ("个人视角口语", "error"),
    "可能吧": ("个人视角口语", "error"), "大概": ("个人视角口语", "warning"),
    "也许": ("个人视角口语", "warning"), "差不多": ("个人视角口语", "warning"),
    "变现": ("商业视角", "error"), "卖点": ("商业视角", "error"),
    "打法": ("商业视角", "error"), "闭环营销": ("商业视角", "error"), "私域": ("商业视角", "error"),
    "搞定": ("外来混杂", "error"), "搞得定": ("外来混杂", "error"),
    "彻底解决": ("夸张无据", "error"), "绝对安全": ("夸张无据", "error"),
}
# 「赋能」仅商业语境禁用：命中但同句含「使能/能力接口」豁免——从简：命中即 warning 交人工
BANNED_WARN = {"赋能": ("商业语境待裁", "warning")}
VAGUE = ["相关", "等等", "之类", "若干", "一定程度上"]
DEFINING = ["是指", "定义为", "包括", "分为", "指标为", "阈值为"]
SELF_OK = ["本席", "筹备组", "筹备处", "主权人", "机主"]
SELF_BAD = ["笔者", "我司", "我们团队", "小弟"]

def scan(path):
    text = open(path, encoding="utf-8").read()
    lines = text.split("\n")
    issues, urls = [], []
    in_code = False
    for i, ln in enumerate(lines, 1):
        if ln.strip().startswith("```") or ln.strip().startswith("~~~"):
            in_code = not in_code
        for u in re.findall(r"https?://[^\s\)）>|]+", ln):
            urls.append({"line": i, "url": u})
        if in_code:
            continue  # 代码块内不查术语（引文/日志豁免），链接仍登记
        for w, (cat, sev) in list(BANNED.items()) + list(BANNED_WARN.items()):
            if w in ln:
                if w == "闭环营销":
                    pass
                issues.append({"line": i, "kind": "banned", "word": w, "category": cat, "severity": sev,
                               "excerpt": ln.strip()[:60]})
        for w in SELF_BAD:
            if w in ln:
                issues.append({"line": i, "kind": "self_reference", "word": w,
                               "category": "自称失范（规范：本席/筹备组/主权人/机主）", "severity": "error",
                               "excerpt": ln.strip()[:60]})
        if any(d in ln for d in DEFINING):
            for v in VAGUE:
                if v in ln:
                    issues.append({"line": i, "kind": "vague_in_definition", "word": v,
                                   "category": "模糊术语在关键定义位", "severity": "error",
                                   "excerpt": ln.strip()[:60]})
        elif any(v in ln for v in VAGUE):
            hit = [v for v in VAGUE if v in ln][0]
            issues.append({"line": i, "kind": "vague_narrative", "word": hit,
                           "category": "叙述位模糊术语（建议枚举）", "severity": "warning",
                           "excerpt": ln.strip()[:60]})
    return {"file": path, "issues": issues, "urls": urls,
            "url_count": len(urls), "self_reference_ok": any(s in text for s in SELF_OK)}

def skeleton(path):
    text = open(path, encoding="utf-8").read()
    lines = [l for l in text.split("\n")]
    errs = []
    h1 = [l for l in lines if l.startswith("# ") and not l.startswith("## ")]
    if len(h1) != 1:
        errs.append(f"H1 数量={len(h1)}（应恰为 1）")
    first_nonempty = next((l for l in lines if l.strip()), "")
    if h1 and first_nonempty != h1[0]:
        errs.append("H1 非首个非空行")
    for f in ["文档标识", "版本", "状态", "更新日期", "责任席", "关联锚点"]:
        if f"| {f} |" not in text:
            errs.append(f"文档头缺要素：{f}")
    if not re.search(r"^## (变更记录|CHANGELOG|更新记录)\s*$", text, re.M):
        errs.append("缺变更记录节")
    return errs

def report(r, sk):
    errs = [i for i in r["issues"] if i["severity"] == "error"]
    warns = [i for i in r["issues"] if i["severity"] == "warning"]
    out = [f"预检报告 {r['file']}",
           f"一、术语闸：{'退回' if errs else '通过'}（error={len(errs)} warning={len(warns)}）"]
    for i in r["issues"]:
        out.append(f"  [{i['severity']}] 行{i['line']} {i['category']}：「{i['word']}」｜{i['excerpt']}")
    out.append(f"  链接登记 {r['url_count']} 枚（零改动比对基准）")
    out.append(f"  规范自称在场：{'是' if r['self_reference_ok'] else '否（警告）'}")
    if sk is not None:
        out.append(f"二、骨架闸：{'退回' if sk else '通过'}" + ("" if not sk else "｜" + "；".join(sk)))
    out.append("结论：" + ("退回修改" if (errs or sk) else "可过闸（warning 逐条处置后送审）"))
    return "\n".join(out)

def self_test():
    import tempfile, os
    good = "# 标题\n\n| 字段 | 内容 |\n|------|------|\n| 文档标识 | T-1 |\n| 版本 | v0.1.0 |\n| 状态 | 草案 |\n| 更新日期 | 2026-10-03 |\n| 责任席 | 本席 |\n| 关联锚点 | 无 |\n\n## 正文\n\n本席载明：指标为三项。\n\n## 变更记录\n\n| 版本 | 日期 | 变更摘要 | 责任席 |\n|------|------|----------|--------|\n| v0.1.0 | 2026-10-03 | 初版 | 本席 |\n"
    bad = "# 标题\n\n我觉得这个方案大概能搞定，变现路径相关等等。\n\n定义为若干指标在一定程度上满足。\n"
    with tempfile.TemporaryDirectory() as d:
        gp, bp = os.path.join(d, "g.md"), os.path.join(d, "b.md")
        open(gp, "w", encoding="utf-8").write(good)
        open(bp, "w", encoding="utf-8").write(bad)
        rg, rb = scan(gp), scan(bp)
        assert not [i for i in rg["issues"] if i["severity"] == "error"], f"好件误报: {rg['issues']}"
        assert not skeleton(gp), f"好件骨架误报: {skeleton(gp)}"
        bad_errs = [i for i in rb["issues"] if i["severity"] == "error"]
        assert len(bad_errs) >= 4, f"坏件漏报: {rb['issues']}"
        assert skeleton(bp), "坏件骨架应报错"
    print("self-test PASS")
    return 0

if __name__ == "__main__":
    args = sys.argv[1:]
    if "--self-test" in args:
        sys.exit(self_test())
    if not args or args[0].startswith("--"):
        print(__doc__); sys.exit(2)
    path = args[0]
    r = scan(path)
    sk = skeleton(path) if "--skeleton-only" in args or True else None  # 骨架恒检（最小集）
    if "--json" in args:
        r["skeleton_errors"] = sk
        print(json.dumps(r, ensure_ascii=False, indent=1))
    else:
        print(report(r, sk))
    errs = [i for i in r["issues"] if i["severity"] == "error"]
    sys.exit(1 if errs or sk else 0)
