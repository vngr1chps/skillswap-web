from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import logout

User = get_user_model()
@login_required
def profile_view(request):
    user = request.user
    complex = {
        'user' : user, 
    }
    return render(request, 'profiles/view.html', complex)

@login_required
def edit(request):
    if  request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.telegram = request.POST.get('telegram', user.telegram)
        user.skill_have = request.POST.get('skill_have', user.skill_have)
        user.skill_need = request.POST.get('skill_need', user.skill_need)
        user.bio = request.POST.get('bio', user.bio)
        try:
            user.save()
            return redirect('view')
        except:
            messages.error(request, "Имя пользователя занято")
            return render(request, 'profiles/edit.html', {'user': user})
    else:
        return render(request, 'profiles/edit.html', {'user': request.user})
@login_required
def delete(request):
    if  request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        return redirect('/')
    return redirect('view')