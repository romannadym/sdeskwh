from applications.models import AppHistoryModel, AppHistoryViewedModel

def NotificationsView(request):
    from django.db.models import Q
    from itertools import chain
    from django.db.models import Value, Exists, OuterRef
    new = {}
    old = {}
    notifications = {}
    total = 0
    total_new = 0
    admin = request.user.groups.filter(name = 'Администратор').exists()
    engineer = request.user.groups.filter(name = 'Инженер').exists()

    if request.user.is_authenticated and not admin and not engineer:
        new = AppHistoryModel.objects.filter((Q(application__client = request.user) & (Q(type = 1) | Q(type = 2))) & (Q(viewed__isnull = True) | ~Exists(AppHistoryViewedModel.objects.filter(user = request.user, history__id = OuterRef('pk'))))).annotate(new = Value('1'))
        if new.count() < 50:
            total = 50 - new.count()
        old = AppHistoryModel.objects.filter((Q(application__client = request.user) & (Q(type = 1) | Q(type = 2))) & Q(viewed__user = request.user)).annotate(new = Value('0'))[:total]

    elif engineer:
        new = AppHistoryModel.objects.filter((Q(application__engineer = request.user) & (Q(type = 1) | Q(type = 2) | Q(type = 7))) & (Q(viewed__isnull = True) | ~Exists(AppHistoryViewedModel.objects.filter(user = request.user, history__id = OuterRef('pk'))))).annotate(new = Value('1'))
        if new.count() < 50:
            total = 50 - new.count()
        old = AppHistoryModel.objects.filter((Q(application__engineer = request.user) & (Q(type = 1) | Q(type = 2) | Q(type = 7))) & Q(viewed__user = request.user)).annotate(new = Value('0'))[:total]
    elif admin:
        new = AppHistoryModel.objects.filter((Q(type = 1) | Q(type = 2) | Q(type = 5) | Q(type = 6)) & (Q(viewed__isnull = True) | ~Exists(AppHistoryViewedModel.objects.filter(user = request.user, history__id = OuterRef('pk'))))).annotate(new = Value('1'))
        if new.count() < 50:
            total = 50 - new.count()
        old = AppHistoryModel.objects.filter((Q(type = 1) | Q(type = 2) | Q(type = 5) | Q(type = 6)) & Q(viewed__user = request.user)).annotate(new = Value('0'))[:total]

    notifications = chain(new, old)
    if new:
        total_new = new.count()

    context = {'notifications': notifications, 'new': total_new, 'admin': admin, 'engineer': engineer}

    return context
