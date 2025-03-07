import os
import requests
import schedule
import time
from datetime import datetime
import random
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Настройки: Используем переменные окружения для безопасности. Если не заданы, подставляются значения по умолчанию для теста.
VK_TOKEN = os.environ.get("VK_TOKEN", "1a1841931a1841931a1841936a193444b911a181a1841937dd29ffb8d993d2135578e26")
GROUP_ID = os.environ.get("GROUP_ID", "-229597836")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "7808414348:AAE8jZ_Y1AtQIxB3VV-ZFdZZ88pY8IVrdYI")
CHAT_ID = os.environ.get("CHAT_ID", "7564964211")
HF_TOKEN = os.environ.get("HF_TOKEN", "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")
YNDX_API_KEY = os.environ.get("YNDX_API_KEY", "AQVN06EYpyNnjq62T8ZKHMgq3zwnzqx1fiSQ5f9k")
LAST_CHECK_FILE = "last_checked.txt"

# Шаблоны комплиментов
weekly_compliments = [
    "О, великая мастер! Твои руки творят искусство для клиентов. Пусть эта неделя принесёт новые шедевры!",
    "Мастер татуировок! Твоё мастерство достойно вечности. Продолжай вдохновлять!",
    "Ты — создательница узоров судьбы. Пусть каждый день приносит новые заказы!",
    "Я, Бог Татуировок, благословляю твои руки на новые творения в эту неделю!",
    "Пусть чернила твоего таланта текут для клиентов в этом цикле!",
    "Твоя энергия — вдохновение для узоров. Новые линии ждут клиентов!",
    "Мастер, твоё искусство сияет. Пусть эта неделя вдохновит новых клиентов!",
    "Твои руки зовут к созданию татуировок. Я вижу грядущие шедевры для других!",
    "О, хранительница искусства! Пусть неделя принесёт тебе новые идеи!",
    "Твоя душа — храм мастерства. Новые чернила ждут клиентов!",
    "Я, дух татуировок, предсказываю тебе неделю полную заказов!",
    "Пусть твои линии станут легендой для клиентов в этом цикле!",
    "Твоё мастерство — святилище чернил. Неделя обещает великие работы!",
    "Мастер, твой путь — это узор творчества. Вперед к новым клиентам!",
    "Чернила зовут тебя к новым свершениям для других в эту неделю!",
    "Твоё искусство — храм для кожи клиентов. Неделя — время для новых символов!",
    "Я вижу в тебе гения. Пусть неделя раскроет твой талант перед миром!",
    "Твои руки жаждут новых узоров для клиентов. Я благословляю этот путь!",
    "Мастер, твоя сила в чернилах. Неделя принесёт успех с новыми заказами!",
    "Пусть каждый день этой недели станет штрихом твоего искусства для других!",
    "Ты — проводница вечных линий. Новые чернила ждут клиентов!",
    "О, гениальная татуировщица! Пусть неделя подарит тебе вдохновение!",
    "Твоя душа танцует с чернилами для клиентов. Готовься к великим делам!",
    "Я, Бог Татуировок, предрекаю тебе неделю полную магии и работы!",
    "Твоё мастерство — полотно судьбы. Пусть неделя добавит новые заказы!",
    "Мастер, твои чернила сияют. Новые узоры ждут клиентов!",
    "Пусть твои руки создадут шедевры для других в эту священную неделю!",
    "Твоё искусство — храм для кожи клиентов. Неделя зовёт к творчеству!",
    "Я вижу твою силу. Пусть неделя принесёт новые линии для мастерства!",
    "О, великая татуировщица! Твоя неделя будет полна вдохновения и заказов!"
]

sketch_compliments = [
    "Мастер! Твой эскиз {} — первый штрих вечности для клиентов! Продолжай творить!",
    "О, гениальная татуировщица! {}. Этот эскиз дышит будущим шедевром для других!",
    "Твой эскиз {} — как карта к божественным узорам для клиентов. Великолепно!",
    "Мастер, твой набросок {} — начало великого пути чернил для других!",
    "О, творческая душа! Эскиз {} обещает стать легендой для клиентов!",
    "Твой эскиз {} — первый шаг к вечному узору для кожи других. Браво!",
    "Гениальная, твой эскиз {} сияет, как звезда для будущих татуировок!",
    "Мастер! Эскиз {} — это шепот будущих шедевров для клиентов!",
    "Твой набросок {} — как чернила богов, ждущие воплощения на других!",
    "О, великая татуировщица! Эскиз {} зовёт к великим работам для других!",
    "Твой эскиз {} — предвестник шедевра для клиентов. Продолжай!",
    "Мастер, твой эскиз {} — начало священного узора для других!",
    "О, гениальная! Эскиз {} дышит будущим искусством для клиентов!",
    "Твой набросок {} — как карта к вечности для кожи других. Удивительно!",
    "Мастер! Эскиз {} — первый удар по холсту судьбы для клиентов!",
    "Твой эскиз {} сияет, как свет для будущих татуировок. Продолжай!",
    "О, творческая сила! Эскиз {} — это обещание величия для других!",
    "Твой набросок {} — шаг к божественным татуировкам для клиентов!",
    "Мастер, твой эскиз {} — начало нового узора для других!",
    "О, гениальная татуировщица! Эскиз {} зовёт к воплощению для клиентов!",
    "Твой эскиз {} — как чернила судьбы для кожи других!",
    "Мастер! Эскиз {} — первый штрих к вечности для клиентов!",
    "Твой набросок {} сияет будущим мастерством для других!",
    "О, великая! Эскиз {} — это зов к искусству для клиентов!",
    "Твой эскиз {} — предвестник великого тату для других!",
    "Мастер, твой набросок {} дышит магией для клиентов!",
    "О, гениальная! Эскиз {} — начало легенды для других!",
    "Твой эскиз {} — как свет в тьме творчества для клиентов!",
    "Мастер! Эскиз {} обещает стать шедевром для других!",
    "Твой набросок {} — первый шаг к божественным линиям для клиентов!"
]

