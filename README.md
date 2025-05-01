# Telegram Click Bot

## Features
- /start sends ad link with inline button
- /stat shows total users, clicks, income
- Tracks users and clicks in JSON file

## Setup
1. Add to GitHub
2. Deploy to Render
3. Set environment variables:
   - BOT_TOKEN: Your Telegram bot token
   - ADS_LINK: Your advertisement URL
4. Set Webhook using:
   https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook?url=https://your-render-url.onrender.com