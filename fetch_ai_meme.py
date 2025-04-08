import praw
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random
import time
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)

# Google Sheets Authentication
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
service_account_path = os.getenv("SERVICE_ACCOUNT_JSON_PATH")
creds = ServiceAccountCredentials.from_json_keyfile_name(service_account_path, scope)
client = gspread.authorize(creds)

# Open the "AI Memes" worksheet
spreadsheet = client.open("Newsletter_automation")
sheet = spreadsheet.worksheet("AI Memes")

# List of subreddits to fetch memes from
subreddits = ["ArtificialInteligence", "memes", "LocalLLaMA", "singularity"]

# List of AI-related keywords to filter posts
ai_keywords = ["AI", "artificial intelligence", "chatgpt", "deep learning", "openai", "llm", "gpt", "generative AI", "AI model",]

# Fetch existing meme URLs to avoid duplicates
existing_memes = [row[2] for row in sheet.get_all_values()[1:]]  # Skip header row

# Track how many memes are added
memes_added = 0

# Get today's date in YYYY-MM-DD format
today_date = datetime.today().strftime('%Y-%m-%d')

# Iterate through subreddits to fetch memes
for subreddit in subreddits:
    print(f"🔍 Fetching memes from r/{subreddit}...")
    
    try:
        subreddit_instance = reddit.subreddit(subreddit)
        posts = subreddit_instance.hot(limit=15)  # Fetch 15 posts (ensuring variety)

        # Filter only AI-related image posts
        image_memes = []
        for post in posts:
            if hasattr(post, "preview") and "images" in post.preview:
                image_url = post.preview["images"][0]["source"]["url"]

                # Check if the title contains AI-related keywords
                if any(keyword.lower() in post.title.lower() for keyword in ai_keywords):
                    image_memes.append((post.title, image_url))

        # If no AI memes found, move to the next subreddit
        if not image_memes:
            print(f"❌ No AI-related memes found in r/{subreddit}. Skipping...")
            continue

        # Shuffle memes to add variety
        random.shuffle(image_memes)

        # Add up to 5 unique AI memes to Google Sheets
        for meme_title, meme_url in image_memes:
            if meme_url not in existing_memes:  # Avoid duplicates
                sheet.append_row([today_date, meme_title, meme_url, "Pending", ""])
                print(f"✅ Meme Added: {meme_title} - {meme_url} on {today_date}")
                memes_added += 1
                existing_memes.append(meme_url)  # Add to list to prevent duplicate checks

                if memes_added >= 5:
                    print("🎉 Fetched 5 memes. Stopping.")
                    break

        # Delay to avoid hitting Reddit API rate limits
        time.sleep(3)  # 3-second delay per subreddit

        # Stop fetching if 5 memes have been added
        if memes_added >= 5:
            break

    except Exception as e:
        print(f"⚠️ Error fetching from r/{subreddit}: {e}")

print("✅ Meme fetching complete!")