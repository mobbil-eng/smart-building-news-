# Smart Building News Aggregator

Автоматический сборщик новостей о умных зданиях, IoT и цифровизации недвижимости с отправкой в Telegram.

## Что это делает

- 📰 Собирает новости из RSS источников (Habr, CNews, TechCrunch, ArsTechnica)
- 🔍 Фильтрует по ключевым словам (умное здание, IoT, smart building и т.д.)
- 🚫 Автоматически дедупликирует (не отправляет одну новость дважды)
- 📱 Отправляет в Telegram через бота
- ⏰ Запускается ежедневно по расписанию (GitHub Actions)

## Быстрый старт

### 1. Создайте Telegram бота

1. Напишите @BotFather в Telegram
2. Выполните `/newbot`
3. Следуйте инструкциям, получите токен вида: `7540188268:AAG_lXEmrWR2O2BTMlbTuTe1iJLiyWCCtyg`

### 2. Найдите ваш Telegram ID

Несколько способов:
- Напишите @userinfobot в Telegram — он вам его скажет
- Или используйте этот скрипт:
  ```bash
  curl "https://api.telegram.org/bot{TOKEN}/getUpdates" | grep '"id"'
  ```

### 3. Создайте GitHub репо и добавьте секреты

Создайте репо и в `Settings > Secrets and variables > Actions` добавьте:

- `TELEGRAM_BOT_TOKEN` — токен вашего бота
- `TELEGRAM_CHAT_ID` — ваш ID в Telegram (как число, например: `123456789`)

### 4. Готово!

GitHub Actions будет запускать скрипт каждый день в 9:00 UTC.

## Тестирование локально

```bash
# Установите зависимости
pip install -r requirements.txt

# Установите переменные окружения
export TELEGRAM_BOT_TOKEN="your_token_here"
export TELEGRAM_CHAT_ID="your_id_here"

# Запустите
python main.py
```

## Кастомизация

### Изменить время запуска

Отредактируйте `.github/workflows/fetch-news.yml`:

```yaml
on:
  schedule:
    - cron: '0 18 * * *'  # 18:00 UTC вместо 9:00
```

Формат: `minute hour day month day_of_week` (UTC)

### Добавить новые RSS источники

Отредактируйте `main.py`, в разделе `RSS_SOURCES`:

```python
RSS_SOURCES = [
    'https://ваш-новый-источник.com/feed/',
    # ...остальные
]
```

### Изменить ключевые слова

Отредактируйте `KEYWORDS` в `main.py`.

## Структура проекта

```
smart-building-news/
├── .github/workflows/
│   └── fetch-news.yml          # GitHub Actions расписание
├── main.py                      # Основной скрипт
├── requirements.txt             # Python зависимости
├── seen_articles.json           # Дедупликация (генерируется автоматически)
└── README.md                    # Этот файл
```

## Как это работает

1. **GitHub Actions** — запускает скрипт по расписанию
2. **main.py** — парсит RSS, фильтрует, отправляет в Telegram
3. **seen_articles.json** — отслеживает отправленные статьи (коммитится в репо)

## Проблемы

**"Bot token invalid"** — проверьте, что `TELEGRAM_BOT_TOKEN` и `TELEGRAM_CHAT_ID` правильно установлены в Secrets.

**"Не получаю сообщения"** — убедитесь, что:
1. Вы подписаны на своего бота
2. Бот вам что-то отправлял хотя бы один раз
3. TELEGRAM_CHAT_ID это ваше личное ID, не username (@m0bil)

**Как узнать свой ID?** Напишите боту что-нибудь, потом:
```bash
curl "https://api.telegram.org/bot{TOKEN}/getUpdates"
```

## Дополнения

Когда workflow поиска завершится, я добавлю больше источников и Telegram каналов.
