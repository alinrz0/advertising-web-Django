from django.shortcuts import render
from django.views.generic import TemplateView,DetailView
from django.db import connections

from django.template.response import TemplateResponse
from django.db import connections,connection
from django.http import Http404

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

# import mysql.connector
# from django.shortcuts import render



# # Create your views here.

# def get (request):
#     ads = get_ads_from_database()
#     return render(request, 'ads/ads_list.html', {'ads': ads})



# def get_ads_from_database():
#     # Connect to MySQL database
#     connection = mysql.connector.connect(
#         host="127.0.0.1",
#         user="root",
#         password="ermi1ermi2ermi123",
#         database="mydb"
#     )
#     cursor = connection.cursor()

#     # Fetch ads from database
#     cursor.execute("SELECT title FROM ads")
#     ads = cursor.fetchall()

#     connection.close()
#     return ads



