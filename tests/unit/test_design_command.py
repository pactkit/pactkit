"""Tests for STORY-035: /project-design command — Product Designer for Greenfield Projects."""


def _prompts():
    import importlib

    import pactkit.prompts as p
    importlib.reload(p)
    return p


# ---------------------------------------------------------------------------
# Scenario 1: Command Registered in COMMANDS_CONTENT
# ---------------------------------------------------------------------------
class TestDesignCommandRegistered:
    """S1: project-design.md is registered in COMMANDS_CONTENT."""

    def test_key_exists(self):
        p = _prompts()
        assert 'project-design.md' in p.COMMANDS_CONTENT

    def test_contains_command_header(self):
        p = _prompts()
        assert '# Command: Design' in p.COMMANDS_CONTENT['project-design.md']

    def test_has_frontmatter(self):
        p = _prompts()
        assert p.COMMANDS_CONTENT['project-design.md'].strip().startswith('---')


# ---------------------------------------------------------------------------
# Scenario 2: Agent Registered in AGENTS_EXPERT
# ---------------------------------------------------------------------------
class TestProductDesignerAgent:
    """S2: product-designer agent exists with required fields."""

    def test_agent_exists(self):
        p = _prompts()
        assert 'product-designer' in p.AGENTS_EXPERT

    def test_has_desc(self):
        p = _prompts()
        agent = p.AGENTS_EXPERT['product-designer']
        assert 'desc' in agent
        assert len(agent['desc']) > 10

    def test_has_tools(self):
        p = _prompts()
        agent = p.AGENTS_EXPERT['product-designer']
        assert 'tools' in agent
        assert 'Read' in agent['tools']
        assert 'Write' in agent['tools']

    def test_has_skills(self):
        p = _prompts()
        agent = p.AGENTS_EXPERT['product-designer']
        assert 'skills' in agent
        assert 'pactkit-visualize' in agent['skills']
        assert 'pactkit-scaffold' in agent['skills']
        assert 'pactkit-board' in agent['skills']

    def test_has_prompt(self):
        p = _prompts()
        agent = p.AGENTS_EXPERT['product-designer']
        assert 'prompt' in agent
        assert len(agent['prompt']) > 100

    def test_prompt_has_four_sections(self):
        p = _prompts()
        prompt = p.AGENTS_EXPERT['product-designer']['prompt']
        assert '## Goal' in prompt
        assert '## Boundaries' in prompt
        assert '## Output' in prompt
        assert '## Protocol' in prompt

    def test_boundary_no_implementation_code(self):
        p = _prompts()
        prompt = p.AGENTS_EXPERT['product-designer']['prompt']
        assert 'implementation code' in prompt.lower() or 'not write' in prompt.lower()


