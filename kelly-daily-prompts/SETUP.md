# Daily Kevin Kelly prompt — push notification setup

`prompts.json` in this folder has all 88 items from Kevin Kelly's
["88 Prompts for Long Term Thinking"](https://kevinkelly.substack.com/p/88-prompts-for-long-term-thinking).

A recurring Routine (`create_trigger`) can't be created from a GitHub-task
session — that action needs a live interactive approval that only exists in a
regular Claude chat/app session. To finish this, open a normal Claude
conversation (claude.ai or the Claude app — not a GitHub-linked coding
session) and paste the request below. Claude will call `create_trigger` and
you'll get an approval prompt to confirm it.

## What to paste into a live Claude chat

> Set up a daily Routine that fires at 9:45am Eastern and sends me a push
> notification with one random prompt from Kevin Kelly's "88 Prompts for
> Long Term Thinking." Pick a different one than recent days if possible.
> Here are all 88, numbered:
>
> [paste the contents of `prompts.json`'s `prompts` array here, or attach
> the file]

Claude will create a Routine with a cron schedule (`45 13 * * *` UTC =
9:45am Eastern during EDT; adjust to `45 12 * * *` during EST if you want it
pinned to standard time) that fires into that chat session and sends a
`PushNotification` with the chosen prompt.

## Alternative: real email instead of a push notification

If you'd rather get an actual email (not a push notification), the
alternative is a GitHub Actions workflow in this repo that runs on a daily
cron and sends mail via SMTP (e.g. Gmail with an App Password stored as
repo secrets `MAIL_USERNAME` / `MAIL_PASSWORD`). Ask for that explicitly and
it can be added as a `.github/workflows/daily-kelly-prompt.yml` workflow
plus a small script that reads `prompts.json` and mails a random entry.
