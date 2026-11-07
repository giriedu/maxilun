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
    "maxilun-desktop",
    "maxilun-mobile",
    "maxilun-iot",
    "maxilun-network",
    "maxilun-ai",
]
EXPECTED_AGENTS = [
    "maxilun-orchestrator",
    "maxilun-scout",
    "maxilun-architect",
    "maxilun-maker",
    "maxilun-studio",
    "maxilun-verifier",
    "maxilun-coder-frontend",
    "maxilun-coder-backend",
    "maxilun-coder-mobile",
    "maxilun-coder-systems",
    "maxilun-ui-designer",
    "maxilun-ui-motion",
    "maxilun-ui-reviewer",
]
REQUIRED_REFERENCES = [
    "engines.md",
    "discovery.md",
    "purity-catalog.md",
    "code-hygiene.md",
    "surgical-discipline.md",
]

REQUIRED_PUBLIC_DOCS = ["SKILL-CONTRACTS.md", "ROUTING-MATRIX.md", "PURITY-GATE.md", "BENCHMARKS.md"]

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

FORBIDDEN_EXTERNAL = ["antislop", "anti-slop", "frontend-design", "brainstorming", "superpowers", "impeccable", "pbakaus", "bang-motion", "archify", "ui-ux-pro-max"]
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
    print(f"🧪 Checking {len(EXPECTED_SKILLS)} skills existence...")
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
        if "license: Free-to-Use" not in fm:
            print(f"  ❌ {skill}: License is not Free-to-Use")
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
    for md_file in SKILLS_DIR.rglob("*.md"):
        if "design-md" in md_file.parts:
            continue
        content = md_file.read_text(encoding="utf-8").lower()
        rel_name = str(md_file.relative_to(REPO_ROOT))
        for token in FORBIDDEN_EXTERNAL:
            if token in content:
                print(f"  ❌ {rel_name}: references external skill '{token}'")
                passed = False
        for token in FORBIDDEN_LAYOUT:
            if token in content:
                print(f"  ❌ {rel_name}: references removed layout '{token}'")
                passed = False
    if passed:
        print("  ✅ No external-skill or legacy rules references")
    return passed


def test_no_pipe_to_interpreter():
    print("\n🧪 Checking skills for pipe-to-interpreter patterns (skills.sh security audit)...")
    passed = True
    pipe_pattern = re.compile(r"\b(?:curl|wget)\b[^\n]*\|\s*(?:sh|bash|zsh|python|python3|node|perl|ruby|pwsh|powershell)\b", re.IGNORECASE)
    for md_file in SKILLS_DIR.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        m = pipe_pattern.search(content)
        if m:
            print(f"  ❌ {md_file.relative_to(REPO_ROOT)}: pipe-to-interpreter pattern '{m.group(0)}'")
            passed = False
    if passed:
        print("  ✅ Zero pipe-to-interpreter patterns across all skills and references")
    return passed


def test_section_numbering():
    print("\n🧪 Validating section numbering and spine order...")
    passed = True
    for skill in EXPECTED_SKILLS:
        lines = read_skill(skill).splitlines()
        fence = False
        nums = []
        h1_line = None
        contract_line = None
        last_num_line = None
        related_line = None
        for idx, line in enumerate(lines, 1):
            if line.strip().startswith("```"):
                fence = not fence
                continue
            if fence:
                continue
            if h1_line is None and re.match(r"^# \S", line):
                h1_line = idx
            if contract_line is None and line.strip() in ("## Skill Contract", "## Distribution Contract"):
                contract_line = idx
            if line.strip() == "## Related Skills":
                related_line = idx
            m = re.match(r"^## (\d+)\. ", line)
            if m:
                nums.append(int(m.group(1)))
                last_num_line = idx
        dupes = sorted({n for n in nums if nums.count(n) > 1})
        if dupes:
            print(f"  ❌ {skill}: duplicate section numbers {dupes}")
            passed = False
        elif nums and nums != list(range(1, len(nums) + 1)):
            print(f"  ❌ {skill}: non-sequential numbering {nums} (expected 1..{len(nums)})")
            passed = False
        if h1_line is None or (contract_line is not None and h1_line > contract_line):
            print(f"  ❌ {skill}: '# Title' must precede contract heading")
            passed = False
        if related_line is not None and last_num_line is not None and last_num_line > related_line:
            print(f"  ❌ {skill}: numbered section appears after '## Related Skills'")
            passed = False
    if passed:
        print("  ✅ Sequential 1..N section numbering and clean spine order")
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
    print("\n🧪 Checking skill size budget (<= 300 lines ceiling)...")
    warn = False
    hard_fail = False
    for skill in EXPECTED_SKILLS:
        lines = len(read_skill(skill).splitlines())
        if lines > 300:
            print(f"  ❌ {skill}: {lines} lines (hard limit 300) — move detail into references/")
            hard_fail = True
        elif lines > 260:
            print(f"  ⚠️  {skill}: {lines} lines — approaching 300-line ceiling")
            warn = True
    if not hard_fail:
        print(f"  ✅ All {len(EXPECTED_SKILLS)} skills strictly <= 300 lines" + (" (warnings above)" if warn else ""))
    return not hard_fail


