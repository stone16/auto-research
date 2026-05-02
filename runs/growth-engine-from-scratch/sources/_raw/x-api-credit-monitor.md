# Repo: x-api-credit-monitor

## README.md
```markdown
# x-api-credit-monitor

> Daily heartbeat + low-balance alert for X Developer Console credits,
> delivered to Lark.

## What this does

Every day at 09:00 local time this tool logs into `console.x.com` using your
Chrome session cookies, reads the current credit balance and last-7-day
spend, and posts a Lark message to the "Getu Ops Alerts" channel showing
balance, average daily burn, and days remaining. When the balance drops
below `LOW_BALANCE_THRESHOLD` it also posts a low-balance alert. When the
Chrome session has expired, it posts a "please re-login" alert so the next
day's run recovers automatically once you sign in again.

It runs as a macOS **launchd user agent**; no extra server or supervisor
is involved.

## Requirements

- macOS (launchd + `plutil` are used)
- Google Chrome with a logged-in profile at `console.x.com`
- Python 3.11 or newer
- A Lark **custom bot** webhook in the destination channel, with
  signature verification enabled

## Lark custom bot setup

One-time setup inside the Lark channel that should receive heartbeats:

1. Open the channel → **Settings (⋯)** → **Bots** → **Add bot** →
   **Custom Bot**.
2. Give it a name (e.g. `x-credit-monitor`) and description, then
   **Add**.
3. On the generated webhook page: **enable Signature verification** (this
   is mandatory for this tool — the code always signs requests).
4. Copy the **Webhook URL** → `LARK_WEBHOOK_URL` in `.env`.
5. Copy the **Sign secret** → `LARK_SIGN_SECRET` in `.env`.

The sign secret is never logged at any level — not at DEBUG, INFO,
WARNING, or ERROR — and never written to the stdout/stderr log files.

## Configuration (.env)

Copy `.env.example` to `.env` and fill in each field. The five required
variables are:

| Variable                      | Purpose                                                                                                                                       | Example                                              |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| `X_ACCOUNT_ID`                | X Developer Console account id — visible in the `console.x.com` URL once you are logged in.                                                   | `1234567890`                                         |
| `LARK_WEBHOOK_URL`            | Full custom-bot webhook URL (from step 4 above).                                                                                              | `https://open.larksuite.com/open-apis/bot/v2/hook/...` |
| `LARK_SIGN_SECRET`            | Sign secret for the bot (from step 5 above). Never logged at any level.                                                                       | `abcdef0123...`                                      |
| `LOW_BALANCE_THRESHOLD`       | Dollar threshold below which an extra 🚨 alert fires alongside the heartbeat. Default 10 if unset.                                             | `10`                                                 |
| `CHROME_PROFILE_DIR` **or** `CHROME_PROFILE_DISPLAY_NAME` | Which Chrome profile to read cookies from. See "Switching profiles" below. | `Profile 3` or `dev (getu.ai)`                       |

**Chrome profile precedence rule:** if both `CHROME_PROFILE_DIR` and
`CHROME_PROFILE_DISPLAY_NAME` are set, `CHROME_PROFILE_DIR` wins and the
display-name lookup is skipped entirely. If neither is set, the tool
falls back to the `Default` profile with a WARNING. This dual-mode
configuration is the escape hatch if the display-name-based lookup
silently breaks (see "Switching profiles" for details).

## Install

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
# Install the `x_credit_monitor` package itself so `python -m x_credit_monitor`
# (and the plist's ProgramArguments) can find it.
.venv/bin/pip install -e .
cp .env.example .env
# edit .env and fill in the 5 variables above

# Manual smoke test — runs the monitor once, immediately, against the
# current configuration. Should post exactly one heartbeat to Lark.
.venv/bin/python -m x_credit_monitor

# Wire it into launchd so it fires daily at 09:00.
bash install.sh

