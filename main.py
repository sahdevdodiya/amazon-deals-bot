import requests
from bs4 import BeautifulSoup
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler
import pytz  # ✅ Add this

bot_token = "7667300588:AAHUT5LgzqtYRs2oeC0VwF42nJSOkGKtL-0"
chat_id = "5663591941"

def scrape_amazon_deals():
    url = "https://www.amazon.in/deals"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    deals = []
    for item in soup.select('.DealContent'):
        title = item.select_one('.DealTitle')
        link = item.select_one('a')
        if title and link:
            title_text = title.get_text(strip=True)
            href = link['href']
            full_link = "https://www.amazon.in" + href
            deals.append(f"{title_text}\n{full_link}")

    return deals[:5]

def send_deals_to_telegram():
    bot = Bot(token=bot_token)
    deals = scrape_amazon_deals()
    for deal in deals:
        bot.send_message(chat_id=chat_id, text=deal)

# ✅ Set timezone using pytz (India or UTC)
timezone = pytz.timezone("Asia/Kolkata")  # or "UTC"

scheduler = BlockingScheduler(timezone=timezone)
scheduler.add_job(send_deals_to_telegram, 'interval', hours=1)
scheduler.start()
