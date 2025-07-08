# AiDi – Your Daily AI Digest

AiDi is a modern, friendly, and professional AI assistant that delivers daily digests of AI and tech news directly to Telegram. Powered by GPT‑4, AiDi aggregates headlines from top sources like OpenAI, Microsoft, Google, Anthropic, and more.

This repository contains the codebase for deploying AiDi as an Azure Function with automatic GitHub integration for continuous deployment.

---

## Features
- GPT‑4 powered summaries with AiDi’s unique personality
- Aggregates and deduplicates news across multiple RSS feeds
- Clean, concise Telegram messages with Markdown formatting and “Read more” buttons
- Runs as a serverless Azure Function (low cost and scalable)
- Easy GitHub Actions deployment for automatic updates

---

## Repository Structure
aidi-daily-digest/
├── main.py             # Core logic: fetch, summarize, send
├── requirements.txt    # Python dependencies
├── host.json           # Azure Function host settings
└── function/
└── function.json   # Timer trigger configuration

---

## Getting Started

### Prerequisites
- Azure account with a Function App
- Telegram Bot (created via [@BotFather](https://t.me/BotFather))
- OpenAI API key ([Generate here](https://platform.openai.com/api-keys))
- Python 3.11+ (for local testing)

---

### Environment Variables
Set the following environment variables in Azure → Configuration → Application Settings:

| Name                 | Description                          |
|----------------------|--------------------------------------|
| `OPENAI_API_KEY`     | Your OpenAI API Key                 |
| `TELEGRAM_BOT_TOKEN` | Token for your Telegram bot         |
| `TELEGRAM_CHAT_ID`   | Chat ID to send daily digests to    |

---

### Deployment
1. Link this repository in Azure Deployment Center (GitHub as source).
2. Azure automatically builds and deploys using GitHub Actions.
3. Set environment variables as shown above.
4. Restart the Function App after deployment.

---

### Schedule
By default, AiDi runs daily at 07:00 CET (adjustable in `function/function.json`).

---

## License
This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## About
AiDi (short for *AI Digest*) is your professional AI companion, delivering timely and relevant summaries to keep you ahead in the world of Artificial Intelligence and technology.
