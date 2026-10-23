#!/usr/bin/env python3
"""
Maxilun Skill Ecosystem Test Suite

Structural and functional validation:
- 18 skills exist with valid frontmatter and one shared version
- Every skill embeds the identical CORE-RULES block (drift detection)
- Every referenced file inside a skill resolves from that skill's folder
- No references to external skills or to the removed root rules/ layout
- Section numbering is unique and sequential
- Banned vocabulary purity self-check
- Knowledge Graph scanner functional verification
- Cross-references between specialists
"""

import os
import sys
import re
import tempfile
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills" if (REPO_ROOT / "skills").exists() else REPO_ROOT / ".agents" / "skills"
ORCHESTRATOR = SKILLS_DIR / "maxilun"

sys.path.insert(0, str(SKILLS_DIR / "maxilun-knowledge-graph"))

EXPECTED_SKILLS = [
    "maxilun",
    "maxilun-knowledge-graph",
    "maxilun-scaffold",
    "maxilun-architect",
    "maxilun-sentinel",
    "maxilun-engineer",
    "maxilun-data",
    "maxilun-frontend",
    "maxilun-verify",
    "maxilun-insight",
    "maxilun-deploy",
    "maxilun-docsmith",
    "maxilun-craft",
    "maxilun-motion",
    "maxilun-cinecode",
    "maxilun-diagrams",
    "maxilun-content",
    "maxilun-seo-audit",
]

REQUIRED_REFERENCES = [
    "engines.md",
    "discovery.md",
    "purity-catalog.md",
    "code-hygiene.md",
]

BANNED_WORDS = [
    r"\bdelve\b",
    r"\btapestry\b",
    r"\bsynergy\b",
    r"\bholistic\b",
    r"\bleverage\b",
    r"\bseamlessly\b",
    r"\brobust\b",
    r"\bcutting-edge\b",
    r"\bgame-changer\b",
    r"\brevolutionary\b",
    r"\bsupercharge\b",
    r"\bdive in\b",
]

PURE_EXEMPT_SKILLS = ["maxilun", "maxilun-content", "maxilun-docsmith"]

FORBIDDEN_EXTERNAL = ["antislop", "frontend-design", "brainstorming", "superpowers"]
FORBIDDEN_LAYOUT = ["rules/always-on.md", "rules/maxilun-global.md", "rules/code-hygiene.md", "rules/purity-catalog.md"]

CORE_START = "<!-- CORE-RULES:START -->"
CORE_END = "<!-- CORE-RULES:END -->"


def parse_frontmatter(content: str) -> str:
    parts = content.split("---")
    if len(parts) >= 3:
        return parts[1]
    return ""


def skill_path(skill: str) -> Path:
    return SKILLS_DIR / skill / "SKILL.md"


def read_skill(skill: str) -> str:
    return skill_path(skill).read_text(encoding="utf-8")


def extract_core_block(content: str) -> str:
    m = re.search(re.escape(CORE_START) + r"(.*?)" + re.escape(CORE_END), content, re.DOTALL)
    if not m:
        return ""
    return re.sub(r"\s+", " ", m.group(1)).strip()


def test_skills_exist():
    print("🧪 Checking 18 skills existence...")
    missing = [s for s in EXPECTED_SKILLS if not skill_path(s).exists()]
    for s in EXPECTED_SKILLS:
        if skill_path(s).exists():
            print(f"  ✅ Found {s}/SKILL.md")
    if missing:
        print(f"  ❌ Missing skills: {', '.join(missing)}")
        return False
    return True


