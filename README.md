# Ticket Hunter

Scripts for watching Eventbrite and Ticketmaster pages until tickets appear.

## What's Here

- **main_eventbrite_no_email.py** - Watches an Eventbrite event, opens your browser when tickets show up
- **main_ticketmaster_email.py** - Watches a Ticketmaster event, emails you when tickets show up

## Requirements

- Python 3.7 or newer
- Chrome browser
- Gmail account (only for the Ticketmaster script)
- Windows, macOS, or Linux

## Setup

### 1. Get Python

Grab it from [python.org](https://www.python.org/downloads/). On Windows, tick "Add Python to PATH" during install.

Check it worked:
```bash
python --version
```

If that fails, try `python3` instead. Use whichever works for all the commands below.

### 2. Get the Code

**Option A - Using Git (if you have it):**
```bash
git clone https://github.com/ryandeering/ticket-hunter
cd ticket-hunter
```

**Option B - Download ZIP:**
1. Go to https://github.com/ryandeering/ticket-hunter
2. Click "Code" → "Download ZIP"
3. Extract and navigate to the folder:
   ```bash
   cd path/to/ticket-hunter
   ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This pulls in selenium and webdriver-manager.

## Eventbrite Script

### Configuration

Open `main_eventbrite_no_email.py` in a text editor and update line 13 with your event URL:

```python
TICKET_URL = 'https://www.eventbrite.com/e/event-name-tickets-123456789'
```

### Run It

```bash
python main_eventbrite_no_email.py
```

Runs Chrome in headless mode and checks the page every 30-40 seconds. When tickets appear, opens your default browser to the event page. Continues monitoring after finding tickets.

```
Beginning hunt!
Hunting for tickets...
No tickets yet.
Hunting for tickets...
Tickets found!
```

Stop with Ctrl+C (Cmd+C on Mac).

## Ticketmaster Script

### Gmail Setup (Important!)

You need a special password for this. **Your regular Gmail password won't work** - you need to create an "App Password".

**Step-by-step:**
1. Go to [myaccount.google.com/security](https://myaccount.google.com/security)
2. Find "2-Step Verification" and turn it on (if it isn't already)
3. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
4. Under "Select app", choose "Other (Custom name)"
5. Type something like "Ticket Hunter" and click Generate
6. Google will show you a 16-character password like `abcd efgh ijkl mnop`
7. Copy it and remove all the spaces so it looks like `abcdefghijklmnop`
8. Keep this password - you'll need it in the next step

### Configuration

Edit `main_ticketmaster_email.py`:

**Line 18** - Your event URL:
```python
TICKET_URL = "https://www.ticketmaster.ie/fontaines-dc-dublin-06-12-2024/event/1800608AAFFF287C"
```

**Lines 24-26** - Email configuration:
```python
SENDER_EMAIL = "your-email@gmail.com"
SENDER_PASSWORD = "abcdefghijklmnop"
RECIPIENT_EMAIL = "your-email@gmail.com"
```

### Run It

```bash
python main_ticketmaster_email.py
```

First run sends a test email to verify SMTP configuration. Creates `.first_run_complete` marker file. Delete this file to re-test email setup.

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

Stop with Ctrl+C (Cmd+C on Mac).

## Troubleshooting

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

**Windows/macOS:**
Install from [google.com/chrome](https://www.google.com/chrome/)

**Linux:**
```bash
sudo apt install google-chrome-stable
```

**Linux (ARM):**
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

## Notes

- Keep terminal open - script must stay running to monitor
- Alerts only - doesn't purchase tickets automatically
- Website changes may break monitoring (selectors need updating)
- App Password only grants email sending access
- Revoke access anytime at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)

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