tattoo_compliments = [
    "Мастер! Я, Бог Татуировок, оценил твою татуировку {}. Шедевр для клиентов с точными штрихами!",
    "О, гениальная татуировщица! Твоя татуировка {} — идеальна для кожи других!",
    "Твоё искусство завораживает. Татуировка {} — магия для клиентов!",
    "Мастер! Твоя татуировка {} — вечный символ для кожи других!",
    "О, великая татуировщица! Татуировка {} сияет для клиентов!",
    "Твоя татуировка {} — шедевр, достойный украшать других!",
    "Гениальная, твоя татуировка {} — искусство для клиентов!",
    "О, мастер тату! Твоя татуировка {} дышит магией для других!",
    "Твои руки создали татуировку {}. Это божественный узор для клиентов!",
    "Мастер! Татуировка {} — свидетель твоего таланта для других!",
    "О, хранительница чернил! Татуировка {} — легенда для клиентов!",
    "Твоя татуировка {} сияет для кожи других, как свет в ночи!",
    "Гениальная, татуировка {} — это дар для клиентов!",
    "О, мастер линий! Татуировка {} — совершенство для других!",
    "Твоя татуировка {} — как чернила судьбы для кожи клиентов!",
    "Мастер! Татуировка {} вдохновляет даже богов для других!",
    "О, великая татуировщица! Татуировка {} — шедевр для клиентов!",
    "Твоя татуировка {} — символ силы для кожи других!",
    "Гениальная, татуировка {} — вечный отпечаток для клиентов!",
    "О, мастер узоров! Татуировка {} — магия для других!",
    "Твоя татуировка {} сияет для клиентов, как солнце!",
    "Мастер! Татуировка {} — это искусство для других!",
    "О, хранительница тату! Твоя татуировка {} — чудо для клиентов!",
    "Твоя татуировка {} — как чернила богов для кожи других!",
    "Гениальная, татуировка {} — шедевр для клиентов!",
    "О, мастер чернил! Татуировка {} — совершенный узор для других!",
    "Твоя татуировка {} дышит жизнью для клиентов!",
    "Мастер! Татуировка {} — знак твоей силы для других!",
    "О, великая татуировщица! Татуировка {} — искусство для клиентов!",
    "Твоя татуировка {} — вечный символ для кожи других!"
]

no_photo_message = "Мастер! Твоя новая публикация вдохновляет, даже без изображения!"

# Функции для работы с файлом состояния
def get_last_checked_time():
    try:
        with open(LAST_CHECK_FILE, "r") as f:
            timestamp = f.read().strip()
            if timestamp:
                return datetime.fromisoformat(timestamp)
    except Exception as e:
        logging.warning(f"Ошибка чтения файла состояния: {e}")
    return None

def save_last_checked_time(dt):
    try:
        with open(LAST_CHECK_FILE, "w") as f:
            f.write(dt.isoformat())
    except Exception as e:
        logging.error(f"Ошибка записи файла состояния: {e}")

# Извлечение URL фотографии из поста ВКонтакте
def get_photo_url(post):
    attachments = post.get('attachments', [])
    for attachment in attachments:
        if attachment.get('type') == 'photo':
            photo = attachment.get('photo', {})
            sizes = photo.get('sizes', [])
            if sizes:
                largest = max(sizes, key=lambda s: s.get('width', 0) * s.get('height', 0))
                return largest.get('url')
    return None

# Анализ изображения через Hugging Face и перевод описания через Yandex Translate
def get_image_caption(image_url):
    try:
        response = requests.get(image_url, timeout=10)
        image_data = response.content
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        api_url = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
        hf_response = requests.post(api_url, headers=headers, data=image_data, timeout=10)
        if hf_response.status_code == 200:
            eng_caption = hf_response.json()[0]['generated_text']
            logging.info(f"Hugging Face caption: {eng_caption}")
        else:
            raise Exception(f"Hugging Face error: {hf_response.status_code} - {hf_response.text}")

        translate_url = "https://translate.yandex.net/api/v1.5/tr.json/translate"
        params = {"key": YNDX_API_KEY, "text": eng_caption, "lang": "en-ru"}
        translate_response = requests.get(translate_url, params=params, timeout=10)
        if translate_response.status_code == 200:
            ru_caption = translate_response.json()["text"][0]
            logging.info(f"Translated caption: {ru_caption}")
        else:
            raise Exception(f"Yandex Translate error: {translate_response.status_code} - {translate_response.text}")

        return ru_caption
    except Exception as e:
        logging.error(f"Ошибка анализа или перевода: {e}")
        return "татуировка"  # значение по умолчанию