def test_frontmatter():
    print("\n🧪 Validating frontmatter schema and version consistency...")
    passed = True
    versions = set()
    for skill in EXPECTED_SKILLS:
        fm = parse_frontmatter(read_skill(skill))
        if not fm:
            print(f"  ❌ {skill}: Missing or invalid frontmatter")
            passed = False
            continue
        name_match = re.search(r"^name:\s*([^\s]+)", fm, re.MULTILINE)
        if not name_match or name_match.group(1).strip() != skill:
            print(f"  ❌ {skill}: 'name' does not match directory")
            passed = False
        if "description:" not in fm:
            print(f"  ❌ {skill}: Missing 'description'")
            passed = False
        version_match = re.search(r"^\s+version:\s*['\"]?(\d+\.\d+\.\d+)['\"]?\s*$", fm, re.MULTILINE)
        if not version_match:
            print(f"  ❌ {skill}: Missing or invalid semantic version")
            passed = False
        else:
            versions.add(version_match.group(1))
        if "license: Maxilun-Source-Available-2.0" not in fm:
            print(f"  ❌ {skill}: License is not Maxilun-Source-Available-2.0")
            passed = False
        if not re.search(r"^  ecosystem:\s*maxilun\s*$", fm, re.MULTILINE):
            print(f"  ❌ {skill}: Missing ecosystem: maxilun marker")
            passed = False
    if len(versions) == 1:
        print(f"  ✅ All skills report version {versions.pop()}")
    else:
        print(f"  ❌ Version drift across skills: {sorted(versions)}")
        passed = False
    return passed


def test_core_rules_block():
    print("\n🧪 Validating embedded CORE-RULES block...")
    passed = True
    blocks = {}
    for skill in EXPECTED_SKILLS:
        content = read_skill(skill)
        block = extract_core_block(content)
        if not block:
            print(f"  ❌ {skill}: Missing CORE-RULES block")
            passed = False
            continue
        blocks[skill] = block
    if not blocks:
        return False
    unique = set(blocks.values())
    if len(unique) == 1:
        print(f"  ✅ Identical CORE-RULES block in all {len(blocks)} skills")
    else:
        print(f"  ❌ CORE-RULES drift: {len(unique)} distinct variants")
        canonical = blocks.get("maxilun")
        for skill, block in blocks.items():
            if block != canonical:
                print(f"     differs: {skill}")
        passed = False
    return passed


def test_references_present():
    print("\n🧪 Validating bundled references...")
    passed = True
    for ref in REQUIRED_REFERENCES:
        p = ORCHESTRATOR / "references" / ref
        if p.exists() and p.stat().st_size > 500:
            print(f"  ✅ references/{ref}")
        else:
            print(f"  ❌ Missing or empty references/{ref}")
            passed = False
    return passed


def test_reference_paths_resolve():
    print("\n🧪 Resolving every file path referenced inside skills...")
    passed = True
    pattern = re.compile(r"`((?:\.\./[\w.-]+/)*references/[\w.-]+\.md)`")
    for skill in EXPECTED_SKILLS:
        content = read_skill(skill)
        for rel in set(pattern.findall(content)):
            target = (SKILLS_DIR / skill / rel).resolve()
            if target.exists():
                print(f"  ✅ {skill}: {rel}")
            else:
                print(f"  ❌ {skill}: {rel} does not resolve to a file")
                passed = False
    return passed


def test_no_external_or_legacy_refs():
    print("\n🧪 Checking for external-skill and legacy rules references...")
    passed = True
    for skill in EXPECTED_SKILLS:
        content = read_skill(skill)
        for token in FORBIDDEN_EXTERNAL:
            if token in content:
                print(f"  ❌ {skill}: references external skill '{token}'")
                passed = False
        for token in FORBIDDEN_LAYOUT:
            if token in content:
                print(f"  ❌ {skill}: references removed layout '{token}'")
                passed = False
    if passed:
        print("  ✅ No external-skill or legacy rules references")
    return passed


def test_section_numbering():
    print("\n🧪 Validating section numbering...")
    passed = True
    for skill in EXPECTED_SKILLS:
        lines = read_skill(skill).splitlines()
        fence = False
        nums = []
        for line in lines:
            if line.strip().startswith("```"):
                fence = not fence
                continue
            m = re.match(r"^## (\d+)\. ", line)
            if m and not fence:
                nums.append(int(m.group(1)))
        dupes = sorted({n for n in nums if nums.count(n) > 1})
        if dupes:
            print(f"  ❌ {skill}: duplicate section numbers {dupes}")
            passed = False
        elif nums and nums != list(range(nums[0], nums[0] + len(nums))):
            print(f"  ⚠️  {skill}: non-sequential numbering {nums}")
    if passed:
        print("  ✅ No duplicate section numbers")
    return passed


