# Claude Code Workflow (Boris Cherny's Setup)

> **Source:** Boris Cherny (Claude Code Creator) - [X Thread](https://x.com/i/status/2007179832300581177)
> **Saved:** 2026-01-28

---

## Core Philosophy

- Claude Code works great out of the box - minimal customization needed
- No single "correct" way - customize and hack as you like
- Give Claude a way to verify its work = 2-3x quality improvement

---

## 1. Parallel Sessions

Run **5 Claudes in parallel** in terminal tabs (numbered 1-5).
Use system notifications to know when Claude needs input.

```
# iTerm2 notifications setup
🔗 https://code.claude.com/docs/en/terminal-config#iterm-2-system-notifications
```

---

## 2. Web + Local Hybrid

- Run 5-10 additional Claudes on `claude.ai/code` in parallel
- Hand off local sessions to web using `&`
- Use `--teleport` to move sessions back and forth
- Start sessions from Claude iOS app and check later

---

## 3. Model Selection

**Use Opus 4.5 with thinking for everything.**

> "It's the best coding model I've ever used, and even though it's bigger & slower than Sonnet, since you have to steer it less and it's better at tool use, it is almost always faster than using a smaller model in the end."

---

## 4. Shared CLAUDE.md

- Single `CLAUDE.md` checked into git
- Whole team contributes multiple times a week
- **Key rule:** Anytime Claude does something incorrectly, add it to CLAUDE.md
- Each team maintains their own and keeps it up to date

---

## 5. GitHub Integration

Use `@.claude` in PR reviews to add things to CLAUDE.md as part of PRs.

```bash
# Install the GitHub Action
/install-github-action
```

This enables "Compounding Engineering" - improvements accumulate over time.

---

## 6. Plan Mode First

**Most sessions start in Plan mode** (shift+tab twice).

Workflow:
1. Enter Plan mode
2. Go back and forth with Claude until you like the plan
3. Switch to auto-accept edits mode
4. Claude can usually 1-shot the implementation

> "A good plan is really important."

---

## 7. Slash Commands for Inner Loops

Create commands for workflows done many times a day:
- Saves from repeated prompting
- Claude can use these workflows too
- Commands checked into `.claude/commands/`

Example: `/commit-push-pr` used dozens of times daily.

```bash
# Use inline bash to pre-compute info for speed
🔗 https://code.claude.com/docs/en/slash-commands#bash-command-execution
```

---

## 8. Subagents for Common Workflows

Use specialized subagents for recurring tasks:

| Agent | Purpose |
|-------|---------|
| `code-simplifier` | Simplifies code after Claude is done |
| `verify-app` | Detailed E2E testing instructions |

Think of subagents as automating workflows done for most PRs.

```
🔗 https://code.claude.com/docs/en/sub-agents
```

---

## 9. PostToolUse Hook for Formatting

Use a hook to auto-format Claude's code:
- Claude generates well-formatted code ~90% of the time
- Hook handles the last 10%
- Avoids formatting errors in CI

---

## 10. Pre-Allow Safe Commands

Instead of `--dangerously-skip-permissions`:

```bash
/permissions
```

Pre-allow common safe bash commands to avoid unnecessary prompts.
Check these into `.claude/settings.json` and share with team.

---

## 11. Tool Integration

Claude Code uses all your tools:

| Tool | Purpose |
|------|---------|
| Slack MCP | Search and post messages |
| BigQuery (bq CLI) | Analytics queries |
| Sentry | Error logs |

Configuration checked into `.mcp.json` and shared with team.

---

## 12. Long-Running Tasks

Options for extended operations:

1. **Prompt Claude** to verify work with background agent when done
2. **Agent Stop hook** for deterministic verification
3. **ralph-wiggum plugin** for autonomous loops

For unattended work in sandbox:
```bash
--permission-mode=dontAsk
# or
--dangerously-skip-permissions
```

```
🔗 https://github.com/anthropics/claude-plugins-official/tree/main/plugins%2Fralph-wiggum
🔗 https://code.claude.com/docs/en/hooks-guide
```

---

## 13. Verification is Critical

> "Probably the most important thing to get great results out of Claude Code -- give Claude a way to verify its work."

Verification methods by domain:

| Domain | Verification |
|--------|--------------|
| Web UI | Claude Chrome extension - opens browser, tests UI, iterates |
| Backend | Run test suite |
| CLI | Run bash commands |
| Mobile | Phone simulator |

**Invest in making verification rock-solid.**

```
🔗 code.claude.com/docs/en/chrome
```

---

## Quick Reference

| Shortcut | Action |
|----------|--------|
| `shift+tab` (x2) | Enter Plan mode |
| `&` | Hand off to web |
| `--teleport` | Move session between local/web |
| `/permissions` | Pre-allow commands |
| `/commit-push-pr` | Commit, push, create PR |

---

## This Project's Application

For the Creatio Reports Fix project:

1. **CLAUDE.md** - Keep updated with learnings (already doing this)
2. **Plan mode** - Use for complex handler changes (v19.x iterations)
3. **Verification** - Use `test_report_service.py` and browser testing
4. **Subagents** - Consider for code review before PROD deployment
