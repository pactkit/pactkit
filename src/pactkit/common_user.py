"""
PactKit Common User Installer (Experience Mode)
Standalone, self-contained, zero external dependencies.
Generates a lightweight PDCA workflow for Claude Code.

Usage:
    pactkit init --mode common              # Install to ~/.claude/
    pactkit init --mode common -t /tmp/out  # Preview to custom dir
"""
import sys
import argparse
from pathlib import Path
import textwrap

# --- Configuration ---
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'

def print_success(msg): print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} {msg}")
def print_info(msg): print(f"{Colors.BLUE}[INFO]{Colors.ENDC} {msg}")
def print_warn(msg): print(f"{Colors.YELLOW}[WARN]{Colors.ENDC} {msg}")

def ensure_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip(), encoding="utf-8")
    print_success(f"Generated: {path}")

# --- Content Definitions ---

def get_common_user_config():
    """
    Experience Mode Configuration.
    Pure prompt injection only. No scripts, no tools, no cross-file references.
    """

    claude_md = textwrap.dedent("""\
    # Claude Code — Lightweight PDCA

    ## Core Protocol
    - **Language**: Mirror the user's input language.
    - **Tone**: Concise, professional, engineering-first.
    - **Git**: Use Conventional Commits (`feat`, `fix`, `docs`, `chore`).

    ## Workflow: PDCA
    This environment follows a lightweight **Plan → Act → Check → Done** cycle:

    | Step | Command | What it does |
    |------|---------|--------------|
    | Plan | `/plan` | Analyze the request, create a TODO list |
    | Act  | `/act`  | Implement the next pending task |
    | Check| `/check`| Review code quality and run tests |
    | Done | `/done` | Summarize work and prepare a git commit |

    ## Guidelines
    - Keep plans in a `TODO.md` file at the project root.
    - One task at a time: implement, then review, then commit.
    - Prefer editing existing files over creating new ones.
    """)

    cmd_plan = textwrap.dedent("""\
    ---
    description: "Analyze requirements and create a plan"
    ---

    # Command: Plan (Lite)
    - **Usage**: `/plan "Feature or bug description"`

    ## Your Role
    You are a Technical Lead. Analyze the user's request and create a structured plan.

    ## Steps
    1. Read the user's request carefully.
    2. If a `TODO.md` exists at the project root, read it and update it.
       If not, create a new `TODO.md`.
    3. Break down the requirement into clear, checkable steps:
       - Use `- [ ] Step description` format.
       - Each step should be small enough to implement in one pass.
    4. Identify which existing files will need changes.

    ## Rules
    - Do NOT write any code in this step — only plan.
    - Do NOT create new directories or files (except `TODO.md`).
    - Present the plan to the user for confirmation before proceeding.
    """)

    cmd_act = textwrap.dedent("""\
    ---
    description: "Implement the next task from the plan"
    ---

    # Command: Act (Lite)
    - **Usage**: `/act`

    ## Your Role
    You are a Developer. Execute the next pending task from the plan.

    ## Steps
    1. Read `TODO.md` to find the first unchecked item (`- [ ]`).
    2. Understand the relevant code context by reading the target files.
    3. Write the code to implement this single task.
    4. Mark the item as done: `- [x]` in `TODO.md`.

    ## Rules
    - Implement only ONE task per invocation.
    - Prefer editing existing files over creating new ones.
    - Stop after implementation — do not review or commit.
    """)

    cmd_check = textwrap.dedent("""\
    ---
    description: "Review code and run tests"
    ---

    # Command: Check (Lite)
    - **Usage**: `/check`

    ## Your Role
    You are a Code Reviewer. Verify the quality of recent changes.

    ## Steps
    1. Review the files modified since the last commit (`git diff`).
    2. Check for:
       - Logic errors or obvious bugs
       - Syntax issues
       - Deviations from the plan in `TODO.md`
    3. If tests exist in the project, run them.
    4. Report findings to the user.

    ## Rules
    - Do NOT fix issues yourself — only report them.
    - If tests fail, explain which tests failed and why.
    - If everything looks good, say so and suggest proceeding to `/done`.
    """)

    cmd_done = textwrap.dedent("""\
    ---
    description: "Summarize work and prepare a git commit"
    ---

    # Command: Done (Lite)
    - **Usage**: `/done`

    ## Your Role
    You are a Release Engineer. Wrap up the current work session.

    ## Steps
    1. Read `TODO.md` to summarize what was completed.
    2. Review `git diff` to confirm all changes are intentional.
    3. Generate a Conventional Commit message:
       - Format: `type(scope): description`
       - Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`
    4. Present the commit command to the user for confirmation.
    5. After the user confirms, execute the commit.
    6. Clean up completed items in `TODO.md` (remove or archive them).

    ## Rules
    - NEVER commit without user confirmation.
    - NEVER push to remote unless the user explicitly asks.
    """)

    return {
        "claude_md": claude_md,
        "commands": {
            "plan.md": cmd_plan,
            "act.md": cmd_act,
            "check.md": cmd_check,
            "done.md": cmd_done,
        }
    }


def main():
    parser = argparse.ArgumentParser(description="PactKit Common User Installer (Experience Mode)")
    parser.add_argument("-t", "--target", type=str, help="Specify target directory (default: ~/.claude)", default=None)
    args = parser.parse_args()

    if args.target:
        claude_root = Path(args.target).resolve()
        print_warn(f"Running in PREVIEW mode. Generating files to: {claude_root}")
    else:
        claude_root = Path.home() / ".claude"
        print_info("Running in INSTALL mode. Targeting: ~/.claude")

    config = get_common_user_config()

    # 1. Generate CLAUDE.md (inline PDCA, no cross-file references)
    ensure_file(claude_root / "CLAUDE.md", config["claude_md"])

    # 2. Generate Commands (4 lightweight PDCA commands)
    cmds_dir = claude_root / "commands"
    for filename, content in config["commands"].items():
        ensure_file(cmds_dir / filename, content)

    print_info("Common User Configuration Generated!")

    if args.target:
        print(f"""
    {Colors.YELLOW}Preview Generation Complete.{Colors.ENDC}
    Check the '{args.target}' directory to verify the structure.

    To install for real, run:
    {Colors.GREEN}pactkit init --mode common{Colors.ENDC}
        """)
    else:
        print(f"""
    {Colors.GREEN}Your Environment is ready! (Experience Mode){Colors.ENDC}

    How to use (in any project):
    1. {Colors.BLUE}/plan "Fix login bug"{Colors.ENDC}  -> Creates TODO.md
    2. {Colors.BLUE}/act{Colors.ENDC}                    -> Writes code
    3. {Colors.BLUE}/check{Colors.ENDC}                  -> Reviews code
    4. {Colors.BLUE}/done{Colors.ENDC}                   -> Commits code
        """)

if __name__ == "__main__":
    main()