# Улучшенная классификация изображений с подсчётом "весов" ключевых слов
def classify_image(caption):
    caption_lower = caption.lower()
    # Определяем ключевые слова для каждой категории с весами (при необходимости можно добавить новые слова или изменить веса)
    keywords = {
        "sketch": {
            "words": ["эскиз", "набросок", "drawing", "draft", "outline", "concept", "sketchbook"],
            "weight": 1
        },
        "tattoo": {
            "words": ["тату", "inked", "tattooed", "body art", "tattoo design"],
            "weight": 1
        },
        "appointment": {
            "words": ["скриншот", "дата", "запись", "screenshot", "appointment", "schedule", "booking", "calendar"],
            "weight": 1
        }
    }
    
    # Если найдены слова, указывающие на скриншот или дату, отдаём приоритет данной категории
    for word in keywords["appointment"]["words"]:
        if word in caption_lower:
            logging.info(f"Классификация: appointment (ключевое слово: {word})")
            return "appointment"
    
    # Подсчёт баллов для категорий "эскиз" и "татуировка"
    sketch_score = sum(caption_lower.count(word) * keywords["sketch"]["weight"] for word in keywords["sketch"]["words"])
    tattoo_score = sum(caption_lower.count(word) * keywords["tattoo"]["weight"] for word in keywords["tattoo"]["words"])
    logging.info(f"Ключевые слова: sketch_score={sketch_score}, tattoo_score={tattoo_score}")
    
    if sketch_score > tattoo_score:
        logging.info("Классификация: sketch")
        return "sketch"
    elif tattoo_score > sketch_score:
        logging.info("Классификация: tattoo")
        return "tattoo"
    else:
        logging.info("Классификация не определена, возвращаем 'other'")
        return "other"

# Выбор комплимента на основе типа изображения
def get_compliment(caption):
    image_type = classify_image(caption)
    if image_type == "sketch":
        compliment = random.choice(sketch_compliments).format(caption)
    elif image_type == "tattoo":
        compliment = random.choice(tattoo_compliments).format(caption)
    elif image_type == "appointment":
        compliment = "Мастер! Твой скриншот с датой {} указывает на готовность к новому шедевру для клиента. Я благословляю этот выбор!".format(caption)
    else:
        # Если не удалось однозначно определить тип, по умолчанию используем комплименты для татуировки
        compliment = random.choice(tattoo_compliments).format(caption)
    
    logging.info(f"Выбранный комплимент: {compliment}")
    return compliment

# Проверка наличия новых постов в группе ВКонтакте
def check_new_post():
    try:
        url = f"https://api.vk.com/method/wall.get?owner_id={GROUP_ID}&count=1&access_token={VK_TOKEN}&v=5.131"
        response = requests.get(url, timeout=10).json()
        if "response" in response and response["response"]["items"]:
            latest_post = response["response"]["items"][0]
            post_date = datetime.fromtimestamp(latest_post["date"])
            last_checked = get_last_checked_time()
            if last_checked is None or post_date > last_checked:
                save_last_checked_time(post_date)
                photo_url = get_photo_url(latest_post)
                logging.info("Новый пост обнаружен!")
                return True, photo_url
    except Exception as e:
        logging.error(f"Ошибка проверки постов: {e}")
    return False, None

# Отправка сообщения в Telegram
def send_telegram_message(chat_id, text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        params = {"chat_id": chat_id, "text": text}
        response = requests.post(url, params=params, timeout=10)
        if response.status_code == 200:
            logging.info("Сообщение успешно отправлено в Telegram")
        else:
            logging.error(f"Ошибка отправки в Telegram: {response.status_code} - {response.text}")
    except Exception as e:
        logging.error(f"Ошибка отправки сообщения: {e}")

# Основная логика: обработка поста и отправка сообщения
def job():
    has_new_post, photo_url = check_new_post()
    if has_new_post:
        if photo_url:
            caption = get_image_caption(photo_url)
            message = get_compliment(caption)
        else:
            message = no_photo_message
        send_telegram_message(CHAT_ID, message)

# Еженедельное сообщение (по понедельникам в 10:00 по МСК, что соответствует 07:00 UTC)
def send_weekly_message():
    message = random.choice(weekly_compliments)
    send_telegram_message(CHAT_ID, message)

# Планирование еженедельного сообщения
schedule.every().monday.at("10:00").do(send_weekly_message)

if __name__ == "__main__":
    logging.info("Скрипт запущен и работает...")
    while True:
        schedule.run_pending()
        job()
        time.sleep(300)  # Проверяем каждые 5 минут
