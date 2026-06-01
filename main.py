#!/usr/bin/env python3
import feedparser
import requests
import json
import os
from datetime import datetime
from urllib.parse import urlparse

# Ключевые слова для фильтрации
KEYWORDS = [
    'умное здание',
    'smart building',
    'цифровая недвижимость',
    'digital real estate',
    'умный дом',
    'smart home',
    'умное жкх',
    'цифровизация недвижимости',
    'real estate tech',
    'proptech',
    'умный город',
    'smart city',
    'iot',
    'интернет вещей',
    'автоматизация зданий',
    'building automation'
]

# RSS источники
RSS_SOURCES = [
    # Русскоязычные - основные
    'https://www.cnews.ru/feed/',
    'https://habr.com/feed/best/',
    'https://vc.ru/feed',

    # Русскоязычные - недвижимость и умные здания
    'https://ujin.tech/feed/',
    'https://digitaldeveloper.ru/feed/',
    'https://www.kommersant.ru/rss/main',
    'https://www.hitechbuilding.ru/rss',

    # Иностранные - tech и smart buildings
    'https://feeds.arstechnica.com/arstechnica/index',
    'https://feeds2.techcrunch.com/techcrunch/',
    'https://www.akoode.com/feed/',
]

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
SEEN_FILE = 'seen_articles.json'

def load_seen_articles():
    """Загружает список уже отправленных статей"""
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_seen_articles(seen):
    """Сохраняет список отправленных статей"""
    with open(SEEN_FILE, 'w', encoding='utf-8') as f:
        json.dump(seen, f, ensure_ascii=False, indent=2)

def get_article_id(link):
    """Создаёт уникальный ID для статьи на основе ссылки"""
    return link

def matches_keywords(text):
    """Проверяет, совпадает ли текст с ключевыми словами"""
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in KEYWORDS)

def fetch_articles():
    """Собирает статьи из всех RSS источников"""
    articles = []

    for source_url in RSS_SOURCES:
        try:
            feed = feedparser.parse(source_url)
            for entry in feed.entries[:20]:  # Последние 20 статей
                title = entry.get('title', '')
                link = entry.get('link', '')
                summary = entry.get('summary', '')

                if not title or not link:
                    continue

                # Проверяем совпадение с ключевыми словами
                if matches_keywords(f"{title} {summary}"):
                    articles.append({
                        'title': title,
                        'link': link,
                        'summary': summary[:200],  # Первые 200 символов
                        'source': urlparse(link).netloc,
                        'fetched_at': datetime.now().isoformat()
                    })
        except Exception as e:
            print(f"Ошибка при обработке {source_url}: {e}")

    return articles

def send_to_telegram(article):
    """Отправляет статью в Telegram"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID не установлены")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    message = f"🏢 {article['title']}\n\n📰 {article['source']}\n\n{article['link']}"

    try:
        response = requests.post(url, json={
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message
        }, timeout=10)

        if response.status_code == 200:
            print(f"✅ Отправлено: {article['title'][:50]}...")
            return True
        else:
            print(f"❌ Ошибка Telegram: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")
        return False

def main():
    """Основная логика"""
    print("🔍 Начинаю поиск новостей...")

    seen = load_seen_articles()
    articles = fetch_articles()

    if not articles:
        print("⚠️ Новые статьи не найдены")
        return

    print(f"📊 Найдено {len(articles)} статей")

    sent_count = 0
    for article in articles:
        article_id = get_article_id(article['link'])

        if article_id in seen:
            print(f"⏭️ Пропущено (уже отправлено): {article['title'][:40]}...")
            continue

        if send_to_telegram(article):
            seen[article_id] = article['fetched_at']
            sent_count += 1

    save_seen_articles(seen)
    print(f"\n✨ Отправлено {sent_count} новых статей")

if __name__ == '__main__':
    main()