def test_no_ceremony_or_self_check_gates():
    print("\n🧪 Checking skills for ceremonial HUD banners and self-checked gate theater...")
    forbidden_banners = [
        "🎯 [FOKUS]",
        "⚡ [TINDAKAN]",
        "🔒 DESIGN CONTEXT CHECK",
        "🔒 DELIVERY GATE",
        "📋 Parking Lot",
        "✅ [VERIFIKASI SUKSES]",
        "⚠️ [TEMUAN KEAMANAN]",
        "🌐 [KNOWLEDGE GRAPH]",
        "📋 [AUDIT SEO]",
        "🔍 [DIAGNOSIS]",
    ]
    passed = True
    for skill in EXPECTED_SKILLS:
        content = read_skill(skill)
        for banner in forbidden_banners:
            if banner in content:
                print(f"  ❌ {skill}: contains deprecated ceremonial banner '{banner}'")
                passed = False
        fence = False
        for idx, line in enumerate(content.splitlines(), 1):
            if line.strip().startswith("```"):
                fence = not fence
                continue
            if not fence and re.match(r"^\s*-\s*\[[ xX]\]\s+", line):
                print(f"  ❌ {skill}:{idx}: contains self-checked checkbox item '{line.strip()}'")
                passed = False
    if passed:
        print(f"  ✅ Zero ceremonial HUD banners or self-checked checkboxes across all {len(EXPECTED_SKILLS)} skills")
    return passed


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
        ORCHESTRATOR / "references" / "surgical-discipline.md",
        REPO_ROOT / "scripts" / "install.sh",
        REPO_ROOT / "scripts" / "install.ps1",
        REPO_ROOT / "scripts" / "uninstall.sh",
        REPO_ROOT / "scripts" / "uninstall.ps1",
        REPO_ROOT / "scripts" / "repomap.py",
        REPO_ROOT / "scripts" / "ui-purity-linter.py",
        REPO_ROOT / "docs" / "INSTALL.md",
        REPO_ROOT / "docs" / "SKILLS.md",
        REPO_ROOT / "docs" / "ENGINES.md",
        REPO_ROOT / "docs" / "UNINSTALL.md",
        REPO_ROOT / "docs" / "EXAMPLES.md",
        REPO_ROOT / "docs" / "RELEASE.md",
        REPO_ROOT / "docs" / "decisions" / "README.md",
        *[REPO_ROOT / "docs" / doc for doc in REQUIRED_PUBLIC_DOCS],
        SKILLS_DIR / "maxilun-craft" / "references" / "design-md" / "README.md",
        SKILLS_DIR / "maxilun-craft" / "references" / "design-md" / "index.md",
        SKILLS_DIR / "maxilun-craft" / "references" / "component-mobile-patterns.md",
        SKILLS_DIR / "maxilun-craft" / "references" / "interface-engineering.md",
        SKILLS_DIR / "maxilun-architect" / "references" / "index.md",
        SKILLS_DIR / "maxilun-architect" / "references" / "api-distributed-patterns.md",
        SKILLS_DIR / "maxilun-architect" / "references" / "migration-operations-playbook.md",
        SKILLS_DIR / "maxilun-docsmith" / "references" / "index.md",
        SKILLS_DIR / "maxilun-docsmith" / "references" / "prd-rfc-specs.md",
        SKILLS_DIR / "maxilun-docsmith" / "references" / "openapi-contracts.md",
        SKILLS_DIR / "maxilun-docsmith" / "references" / "runbooks-adr.md",
        SKILLS_DIR / "maxilun-docsmith" / "references" / "llms-txt-spec.md",
        SKILLS_DIR / "maxilun-scaffold" / "references" / "index.md",
        SKILLS_DIR / "maxilun-scaffold" / "references" / "doc-templates.md",
        SKILLS_DIR / "maxilun-scaffold" / "references" / "prd-archetypes.md",
        SKILLS_DIR / "maxilun-motion" / "references" / "index.md",
        SKILLS_DIR / "maxilun-motion" / "references" / "motion-components.md",
        SKILLS_DIR / "maxilun-motion" / "references" / "choreography-styles.md",
        SKILLS_DIR / "maxilun-motion" / "assets" / "starter-opener.html",
        SKILLS_DIR / "maxilun-motion" / "assets" / "starter-explainer.html",
        SKILLS_DIR / "maxilun-cinecode" / "scaffold" / "src" / "components" / "Effects.tsx",
        SKILLS_DIR / "maxilun-cinecode" / "scaffold" / "src" / "components" / "VideoClip.tsx",
        SKILLS_DIR / "maxilun-cinecode" / "scaffold" / "src" / "components" / "KineticTypography.tsx",
        SKILLS_DIR / "maxilun-cinecode" / "scaffold" / "src" / "components" / "MotionShapes.tsx",
        SKILLS_DIR / "maxilun-cinecode" / "scaffold" / "src" / "components" / "DataMotion.tsx",
        SKILLS_DIR / "maxilun-cinecode" / "references" / "index.md",
        SKILLS_DIR / "maxilun-cinecode" / "references" / "composition-api.md",
        SKILLS_DIR / "maxilun-cinecode" / "references" / "video-production-pipeline.md",
        SKILLS_DIR / "maxilun-cinecode" / "references" / "soundtrack-audio-production.md",
        SKILLS_DIR / "maxilun-content" / "references" / "index.md",
        SKILLS_DIR / "maxilun-content" / "references" / "cinematic-scriptwriting.md",
        SKILLS_DIR / "maxilun-knowledge-graph" / "LENS.md",
        SKILLS_DIR / "maxilun-knowledge-graph" / "graph-viewer" / "lens.html",
        REPO_ROOT / "assets" / "banner.jpg",
        REPO_ROOT / "assets" / "architecture-overview.svg",
        REPO_ROOT / "assets" / "raw-vs-maxilun-proof.svg",
        REPO_ROOT / "README.md",
        REPO_ROOT / "README.id.md",
        REPO_ROOT / "LICENSE",
        REPO_ROOT / "package.json",
        REPO_ROOT / "skills.sh.json",
        REPO_ROOT / "docs" / "HARNESS.md",
        REPO_ROOT / "harness" / "__init__.py",
        REPO_ROOT / "harness" / "cli.py",
        REPO_ROOT / "harness" / "purity_validator.py",
        REPO_ROOT / "harness" / "router.py",
        REPO_ROOT / "harness" / "benchmarks.py",
        REPO_ROOT / "harness" / "ast_inspector.py",
        REPO_ROOT / "harness" / "sandbox_runner.py",
        REPO_ROOT / "harness" / "live_evaluator.py",
        REPO_ROOT / "harness" / "hook_installer.py",
        REPO_ROOT / "harness" / "triage_evaluator.py",
        REPO_ROOT / "harness" / "dashboard.py",
        REPO_ROOT / "harness" / "engine" / "__init__.py",
        REPO_ROOT / "harness" / "engine" / "skills_loader.py",
        REPO_ROOT / "harness" / "engine" / "context.py",
        REPO_ROOT / "harness" / "engine" / "provider.py",
        REPO_ROOT / "harness" / "engine" / "middleware.py",
        REPO_ROOT / "harness" / "engine" / "agent_loop.py",
        REPO_ROOT / "harness" / "tools" / "__init__.py",
        REPO_ROOT / "harness" / "tools" / "registry.py",
        REPO_ROOT / "harness" / "tools" / "fs_tools.py",
        REPO_ROOT / "harness" / "tools" / "bash_tool.py",
        REPO_ROOT / "harness" / "tools" / "kg_tool.py",
    ]
    all_ok = True
    for p in paths_to_verify:
        if not p.exists():
            print(f"  ❌ Missing path: {p.relative_to(REPO_ROOT)}")
            all_ok = False
        else:
            print(f"  ✅ {p.relative_to(REPO_ROOT)}")
    return all_ok


