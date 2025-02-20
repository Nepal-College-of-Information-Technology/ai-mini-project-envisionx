from django.shortcuts import render, get_object_or_404, redirect,HttpResponse
from django.http import JsonResponse
from .models import ChatRoom,ChatRoomMessages
from .forms import ChatMessagesForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import tensorflow as tf
import json
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import re
import pandas as pd
from nltk.stem import WordNetLemmatizer
import keras

from keras.preprocessing.sequence import pad_sequences
from django.contrib import messages
import os
from tensorflow.keras.preprocessing.text import Tokenizer


@login_required
def homePageLogic(request):
    chat_room = get_object_or_404(ChatRoom, room_name='Room 1')
    chat_messages = chat_room.messages.all()
    form = ChatMessagesForm()
    

    if request.method == 'POST':
        action = request.POST.get('action')
        print(action)
        if action == 'logout':
            logout(request)
            return redirect('login')
        
        if action == 'Change':
            #here the main plan is to retrieve atleast 10 messages from the database for the specific user. If there are less than 10 messages,
            #then disiplay "not enough data or something similar", and if there is enough data then run another function will that will average the data
            #from the 10 messages and return a youtube link corresponding to the result. We update the link according to the stats

            messageList = ChatRoomMessages.objects.filter(author=request.user)
            messageL = []

            for message in messageList:
                messageL.append(message.body)

            # print(len(messageL))
            if (len(messageL)) < 10:
                 messages.info(request, 'Requires atleast 10 messages to enable music feature!')
                
            else:
                sentiment = msgPick(messageL[:10])
                print(sentiment)
                songLink = pickSong(sentiment)
                # songLink = "https://www.youtube.com/embed/I35paFqFOPk"
                return render(request, 'index.html', {'chat_messages': chat_messages, 'form': form, 'user': request.user, "youtubelink": songLink})

                #  return render(request, 'index.html', {'chat_messages': chat_messages, 'form': form, 'user': request.user})

            # print(modelTest("I have had a tough day today"))
        
        form = ChatMessagesForm(request.POST)
        if form.is_valid():

            print("2")
            message_content = form.cleaned_data['body']
            print(message_content)

            message = form.save(commit=False)
            print(modelTest(message))

            message.author = request.user
            message.room = chat_room
            message.save()
            
            form = ChatMessagesForm()

    return render(request, 'index.html', {'chat_messages': chat_messages, 'form': form, 'user': request.user})

def pickSong(sentiment):
    if sentiment == "calm":
        return "https://www.youtube.com/embed/xRcWlA1I9z0"
    elif sentiment == "sad":
        return "https://www.youtube.com/embed/MVeeRCRw5kM"
    else:
        return "https://www.youtube.com/embed/I35paFqFOPk"


def msgPick(messageL: list):

    #discard the messages that have a length of less than 10
    
    # print(messageL)

    results = []
    for msg in messageL:
        if len(msg) < 10:
            continue  
        else:
            result = modelTest(msg)  
            results.append(result)

    count_calm = results.count("calm")
    count_sad = results.count("sad")
    count_happy = results.count("happy")

    print(results)

    counts = {'calm': count_calm, 'sad': count_sad, 'happy': count_happy}

    max_count_variable = max(counts, key=counts.get)

    return max_count_variable




def modelTest(message):
    # model_path = os.path.abspath('../../model/sentimentmodel.h5')
    # print(model_path)
    new_model = tf.keras.models.load_model('../../model/sentimentmodel.h5')
    with open('../../model/tokenizer.json') as json_file:
        json_string = json_file.read()

    tokenizer1 = tf.keras.preprocessing.text.tokenizer_from_json(json_string)
    tokenizer1.oov_token = '<UNK>'

    nltk.download('stopwords')
    nltk.download('wordnet')
    stop_words = stopwords.words('english')
    stemmer = SnowballStemmer('english')
    lemmatizer = WordNetLemmatizer()


    text_cleaning_re = "@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+"

    def textcleaning(text, stem=False):
        tokens = []
        text = re.sub(text_cleaning_re, ' ', str(text)).strip()
        
        for token in text.split():
            if token not in stop_words:
                if stem:
                    tokens.append(stemmer.stem(token))
                if lemmatizer:
                    tokens.append(lemmatizer.lemmatize(token))
                else:
                    tokens.append(token)
                    
                    
        return " ".join(tokens)
    
    text = message
    words_to_check = ["I", "IT","it", "you", "he", "she", "they", "we", "The", 'the', "I've", "this", "This", "i", "I'm", "It", 'it', "It's" ,"it's" , "how", "How", "Memories", "memories"]  

    words_in_text = text.split()


    filtered_words = [word for word in words_in_text if word not in words_to_check]


    new_text = " ".join(filtered_words)

    print(new_text)

    text = new_text
    list(text)
    text = textcleaning(text)
    print(text)
    

    
    tokenizer1.fit_on_texts([text])
    
    sequences = tokenizer1.texts_to_sequences([text])


    sequences = pad_sequences(sequences, padding='post', maxlen=50)


    predictions = new_model.predict(sequences)

    print(predictions)
    predictions.tolist

    result = ""
    if (predictions[0][0] > 0.45 and predictions[0][0] < 0.55):
        result = "calm"
    else:
        index = np.argmax(predictions)
        if (index == 0):
            result = "sad"
        else:
            result = "happy"

    return result

    

                    