# ---------------------------------------------------------------------------
# Scenario 3: PRD Template Function Exists
# ---------------------------------------------------------------------------
class TestCreatePrdFunction:
    """S3: create_prd() exists in scaffold.py and generates template."""

    def test_function_exists(self):
        from pactkit.skills import scaffold
        assert hasattr(scaffold, 'create_prd')
        assert callable(scaffold.create_prd)

    def test_returns_success_message(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / 'docs' / 'product').mkdir(parents=True)
        from pactkit.skills import scaffold
        result = scaffold.create_prd('TestProduct')
        assert '✅' in result or 'PRD' in result

    def test_creates_prd_file(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        from pactkit.skills import scaffold
        scaffold.create_prd('TestProduct')
        prd_file = tmp_path / 'docs' / 'product' / 'prd.md'
        assert prd_file.exists()
        content = prd_file.read_text()
        assert 'TestProduct' in content


# ---------------------------------------------------------------------------
# Scenario 4: Command Contains All Phases
# ---------------------------------------------------------------------------
class TestDesignCommandPhases:
    """S4: project-design.md contains Phase 0 through Phase 5."""

    def test_all_phases_present(self):
        p = _prompts()
        content = p.COMMANDS_CONTENT['project-design.md']
        for phase in ['Phase 0', 'Phase 1', 'Phase 2', 'Phase 3', 'Phase 4', 'Phase 5']:
            assert phase in content, f"Missing {phase}"


# ---------------------------------------------------------------------------
# Scenario 5: PRD Template Contains Required Sections
# ---------------------------------------------------------------------------
class TestPrdTemplateSections:
    """S5: PRD template has all required section headings."""

    def test_all_sections_present(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        from pactkit.skills import scaffold
        scaffold.create_prd('TestProduct')
        content = (tmp_path / 'docs' / 'product' / 'prd.md').read_text()
        required = [
            'Product Overview',
            'User Personas',
            'Feature Breakdown',
            'Architecture Design',
            'Page/Screen Design',
            'API Design',
            'Non-Functional Requirements',
            'Success Metrics',
            'MVP Roadmap',
        ]
        for section in required:
            assert section in content, f"Missing section: {section}"


# ---------------------------------------------------------------------------
# Scenario 6: Routing Table Updated
# ---------------------------------------------------------------------------
class TestRoutingTableUpdated:
    """S6: RULES_MODULES['routing'] includes /project-design."""

    def test_design_in_routing(self):
        p = _prompts()
        routing = p.RULES_MODULES['routing']
        assert 'project-design' in routing

    def test_role_is_product_designer(self):
        p = _prompts()
        routing = p.RULES_MODULES['routing']
        assert 'Product Designer' in routing


# ---------------------------------------------------------------------------
# Scenario 7: File Atlas Updated
# ---------------------------------------------------------------------------
class TestFileAtlasUpdated:
    """S7: RULES_MODULES['atlas'] includes docs/product/prd.md."""

    def test_prd_in_atlas(self):
        p = _prompts()
        atlas = p.RULES_MODULES['atlas']
        assert 'prd.md' in atlas

    def test_prd_purpose_described(self):
        p = _prompts()
        atlas = p.RULES_MODULES['atlas']
        assert 'Product Requirements Document' in atlas or 'PRD' in atlas


# ---------------------------------------------------------------------------
# Scenario 8: Backward Compatibility
# ---------------------------------------------------------------------------
class TestBackwardCompatibility:
    """S8: All previously existing commands, agents, and rules are intact."""

    def test_existing_commands_present(self):
        p = _prompts()
        expected = [
            'project-plan.md', 'project-act.md', 'project-check.md',
            'project-done.md', 'project-init.md',
            'project-sprint.md', 'project-hotfix.md', 'project-design.md',
        ]
        for cmd in expected:
            assert cmd in p.COMMANDS_CONTENT, f"Missing command: {cmd}"

    def test_existing_agents_present(self):
        p = _prompts()
        expected = [
            'system-architect', 'senior-developer', 'qa-engineer',
            'repo-maintainer', 'system-medic', 'security-auditor',
            'visual-architect', 'code-explorer',
        ]
        for agent in expected:
            assert agent in p.AGENTS_EXPERT, f"Missing agent: {agent}"

    def test_existing_rules_present(self):
        p = _prompts()
        expected = ['core', 'hierarchy', 'atlas', 'routing', 'workflow']
        for rule in expected:
            assert rule in p.RULES_MODULES, f"Missing rule module: {rule}"


# ---------------------------------------------------------------------------
# Scenario 9: PRD Template Includes Priority Scoring
# ---------------------------------------------------------------------------
class TestPrdPriorityScoring:
    """S9: Feature Breakdown contains Impact/Effort/Priority table."""

    def test_priority_table_present(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        from pactkit.skills import scaffold
        scaffold.create_prd('TestProduct')
        content = (tmp_path / 'docs' / 'product' / 'prd.md').read_text()
        assert 'Impact' in content
        assert 'Effort' in content
        assert 'Priority' in content


# ---------------------------------------------------------------------------
# Scenario 10: PRD Template Includes Jobs-to-be-Done
# ---------------------------------------------------------------------------
class TestPrdJobsToBeDone:
    """S10: User Personas section contains JTBD fields."""

    def test_jtbd_fields_present(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        from pactkit.skills import scaffold
        scaffold.create_prd('TestProduct')
        content = (tmp_path / 'docs' / 'product' / 'prd.md').read_text()
        assert 'Functional' in content
        assert 'Emotional' in content
        assert 'Social' in content


# ---------------------------------------------------------------------------
# Scenario 11: PRD Template Includes Three-Horizon Roadmap
# ---------------------------------------------------------------------------
class TestPrdThreeHorizonRoadmap:
    """S11: MVP Roadmap contains Now/Next/Later horizons."""

    def test_horizons_present(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        from pactkit.skills import scaffold
        scaffold.create_prd('TestProduct')
        content = (tmp_path / 'docs' / 'product' / 'prd.md').read_text()
        assert 'Now' in content
        assert 'Next' in content
        assert 'Later' in content


# ---------------------------------------------------------------------------
# Extra: DESIGN_PROMPT exportable from __init__
# ---------------------------------------------------------------------------
class TestDesignPromptExported:
    """DESIGN_PROMPT is importable from pactkit.prompts."""

    def test_importable(self):
        p = _prompts()
        assert hasattr(p, 'DESIGN_PROMPT')
        assert isinstance(p.DESIGN_PROMPT, str)
        assert len(p.DESIGN_PROMPT) > 200
