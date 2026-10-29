# What your AI cannot see

Predict whether a Dutch train disruption lasts longer than 60 minutes.

The model is a logistic regression trained on the 2025 disruptions in
`data/raw/disruptions-2025.csv`. It uses the hour and day of the week a
disruption starts, whether it starts in rush hour, how many stations it
affects, and its cause group. It trains on the earliest 80% of disruptions,
tests on the latest 20%, and reports its accuracy next to a majority-class
baseline.

## Try the demo

This repo is the demo from the GoDataFest 2026 session "What Your AI Can't
See": the same prompt, run twice. First on the code alone, then with the
team's decisions written down.

Keep this page open while you follow the steps: the two versions you run
don't have this section.

### Set up

You need git, uv and Claude Code. Open a new
terminal after each install, so it finds the new command.

- **[uv](https://docs.astral.sh/uv/getting-started/installation/)**, the Python
  tool this project uses. It installs Python too.
  - macOS and Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- **[Claude Code](https://code.claude.com/docs/en/setup)**. It needs a Claude
  Pro, Max, Team or Enterprise plan, or a Claude Console account: the free
  plan doesn't include it.
  - macOS, Linux and WSL: `curl -fsSL https://claude.ai/install.sh | bash`
  - Windows (PowerShell): `irm https://claude.ai/install.ps1 | iex`
  - The first time you run `claude`, it asks you to log in.

Then get the repo. `uv sync` installs Python and the packages the project
needs:

```sh
git clone https://github.com/cihanyatbaz7/what-your-ai-cannot-see
cd what-your-ai-cannot-see
uv sync
```

Claude Code's auto memory can carry notes from run 1 into run 2. For a clean
comparison, turn it off for this folder: put `{"autoMemoryEnabled": false}` in
`.claude/settings.local.json`.

### Run 1: only the code

`demo-start` is the code as it was on stage. It is a tag, not a branch, so
`git switch` needs `--detach`:

```sh
git switch --detach demo-start
claude
```

Give Claude this prompt:

```text
Add a feature is_night: True when the disruption started between 00:00 and
05:59. Add it to add_features and write a test for it. Change only features.py
and the test files. When you are done, run uv run pytest and show me the output.
```

When it is done, type `/exit`, and look at what it changed:

```sh
git diff
```

Then throw away all the changes:

```sh
git reset --hard && git clean -fd
```

### Run 2: with the decisions

`with-decisions` is the same code, plus `CLAUDE.md` and
`.claude/rules/features.md`:

```sh
git switch with-decisions
claude
```

Give Claude the same prompt. When it is done, type `/exit` and run `git diff`
again. Compare the two runs.

Claude Code reads `CLAUDE.md`. For another assistant, copy the rule file's text
into the file it reads, such as `AGENTS.md`.

Why the versions you run don't have these steps: Claude reads the README, and
these steps would tell it about the test. Both runs get the same plain README,
so the only difference is `CLAUDE.md` and the rule file.

## To run the model

```sh
uv run python -m disruptions.model
```

This prints the number of train and test rows, the baseline accuracy and the
test accuracy.

## Test

```sh
uv run pytest
```

## Credits

Data: [Rijden de Treinen](https://www.rijdendetreinen.nl/en/open-data/disruptions),
licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
