# Düsseldorf Appointment Notifier

An automated appointment availability notifier that monitors the Düsseldorf Fahrerlaubnisbehörde booking portal and sends a Telegram alert when appointments become available.

Built and deployed using **AI-assisted development with ChatGPT and Claude**, despite having no traditional software-development background.

## The Problem

Appointments for the **Umschreibung eines ausländischen Führerscheins (Anlage 11 FeV)** at the Düsseldorf Fahrerlaubnisbehörde can be difficult to secure because availability changes unpredictably.

Repeatedly checking the portal manually was inefficient, so I wanted a system that would monitor availability automatically and notify me only when an appointment appeared.

## The Solution

I built an automated workflow that:

1. Checks the Düsseldorf appointment portal.
2. Follows the relevant booking path for the driver's licence exchange service.
3. Determines whether appointments are available.
4. Sends a Telegram alert when availability is detected.
5. Runs automatically in the cloud without requiring my laptop to remain switched on.

The notifier does **not** automatically book appointments. It detects availability and alerts the user so that the appointment can be booked manually through the official portal.

## Outcome

✅ **Successfully used in live operation**

The notifier detected newly released appointments for the following Monday and automatically sent me a Telegram alert.

I responded to the alert, accessed the booking portal and **successfully secured an appointment**.

The complete workflow was therefore validated in real-world use:

**Automated monitoring → Appointment detected → Telegram alert → Successful booking**

The project achieved its original purpose: replacing repeated manual checks with an automated process that produced a successful real-world outcome.

## How It Works

The Python script checks the booking portal and classifies the response into different states:

* `NO_APPOINTMENTS` – the system is reachable but no appointments are available.
* `APPOINTMENTS_FOUND` – appointment availability has been detected and a Telegram notification is triggered.
* `NEEDS_REVIEW` – the response differs from the expected structure and requires review.
* `ERROR` – the availability check could not be completed successfully.

This helps distinguish genuine availability from website changes or technical failures.

## Automation Architecture

The notifier runs in the cloud using **GitHub Actions**.

The GitHub Actions workflow was initially configured with the following cron schedule:

`7,37 * * * *`

During testing, I found that scheduled GitHub Actions runs could start later than expected. I therefore used **Claude to troubleshoot the scheduling issue and help configure cron-job.org as an external scheduler**.

cron-job.org sends an external trigger to the GitHub workflow at scheduled intervals, providing an additional mechanism for initiating the availability check.

The resulting workflow is:

**cron-job.org → GitHub Actions → Python script → Düsseldorf booking portal → Telegram alert**

This means the monitoring can continue automatically even when my local computer is switched off.

## Telegram Notifications

A private **Telegram Bot** provides the notification layer.

When the Python script detects appointment availability, it triggers a Telegram message so that I can immediately access the official booking portal.

The Telegram integration was tested independently before being incorporated into the automated workflow.

## Technology

* **Python** – availability-checking logic
* **Requests** – HTTP requests to the booking system
* **BeautifulSoup** – parsing booking-page responses
* **Telegram Bot** – real-time notifications
* **GitHub** – source control and project hosting
* **GitHub Actions** – cloud-based execution
* **GitHub Secrets** – secure credential storage
* **cron-job.org** – external scheduling and workflow triggering
* **ChatGPT** – AI-assisted development, explanation and troubleshooting
* **Claude** – debugging, troubleshooting and external scheduler configuration

## AI-Assisted Development

I built this project without a traditional software-development background, using **ChatGPT and Claude as development and troubleshooting tools**.

I defined the problem, desired behaviour and workflow, then used AI assistance to:

* Translate the booking journey into program logic
* Generate and understand the required Python code
* Interpret errors and execution logs
* Troubleshoot failed GitHub Actions runs
* Diagnose HTTP-request and page-parsing behaviour
* Configure and test Telegram notifications
* Configure GitHub Actions and GitHub Secrets
* Investigate scheduling delays
* Configure **cron-job.org with Claude's assistance**
* Test the workflow against the live booking system
* Iterate until the complete process worked successfully

AI generated and explained much of the technical implementation, while I directed the problem-solving process, tested the outputs, identified failures and determined what needed to change.

The project demonstrates how AI-assisted development can enable someone without a software-engineering background to move from **identifying a problem to building, deploying and successfully using a working solution**.

## Project Structure

`notifier.py`
Main Python script responsible for checking availability and triggering Telegram notifications.

`requirements.txt`
Python dependencies required by the notifier.

`.github/workflows/check.yml`
GitHub Actions workflow responsible for executing the availability check in the cloud.

## Status

🟢 **Successfully completed**

The notifier has:

* Run automatically in the cloud
* Monitored the live Düsseldorf booking system
* Detected genuine appointment availability
* Triggered the intended Telegram notification
* Enabled a successful appointment booking
* Demonstrated successful end-to-end operation

## What I Learned

This project gave me practical exposure to **AI-assisted development, Python, HTTP requests, HTML parsing, GitHub, GitHub Actions, cloud execution, debugging, scheduled automation and Telegram integrations**.

More importantly, it demonstrated that I could use AI to bridge a technical knowledge gap and take ownership of the entire problem-solving cycle:

**Problem identification → solution design → build → test → troubleshoot → deploy → real-world outcome**

## Disclaimer

This project was created for personal use and learning purposes.

It monitors publicly accessible appointment availability and does not automatically reserve appointments, bypass access controls or guarantee availability. Appointments are booked manually through the official Düsseldorf booking system.
