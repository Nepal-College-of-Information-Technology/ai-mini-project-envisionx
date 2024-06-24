from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import get_user_model

User=get_user_model()

# import firebase_admin
# from firebase_admin import auth

def registerLogic(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            confirm = request.POST['cpassword']

        except MultiValueDictKeyError as e:
            messages.error(request, f"Missing field: {str(e)}")
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('register')
        
        if password != confirm:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        myUser = User.objects.create_user(username=username, email=email, password=password)
        myUser.save()

        # Welcome Email
        # subject = "Welcome to ChatWave!!"
        # message = f"Hello, {myUser.username}!!\nWelcome to ChatWave!!"
        # from_email = settings.EMAIL_HOST_USER
        # to_list = [myUser.email]
        # send_mail(subject, message, from_email, to_list, fail_silently=True)

        # messages.success(request, "Your account has been successfully created! Please activate your account by clicking the link sent in your email.")

        # # Account activation email
        # current_site = get_current_site(request)
        # email_subject = "Activate your account for Chatwave"
        # message2 = render_to_string('email_confirmation.html', {
        #     'name': myUser.username,
        #     'domain': current_site.domain,
        #     'uid': urlsafe_base64_encode(force_bytes(myUser.pk)),
        #     'token': generate_token.make_token(myUser)
        # })

        # email = EmailMessage(
        #     email_subject,
        #     message2,
        #     settings.EMAIL_HOST_USER,
        #     [myUser.email],
        # )
        # email.fail_silently = True
        # email.send()

        return redirect('login')  # Redirect to sign_in after signup
    
    return render(request, 'register.html')



def loginLogic(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password') 
        # print(email,password) 
       
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  
        
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login')
    return render(request, 'login.html')   
   
            
# def activate(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         myUser = User.objects.get(pk=uid)  # Corrected from User.object to User.objects
    
#     except (ValueError, TypeError, OverflowError, User.DoesNotExist):
#         myUser = None
    
#     if myUser is not None and generate_token.check_token(myUser, token):
#         myUser.is_active = True
#         myUser.save()
#         login(request, myUser)
#         return redirect('home')  # Redirect to 'home' after successful activation
    
#     else:
#         return render(request, 'activation_failed.html')                  




