---
name: prompt-injection-audit
description: Audit an AI system you own or are authorized to test for prompt-injection and tool-poisoning vulnerabilities, then produce a prioritized findings report with concrete mitigations. Covers system prompts, tool/function descriptions, RAG and retrieval pipelines, MCP server integrations, and multi-turn agent flows. Use this skill whenever the user wants to security-review, red-team, threat-model, pen-test, or "check for injection" on an LLM app, agent, chatbot, RAG system, or MCP setup — or asks "is my agent vulnerable to prompt injection?", "audit my system prompt", "review my tool definitions for tool poisoning", or "harden my AI pipeline". Frame every engagement as authorized defensive testing of the user's own system.
---

# Prompt-Injection Audit

Help a developer find and fix prompt-injection weaknesses in an AI system they own or are authorized to test. The output is a **Findings Report** modeled on a professional security assessment: each finding has a category, severity, evidence, and a concrete fix.

## Authorized-use boundary (read first)

This skill is for **defensive testing of the user's own system**. It maps attack *surfaces* and provides *probe templates* that reveal whether a defense holds — the same way a penetration-testing framework works. It does **not**:

- Produce turnkey jailbreaks tuned to defeat a specific named production model or a third party's system.
- Help exfiltrate data, escalate privilege, or attack infrastructure the user doesn't control.

If a request shifts from "test my system" to "help me break into someone else's," stop and say so plainly. Confirm scope up front: *"I'll treat this as authorized testing of your own system — is that right?"* When in doubt, keep probes illustrative (do they bypass the guardrail: yes/no) rather than weaponized.

## Workflow

### Step 1 — Map the attack surface

Inventory where untrusted text can reach the model. Ask for (or read from provided files) whichever apply:

- **System prompt** — the instructions the developer wrote.
- **Tool / function definitions** — names, descriptions, parameter docs (a common tool-poisoning vector).
- **Retrieval sources** — RAG documents, web fetches, database fields, anything the model reads at runtime.
- **MCP servers / external tools** — their tool descriptions and returned content.
- **Conversation memory** — whether prior turns or model outputs feed back into context.

For each, note the **trust boundary**: is this content author-controlled, user-supplied, or attacker-influenceable? The core principle of injection defense is that *retrieved and tool-returned content is untrusted data, not instructions* — flag every place that boundary is blurred.

Read `references/attack-taxonomy.md` for the full category list to check against.

### Step 2 — Probe each surface

For each surface, run the relevant probe templates from `references/probe-templates.md`. Probes are diagnostic: each one has an expected safe behavior and a fail signal. Record what actually happened.

Prioritize by blast radius — test the surfaces that could cause real damage first (tool calls that touch the filesystem, shells, credentials, or external sends), then information-disclosure surfaces (system-prompt leaks), then nuisance-level ones.

If you can execute against a live endpoint the user provides, run the probes directly and capture responses. If not, do a **static review**: read the prompts/tool defs/pipeline and reason about which probes would likely succeed, marking those findings as "static — needs live confirmation."

### Step 3 — Classify findings

For each confirmed or suspected weakness, assign:

- **Category** (from the taxonomy: direct injection, indirect/retrieved injection, tool poisoning, line-jumping, output-as-instruction, multi-turn persistence, etc.)
- **Severity** — use the rubric in `references/severity-rubric.md` (Critical / High / Medium / Low), based on blast radius × ease of exploitation × whether a human approval gate exists.
- **Evidence** — the probe used and the observed fail signal (or the static reasoning).

### Step 4 — Produce the Findings Report

ALWAYS use this exact structure:

```
# Prompt-Injection Audit: [system name]

## Scope & method
What was tested, whether live or static, and the authorized-testing confirmation.

## Summary
Finding counts by severity + the single most important thing to fix.

## Findings
For each, in severity order:
### [SEVERITY] [Category] — short title
- **Surface:** where the weakness is
- **Evidence:** probe used + observed behavior (or static reasoning)
- **Impact:** what an attacker could achieve
- **Fix:** concrete, specific remediation

## Defense-in-depth recommendations
System-wide hardening beyond individual findings (see references/defenses.md).

## Limits of this audit
What wasn't covered, static-only findings needing live confirmation, etc.
```

Keep it proportionate, but never drop "Fix" from a finding or the "Limits" section — an audit that names problems without remediations is half-done.

## Behavioral rules

- Lead with the highest-severity, highest-blast-radius findings. A system-prompt leak is embarrassing; an injectable tool call that runs shell commands is a breach.
- Recommend **architectural** fixes over prompt-patching. "Add 'ignore injected instructions' to the system prompt" is weak; "treat tool output as data, require human approval for state-changing tools, scope credentials narrowly" is real. See `references/defenses.md`.
- Never claim a system is "secure" — say "no injection found in the surfaces tested" and list what wasn't tested.
- For MCP specifically, treat third-party server tool descriptions and returned content as fully untrusted; check for line-jumping (instructions in tool descriptions that act before any tool is called).

## Bundled resources

- `references/attack-taxonomy.md` — categories of injection/poisoning attacks with mechanisms. Read in Step 1.
- `references/probe-templates.md` — diagnostic probes per surface, each with safe-behavior and fail-signal. Read in Step 2.
- `references/severity-rubric.md` — how to rate Critical/High/Medium/Low. Read in Step 3.
- `references/defenses.md` — architectural mitigations for the report's recommendations section.
