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
from django.contrib.auth import get_user_model

User=get_user_model()

# import firebase_admin
# from firebase_admin import auth

def registerLogic(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm-password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('sign_up')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('sign_up')
        
        if password != confirm:
            messages.error(request, "Passwords do not match!")
            return redirect('sign_up')

        myUser = User.objects.create_user(email, username, password)
        myUser.is_active = False
        myUser.save()

        # Welcome Email
        subject = "Welcome to Blog App!!"
        message = f"Hello, {myUser.username}!!\nWelcome to Blog App!!"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myUser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        messages.success(request, "Your account has been successfully created! Please activate your account by clicking the link sent in your email.")

        # Account activation email
        current_site = get_current_site(request)
        email_subject = "Activate your account for Blog App"
        message2 = render_to_string('email_confirmation.html', {
            'name': myUser.username,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myUser.pk)),
            'token': generate_token.make_token(myUser)
        })

        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myUser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('sign_in')  # Redirect to sign_in after signup
    
    return render(request, 'register.html')

    



def loginLogic(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']  
       
        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to 'blog' after successful login
        
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login')
    return render(request, 'login.html')   
   
            
                    




