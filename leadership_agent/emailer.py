import smtplib
from email.message import EmailMessage

from content import Brief
from curriculum import CurriculumPosition
from feeds import Episode


def _progress_bar(current: int, total: int, width: int = 20) -> str:
    if total == 0:
        return ""
    filled = round(width * current / total)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {current}/{total}"


def build_subject(pos: CurriculumPosition) -> str:
    title = pos.episode["title"]
    # Truncate long titles so the subject stays readable
    if len(title) > 55:
        title = title[:52] + "..."
    return f"Day {pos.day} | {title}"


def build_body(
    pos: CurriculumPosition,
    brief: Brief,
    tomorrow_title: str | None,
) -> str:
    sep = "─" * 52
    takeaways = "\n".join(f"  {i+1}. {t}" for i, t in enumerate(brief.takeaways))
    progress = _progress_bar(pos.index_in_phase, pos.total_in_phase)

    tomorrow_section = ""
    if tomorrow_title:
        tomorrow_section = f"\nTOMORROW\n  {tomorrow_title}\n"

    link_section = ""
    if pos.episode.get("link"):
        link_section = f"\nListen: {pos.episode['link']}\n"

    return f"""{sep}
  LEADERSHIP BRIEF  ·  Day {pos.day}
  {pos.phase_label}  {progress}
{sep}

TODAY'S EPISODE
  "{pos.episode['title']}"

{brief.summary}

KEY TAKEAWAYS
{takeaways}

TODAY'S ACTION
  {brief.action_item}
{link_section}{tomorrow_section}{sep}
Manager Tools · manager-tools.com
"""


def send(
    gmail_address: str,
    gmail_app_password: str,
    to_email: str,
    pos: CurriculumPosition,
    brief: Brief,
    tomorrow_title: str | None = None,
) -> None:
    msg = EmailMessage()
    msg["Subject"] = build_subject(pos)
    msg["From"] = f"Leadership Brief <{gmail_address}>"
    msg["To"] = to_email
    msg.set_content(build_body(pos, brief, tomorrow_title))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(gmail_address, gmail_app_password)
        smtp.send_message(msg)
