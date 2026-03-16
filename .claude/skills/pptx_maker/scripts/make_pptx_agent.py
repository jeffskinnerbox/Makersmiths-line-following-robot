#!/usr/bin/env python3
"""
make_pptx_agent.py
------------------
Run from Claude Code (or any terminal) to spin up a Claude sub-agent
that reads a file and generates a PPTX using PptxGenJS.

Usage:
    python make_pptx_agent.py rosgraph.dot
    python make_pptx_agent.py architecture.md
    python make_pptx_agent.py report.json

Requirements:
    pip install claude-agent-sdk          # or: pip install claude_agent_sdk
    npm install -g pptxgenjs              # agent needs this at runtime
    export ANTHROPIC_API_KEY=sk-...
"""

import asyncio
import sys
from pathlib import Path

from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    TextBlock,
    ResultMessage,
)

# ── Prompt given to the sub-agent ────────────────────────────────────────────

SYSTEM_PROMPT = """
You are a specialist that analyses input files and produces polished
PowerPoint presentations using PptxGenJS (Node.js).

Workflow you MUST follow exactly:
1. Read the input file the user specifies.
2. Analyse its content thoroughly (nodes, topics, data, structure — whatever
   is relevant).
3. Write a complete, self-contained Node.js script that uses PptxGenJS
   (require path: /home/claude/.npm-global/lib/node_modules/pptxgenjs or the
   system global, whichever resolves).  The script must:
     - Use a dark, professional colour theme with clear typography.
     - Build 6-10 slides covering: title, overview/architecture, key
       components, data-flow or relationships, detail slides, and a summary.
     - Write the finished .pptx to the same directory as the input file,
       named <input_stem>_presentation.pptx.
4. Save the script as /tmp/make_pptx.js.
5. Execute it with: node /tmp/make_pptx.js
6. Confirm the output file was created and print its path.

Do not ask clarifying questions. Proceed autonomously.
""".strip()


# ── Agent runner ──────────────────────────────────────────────────────────────

async def run_agent(input_file: Path) -> None:
    """Spawn a sub-agent that reads input_file and writes a PPTX."""

    if not input_file.exists():
        print(f"[error] File not found: {input_file}")
        sys.exit(1)

    prompt = f"Analyse this file and create a professional PowerPoint: {input_file.resolve()}"

    options = ClaudeAgentOptions(
        system_prompt=SYSTEM_PROMPT,
        allowed_tools=["Read", "Write", "Bash"],   # auto-approve these
        permission_mode="acceptEdits",              # accept file writes without asking
        max_turns=25,                               # enough for read → write → run
    )

    print(f"[agent] Starting — input: {input_file.name}")
    print("[agent] Tools: Read, Write, Bash  |  permission_mode: acceptEdits\n")

    turn = 0
    async for message in query(prompt=prompt, options=options):

        if isinstance(message, AssistantMessage):
            turn += 1
            for block in message.content:
                if isinstance(block, TextBlock) and block.text.strip():
                    # Print agent reasoning / status lines
                    for line in block.text.strip().splitlines():
                        print(f"  [turn {turn}] {line}")

        elif isinstance(message, ResultMessage):
            print(f"\n[done]  cost=${message.cost_usd:.4f}  "
                  f"tokens={message.usage.input_tokens}in/"
                  f"{message.usage.output_tokens}out")
            if message.result:
                print(f"[result] {message.result.strip()}")


# ── CLI entry-point ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python make_pptx_agent.py <input_file>")
        sys.exit(1)

    asyncio.run(run_agent(Path(sys.argv[1])))
