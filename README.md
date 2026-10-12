# accessibility-screening

Checks a web page against WCAG rules and sorts what it finds by how much each
problem actually blocks someone.

## Install

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Use

```bash
# point it at a URL or a local file
.venv/bin/python -m accessibility_screening.cli https://example.com
.venv/bin/python -m accessibility_screening.cli build/index.html

# ask Claude to write the fix for each finding
export ANTHROPIC_API_KEY=sk-ant-...
.venv/bin/python -m accessibility_screening.cli https://example.com --explain

# write a Markdown report, and fail the build on anything serious or worse
.venv/bin/python -m accessibility_screening.cli https://example.com \
    --markdown report.md --fail-on serious
```

The exit code is non-zero when something hits the `--fail-on` level, which
defaults to `blocker`. That way it works in a CI pipeline.

## How it sorts

The levels are about what the problem does to the person using the page, not
how hard it is to fix.

| Level | What it means |
|---|---|
| `BLOCKER` | someone using assistive technology cannot finish the task |
| `SERIOUS` | they can finish it, but it is much harder |
| `MODERATE` | confusing or inconsistent, still workable |
| `MINOR` | polish |

Inside a level, the problems that show up most often come first. One missing
`alt` is a bug. Forty of them is a process problem, and you fix that a different
way.

## What it checks

Eleven checks across nine success criteria.

| Criterion | Check |
|---|---|
| 1.1.1 Non-text Content | `img` with no `alt` attribute |
| 1.3.1 Info and Relationships | heading levels skipped, missing `h1`, data table with no `th` |
| 2.4.1 Bypass Blocks | no skip link before the navigation |
| 2.4.2 Page Titled | missing or empty `title` |
| 2.4.3 Focus Order | positive `tabindex` |
| 2.4.4 Link Purpose | "click here", "read more", empty link text |
| 3.1.1 Language of Page | missing `lang` on `html` |
| 3.3.2 Labels or Instructions | form control with no label attached to it |
| 4.1.2 Name, Role, Value | `button` with no name, `iframe` with no title |

## What it does not check

Colour contrast, focus visibility, and anything else that needs the page
actually rendered in a browser. Those are real criteria and you cannot work them
out from the markup, so the tool stays quiet instead of guessing.

**A clean run does not mean the page is accessible.** It means these checks
found nothing, which is the floor and not the ceiling.

## Tests

```bash
.venv/bin/python -m pytest tests/ -q
```

39 tests. Every check has one test that should fail and one that should pass.
False alarms matter more than missed findings here, because once a tool starts
crying wolf people turn it off.
