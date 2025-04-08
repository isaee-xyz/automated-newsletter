# AI-Powered Newsletter Engine

An end-to-end automated newsletter system that curates weekly AI memes, DIY automation guides, and real-world AI case studies — all on autopilot.

This project was built using AI-native workflows and conversational coding, with minimal manual ops. It’s designed to run reliably, save time, and scale content without needing a content or ops team.

---

## 💡 What It Does

- Fetches the most engaging AI memes from Reddit using PRAW
- Generates a custom DIY automation guide using OpenAI GPT
- Scrapes and selects a recent AI case study using Google Search API
- Compiles the newsletter and sends it using Gmail SMTP
- Tracks approval and send status using a connected Google Sheet

---

## 🛠 Tech Stack

- **Python**: Core scripting
- **OpenAI GPT**: Automation guide generation
- **PRAW (Reddit API)**: Meme scraping
- **Google Custom Search API**: Case study discovery
- **Gmail SMTP**: Email delivery
- **Google Sheets + gspread**: Data coordination
- **dotenv**: Credential security

---

## ⚙️ Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/isaee-xyz/automated-newsletter.git
   cd automated-newsletter
