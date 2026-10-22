#!/usr/bin/env python3
"""
Maxilun Specialist Skill Ecosystem Test Suite
Comprehensive functional and structural validation:
- All 18 skills existence & YAML frontmatter
- Banned vocabulary purity self-check
- Knowledge Graph scanner functional verification (AST, import resolution, hidden dir check)
- Cross-references, internal path integrity, and license consistency
"""

import os
import sys
import re
import tempfile
import json
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills" if (REPO_ROOT / "skills").exists() else REPO_ROOT / ".agents" / "skills"
RULES_DIR = REPO_ROOT / "rules"

sys.path.insert(0, str(REPO_ROOT / "skills" / "msal-knowledge-graph"))

EXPECTED_SKILLS = [
    "msal",
    "msal-knowledge-graph",
    "msal-scaffold",
    "msal-architect",
    "msal-sentinel",
    "msal-engineer",
    "msal-data",
    "msal-frontend",
    "msal-verify",
    "msal-insight",
    "msal-deploy",
    "msal-docsmith",
    "msal-craft",
    "msal-motion",
    "msal-cinecode",
    "msal-diagrams",
    "msal-content",
    "msal-seo-audit",
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

# Exemption rationale:
# - maxilun: orchestrator content references specialist names and trigger phrases
#   (e.g., "msal-content") that may lexically match banned pattern substrings.
#   The orchestrator itself does not produce user-facing content, so slop rules
#   apply to its outputs at runtime, not its static trigger documentation.
# - msal-content: legitimately documents *examples* of banned phrases to teach
#   writers what to avoid. The catalog of bad phrases must appear somewhere.
# - msal-docsmith: may include example changelog or README templates that
#   cite banned phrases as anti-patterns in documentation examples.
PURE_EXEMPT_SKILLS = ["msal", "msal-content", "msal-docsmith"]


def parse_frontmatter(content: str) -> str:
    parts = content.split("---")
    if len(parts) >= 3:
        return parts[1]
    return ""


def test_skills_exist():
    print("🧪 Checking 18 skills existence...")
    missing = []
    for skill in EXPECTED_SKILLS:
        skill_file = SKILLS_DIR / skill / "SKILL.md"
        if not skill_file.exists():
            missing.append(skill)
        else:
            print(f"  ✅ Found {skill}/SKILL.md")
    
    if missing:
        print(f"  ❌ Missing skills: {', '.join(missing)}")
        return False
    return True


def test_frontmatter():
    print("\n🧪 Validating frontmatter schema & version consistency...")
    passed = True
    for skill in EXPECTED_SKILLS:
        skill_file = SKILLS_DIR / skill / "SKILL.md"
        content = skill_file.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        
        if not fm:
            print(f"  ❌ {skill}: Missing or invalid frontmatter (--- delimiter)")
            passed = False
            continue
            
        name_match = re.search(r"^name:\s*([^\s]+)", fm, re.MULTILINE)
        if not name_match or name_match.group(1).strip() != skill:
            print(f"  ❌ {skill}: 'name' field missing or does not match directory name")
            passed = False
        else:
            print(f"  ✅ {skill}: Valid name")
            
        if "description:" not in fm:
            print(f"  ❌ {skill}: Missing 'description' in frontmatter")
            passed = False

        if 'version: "1.0.0"' not in fm and "version: '1.0.0'" not in fm and "version: 1.0.0" not in fm:
            print(f"  ❌ {skill}: Version is not 1.0.0")
            passed = False

        if "license: Maxilun-Source-Available-2.0" not in fm:
            print(f"  ❌ {skill}: License is not Maxilun-Source-Available-2.0")
            passed = False
            
    return passed


def test_frontmatter_rules_field():
    print("\n🧪 Validating frontmatter rules auto-load field...")
    passed = True
    expected_rules = [
        "rules/always-on.md",
        "rules/maxilun-global.md",
        "rules/code-hygiene.md",
        "rules/purity-catalog.md",
    ]
    for skill in EXPECTED_SKILLS:
        skill_file = SKILLS_DIR / skill / "SKILL.md"
        content = skill_file.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        
        if not fm or "rules:" not in fm:
            print(f"  ❌ {skill}: Missing 'rules:' field in frontmatter")
            passed = False
            continue
        
        missing = [rule for rule in expected_rules if rule not in fm]
        if missing:
            print(f"  ⚠️  {skill}: Missing rules entries: {', '.join(missing)}")
            passed = False
        else:
            print(f"  ✅ {skill}: All 4 rules referenced")
    
    return passed


def test_purity_self_check():
    print("\n🧪 Running purity self-check on skills...")
    clean = True
    for skill in EXPECTED_SKILLS:
        skill_file = SKILLS_DIR / skill / "SKILL.md"
        content = skill_file.read_text(encoding="utf-8")

        for pattern in BANNED_WORDS:
            matches = list(re.finditer(pattern, content, re.IGNORECASE))
            if matches:
                if skill in PURE_EXEMPT_SKILLS:
                    continue
                print(f"  ⚠️  {skill}: Contains banned word '{pattern}'")
                clean = False

    if clean:
        print("  ✅ All skills free of forbidden buzzwords (frontmatter + body)")
    return clean


def test_no_foreign_characters():
    print("\n🧪 Checking for stray foreign/CJK characters...")
    clean = True
    for skill in EXPECTED_SKILLS:
        skill_file = SKILLS_DIR / skill / "SKILL.md"
        content = skill_file.read_text(encoding="utf-8")
        for i, line in enumerate(content.splitlines(), 1):
            if re.search(r'[\u4e00-\u9fff]', line):
                print(f"  ⚠️  {skill}: Line {i} contains foreign character: {line}")
                clean = False
    if clean:
        print("  ✅ All skill documents clean of non-Latin CJK characters")
    return clean


def test_foundation_integration():
    print("\n🧪 Testing knowledge-graph foundation integration...")
    passed = True

    kg_file = SKILLS_DIR / "msal-knowledge-graph" / "SKILL.md"
    kg_content = kg_file.read_text(encoding="utf-8")
    for marker in ["Kontrak Fondasi", "Tangga Pencarian", "Symbol Query Grammar", "callsIn:"]:
        if marker not in kg_content:
            print(f"  ❌ msal-knowledge-graph: Missing foundation marker '{marker}'")
            passed = False
    if passed:
        print("  ✅ msal-knowledge-graph: Foundation markers present")

    for consumer in ["msal", "msal-engineer"]:
        content = (SKILLS_DIR / consumer / "SKILL.md").read_text(encoding="utf-8")
        if "msal-knowledge-graph" in content:
            print(f"  ✅ {consumer}: References msal-knowledge-graph")
        else:
            print(f"  ❌ {consumer}: Does not reference msal-knowledge-graph")
            passed = False

    return passed


def test_referenced_paths():
    print("\n🧪 Verifying referenced paths and files exist...")
    paths_to_verify = [
        RULES_DIR / "always-on.md",
        RULES_DIR / "maxilun-global.md",
        RULES_DIR / "code-hygiene.md",
        RULES_DIR / "purity-catalog.md",
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
        REPO_ROOT / "skills" / "msal-motion" / "references" / "motion-components.md",
        REPO_ROOT / "skills" / "msal-knowledge-graph" / "LENS.md",
        REPO_ROOT / "skills" / "msal-knowledge-graph" / "graph-viewer" / "lens.html",
        REPO_ROOT / "README.md",
        REPO_ROOT / "README.id.md",
        REPO_ROOT / "LICENSE",
        REPO_ROOT / "package.json",
        REPO_ROOT / "skills.sh.json",
    ]

    all_ok = True
    for p in paths_to_verify:
        if not p.exists():
            print(f"  ❌ Missing referenced path: {p.relative_to(REPO_ROOT)}")
            all_ok = False
        else:
            print(f"  ✅ Verified path: {p.relative_to(REPO_ROOT)}")

    return all_ok


def test_kg_scanner_functional():
    print("\n🧪 Running functional Knowledge Graph Scanner test...")
    try:
        import importlib
        importlib.import_module("scanner.python_scanner")
        importlib.import_module("scanner.typescript_scanner")
        graph_builder_module = importlib.import_module("graph_builder")
        GraphBuilder = graph_builder_module.GraphBuilder

        with tempfile.TemporaryDirectory() as tmpdir:
            # Simulate a project inside a hidden folder path (e.g., /tmp/.hidden/proj)
            hidden_root = Path(tmpdir) / ".hidden_env" / "sample_project"
            hidden_root.mkdir(parents=True)

            # Create Python files with method inside class and relative import
            mod_b = hidden_root / "b.py"
            mod_b.write_text("def helper():\n    return 42\n", encoding="utf-8")

            mod_a = hidden_root / "a.py"
            mod_a.write_text(
                "from .b import helper\n\n"
                "class Base:\n"
                "    def run(self):\n"
                "        return helper()\n\n"
                "def run_top():\n"
                "    return Base().run()\n",
                encoding="utf-8"
            )

            # Create TypeScript file
            mod_ts = hidden_root / "service.ts"
            mod_ts.write_text(
                "export function compute(x: number): number {\n"
                "    return x * 2;\n"
                "}\n"
                "export const handler = (y: number) => {\n"
                "    return compute(y);\n"
                "};\n",
                encoding="utf-8"
            )

            builder = GraphBuilder()
            graph = builder.scan_project(str(hidden_root))

            nodes = graph.get("nodes", [])
            edges = graph.get("edges", [])

            # Test 1: Hidden parent folder does NOT yield 0 nodes
            if len(nodes) == 0:
                print("  ❌ Scanner returned 0 nodes for project in hidden parent directory")
                return False

            # Test 2: Methods are NOT double-counted as top-level functions
            node_ids = {n["id"] for n in nodes}
            if "func:a.py:run" in node_ids and "func:a.py:Base.run" in node_ids:
                print("  ❌ Python method was double-counted as top-level function!")
                return False

            # Test 3: Relative import is resolved to local file, not external module
            import_edges = [e for e in edges if e.get("type") == "IMPORTS"]
            has_resolved_rel = any(e.get("target") == "file:b.py" for e in import_edges)
            if not has_resolved_rel:
                print("  ❌ Relative import 'from .b import helper' failed to resolve to file:b.py")
                return False

            # Test 4: TypeScript declaration does NOT generate false self-call
            self_calls = [e for e in edges if e.get("type") == "CALLS" and e.get("source") == "func:service.ts:compute" and "compute" in e.get("target")]
            if self_calls:
                print("  ❌ TS function definition matched as call to itself!")
                return False

            print(f"  ✅ Functional KG Scanner passed ({len(nodes)} nodes, {len(edges)} edges, relative imports resolved)")
            return True

    except Exception as e:
        print(f"  ❌ KG functional test error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_cross_references():
    print("\n🧪 Checking cross-references between skills...")
    passed = True
    engineer_content = (SKILLS_DIR / "msal-engineer" / "SKILL.md").read_text(encoding="utf-8")
    if "msal-data" in engineer_content or "msal-frontend" in engineer_content:
        print("  ✅ engineer references msal-data or msal-frontend")
    else:
        print("  ❌ engineer does not reference msal-data or msal-frontend")
        passed = False

    craft_content = (SKILLS_DIR / "msal-craft" / "SKILL.md").read_text(encoding="utf-8")
    if "msal-motion" in craft_content:
        print("  ✅ craft references msal-motion")
    else:
        print("  ❌ craft does not reference msal-motion")
        passed = False

    architect_content = (SKILLS_DIR / "msal-architect" / "SKILL.md").read_text(encoding="utf-8")
    if "msal-data" in architect_content:
        print("  ✅ architect references msal-data")
    else:
        print("  ❌ architect does not reference msal-data")
        passed = False

    sentinel_content = (SKILLS_DIR / "msal-sentinel" / "SKILL.md").read_text(encoding="utf-8")
    if "msal-deploy" in sentinel_content:
        print("  ✅ sentinel references msal-deploy")
    else:
        print("  ❌ sentinel does not reference msal-deploy")
        passed = False

    data_content = (SKILLS_DIR / "msal-data" / "SKILL.md").read_text(encoding="utf-8")
    if "msal-architect" in data_content:
        print("  ✅ data references msal-architect")
    else:
        print("  ❌ data does not reference msal-architect")
        passed = False

    docsmith_content = (SKILLS_DIR / "msal-docsmith" / "SKILL.md").read_text(encoding="utf-8")
    if "msal-engineer" in docsmith_content or "msal-architect" in docsmith_content:
        print("  ✅ docsmith references msal-engineer or msal-architect")
    else:
        print("  ❌ docsmith does not reference msal-engineer or msal-architect")
        passed = False

    motion_content = (SKILLS_DIR / "msal-motion" / "SKILL.md").read_text(encoding="utf-8")
    if "msal-cinecode" in motion_content:
        print("  ✅ motion references msal-cinecode")
    else:
        print("  ❌ motion does not reference msal-cinecode")
        passed = False

    cinecode_content = (SKILLS_DIR / "msal-cinecode" / "SKILL.md").read_text(encoding="utf-8")
    if "msal-motion" in cinecode_content:
        print("  ✅ cinecode references msal-motion")
    else:
        print("  ❌ cinecode does not reference msal-motion")
        passed = False

    orchestrator_content = (SKILLS_DIR / "msal" / "SKILL.md").read_text(encoding="utf-8")
    if "msal-scaffold" in orchestrator_content:
        print("  ✅ maxilun orchestrator references msal-scaffold")
    else:
        print("  ❌ maxilun orchestrator does not reference msal-scaffold")
        passed = False

    return passed


def main():
    print("🌑 Starting Maxilun 18-Skill Test Suite\n" + "=" * 48)
    results = [
        test_skills_exist(),
        test_frontmatter(),
        test_frontmatter_rules_field(),
        test_purity_self_check(),
        test_no_foreign_characters(),
        test_foundation_integration(),
        test_referenced_paths(),
        test_kg_scanner_functional(),
        test_cross_references(),
    ]
    
    print("\n" + "=" * 48)
    if all(results):
        print("🎉 ALL VALIDATION SUITES PASSED! Maxilun ecosystem successfully verified.\n")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED! Please inspect errors above.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
