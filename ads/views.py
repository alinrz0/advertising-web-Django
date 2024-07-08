from django.shortcuts import render,redirect
from django.views.generic import TemplateView,DetailView,CreateView
import datetime
from django.core.files.storage import FileSystemStorage
from django.template.response import TemplateResponse
from django.db import connections,connection
from django.http import JsonResponse
from django.urls import reverse

class AdListView(TemplateView):
    template_name = 'ads/ads_list.html'

    def get(self, request):
        with connections['default'].cursor() as cursor:
            query = """
                SELECT a.*, i.IMG_Link,i.IMG_ID
                FROM mydb.ads a 
                LEFT JOIN ( 
                    SELECT Ad_ID, MIN(img_id) as min_img_id 
                    FROM img_of_ad 
                    GROUP BY Ad_ID 
                ) i_sub ON a.Ad_ID = i_sub.Ad_ID 
                LEFT JOIN img_of_ad i ON i_sub.Ad_ID = i.Ad_ID AND i_sub.min_img_id = i.img_id 
                WHERE a.AD_STATUS='ACCEPTED' AND a.Deleted_at IS NULL
                ORDER BY a.Add_Time DESC;
            """
            cursor.execute(query)
            rows = self.dictfetchall(cursor)
        return TemplateResponse(request, self.template_name, {'ads': rows})

    def dictfetchall(self, cursor):
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]



class AdDetailView(DetailView):
    template_name = 'ads/ad_detail.html'
    context_object_name = 'ad'

    def increment_view_count(self, ad_id):
            with connection.cursor() as cursor:
                cursor.execute("UPDATE ads SET Views = Views + 1 WHERE Ad_ID = %s", [ad_id])
                
    def get_object(self):
        pk = self.kwargs['pk']
        self.increment_view_count(pk)
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM ads WHERE Ad_ID = %s ", [pk])
            result = cursor.fetchone()
            if result:
                identifier = result[9]
                if identifier == 'USER':
                    cursor.execute("SELECT a.*, u.First_Name ,u.Last_Name, u.Phone_Number, c.City_Name,p.Province_Name,ac.Category_Name  FROM ads a JOIN ads_of_users au ON a.Ad_ID=au.Ad_ID JOIN users u ON au.User_ID=u.User_ID JOIN city c ON a.City_ID=c.City_ID JOIN province p ON c.Province_ID=p.Province_ID JOIN ad_category ac ON ac.Ad_Category_ID=a.Category_ID WHERE a.Ad_ID = %s", [pk])
                    user_result = cursor.fetchone()
                    ad_data=dict(zip([col[0] for col in cursor.description], result), **dict(zip([col[0] for col in cursor.description], user_result)))
                elif identifier == 'BUSINESS':
                    cursor.execute("SELECT a.* ,b.Business_Name,b.Address,c.City_Name,p.Province_Name,ac.Category_Name FROM ads a JOIN ads_of_business ab ON a.Ad_ID=ab.Ad_ID JOIN business b ON ab.Business_ID=b.Business_ID JOIN city c ON a.City_ID=c.City_ID JOIN province p ON c.Province_ID=p.Province_ID JOIN ad_category ac ON ac.Ad_Category_ID=a.Category_ID WHERE a.Ad_ID = %s", [pk])
                    business_result = cursor.fetchone()
                    ad_data=dict(zip([col[0] for col in cursor.description], result), **dict(zip([col[0] for col in cursor.description], business_result)))
                else:
                    ad_data=dict(zip([col[0] for col in cursor.description], result))
                # Retrieve img_of_ad data
                cursor.execute("SELECT * FROM img_of_ad WHERE Ad_ID = %s", [pk])
                img_of_ad_results = cursor.fetchall()
                ad_data['img_of_ad'] = [dict(zip([col[0] for col in cursor.description], row)) for row in img_of_ad_results]

                # Retrieve meta data
                cursor.execute("SELECT * FROM meta WHERE Ad_ID = %s", [pk])
                meta_results = cursor.fetchall()
                ad_data['meta'] = [dict(zip([col[0] for col in cursor.description], row)) for row in meta_results]
                return ad_data
            else:
                return {}  # or return a default ad object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM report_kind")
            report_kinds = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
        context['report_kinds'] = report_kinds
        return context
    
    
    def post(self, request, *args, **kwargs):
        report_note = request.POST.get('report_note')
        report_kind = request.POST.get('report_kind')
        user_id=request.session.get('user_id')
        with connection.cursor() as cursor:
            # Insert ad data
            cursor.execute("""
                INSERT INTO ad_reports (Note_Report, Report_Kind_ID, Reporter_ID, Ad_ID)
                VALUES (%s, %s, %s, %s
                )
            """, [
                report_note,
                report_kind,
                user_id,
                self.kwargs['pk']
            ])
        return redirect(reverse('ad_detail', args=(self.kwargs['slug'],self.kwargs['pk'])))
    
def empty_url(request):
    return redirect("ads_list")


class CreateAdView(CreateView):
    template_name = 'ads/create_ad.html'
    success_url = '/ads'  # redirect to ad list after creation

    def get(self, request, *args, **kwargs):
        if 'user_id' in request.session:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM city")
                cities = cursor.fetchall()
                cursor.execute("SELECT * FROM ad_category")
                categories = cursor.fetchall()
            return render(request, self.template_name, {'cities':cities,'categories':categories})
        else:
            return redirect('/accounts/login')
    
    def post(self, request, *args, **kwargs):
        identifier=request.GET.get('identifier','USER')
        with connection.cursor() as cursor:
            # Insert ad data
            cursor.execute("""
                INSERT INTO ads (Title, INFO, Price, City_ID, Category_ID, Identifier)
                VALUES (%s, %s, %s, %s, %s, %s
                )
            """, [
                request.POST['title'],
                request.POST['description'],
                request.POST['price'],
                request.POST['city_id'],
                request.POST['category_id'],
                identifier
            ])
            cursor.execute("SELECT LAST_INSERT_ID()")
            ad_id = cursor.fetchone()[0]

            # Insert user or business data
            if identifier == 'USER':
                cursor.execute("""
                    INSERT INTO ads_of_users (Ad_ID, User_ID)
                    VALUES (%s, %s)
                """, [ad_id, request.session['user_id']])
                
            # elif request.POST['identifier'] == 'BUSINESS':
            #     cursor.execute("""
            #         INSERT INTO ads_of_business (Ad_ID, Business_ID)
            #         VALUES (%s, %s)
            #     """, [ad_id, request.POST['business_id']])
                
                
            # # Insert img_of_ad data
            fs = FileSystemStorage(location='static/img', base_url='/static/img/')
            for img in request.FILES.getlist('images'):
                filename = fs.save(img.name, img)
                uploaded_file_url = fs.url(filename).replace('/static/img/', 'img/')
                
                cursor.execute("""
                    INSERT INTO img_of_ad (Ad_ID, IMG_Link)
                    VALUES (%s, %s)
                """, [ad_id, uploaded_file_url])

            # # Insert meta data
            for i in range(0, len(request.POST.getlist('meta[]')), 2):
                meta_key = request.POST.getlist('meta[]')[i]
                meta_value = request.POST.getlist('meta[]')[i+1]
                cursor.execute("""
                    INSERT INTO meta (Ad_ID, `key`, value)
                    VALUES (%s, %s, %s)
                """, [ad_id, meta_key, meta_value])


        return redirect(self.success_url)
    
    
