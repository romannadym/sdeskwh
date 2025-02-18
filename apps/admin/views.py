from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def IndexView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'admin-index')

    return render(request, 'admin/index.html')
