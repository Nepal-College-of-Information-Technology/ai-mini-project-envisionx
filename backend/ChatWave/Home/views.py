from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import ChatRoom
from .forms import ChatMessagesForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required
def homePageLogic(request):
    chat_room = get_object_or_404(ChatRoom, room_name='Room 1')
    chat_messages = chat_room.messages.all()
    form = ChatMessagesForm()

    if request.headers.get('HX-Request'):
        form = ChatMessagesForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.room = chat_room
            message.save()
            context = {
                'message': message,
                'user': request.user,
            }
            return render(request, 'partials/chat_message_p.html', context)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        if request.method == 'POST':
            action = request.POST.get('action')
            if action == 'logout':
                # print("logout clicked!")
                logout(request)
                return redirect('login')
            form = ChatMessagesForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.author = request.user
                message.room = chat_room
                message.save()
                form = ChatMessagesForm()

    return render(request, 'index.html', {'chat_messages': chat_messages, 'form': form, 'user': request.user})
