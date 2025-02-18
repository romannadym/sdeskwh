from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Prefetch, Max
import django
from bs4 import BeautifulSoup
import telegram
from integrator.celery import app
from django.contrib.auth import get_user_model
from django.http import HttpResponse
User = get_user_model()

from applications.models import ApplicationModel, AppStatusModel, StatusModel, AppHistoryModel, ApplicationArchiveModel

@app.task
def CloseApplication():

    status = StatusModel.objects.get(id = 4)
    user = User.objects.get(id = 1)

    records = []
    old_apps = []
    delta = django.utils.timezone.now() - timedelta(days = 14)#3
    apps = ApplicationModel.objects.filter(status_id = 3).prefetch_related(Prefetch('appstatuses', queryset = AppStatusModel.objects.filter(status_id = 3)))

    for app in apps:
        for st in app.appstatuses.all():
            if(st.pubdate < delta):
                records.append({'application': app, 'status_id': 4})
                app.status = status
                app.save()

                AppHistoryModel.objects.create(type = 1, text = 'Статус заявки изменен на "' + str(status) + '". Закрыто автоматически', application = app, author = user)

    list = [AppStatusModel(**vals) for vals in records]

    AppStatusModel.objects.bulk_create(list)

    for app in apps:
        text = render_to_string('applications/mail.html', {'id': app.pk, 'url': request.build_absolute_uri(app.get_absolute_url()), 'status': status, 'type': 'edit'})
        mail = EmailMessage('Изменение статуса заявки', text, settings.EMAIL_HOST_USER, [app.contact.email])
        mail.content_subtype = "html"
        try:
            mail.send()
        except Exception:
            AppHistoryModel.objects.create(type = 3, text = 'Не удалось отправить сообщение об изменении статуса заявки на "' + str(status) + '" на адрес электронной почты ' + app.contact.email, application = app, author = user)
        else:
            AppHistoryModel.objects.create(type = 3, text = 'Отправлено сообщение об изменении статуса заявки на "' + str(status) + '" на адрес электронной почты ' + app.contact.email, application = app, author = user)

        telegram_settings = settings.TELEGRAM
        bot = telegram.Bot(token = telegram_settings['bot_token'])
        text = render_to_string('applications/telegram.html', {'id': app.pk, 'url': request.build_absolute_uri(app.get_absolute_url()), 'status': status, 'type': 'edit'})
        try:
            bot.send_message(chat_id = telegram_settings['channel_id'], text = text, parse_mode = telegram.ParseMode.HTML)
        except Exception:
            AppHistoryModel.objects.create(type = 4, text = 'Не удалось отправить сообщение об изменении статуса заявки на "' + str(status) + '" в телеграм-канал', application = app, author = user)
        else:
            AppHistoryModel.objects.create(type = 4, text = 'Отправлено сообщение об изменении статуса заявки на "' + str(status) + '" в телеграм-канал', application = app, author = user)

    # Архив заявок
    delta = django.utils.timezone.now() - relativedelta(years = 1)
    archives = ApplicationModel.objects.filter(status_id = 4, pubdate__lt = delta)
    for record in archives:
        try:
            ApplicationArchiveModel.objects.create(old_id = record.id, priority = record.priority, equipment = record.equipment, problem = record.problem,\
                contact = record.contact, client = record.client, engineer = record.engineer, pubdate = record.pubdate,\
                status = record.status, creator = record.creator)

            record.delete()
        except Exception:
            pass

    return HttpResponse(apps)

@app.task
def CommentsFromEmails():
    import imaplib
    import email
    from email.header import decode_header
    import datetime
    import re
    from django.conf import settings
    from django.contrib.auth import get_user_model
    from applications.models import EmailLastUID, AppCommentModel

    try:
        last_uid = EmailLastUID.objects.get(id = 1)
    except:
        last_uid = None

    date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")

    imap = imaplib.IMAP4_SSL(settings.EMAIL_HOST_IMAP)
    imap.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

    imap.select('INBOX', True)

    if last_uid:
        result, data = imap.search('utf-8', 'UID', str(last_uid.uid) + ':*', 'subject', u'заявк'.encode('utf-8'))
    else:
        result, data = imap.search('utf-8', 'SINCE', date, 'subject', u'заявк'.encode('utf-8'))

    email_uids = data[0].split()

    if len(email_uids) > 0:
        latest_email_uid = email_uids[-1]
        first_email_uid = email_uids[0]

        if int(latest_email_uid) < last_uid.uid:
            return HttpResponse('successful')
    else:
        return HttpResponse('successful')

    messages = []
    comments = []
    successful = True

    for message in email_uids:
        result, data = imap.uid('fetch', message, '(RFC822)')
        raw_email = data[0][1].decode('utf-8')

        email_message = email.message_from_string(raw_email)

        try:
            subject = decode_header(email_message['Subject'])[0][0].decode()
        except:
            subject = email_message['Subject']

        app_text = re.search(r"^.*заявк. № \d+", subject, re.IGNORECASE | re.UNICODE)
        if app_text:
            app_number = re.search(r"\d+", app_text.group(), re.IGNORECASE | re.UNICODE).group()
            if app_number:
                from_email = email.utils.parseaddr(email_message['From'])[1]

                if email_message.is_multipart():
                    for payload in email_message.get_payload():
                        body = payload.get_payload(decode = True).decode('utf-8')
                else:
                    body = email_message.get_payload(decode = True).decode('utf-8')

                body_tag_position = body.find('<body')
                if body_tag_position:
                    body = body[body_tag_position:]
                    body_tag_close_position = body.find('>') + 1
                    body = body[body_tag_close_position:]

                messages.append({'text': body, 'application_id': int(app_number), 'author_id': from_email, 'email_date': datetime.datetime.strptime(email_message['Date'], '%a, %d %b %Y %H:%M:%S %z')})


    if messages:
        User = get_user_model()
        users = User.objects.all().values('id', 'email')
        for message in messages:
            message['author_id'] = next((row['id'] for row in users if row['email'] == message['author_id']), None)
            if message['author_id']:
                try:
                    AppCommentModel.objects.create(**message)
                except:
                    successful = False

    if successful:
        if last_uid:
            last_uid.success = True
            last_uid.uid = int(latest_email_uid) + 1
            last_uid.pubdate = datetime.datetime.now()
            last_uid.save()
        else:
            EmailLastUID.objects.create(success = True, uid = latest_email_uid)
    return HttpResponse(successful)

    # if comments:
    #     try:
    #         AppCommentModel.objects.bulk_create([AppCommentModel(**vals) for vals in comments])
    #         if last_uid:
    #             last_uid.success = True
    #             last_uid.uid = latest_email_uid
    #             last_uid.save()
    #         else:
    #             EmailLastUID.objects.create(success = True, uid = latest_email_uid)
    #         return HttpResponse('successful')
    #     except:
    #         return HttpResponse('failed')
