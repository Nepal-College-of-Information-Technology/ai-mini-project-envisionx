from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
import firebase_admin
from firebase_admin import auth

def registerLogic(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        username = request.POST["username"]
        
        try:
            user = auth.create_user(
                email = email,
                display_name = username,
                password = password
            )
            return JsonResponse({'status': 'User created successfully'}, status=200)
        
        except Exception as err:
            return JsonResponse({'status': 'Error creating user', 'error': str(err)}, status=400)
    return render(request, 'register.html')



def loginLogic(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        
        try:
            user = auth.get_user_by_email(email)
            return JsonResponse({'status': 'User logged in successfully'}, status=200)
            
        except Exception as err:
            return JsonResponse({'status': 'Error logging in', 'error': str(err)}, status=400)
        
    return render(request, 'login.html')
            
                    




