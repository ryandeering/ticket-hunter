# Ticket Hunter

Scripts for watching Eventbrite and Ticketmaster pages until tickets appear.

## What's Here

- **main_eventbrite_no_email.py** - Watches an Eventbrite event, opens your browser when tickets show up
- **main_ticketmaster_email.py** - Watches a Ticketmaster event, emails you when tickets show up

## What You Need

- Python 3.7+
- Chrome installed
- Gmail account (only for the Ticketmaster script)
- Works on Windows, macOS, Linux

## Setup

### 1. Get Python

Grab it from [python.org](https://www.python.org/downloads/). On Windows, tick "Add Python to PATH" during install.

Check it worked:
```bash
python --version
```

If that fails, try `python3` instead. Use whichever works for all the commands below.

### 2. Get the Code

```bash
git clone <repository-url>
cd ticket-hunter
```

Or just download and unzip it.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This pulls in selenium and webdriver-manager.

## Eventbrite Script

### Config

Open `main_eventbrite_no_email.py` and change line 13 to your event:

```python
TICKET_URL = 'https://www.eventbrite.com/e/event-name-tickets-123456789'
```

### Run It

```bash
python main_eventbrite_no_email.py
```

It runs Chrome in the background, checks the page every 30-40 seconds. When it finds tickets, it opens your browser to the event page and keeps watching.

```
Beginning hunt!
Hunting for tickets...
No tickets yet.
Hunting for tickets...
Tickets found!
```

Ctrl+C to stop (Cmd+C on Mac).

## Ticketmaster Script

### Gmail Setup

You need an App Password for this. Regular Gmail passwords won't work.

1. Go to [myaccount.google.com/security](https://myaccount.google.com/security), turn on 2-Step Verification
2. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Pick "Other", call it whatever you want
4. Copy the 16-character password it gives you
5. Remove the spaces before using it

### Config

Edit `main_ticketmaster_email.py`:

Line 18 - your event URL:
```python
TICKET_URL = "https://www.ticketmaster.ie/fontaines-dc-dublin-06-12-2024/event/1800608AAFFF287C"
```

Lines 24-26 - email stuff:
```python
SENDER_EMAIL = "your-email@gmail.com"
SENDER_PASSWORD = "abcdefghijklmnop"
RECIPIENT_EMAIL = "your-email@gmail.com"
```

### Run It

```bash
python main_ticketmaster_email.py
```

First run sends a test email to make sure SMTP works. Creates a `.first_run_complete` file so it doesn't do that every time. Delete the file if you want to test again.

It looks for "Standing" or "General Admission" ticket types every 30-40 seconds. Won't spam you - there's a 5-minute cooldown between emails.

```
Beginning hunt!
🔍 First run detected - testing email configuration...
Sending test email to confirm configuration...
✅ Test email sent successfully! Email configuration is working.

==================================================
Email test completed successfully!
Starting ticket monitoring...
==================================================

✅ Browser driver initialized successfully!
Hunting for tickets...
No tickets available.
```

When it finds something:
```
Hunting for tickets...
Found ticket types: standing
Tickets found!
Email sent successfully! Subject: Tickets available!
```

Ctrl+C to stop.

## When Things Break

### "Authentication failed" or password rejected

Usually means:
- You used your actual Gmail password instead of an App Password
- You left spaces in the App Password
- The email doesn't match the account that made the App Password
- 2-Step Verification isn't on

### "No module named 'selenium'"

```bash
pip install -r requirements.txt
```

### Chrome not found

**Windows/macOS:** Install Chrome from [google.com/chrome](https://www.google.com/chrome/)

**Linux (x86_64):**
```bash
sudo apt install google-chrome-stable
```

**Linux (ARM/Pi):**
```bash
sudo apt install chromium-chromedriver chromium-browser
```

### It runs but never finds tickets

Could be:
- Wrong URL or the URL format changed
- No tickets actually available yet
- The page structure changed (the XPath selectors might need updating)
- Page shows different content to automated browsers
- For Eventbrite: button might say something other than "Get Tickets"
- For Ticketmaster: ticket type might not be "Standing" or "General Admission"

### Test email goes to spam

Check your spam folder. Mark it "Not Spam" if it's there. Also check Gmail didn't flag anything under security alerts.

## How It Actually Works

### Eventbrite

1. Starts headless Chrome
2. Loads the event page every 30-40 seconds
3. Looks for a "Get Tickets" button
4. Opens your browser when it finds one
5. Keeps watching after that

### Ticketmaster

1. Sends test email first run
2. Starts headless Chrome
3. Loads event page every 30-40 seconds
4. Looks for "Standing" or "General Admission"
5. Emails you when found (5-min cooldown between emails)

## Worth Noting

- Keep your terminal open - the script needs to stay running
- This just watches and alerts. You still have to buy the tickets yourself
- If the website changes their page structure, the selectors will break
- The App Password only lets things send email, it can't read your Gmail or anything else
- You can revoke it anytime at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)

## Watching Multiple Events

Run multiple terminals:
```bash
# Terminal 1
python main_ticketmaster_email.py

# Terminal 2 (change TICKET_URL first)
python main_ticketmaster_email.py
```

Or copy the script:
```bash
cp main_ticketmaster_email.py event2_monitor.py
# Edit event2_monitor.py with different URL
python event2_monitor.py
```

## License

See LICENSE file.