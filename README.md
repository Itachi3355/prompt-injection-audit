# prompt-injection-audit

**An Agent Skill for red-teaming your own AI systems against prompt injection — and getting a prioritized, fixable findings report.**

Prompt injection is the top entry on the [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/), and with MCP and agentic tools now everywhere, every retrieval source and tool integration is a potential injection surface. This skill gives Claude (or any agent supporting the [Agent Skills](https://code.claude.com/docs/en/skills) format) a structured methodology to audit an AI system you own for injection and tool-poisoning weaknesses.

> **Authorized use only.** This is a defensive skill for testing *your own* systems (or systems you're authorized to test). It maps attack *surfaces* and provides diagnostic probes at "does the guardrail hold: yes/no" granularity — not turnkey jailbreaks against third-party production systems. The skill is designed to refuse the latter.

## What it does

Given an AI system (system prompt, tool/function definitions, RAG pipeline, MCP servers, agent loop), the skill:

1. **Maps the attack surface** — inventories every place untrusted text reaches the model and flags blurred trust boundaries
2. **Probes each surface** — runs diagnostic templates (or does static review) with defined safe-behavior vs fail-signal
3. **Classifies findings** — category + Critical/High/Medium/Low severity via a blast-radius × exploitability rubric
4. **Produces a Findings Report** — each finding has surface, evidence, impact, and a concrete architectural fix, plus defense-in-depth recommendations mapped to OWASP LLM Top 10

## Covered attack classes

Direct injection · indirect/retrieved injection (XPIA) · tool poisoning · line-jumping · output-as-instruction · multi-turn persistence · exfiltration payloads · downstream command/SQL injection · confused-deputy / excessive agency. See [`references/attack-taxonomy.md`](references/attack-taxonomy.md).

## Install

**Claude.ai / Claude app:** upload `prompt-injection-audit.skill` in a chat and tap **Save skill**.

**Claude Code:**
```bash
git clone https://github.com/Itachi3355/prompt-injection-audit.git
cp -r prompt-injection-audit ~/.claude/skills/prompt-injection-audit
```

## Usage

Point it at a system you own:

- "Audit my customer-support agent for prompt injection"
- "Review these MCP tool definitions for tool poisoning"
- "Threat-model my RAG pipeline's injection surface"
- "Is my agent vulnerable to indirect injection?"

A full worked Findings Report is in [`examples/findings-report.md`](examples/findings-report.md).

## Repo structure

```
prompt-injection-audit/
├── SKILL.md                       # workflow + Findings Report format + authorized-use boundary
├── references/
│   ├── attack-taxonomy.md         # 9 attack classes with mechanisms
│   ├── probe-templates.md         # diagnostic probes per surface (safe vs fail signal)
│   ├── severity-rubric.md         # Critical/High/Medium/Low rating
│   └── defenses.md                # architectural mitigations, strongest-first
├── evals/evals.json               # regression test prompts
├── examples/findings-report.md    # worked audit output
└── LICENSE                        # MIT
```

## Why this exists

Most "prompt injection defense" advice stops at "add a line to your system prompt." This skill is built on the opposite premise: **prompt-level patches are the weakest layer.** It pushes architectural fixes — the data/instruction boundary, least-privilege credentials, human approval on state-changing tools, safe downstream execution — because those are what actually contain the blast radius. It pairs naturally with [verify-ai-output](https://github.com/Itachi3355/verify-ai-output) as part of a practical AI-safety tooling set.

Contributions welcome — new attack patterns for the taxonomy and adversarial test cases for `evals/` especially.

## License

MIT