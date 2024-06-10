from django.shortcuts import render
from django.views.generic import ListView
from django.db import connections

class AdListView(ListView):
    template_name = 'ads/ads_list.html'
    context_object_name = "ads"

    def get_queryset(self):
        with connections['default'].cursor() as cursor:
            query="SELECT a.*, i.* FROM mydb.ads a LEFT JOIN ( SELECT Ad_ID, MIN(img_id) as min_img_id FROM img_of_ad GROUP BY Ad_ID ) i_sub ON a.Ad_ID = i_sub.Ad_ID LEFT JOIN img_of_ad i ON i_sub.Ad_ID = i.Ad_ID AND i_sub.min_img_id = i.img_id;"
            cursor.execute(query)
            rows = self.dictfetchall(cursor)
        return rows

    def dictfetchall(self, cursor):
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]






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



