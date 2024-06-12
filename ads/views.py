<<<<<<< HEAD
from django.shortcuts import render,redirect
from django.views.generic import TemplateView,DetailView
from django.db import connections


from django.template.response import TemplateResponse
from django.db import connections,connection


=======
from django.shortcuts import render
from django.views.generic import TemplateView,DetailView
from django.db import connections

from django.template.response import TemplateResponse
from django.db import connections,connection
from django.http import Http404

>>>>>>> 25138200c661c10e0f2ad703afa3b5e2c53041a1
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
<<<<<<< HEAD
                WHERE a.AD_STATUS='ACCEPTED'
=======
>>>>>>> 25138200c661c10e0f2ad703afa3b5e2c53041a1
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
<<<<<<< HEAD
    context_object_name = 'ad'

    def get_object(self):
        pk = self.kwargs['pk']
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
=======
    context_object_name='ad'

    def get_object(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM ads WHERE Ad_ID = %s", [self.kwargs['pk']])
            result = cursor.fetchone()
            if result:
                return dict(zip([col[0] for col in cursor.description], result))
            else:
                return {}  # or return a default ad object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
>>>>>>> 25138200c661c10e0f2ad703afa3b5e2c53041a1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def empty_url(request):
    return redirect("ads_list")