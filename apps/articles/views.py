from django.shortcuts import render, redirect
from articles.models import ArticleModel

def ArticleListView(request):
    if not request.user.has_perm('articles.view_articlemodel') or request.user.groups.filter(name = 'Без БЗ').exists():
        return redirect('login')

    import sphinxapi
    import math
    from django.forms.models import model_to_dict

    client = sphinxapi.SphinxClient()
    client.SetServer('127.0.0.1', 9312)

    items = 50
    search = 'a'

    pagination = {
        'page': 1,
        'total': 0,
        'num_pages': 0,
        'number': 0
    }
    if request.method == 'POST':
        from django.http import JsonResponse
        pagination['page'] = int(request.POST.get('page'))

        if request.POST.get('search'):
            search = request.POST.get('search').replace('$', '').replace('/', '')

    # sphinx = "SELECT * FROM articles_articlemodel WHERE id"
    #
    # sql = 'SELECT id, title FROM integrator.articles_articlemodel WHERE id'
    # if direction:
    #     sql = sql + ' >= '
    #     sphinx = sphinx + " >= "
    # else:
    #     sql = sql + ' <= '
    #     sphinx = sphinx + " <= "
    #
    # sql = sql + str(to_elm)
    # sphinx = sphinx + str(to_elm)
    #
    #
    #     if search:
    #         sql = sql + ' AND MATCH (title, number, header, summary, text, products) AGAINST ("' + search + '" IN NATURAL LANGUAGE MODE)'
    #         sphinx = sphinx + " AND MATCH ('" + search + "')"
    #         # sphinx = sphinx + ' AND (title = "' + search + '" OR text = "' + search + '" OR number = "' + search + '" OR header = "' + search + '" OR summary = "' + search + '" OR products = "' + search + '")'
    #
    # sql = sql + ' ORDER BY id'
    # sphinx = sphinx + " ORDER BY id"
    # if not direction:
    #     sql = sql + ' DESC'
    #     sphinx = sphinx + ' DESC'
    #
    # sql = sql + ' limit ' + str(items)
    # sphinx = sphinx + " limit " + str(items)

    from django.http import HttpResponse
    client.SetRetries(1);
    client.SetMatchMode(sphinxapi.SPH_MATCH_PHRASE);
    client.SetLimits((pagination['page'] - 1) * items, items, max(1000, (pagination['page'] * items) + 100));
    # client.SetLimits((20 - 1) * items, items);
    rows = client.Query(search)
    # return HttpResponse(str(rows))
    indexes = [elm['id'] for elm in rows['matches']]
    pagination['total'] = rows['total_found']
    pagination['num_pages'] = math.ceil(rows['total_found'] / items);
    pagination['range'] = list(range(1, pagination['num_pages'] + 1))
    pagination['number'] = (pagination['page'] - 1) * items



    # if not direction:
    #     sql = 'SELECT * FROM integrator.articles_articlemodel t1, (' + sql + ') subquery WHERE subquery.id = t1.id ORDER BY t1.id'
    #
    # articles = ArticleModel.objects.raw(sql)

    articles = ArticleModel.objects.filter(id__in = indexes)
    result = [model_to_dict(item) for item in articles]


    # if result[0]['id'] == to_elm:
    #     result.pop(0)
    #     pagination['prev_id'] = result[0]['id']
    # elif result[-1]['id'] == to_elm:
    #     result.pop()
    #     pagination['next_id'] = result[-1]['id']
    # else:
    #     result.pop()
    #
    # if len(result) == (items - 1):
    #     if direction:
    #         result.pop()
    #         pagination['next_id'] = result[-1]['id']
    #     else:
    #         result.pop(0)
    #         pagination['prev_id'] = result[0]['id']

    if request.method == 'POST':
        return JsonResponse({'data': result,
            'pagination': pagination,
        }, safe = False)

    context = {'list': result, 'pagination': pagination}
    return render(request, 'articles/list.html', context)

def ArticleDetailView(request, pk):
    if not request.user.has_perm('articles.view_articlemodel') or request.user.groups.filter(name = 'Без БЗ').exists():
        return redirect('login')

    article = ArticleModel.objects.get(pk = pk)
    context = {'article': article}
    return render(request, 'articles/detail.html', context)
