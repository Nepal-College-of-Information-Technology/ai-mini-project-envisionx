from django.shortcuts import render, get_object_or_404,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *


@login_required()
def homePageLogic(request):
    chat_room = get_object_or_404(ChatRoom, room_name='Room 1')
    chat_messages = chat_room.messages.all()
    form = ChatMessagesForm()

    if request.method == "POST":
        form = ChatMessagesForm(request.POST)

        if form.is_valid():  
            message = form.save(commit=False)
            message.author = request.user
            message.room = chat_room 
            message.save()
            return redirect('home')


    return render(request, 'index.html', {'chat_messages': chat_messages, 'form': form})