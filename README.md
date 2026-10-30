# Düsseldorf Appointment Notifier

## The problem
I needed an appointment to exchange my UK driving licence in
Düsseldorf, but the booking website showed no availability.
Checking repeatedly was time-consuming, and newly released
appointments could appear between visits.

## The solution
A Python tool that checks appointment availability and sends
a Telegram notification when appointment suggestions are detected.
GitHub Actions is configured to run checks every 30 minutes,
without requiring my laptop to stay switched on.

Appointments must still be booked manually.

## Tools
- Python
- Requests and BeautifulSoup
- Telegram Bot API
- GitHub Actions
- GitHub Secrets for credentials

## Development approach
Built with ChatGPT-assisted coding and troubleshooting.
I defined the problem, configured the tools and credentials,
tested the website checks and Telegram notifications, and
deployed the workflow.

## Status
Manual cloud checks and Telegram delivery tested successfully.
Recurring schedule configured; automatic execution awaiting
confirmation.
