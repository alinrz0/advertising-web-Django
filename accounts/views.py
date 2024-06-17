from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.views.generic import View
from django.db import connection
import random
import datetime

class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        email = request.POST.get('email')
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE Email = %s", (email,))
            user = cursor.fetchone()
            if user:
                code = str(random.randint(100000, 999999))
                print(code)
                request.session['email'] = email
                request.session['code'] = code
                request.session['code_timestamp'] = datetime.datetime.now().timestamp()
                return redirect('verify_code')
            else:
                return render(request, 'accounts/login.html', {'error': 'Email not found'})

from django.db import connection

class VerifyCodeView(View):
    def get(self, request):
        return render(request, 'accounts/verify_code.html')

    def post(self, request):
        code = request.POST.get('code')
        if 'code' in request.session:
            code_timestamp = request.session['code_timestamp']
            if datetime.datetime.now().timestamp() - code_timestamp > 120:
                del request.session['code']
                del request.session['code_timestamp']
                return render(request, 'accounts/verify_code.html', {'error': 'Code has expired'})
            elif code == request.session.get('code'):
                del request.session['code']
                del request.session['code_timestamp']
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM users WHERE Email = %s", [request.session['email']])
                    row = cursor.fetchone()
                    request.session['user_id']=row[0]
                    request.session['first_name'] = row[2]
                    request.session['last_name'] = row[3]
                    request.session['image'] = row[7]
                    return redirect('ads_list')
                
            else:
                return render(request, 'accounts/verify_code.html', {'error': 'Invalid code'})
        else:
            return render(request, 'accounts/verify_code.html', {'error': 'Code has expired'})

def logout_view(request):
    request.session.pop('user_id', None)
    request.session.pop('first_name', None)
    request.session.pop('last_name', None)
    request.session.pop('image', None)
    return redirect('ads_list')