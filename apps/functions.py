from django.contrib.auth import get_user_model
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

import telegram

def is_admin_or_engineer(user):
    return user.groups.filter(name = 'Администратор').exists()\
        or user.groups.filter(name = 'Инженер').exists()

def get_user_by_id(user_id):
    if user_id:
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(id = user_id)
        except UserModel.DoesNotExist:
            return None
    return None

def get_prms_from_ids(ids_str, field):
    new_param = {}
    ids = ids_str.split('|')
    ids.pop()
    if ids[0]:
        if ids[0] != 'all':
            new_param[field + '_id__in'] = ids
    else:
        new_param[field + '_id'] = None
    return new_param

def send_email(params, title, send_to):
    text = render_to_string('applications/mail.html', params)

    mail = EmailMessage(title, text, settings.EMAIL_HOST_USER, send_to)
    mail.content_subtype = "html"
    try:
        mail.send()
        return True
    except Exception:
        return False

def send_telegram(params):
    text = render_to_string('applications/telegram.html', params)
    telegram_settings = settings.TELEGRAM
    bot = telegram.Bot(token = telegram_settings['bot_token'])
    try:
        bot.send_message(chat_id = telegram_settings['channel_id'], text = text, parse_mode = telegram.ParseMode.HTML)
        return True
    except Exception:
        return False
