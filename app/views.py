from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate ,login , logout

from django.core.mail import send_mail , BadHeaderError
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes 
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator as generate_token
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode
from smtplib import SMTPAuthenticationError
from django.http import JsonResponse
from django.conf import settings
import base64


# 


from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator as generate_token
from django.core.mail import EmailMessage
from django.conf import settings

# Create your views here.

def home(request):
   return  render(request , "login.html")



def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'message': 'Username already exists. Please try a different username.'})

        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': 'Email already registered.'})

        if len(username) > 10:
            return JsonResponse({'success': False, 'message': 'Username must be 10 characters or less.'})
        
        if len(pass1) < 8:
            return JsonResponse({'success': False, 'message': 'Password must be at least 8 characters long.'})


        if pass1 != pass2:
            return JsonResponse({'success': False, 'message': 'Passwords do not match.'})

        if not username.isalnum():
            return JsonResponse({'success': False, 'message': 'Username must be alphanumeric.'})

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False  # User is inactive until they confirm their email
        myuser.save()

        # Send confirmation email
        current_site = get_current_site(request)
        email_subject = "Confirm your email address - Django Login!!"
        message = render_to_string('email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser),
        })
        email = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [myuser.email]
        )
        email.send(fail_silently=True)

        return JsonResponse({'success': True, 'message': 'Your account has been successfully created. We have sent you a confirmation email. Please confirm your account.'})

    return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, 'index.html', {'fname': fname})
        else:
            messages.error(request, 'Bad Credentials')
            return redirect('/')

    return render(request, 'signin.html')




def signout(request):
    logout(request)
    messages.success(request, "logged Out successfull")
    return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = str(urlsafe_base64_decode(uidb64), 'utf-8')
        myuser = User.objects.get(pk=uid)
    
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, 'Your account has been activated successfully. You can now login.')
        return redirect('home')
    else:
        messages.error(request, 'Activation link is invalid or expired.')
        return render(request, 'actfailed.html')



def send_test_email(request):
    try:
        send_mail(
            subject="Your subject",
            message="Your message body",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['shivam96ti@gmail.com']  # Corrected recipient email address
        )
        return HttpResponse('Message sent successfully!')
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    except SMTPAuthenticationError:
        return HttpResponse('SMTP Authentication Error: Check your email settings.')
    except Exception as e:
        return HttpResponse(f'An error occurred: {e}')


def LogoutPage(request):
   logout(request)
   return redirect('/')