def test_purity_self_check():
    print("\n🧪 Running purity self-check on skills...")
    clean = True
    for skill in EXPECTED_SKILLS:
        if skill in PURE_EXEMPT_SKILLS:
            continue
        content = read_skill(skill)
        for pattern in BANNED_WORDS:
            if re.search(pattern, content, re.IGNORECASE):
                print(f"  ⚠️  {skill}: contains banned word '{pattern}'")
                clean = False
    if clean:
        print("  ✅ All non-exempt skills free of forbidden buzzwords")
    return clean


def test_no_foreign_characters():
    print("\n🧪 Checking for stray CJK characters...")
    clean = True
    for skill in EXPECTED_SKILLS:
        for i, line in enumerate(read_skill(skill).splitlines(), 1):
            if re.search(r"[\u4e00-\u9fff]", line):
                print(f"  ⚠️  {skill}:{i} contains CJK characters")
                clean = False
    if clean:
        print("  ✅ No CJK characters found")
    return clean


def test_size_budget():
    print("\n🧪 Checking skill size budget...")
    warn = False
    hard_fail = False
    for skill in EXPECTED_SKILLS:
        lines = len(read_skill(skill).splitlines())
        if lines > 1000:
            print(f"  ❌ {skill}: {lines} lines (hard limit 1000) — split into references/")
            hard_fail = True
        elif lines > 400:
            print(f"  ⚠️  {skill}: {lines} lines — candidate for references/ split")
            warn = True
    if not hard_fail:
        print("  ✅ All skills within hard size limit" + (" (warnings above)" if warn else ""))
    return not hard_fail


def test_foundation_integration():
    print("\n🧪 Testing knowledge-graph foundation integration...")
    passed = True
    kg_content = read_skill("maxilun-knowledge-graph")
    for marker in ["Kontrak Fondasi", "Tangga Pencarian", "Symbol Query Grammar", "callsIn:"]:
        if marker not in kg_content:
            print(f"  ❌ maxilun-knowledge-graph: missing marker '{marker}'")
            passed = False
    if passed:
        print("  ✅ maxilun-knowledge-graph: foundation markers present")
    for consumer in ["maxilun", "maxilun-engineer"]:
        if "maxilun-knowledge-graph" in read_skill(consumer):
            print(f"  ✅ {consumer}: references maxilun-knowledge-graph")
        else:
            print(f"  ❌ {consumer}: does not reference maxilun-knowledge-graph")
            passed = False
    return passed


def test_referenced_paths():
    print("\n🧪 Verifying repository paths...")
    paths_to_verify = [
        ORCHESTRATOR / "references" / "engines.md",
        ORCHESTRATOR / "references" / "discovery.md",
        ORCHESTRATOR / "references" / "purity-catalog.md",
        ORCHESTRATOR / "references" / "code-hygiene.md",
        REPO_ROOT / "scripts" / "install.sh",
        REPO_ROOT / "scripts" / "install.ps1",
        REPO_ROOT / "scripts" / "uninstall.sh",
        REPO_ROOT / "scripts" / "uninstall.ps1",
        REPO_ROOT / "scripts" / "repomap.py",
        REPO_ROOT / "docs" / "INSTALL.md",
        REPO_ROOT / "docs" / "SKILLS.md",
        REPO_ROOT / "docs" / "ENGINES.md",
        REPO_ROOT / "docs" / "UNINSTALL.md",
        REPO_ROOT / "docs" / "EXAMPLES.md",
        REPO_ROOT / "docs" / "RELEASE.md",
        REPO_ROOT / "docs" / "decisions" / "README.md",
        SKILLS_DIR / "maxilun-motion" / "references" / "motion-components.md",
        SKILLS_DIR / "maxilun-knowledge-graph" / "LENS.md",
        SKILLS_DIR / "maxilun-knowledge-graph" / "graph-viewer" / "lens.html",
        REPO_ROOT / "README.md",
        REPO_ROOT / "README.id.md",
        REPO_ROOT / "LICENSE",
        REPO_ROOT / "package.json",
        REPO_ROOT / "skills.sh.json",
    ]
    all_ok = True
    for p in paths_to_verify:
        if not p.exists():
            print(f"  ❌ Missing path: {p.relative_to(REPO_ROOT)}")
            all_ok = False
        else:
            print(f"  ✅ {p.relative_to(REPO_ROOT)}")
    return all_ok


