import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random
import os
from dotenv import load_dotenv

load_dotenv()
# Google API Key and Search Engine ID
API_KEY = os.getenv("GOOGLE_API_KEY")
# Replace with your actual API key
SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
# Replace with your actual search engine ID

# High-Quality AI Case Study Queries
queries = [
    "AI implementation case study site:forbes.com",
    "AI business automation success story site:techcrunch.com",
    "How companies successfully implemented AI site:wired.com",
    "AI-powered solutions improving productivity case study",
    "Real-world example of AI automation in business",
    "AI transformation case study in enterprises",
    "Case study on AI-driven efficiency in finance",
    "How AI improved operations in manufacturing",
    "AI impact on marketing and sales case study",
    "AI-powered logistics and supply chain automation case study"
]

# Keywords for relevance filtering
relevant_keywords = [
    "AI", "Artificial Intelligence", "automation", "machine learning",
    "deep learning", "AI-powered", "AI-driven", "robotics",
    "predictive analytics", "business AI", "computer vision",
    "real-world AI", "AI success story", "automation strategy"
]

# Exclude irrelevant sources
excluded_sites = [
    "healthcareitnews.com", "sciencedaily.com", "arxiv.org", 
    "nature.com", "researchgate.net", "ncbi.nlm.nih.gov", 
    "pubmed.ncbi.nlm.nih.gov"
]

# Google Sheets Authentication
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("ai-meme-automation-1501c4c0f9ba.json", scope)
sheets_client = gspread.authorize(creds)

# Open the "Case Studies" sub-sheet
spreadsheet = sheets_client.open("Newsletter_automation")
sheet = spreadsheet.worksheet("Case Studies")

# Check existing titles in Google Sheets to avoid duplicates
case_study_values = sheet.get_all_values()
print("Case Studies Sheet Data:", case_study_values)  # Debugging print statement

if len(case_study_values) == 0:
    print("⚠️ No data found in the 'Case Studies' sheet. Creating an empty list.")
    existing_titles = []  # Initialize an empty list if no data is found
else:
    existing_titles = [row[0] for row in case_study_values]

# Initialize Variables
title, link, snippet = None, None, None
article_found = False

# Search for AI Case Studies
for query in queries:
    url = f"https://www.googleapis.com/customsearch/v1?q={query} -research -study -news&cx={SEARCH_ENGINE_ID}&key={API_KEY}&dateRestrict=d7&sort=date"
    response = requests.get(url).json()

    if "items" in response:
        for item in response["items"]:
            temp_title = item["title"]
            temp_link = item["link"]
            temp_snippet = item["snippet"]

            # Ensure the article contains relevant AI keywords & is not from an excluded site
            if (any(keyword.lower() in temp_title.lower() for keyword in relevant_keywords)
                    and not any(site in temp_link for site in excluded_sites)):

                if temp_title not in existing_titles:  # Avoid duplicates
                    title, link, snippet = temp_title, temp_link, temp_snippet
                    article_found = True
                    break  # Stop searching when a relevant case study is found

    if article_found:
        break  # Exit loop if an article is found

# **Backup Case: Use Predefined Fallback**
if not article_found:
    title = "No recent relevant articles found. Backup option used."
    link = "https://annusmirabilis.io"
    snippet = "Explore this website for cool automations and learning about AI."

# **Store Case Study in Google Sheets**
if title and title not in existing_titles:
    sheet.append_row([title, link, snippet])
    print(f"✅ Case Study Added: {title} - {link}")
else:
    print("⚠️ No new case study added. Duplicate or no valid data found.")
