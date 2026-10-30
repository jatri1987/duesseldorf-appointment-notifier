import os
import sys
from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


START_URL = "https://termine.duesseldorf.de/select2?md=3"
SERVICE_NAME = "Umschreibung ausländischer Führerschein (Anlage 11 FeV)"


def check_appointments():
    try:
        with requests.Session() as session:
            page = session.get(START_URL, timeout=30)
            page.raise_for_status()
            soup = BeautifulSoup(page.text, "html.parser")

            form = soup.find("form", id="cnc-select-form")
            if form is None:
                return "NEEDS_REVIEW", "Service form not found."

            if form.find("input", attrs={"name": "cnc-5870"}) is None:
                return "NEEDS_REVIEW", "Expected service not found."

            params = {}
            for field in form.find_all("input", attrs={"name": True}):
                if not field.has_attr("disabled"):
                    if field.get("type") in ("hidden", "number"):
                        params[field["name"]] = field.get("value", "")

            params["cnc-5870"] = "1"

            page = session.get(
                urljoin(page.url, form.get("action") or page.url),
                params=params,
                timeout=30,
            )
            page.raise_for_status()
            soup = BeautifulSoup(page.text, "html.parser")

            location = soup.find(
                "input", attrs={"name": "loc", "value": "394"}
            )
            if location is None:
                return "NEEDS_REVIEW", "Expected location not found."

            form = location.find_parent("form")
            if form is None:
                return "NEEDS_REVIEW", "Location form not found."

            data = {}
            for field in form.find_all(
                "input", attrs={"name": True, "type": "hidden"}
            ):
                if not field.has_attr("disabled"):
                    data[field["name"]] = field.get("value", "")

            data["select_location"] = "Weiter"

            page = session.post(
                urljoin(page.url, form.get("action") or page.url),
                data=data,
                timeout=30,
            )
            page.raise_for_status()
            soup = BeautifulSoup(page.text, "html.parser")

            for element in soup.select("script, style, .modal"):
                element.decompose()

            text = " ".join(soup.stripped_strings)

            if SERVICE_NAME not in text or "Höherweg 101" not in text:
                return "NEEDS_REVIEW", "Unexpected page or expired session."

            if "Im Moment sind leider keine freien Termine verfügbar" in text:
                return "NO_APPOINTMENTS", "No appointments available."

            slots = []
            for form in soup.select("form.suggestion_form"):
                date_field = form.find("input", attrs={"name": "date"})
                button = form.find("button")

                if date_field is None or button is None:
                    continue

                date = date_field.get("value", "")
                time = button.get_text(" ", strip=True)

                try:
                    date = datetime.strptime(date, "%Y%m%d")
                except ValueError:
                    continue

                if time and not button.has_attr("disabled"):
                    slots.append(f"{date:%d.%m.%Y} at {time}")

            if slots:
                return "APPOINTMENTS_FOUND", "; ".join(sorted(set(slots))[:5])

            return "NEEDS_REVIEW", "Page changed. Please check manually."

    except requests.RequestException as error:
        return "ERROR", f"Website request failed: {type(error).__name__}"


def send_telegram(message):
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()

    if not token or not chat_id:
        print("Missing Telegram secrets.")
        return False

    try:
        response = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": message},
            timeout=30,
        )
        result = response.json()
        if not result.get("ok"):
            description = str(result.get("description", "Unknown error"))
            description = description.replace(token, "[hidden]")
            description = description.replace(chat_id, "[hidden]")
            print("Telegram rejected the message:", description)
        return result.get("ok") is True
    except (requests.RequestException, ValueError):
        print("Telegram delivery failed.")
        return False


def main():
    # Used for our first cloud test, without checking the booking website.
    if "--test-message" in sys.argv:
        sent = send_telegram("✅ Your GitHub cloud notifier can reach Telegram.")
        return 0 if sent else 1

    status, message = check_appointments()
    print(f"{status} — {message}", flush=True)

    if status == "NO_APPOINTMENTS":
        return 0

    if status == "APPOINTMENTS_FOUND":
        notification = (
            f"📅 Appointment suggestions detected!\n{message}\n\n"
            f"Check and book manually:\n{START_URL}"
        )
    else:
        notification = (
            f"⚠️ Appointment check needs attention.\n{message}\n"
            "Check the GitHub Actions log."
        )

    sent = send_telegram(notification)
    return 0 if sent and status == "APPOINTMENTS_FOUND" else 1


if __name__ == "__main__":
    sys.exit(main())
