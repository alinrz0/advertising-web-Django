from django.shortcuts import render,redirect
from django.views.generic import CreateView
from django.db import connection

# Create your views here.

class CreateBusinessView(CreateView):
    template_name = 'business/create_business.html'
    success_url = '/ads'  # redirect to ad list after creation

    def get(self, request, *args, **kwargs):
        if 'user_id' in request.session:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM city")
                cities = cursor.fetchall()
                cursor.execute("SELECT * FROM business_category")
                categories = cursor.fetchall()
            return render(request, self.template_name, {'cities':cities,'categories':categories})
        else:
            return redirect('/accounts/login')
    
    def post(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            # Insert ad data
            cursor.execute("""
                INSERT INTO business (Business_Name, Address, Registeration_Code, City_ID, Business_Category_ID, User_ID)
                VALUES (%s, %s, %s, %s, %s, %s
                )
            """, [
                request.POST['name'],
                request.POST['address'],
                request.POST['Registeration_Code'],
                request.POST['city_id'],
                request.POST['category_id'],
                request.session['user_id']
            ])


        return redirect(self.success_url)