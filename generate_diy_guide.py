from openai import OpenAI
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv

load_dotenv()
# OpenAI API Key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Connect to Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("ai-meme-automation-1501c4c0f9ba.json", scope)
sheets_client = gspread.authorize(creds)

# Open the Google Sheet
spreadsheet = sheets_client.open("Newsletter_automation")  # Replace with your sheet name
sheet = spreadsheet.worksheet("DIY Automation")

# Generate DIY Automation Guide
prompt = (
    "Suggest a useful AI-powered automation idea that helps with productivity, efficiency, or business growth. "
    "Then, provide a step-by-step guide on how to implement it using free or easily accessible tools. "
    "Keep it short, beginner-friendly, and actionable."
)

response = client.chat.completions.create(
    model="gpt-4o-mini", # Replace with your model name
    messages=[
        {"role": "system", "content": "You are an AI expert creating short, actionable guides."},
        {"role": "user", "content": prompt},
    ]
)

# Extract and print the response
guide = response.choices[0].message.content
#print("Generated Guide:", guide)

# Append the guide to Google Sheets
sheet.append_row(["DIY Automation", guide, "Pending"])
print("✅ DIY Automation Guide added to Google Sheets.")
