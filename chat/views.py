from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404
from social_app.models import User

# Create your views here.


@login_required
def chat_view(request, username):
    try:
        user_to_chat = User.objects.get(username=username)
        if request.user in user_to_chat.get_followers():
            return render(request, 'chat/chat.html', {'user': user_to_chat})
        else:
            return render(request, 'chat/access_denied.html', {'user': user_to_chat})

    except User.DoesNotExist:
        raise Http404("User Not found ... ")
