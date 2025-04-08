import yagmail
import gspread
import markdown
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv

load_dotenv()
# Gmail Credentials
EMAIL_SENDER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

# Connect to Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("ai-meme-automation-1501c4c0f9ba.json", scope)
sheets_client = gspread.authorize(creds)

# Open the Newsletter Sheets
spreadsheet = sheets_client.open("Newsletter_automation")
meme_sheet = spreadsheet.worksheet("AI Memes")
automation_sheet = spreadsheet.worksheet("DIY Automation")
case_study_sheet = spreadsheet.worksheet("Case Studies")

# --- ✅ Selecting the Next Approved Meme in Order ---
meme_data = meme_sheet.get_all_values()

selected_meme = None
selected_row_index = None  # Store the row index to mark it as sent later

for i, row in enumerate(meme_data[1:], start=2):  # Skip header row, start at row 2
    if len(row) >= 5 and row[3].strip().lower() == "approved" and row[4] == "":  # Column D for Approval, Column E for Sent
        selected_meme = row
        selected_row_index = i
        break  # Stop at the first match

if not selected_meme:
    print("⚠️ No new approved memes left to send!")
    exit()

# Extract meme details
meme_date, meme_title, meme_url = selected_meme[:3]  # Extract date, title, and URL

# Mark the meme as "Sent" in the Google Sheet
meme_sheet.update_cell(selected_row_index, 5, "Sent")  # Column E
print(f"✅ Selected Meme: {meme_title} - {meme_url}")

# --- ✅ Fetching Latest DIY Automation Guide ---
automation_data = automation_sheet.get_all_values()
if len(automation_data) > 1:
    automation_title, automation_steps = automation_data[-1][:2]  # Get latest entry
else:
    automation_title = "No Automation Guide Available"
    automation_steps = "There are no new automation guides this week."

# Convert markdown steps to HTML
automation_steps_html = markdown.markdown(automation_steps)

# --- ✅ Fetching Latest AI Case Study ---
case_data = case_study_sheet.get_all_values()
if len(case_data) > 1:
    case_title, case_link, case_summary = case_data[-1][:3]  # Get latest case study
else:
    case_title = "No AI Case Study Found"
    case_link = "#"
    case_summary = "No recent AI case study was available this week."

# --- ✅ Corrected & Clean HTML Email Body ---
email_subject = "🔥 This Week’s AI Automation & Case Study!"

email_body = f"""
<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f4f4f4;">

    <div style="background: white; padding: 20px; border-radius: 10px; max-width: 600px; margin: auto; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);">
        
        <h2 style="color: #333; text-align: center; font-size: 24px;">🚀 This Week’s AI Newsletter</h2>

        <h3 style="background-color: #007bff; color: white; padding: 10px; border-radius: 5px; font-size: 20px;">🔥 Trending AI Meme</h3>
        <p style="font-size: 16px; color: #555;"><b>{meme_title}</b></p>
        <p style="text-align: center;"><img src="{meme_url}" alt="AI Meme" style="width: 100%; max-width: 500px; border-radius: 5px;"></p>
        <p style="font-size: 14px; color: #777;"><i>Posted on: {meme_date}</i></p>

        <h3 style="background-color: #007bff; color: white; padding: 10px; border-radius: 5px; font-size: 20px;">🤖 DIY Automation Guide</h3>
        <p style="font-size: 16px; color: #555;"><b>{automation_title}</b></p>
        <div style="padding: 15px; background-color: #f9f9f9; border-left: 5px solid #007bff; font-size: 15px; line-height: 1.6; color: #555;">
            {automation_steps_html}
        </div>

        <h3 style="background-color: #007bff; color: white; padding: 10px; border-radius: 5px; font-size: 20px;">📊 AI Case Study</h3>
        <p style="font-size: 16px; color: #555;"><b>{case_title}</b></p>
        <p style="font-size: 15px; color: #777; line-height: 1.6;">{case_summary}</p>
        <p style="text-align: center; margin-top: 20px;"><a href="{case_link}" style="text-decoration: none; background: #007bff; color: white; padding: 12px 20px; border-radius: 5px; font-size: 18px;">🔗 Read Full Case Study</a></p>

        <p style="text-align: center; margin-top: 30px; font-size: 14px; color: #999;">Stay ahead in AI! See you next week. 🚀</p>
    
    </div>

</body>
</html>
"""

# --- ✅ Sending Email ---
receiver_email = "gauravchhabrawork7@gmail.com"  # Change to your test email
yag = yagmail.SMTP(EMAIL_SENDER, EMAIL_PASSWORD)
yag.send(to=receiver_email, subject=email_subject, contents=email_body, as_draft=True)
print("✅ Newsletter saved as a draft in Gmail!")