# Confirm the launchd job is registered.
launchctl list | grep com.stometa.xcredit
```

`install.sh` renders the plist template into
`~/Library/LaunchAgents/com.stometa.xcredit.plist` (substituting the
absolute path to this repo) and calls `launchctl bootstrap`. It is
idempotent — running it again after a pull is the supported upgrade path;
it boots out the old incarnation and bootstraps the new one.

**Smoke-fire check after install (optional, posts to Lark):**

```bash
launchctl kickstart -k gui/$(id -u)/com.stometa.xcredit
# wait ~30 seconds, then:
tail ~/Library/Logs/x-credit-monitor.err.log
```

A successful kickstart leaves an empty or clean err log and produces
exactly one heartbeat message in the Lark channel.

## Uninstall

```bash
bash uninstall.sh
```

Boots out the LaunchAgent and removes the plist from
`~/Library/LaunchAgents`. Idempotent — safe to run multiple times.

## Re-login flow

If you receive a **⚠️ re-login alert** in Lark (reason: "cookies not
found" or "session expired"):

1. Open Chrome with the profile configured in `.env`
   (whichever of `CHROME_PROFILE_DIR` / `CHROME_PROFILE_DISPLAY_NAME`
   you set).
2. Visit <https://console.x.com/> and log in.
3. Do nothing else — the next 09:00 run will pick up the fresh cookies
   automatically and resume daily heartbeats.

You do not need to re-run `install.sh` or restart the LaunchAgent.

## Switching profiles

The monitor reads cookies from exactly **one** Chrome profile per run.
To switch which profile is monitored, edit `.env` and leave everything
else alone.

### List on-disk profile directories (for `CHROME_PROFILE_DIR`)

```bash
ls ~/Library/Application\ Support/Google/Chrome/
```

**Only pick `Default` or `Profile N` entries.** Ignore `System Profile`,
`Guest Profile`, `Crashpad`, `GrShaderCache`, `ShaderCache`, and the
other non-user directories. Picking a non-user directory triggers the
fallback path (WARNING + `Default`), not a hard crash, but you will end
up monitoring the wrong profile.

### List display-name-to-directory mapping (for `CHROME_PROFILE_DISPLAY_NAME`)

```bash
python3 -c 'import json,pathlib;p=pathlib.Path.home()/"Library/Application Support/Google/Chrome/Local State";print("\n".join(f"{d}: {v.get(\"name\", \"\")}" for d,v in json.loads(p.read_text())["profile"]["info_cache"].items()))'
```

This prints one line per profile in the form `<dir>: <display name>`.
Use the display name (right of the colon) as `CHROME_PROFILE_DISPLAY_NAME`.

If the display name silently changes (Chrome sync rename, full-width
characters after macOS input-method switch, etc.), the lookup falls back
to `Default` with a WARNING. The robust recovery is to switch to
`CHROME_PROFILE_DIR` set directly to the directory name from the `ls`
command above.

## Troubleshooting

1. **First thing to check:** tail the error log.
   ```bash
   tail ~/Library/Logs/x-credit-monitor.err.log
   ```
2. **Force an immediate run** (does not wait for 09:00):
   ```bash
   launchctl kickstart -k gui/$(id -u)/com.stometa.xcredit
   ```
3. **Smoke-fire check after install:** kickstart once, wait 30 seconds,
   tail the err log — a clean (empty) log means success.
4. **Disable temporarily:** `bash uninstall.sh`. Re-enable with
   `bash install.sh`.
5. **Confirm the job is registered:**
   `launchctl list | grep com.stometa.xcredit`.

## Timezone

The plist fires at **09:00 of the Mac's current system timezone** — this
is how launchd's `StartCalendarInterval` works; it has no built-in
timezone field.

If you travel: either (a) update the Mac's system timezone (the job
continues to fire at 09:00 local), or (b) edit
`~/Library/LaunchAgents/com.stometa.xcredit.plist` and adjust the
`Hour` value under `StartCalendarInterval`, then
`launchctl bootout gui/$(id -u)/com.stometa.xcredit` followed by
`launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.stometa.xcredit.plist`
(or simpler: just re-run `bash install.sh` after editing the template).

```
