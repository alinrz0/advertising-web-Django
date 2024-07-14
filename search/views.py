from django.shortcuts import render
from django.views.generic import View
from django.db import connections,connection
from django.views.generic import TemplateView,DetailView,CreateView

from django.template.response import TemplateResponse

# Create your views here.
class SearchView(TemplateView):
    template_name = 'ads/ads_list.html'
    

    def post(self, request):
        query = request.POST.get('slug')
        city = request.POST.get('city')
        category = request.POST.get('category')
        

        with connections['default'].cursor() as cursor:
            query_sql = """
                SELECT a.*, i.IMG_Link,i.IMG_ID
                FROM mydb.ads a 
                LEFT JOIN ( 
                    SELECT Ad_ID, MIN(img_id) as min_img_id 
                    FROM img_of_ad 
                    GROUP BY Ad_ID 
                ) i_sub ON a.Ad_ID = i_sub.Ad_ID 
                LEFT JOIN img_of_ad i ON i_sub.Ad_ID = i.Ad_ID AND i_sub.min_img_id = i.img_id 
                WHERE a.AD_STATUS='ACCEPTED' AND a.Deleted_at IS NULL
            """

            if query:
                print("a")
                query_sql += " AND (a.Title LIKE %s )"
                cursor.execute(query_sql, ['%' + query + '%'])
            # elif city:
            #     print(city)
            #     print("d")
            #     query_sql += " AND (a.City_ID=  %s )"
            #     cursor.execute(query_sql, ['%' + query + '%'])
            # elif category:
            #     query_sql += " AND (a.Category_ID=  %s )"
            #     cursor.execute(query_sql, ['%' + query + '%'])
            else:
                print("c")
                cursor.execute(query_sql)


            rows = self.dictfetchall(cursor)
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM city")
                cities = self.dictfetchall(cursor)
                
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM ad_category")
                category = self.dictfetchall(cursor)
            
            
        return TemplateResponse(request, self.template_name, {'ads': rows,'cities':cities,'category':category})

    def dictfetchall(self, cursor):
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]