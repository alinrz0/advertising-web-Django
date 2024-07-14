from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.views.generic import View
from django.db import connection
import random
import datetime
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import SignUpForm
from django.core.cache import cache

class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        email = request.POST.get('email')
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE Email = %s", (email,))
            user = cursor.fetchone()
            if user:
                cache.set(f'verification_code:{email}', str(random.randint(100000, 999999)), 120)
                print(cache.get(f'verification_code:{email}'))
                request.session['email'] = email
                return redirect('verify_code')
            else:
                return render(request, 'accounts/login.html', {'error': 'Email not found'})


class VerifyCodeView(View):
    def get(self, request):
        if 'email' not in request.session:
            return redirect('login')
        return render(request, 'accounts/verify_code.html')

    def post(self, request):
        code = request.POST.get('code')
        email = request.session['email']
        stored_code = cache.get(f'verification_code:{email}')
        if stored_code:
            if code == stored_code:
                cache.delete(f'verification_code:{email}')  
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM users WHERE Email = %s", [email])
                    row = cursor.fetchone()
                    if row:
                        # User already exists, just update the session
                        request.session['user_id'] = row[0]
                        request.session['first_name'] = row[2]
                        request.session['last_name'] = row[3]
                        request.session['image'] = row[7]
                    else:
                        # Insert new user
                        first_name = request.session['first_name']
                        last_name = request.session['last_name']
                        phone_number = request.session['phone_number']
                        city_id = request.session['city_id']
                        cursor.execute("""
                            INSERT INTO users (First_Name, Last_Name, Email, Phone_Number, City_ID) 
                            VALUES (%s, %s, %s, %s, %s)
                        """, [first_name, last_name, email, phone_number, city_id])
                        cursor.execute("SELECT * FROM users WHERE Email = %s", [email])
                        row = cursor.fetchone()
                        request.session['user_id'] = row[0]
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
    request.session.pop('email', None)
    return redirect('ads_list')


class SignUpView(FormView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('verify_code')

    def form_valid(self, form):
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        phone_number = form.cleaned_data['phoneNumber']
        city_id = form.cleaned_data['city']

        with connection.cursor() as cursor:
            # Check for existing user with same email or phone number
            cursor.execute("""
                SELECT COUNT(*) FROM users 
                WHERE Email = %s OR Phone_Number = %s
            """, [email, phone_number])
            count = cursor.fetchone()[0]

            if count > 0:
                form.add_error('email', 'A user with this email or phone number already exists.')
                return self.form_invalid(form)

            # Insert new user if no duplicate is found
            self.request.session['first_name']=first_name
            self.request.session['last_name']=last_name
            self.request.session['phone_number']=phone_number
            self.request.session['city_id']=city_id
            self.request.session['email'] = email
            cache.set(f'verification_code:{email}', str(random.randint(100000, 999999)), 120)
            print(cache.get(f'verification_code:{email}'))
            
            
        
        return super().form_valid(form)

    def form_invalid(self, form):
        # If form is invalid, render the form with errors
        return render(self.request, self.template_name, {'form': form})
    
class ProfileView(View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        if 'user_id' not in request.session:
            return redirect('login')
        user_id = request.session['user_id']

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE User_ID = %s", [user_id])
            profile_data = cursor.fetchone()

        return render(request, self.template_name, {'profile_data': profile_data})

    def post(self, request):
        if 'user_id' not in request.session:
            return redirect('login')
        user_id = request.session['user_id']

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE Email = %s AND User_ID!= %s", [email, user_id])
            email_exists = cursor.fetchone()
            cursor.execute("SELECT * FROM users WHERE Phone_Number = %s AND User_ID!= %s", [phone_number, user_id])
            phone_number_exists = cursor.fetchone()

        if email_exists:
            return render(request, self.template_name, {'profile_data': None, 'error': 'Email is already in use'})
        elif phone_number_exists:
            return render(request, self.template_name, {'profile_data': None, 'error': 'Phone number is already in use'})
        else:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE users SET First_Name = %s, Last_Name = %s, Email = %s, Phone_Number = %s WHERE User_ID = %s", [first_name, last_name, email, phone_number, user_id])
                connection.commit()
            return redirect('profile')