def test_kg_scanner_functional():
    print("\n🧪 Running functional Knowledge Graph Scanner test...")
    try:
        import importlib
        importlib.import_module("scanner.python_scanner")
        importlib.import_module("scanner.typescript_scanner")
        GraphBuilder = importlib.import_module("graph_builder").GraphBuilder

        with tempfile.TemporaryDirectory() as tmpdir:
            hidden_root = Path(tmpdir) / ".hidden_env" / "sample_project"
            hidden_root.mkdir(parents=True)

            (hidden_root / "b.py").write_text("def helper():\n    return 42\n", encoding="utf-8")
            (hidden_root / "a.py").write_text(
                "from .b import helper\n\n"
                "class Base:\n"
                "    def run(self):\n"
                "        return helper()\n\n"
                "def run_top():\n"
                "    return Base().run()\n",
                encoding="utf-8",
            )
            (hidden_root / "service.ts").write_text(
                "export function compute(x: number): number {\n"
                "    return x * 2;\n"
                "}\n"
                "export const handler = (y: number) => {\n"
                "    return compute(y);\n"
                "};\n",
                encoding="utf-8",
            )

            graph = GraphBuilder().scan_project(str(hidden_root))
            nodes = graph.get("nodes", [])
            edges = graph.get("edges", [])

            if len(nodes) == 0:
                print("  ❌ Scanner returned 0 nodes for project in hidden parent directory")
                return False

            node_ids = {n["id"] for n in nodes}
            if "func:a.py:run" in node_ids and "func:a.py:Base.run" in node_ids:
                print("  ❌ Python method was double-counted as top-level function")
                return False

            import_edges = [e for e in edges if e.get("type") == "IMPORTS"]
            if not any(e.get("target") == "file:b.py" for e in import_edges):
                print("  ❌ Relative import 'from .b import helper' failed to resolve")
                return False

            self_calls = [
                e for e in edges
                if e.get("type") == "CALLS"
                and e.get("source") == "func:service.ts:compute"
                and "compute" in e.get("target")
            ]
            if self_calls:
                print("  ❌ TS function definition matched as call to itself")
                return False

            print(f"  ✅ Functional KG Scanner passed ({len(nodes)} nodes, {len(edges)} edges)")
            return True

    except Exception as e:
        print(f"  ❌ KG functional test error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_cross_references():
    print("\n🧪 Checking cross-references between skills...")
    checks = [
        ("maxilun-engineer", ["maxilun-data", "maxilun-frontend"]),
        ("maxilun-craft", ["maxilun-motion"]),
        ("maxilun-architect", ["maxilun-data"]),
        ("maxilun-sentinel", ["maxilun-deploy"]),
        ("maxilun-data", ["maxilun-architect"]),
        ("maxilun-docsmith", ["maxilun-engineer", "maxilun-architect"]),
        ("maxilun-motion", ["maxilun-cinecode"]),
        ("maxilun-cinecode", ["maxilun-motion"]),
        ("maxilun", ["maxilun-scaffold"]),
    ]
    passed = True
    for skill, targets in checks:
        content = read_skill(skill)
        if any(t in content for t in targets):
            print(f"  ✅ {skill} references {' or '.join(targets)}")
        else:
            print(f"  ❌ {skill} does not reference {' or '.join(targets)}")
            passed = False
    return passed


def main():
    print("🌑 Starting Maxilun 18-Skill Test Suite\n" + "=" * 48)
    results = [
        test_skills_exist(),
        test_frontmatter(),
        test_core_rules_block(),
        test_references_present(),
        test_reference_paths_resolve(),
        test_no_external_or_legacy_refs(),
        test_section_numbering(),
        test_purity_self_check(),
        test_no_foreign_characters(),
        test_size_budget(),
        test_foundation_integration(),
        test_referenced_paths(),
        test_kg_scanner_functional(),
        test_cross_references(),
    ]

    print("\n" + "=" * 48)
    if all(results):
        print("🎉 ALL VALIDATION SUITES PASSED. Maxilun ecosystem verified.\n")
        sys.exit(0)
    print("❌ SOME TESTS FAILED. Inspect errors above.\n")
    sys.exit(1)


if __name__ == "__main__":
    main()
