
import feedparser
import openai
import requests
import html2text
import os
from datetime import datetime

# === CONFIGURATION ===
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

# RSS Feeds to monitor
FEEDS = [
    "https://openai.com/blog/rss",
    "https://blogs.microsoft.com/feed/",
    "https://blog.google/rss/",
    "https://www.anthropic.com/news/rss",
    "https://www.theverge.com/rss/index.xml",
    "https://feeds.feedburner.com/TechCrunch/"
]

ITEMS_PER_FEED = 2
GPT_MODEL = "gpt-4"

def fetch_and_summarize(feed_url):
    entries = feedparser.parse(feed_url).entries[:ITEMS_PER_FEED]
    summaries = []
    for entry in entries:
        clean_text = html2text.html2text(entry.summary)
        prompt = (f"You are AiDi, a modern, friendly, yet professional AI assistant. "
                  f"Summarize the following news article in 3-4 sentences. "
                  f"Be concise, engaging, and highlight why this news matters to the reader:

"
                  f"Title: {entry.title}
"
                  f"Content: {clean_text}")

        try:
            response = openai.ChatCompletion.create(
                model=GPT_MODEL,
                messages=[{"role": "system", "content": "You are AiDi, an AI news summarizer with a modern, friendly, professional voice."},
                          {"role": "user", "content": prompt}],
                max_tokens=250
            )
            summary_text = response['choices'][0]['message']['content'].strip()
            summaries.append({
                "title": entry.title,
                "summary": summary_text,
                "link": entry.link
            })
        except Exception as e:
            print(f"Error summarizing {entry.title}: {e}")
            continue
    return summaries

def deduplicate(summaries):
    seen_titles = set()
    unique_summaries = []
    for item in summaries:
        title_key = item['title'].lower().strip()
        if title_key not in seen_titles:
            seen_titles.add(title_key)
            unique_summaries.append(item)
    return unique_summaries

def format_for_telegram(summaries):
    date_str = datetime.utcnow().strftime("%B %d, %Y")
    message = f"📢 *AiDi – Your Daily AI Digest – {date_str}*

"
    for item in summaries:
        message += f"💡 *{item['title']}*
"
        message += f"{item['summary']}
"
        message += f"[Read more]({item['link']})

"
    message += "✨ _Brought to you by AiDi, your friendly AI news companion._"
    return message

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "MarkdownV2",
        "disable_web_page_preview": False
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"Telegram API error: {response.text}")

def main(mytimer):
    openai.api_key = OPENAI_API_KEY
    all_summaries = []
    for feed in FEEDS:
        all_summaries.extend(fetch_and_summarize(feed))
    deduped_summaries = deduplicate(all_summaries)
    if deduped_summaries:
        telegram_message = format_for_telegram(deduped_summaries)
        send_to_telegram(telegram_message)
    else:
        print("No new items found.")
