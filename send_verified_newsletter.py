import yagmail
import os
from dotenv import load_dotenv

load_dotenv()
# Gmail Credentials
EMAIL_SENDER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

receiver_email = "subscriber-email@example.com"
subject = "🚀 Your Weekly AI Newsletter"
body = "This is a placeholder. Replace with the reviewed newsletter content."

yag = yagmail.SMTP(EMAIL_SENDER, EMAIL_PASSWORD)
yag.send(to=receiver_email, subject=subject, contents=body)
print("✅ Newsletter Sent!")