def test_skill_contracts():
    print("\n🧪 Checking standalone skill contracts and routing boundaries...")
    required_markers = ["**Owns**:", "**Does not own**:", "**Inputs**:", "**Outputs**:", "**Handoff**:"]
    passed = True
    for skill in EXPECTED_SKILLS:
        content = read_skill(skill)
        contract_heading = "## Skill Contract" if skill != "maxilun" else "## Distribution Contract"
        missing = [marker for marker in [contract_heading, *required_markers] if marker not in content]
        if missing:
            print(f"  ❌ {skill}: missing contract markers {', '.join(missing)}")
            passed = False
    craft_content = read_skill("maxilun-craft")
    if "references/design-md/README.md" not in craft_content or "references/design-md/index.md" not in craft_content:
        print("  ❌ maxilun-craft: design reference instructions are not bundled")
        passed = False
    if passed:
        print("  ✅ All skills expose standalone ownership contracts")
    return passed


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
            (hidden_root / "repo.go").write_text(
                "package main\n\n"
                "type UserRepository interface {\n"
                "    FindByID(id string) (*User, error)\n"
                "}\n\n"
                "type UserRepo struct{}\n\n"
                "func (r *UserRepo) FindByID(id string) (*User, error) {\n"
                "    return nil, nil\n"
                "}\n",
                encoding="utf-8",
            )
            (hidden_root / "service.cpp").write_text(
                "class Service {\n"
                "public:\n"
                "    void run();\n"
                "};\n\n"
                "void Service::run() {\n"
                "}\n",
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
            if "func:repo.go:FindByID" not in node_ids:
                print("  ❌ Go struct method receiver 'FindByID' failed to extract")
                return False

            if "class:repo.go:UserRepository" not in node_ids or "class:repo.go:UserRepo" not in node_ids:
                print("  ❌ Go interface or struct failed to extract")
                return False

            if "func:service.cpp:run" not in node_ids or "class:service.cpp:Service" not in node_ids:
                print("  ❌ C++ class or scoped method failed to extract")
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
        ("maxilun-docsmith", ["maxilun-engineer", "maxilun-architect", "maxilun-craft"]),
        ("maxilun-scaffold", ["maxilun-craft", "maxilun-docsmith"]),
        ("maxilun-motion", ["maxilun-cinecode", "maxilun-craft"]),
        ("maxilun-cinecode", ["maxilun-motion", "maxilun-craft", "maxilun-content"]),
        ("maxilun-content", ["maxilun-cinecode", "maxilun-motion"]),
        ("maxilun", ["maxilun-scaffold"]),
        ("maxilun-desktop", ["maxilun-data", "maxilun-verify"]),
        ("maxilun-mobile", ["maxilun-sentinel", "maxilun-verify"]),
        ("maxilun-iot", ["maxilun-network", "maxilun-sentinel"]),
        ("maxilun-network", ["maxilun-iot", "maxilun-deploy"]),
        ("maxilun-ai", ["maxilun-data", "maxilun-engineer"]),
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


def test_harness_functional():
    print("\n🧪 Running functional Maxilun Harness test...")
    try:
        sys.path.insert(0, str(REPO_ROOT))
        from harness.purity_validator import PurityValidator
        from harness.router import MaxilunRouter
        from harness.benchmarks import BenchmarkRunner
        from harness.ast_inspector import ASTInspector
        from harness.sandbox_runner import SandboxRunner
        from harness.live_evaluator import LiveModelEvaluator
        from harness.triage_evaluator import TriageEvaluator

        # 1. Purity Validator Test
        val = PurityValidator()
        clean_res = val.validate_text("Clean production code without fluff.")
        if not clean_res.passed:
            print("  ❌ PurityValidator failed on clean input")
            return False

        dirty_res = val.validate_text("We delve into this game-changer solution.\n🎯 [FOKUS] Step 1")
        if dirty_res.passed or len(dirty_res.violations) < 2:
            print("  ❌ PurityValidator failed to catch buzzwords or HUD banner")
            return False

        # 2. Router Test
        router = MaxilunRouter()
        route1 = router.route("Bikin migrasi database drop column di postgres")
        if route1.primary_owner != "maxilun-data" or route1.decision_type != 1:
            print("  ❌ MaxilunRouter failed on Type 1 migration routing")
            return False

        route2 = router.route("Fix typo pada header navbar")
        if route2.primary_owner != "maxilun-engineer" or route2.decision_type != 2:
            print("  ❌ MaxilunRouter failed on Type 2 bugfix routing")
            return False

        route_pb = router.route("Bikin aplikasi PowerBuilder dengan DataWindow tabular")
        if route_pb.primary_owner != "maxilun-desktop":
            print(f"  ❌ MaxilunRouter failed on PowerBuilder desktop routing: got {route_pb.primary_owner}")
            return False

        route_mob = router.route("Buat aplikasi Android dengan Kotlin Jetpack Compose")
        if route_mob.primary_owner != "maxilun-mobile":
            print(f"  ❌ MaxilunRouter failed on Android mobile routing: got {route_mob.primary_owner}")
            return False

        route_iot = router.route("Setup firmware ESP32 sensor suhu MQTT")
        if route_iot.primary_owner != "maxilun-iot":
            print(f"  ❌ MaxilunRouter failed on ESP32 IoT routing: got {route_iot.primary_owner}")
            return False

        route_net = router.route("Konfigurasi router MikroTik RouterOS firewall filter")
        if route_net.primary_owner != "maxilun-network":
            print(f"  ❌ MaxilunRouter failed on MikroTik network routing: got {route_net.primary_owner}")
            return False
        route_ai = router.route("Setup hybrid search RAG pipeline dengan embeddings")
        if route_ai.primary_owner != "maxilun-ai":
            print(f"  ❌ MaxilunRouter failed on AI RAG routing: got {route_ai.primary_owner}")
            return False


        # 3. Benchmark Runner Test
        runner = BenchmarkRunner()
        report = runner.run_all()
        if report.total_benchmarks < 5 or report.overall_improvement <= 0:
            print("  ❌ BenchmarkRunner failed to produce positive score delta")
            return False

        # 4. AST Inspector Test
        ast_insp = ASTInspector()
        bad_py = "def query(db, uid):\n    sql = f'SELECT * FROM users WHERE id = {uid}'\n    db.execute(sql)\n"
        ast_res = ast_insp.inspect_python(bad_py)
        if ast_res.passed or not any(f.rule_id == "SEC-003" for f in ast_res.findings):
            print("  ❌ ASTInspector failed to catch Python f-string SQL injection")
            return False

        # 5. Sandbox Runner Test
        sb_sql = SandboxRunner.verify_sql_migration("CREATE TABLE t (id INTEGER PRIMARY KEY);")
        if not sb_sql.passed:
            print(f"  ❌ SandboxRunner failed on valid SQLite DDL: {sb_sql.error}")
            return False

        # 6. Triage Evaluator Test
        te = TriageEvaluator()
        t_res = te.evaluate_response("Fix typo pada navbar", "Bisa jelaskan lebih detail typo-nya di mana?")
        if t_res.passed or not any("ANTI_INTERROGATION" in v for v in t_res.violations):
            print("  ❌ TriageEvaluator failed to catch anti-interrogation violation on Type 2 task")
            return False

        # 7. Live Model Evaluator (Mock fallback)
        live_eval = LiveModelEvaluator()
        live_rep = live_eval.run_evaluation()
        if live_rep.total_scenarios < 3 or live_rep.overall_delta <= 0:
            print("  ❌ LiveModelEvaluator failed to produce valid comparative report")
            return False

        # 8. Autonomous Agent Loop Test
        from harness.engine.agent_loop import MaxilunAgentLoop
        from harness.engine.provider import UniversalProvider
        mock_prov = UniversalProvider(mock_mode=True)
        agent = MaxilunAgentLoop(provider=mock_prov, max_turns=3, verbose=False)
        ctx = agent.run_task("Tolong baca package.json")
        if len(ctx.messages) < 2 or not ctx.active_skill:
            print("  ❌ MaxilunAgentLoop failed to execute autonomous task")
            return False

        print(f"  ✅ Complete Maxilun Harness verification passed (Purity, Router, Benchmarks, AST, Sandbox, Triage, LiveEval, AgentLoop)")
        return True
    except Exception as e:
        print(f"  ❌ Maxilun Harness test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ui_purity_linter():
    print("\n🧪 Running functional UI Purity Linter test (45 AI Design Tells)...")
    linter_path = REPO_ROOT / "scripts" / "ui-purity-linter.py"
    if not linter_path.exists():
        print("  ❌ scripts/ui-purity-linter.py does not exist")
        return False
    import importlib.util
    spec = importlib.util.spec_from_file_location("ui_linter", str(linter_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    success = mod.run_self_test()
    if not success:
        print("  ❌ ui-purity-linter self-test failed")
        return False
    print("  ✅ UI Purity Linter verified functional (45 tells detected deterministically)")
    return True
def test_agents_validity():
    print(f"\n🧪 Checking {len(EXPECTED_AGENTS)} autonomous macro-agents validity & tool security invariants...")
    agents_dir = REPO_ROOT / "agents"
    if not agents_dir.exists():
        print("  ❌ agents/ directory missing")
        return False

    passed = True
    for agent in EXPECTED_AGENTS:
        agent_file = agents_dir / f"{agent}.md"
        if not agent_file.exists():
            print(f"  ❌ Missing agent file: {agent_file}")
            passed = False
            continue

        content = agent_file.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        if not fm:
            print(f"  ❌ {agent}: Missing YAML frontmatter")
            passed = False
            continue

        name_match = re.search(r"^name:\s*([^\s]+)", fm, re.MULTILINE)
        if not name_match or name_match.group(1).strip() != agent:
            print(f"  ❌ {agent}: 'name' mismatch in frontmatter")
            passed = False

        if "tools:" not in fm:
            print(f"  ❌ {agent}: Missing 'tools:' whitelist")
            passed = False

        # Invariant 1: maxilun-scout MUST be strictly read-only
        if agent == "maxilun-scout":
            if any(t in fm for t in ["Write", "Edit"]):
                print(f"  ❌ {agent}: Security invariant broken! Scout MUST be strictly read-only.")
                passed = False

        # Invariant 2: maxilun-verifier MUST NOT modify code
        if agent == "maxilun-verifier":
            if any(t in fm for t in ["Write", "Edit"]):
                print(f"  ❌ {agent}: Security invariant broken! Verifier MUST NOT have code modification tools.")
                passed = False

        # Invariant 3: maxilun-ui-reviewer MUST NOT modify code (objective evaluation)
        if agent == "maxilun-ui-reviewer":
            if any(t in fm for t in ["Write", "Edit"]):
                print(f"  ❌ {agent}: Security invariant broken! UI Reviewer MUST NOT have code modification tools.")
                passed = False
        lines = len(content.splitlines())
        if lines > 200:
            print(f"  ❌ {agent}: Line count exceeds budget ({lines} > 200 lines)")
            passed = False

        print(f"  ✅ {agent}: Verified valid frontmatter & security invariants ({lines} lines)")

    return passed


def main():
    print(f"🌑 Starting Maxilun {len(EXPECTED_SKILLS)}-Skill Test Suite\n" + "=" * 48)
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
        test_skill_contracts(),
        test_kg_scanner_functional(),
        test_cross_references(),
        test_no_pipe_to_interpreter(),
        test_no_ceremony_or_self_check_gates(),
        test_harness_functional(),
        test_ui_purity_linter(),
        test_agents_validity(),
    ]

    print("\n" + "=" * 48)
    if all(results):
        print("🎉 ALL VALIDATION SUITES PASSED. Maxilun ecosystem verified.\n")
        sys.exit(0)
    print("❌ SOME TESTS FAILED. Inspect errors above.\n")
    sys.exit(1)


if __name__ == "__main__":
    main()
