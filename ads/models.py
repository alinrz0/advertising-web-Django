from django.db import models
from django.conf import settings
class AdCategory(models.Model):
    ad_category_id = models.AutoField(db_column='Ad_Category_ID', primary_key=True)  # Field name made lowercase.
    category_name = models.CharField(db_column='Category_Name', max_length=55)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ad_category'
        
    def __str__(self) :
        return self.category_name
        
class City(models.Model):
    city_id = models.AutoField(db_column='City_ID', primary_key=True)  # Field name made lowercase.
    city_name = models.CharField(db_column='City_Name', max_length=55)  # Field name made lowercase.
    province = models.ForeignKey('Province', models.DO_NOTHING, db_column='Province_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'city'
        
    def __str__(self) :
        return self.city_name
    
class Ads(models.Model):
    ad_id = models.AutoField(db_column='Ad_ID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=55)  # Field name made lowercase.
    ad_status = models.CharField(db_column='Ad_STATUS', max_length=10, blank=False, null=False ,choices=[("ACCEPTED", "ACCEPTED"),("UNACCEPTED", "UNACCEPTED")])  # Field name made lowercase.
    info = models.CharField(db_column='INFO', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    add_time = models.DateTimeField(db_column='Add_Time', blank=True, null=True)  # Field name made lowercase.
    price = models.IntegerField(db_column='Price')  # Field name made lowercase.
    city_id = models.ForeignKey(City , models.DO_NOTHING ,db_column='City_ID')  # Field name made lowercase.
    category = models.ForeignKey(AdCategory, models.DO_NOTHING, db_column='Category_ID')  # Field name made lowercase.
    views = models.IntegerField(db_column='Views', blank=True, null=True)  # Field name made lowercase.
    identifier = models.CharField(db_column='Identifier', max_length=8, blank=True, null=True,choices=[("USER", "USER"),("BUSINESS", "BUSINESS")])  # Field name made lowercase.
    deleted_at = models.DateTimeField(db_column='Deleted_at', blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'ads'




class AdReports(models.Model):
    ad_report_id = models.AutoField(db_column='Ad_Report_ID', primary_key=True)  # Field name made lowercase.
    note_report = models.CharField(db_column='Note_Report', max_length=1000)  # Field name made lowercase.
    report_kind = models.ForeignKey('ReportKind', models.DO_NOTHING, db_column='Report_Kind_ID')  # Field name made lowercase.
    reporter = models.ForeignKey('Users', models.DO_NOTHING, db_column='Reporter_ID')  # Field name made lowercase.
    ad = models.ForeignKey('Ads', models.DO_NOTHING, db_column='Ad_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ad_reports'


class AdStatus(models.Model):
    ad_status_id = models.AutoField(db_column='Ad_Status_ID', primary_key=True)  # Field name made lowercase.
    ad = models.ForeignKey('Ads', models.DO_NOTHING, db_column='Ad_ID')  # Field name made lowercase.
    edit_time = models.DateTimeField(db_column='Edit_Time', blank=True, null=True)  # Field name made lowercase.
    suporter = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='Suporter_ID')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=10, blank=False, null=False ,choices=[("ACCEPTED", "ACCEPTED"),("UNACCEPTED", "UNACCEPTED")])  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=1000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ad_status'




class AdsOfBusiness(models.Model):
    ad = models.OneToOneField(Ads, models.DO_NOTHING, db_column='Ad_ID', primary_key=True)  # Field name made lowercase.
    business = models.ForeignKey('Business', models.DO_NOTHING, db_column='Business_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ads_of_business'


class AdsOfUsers(models.Model):
    ad = models.OneToOneField(Ads, models.DO_NOTHING, db_column='Ad_ID', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='User_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ads_of_users'


        
class ImgOfAd(models.Model):
    img_id = models.AutoField(db_column='IMG_ID', primary_key=True)  # Field name made lowercase.
    img_link = models.CharField(db_column='IMG_Link', max_length=255)  # Field name made lowercase.
    ad = models.ForeignKey(Ads, models.DO_NOTHING, db_column='Ad_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'img_of_ad'


class Meta(models.Model):
    meta_id = models.AutoField(db_column='Meta_ID', primary_key=True)  # Field name made lowercase.
    key = models.CharField(max_length=55)
    value = models.CharField(max_length=55)
    ad = models.ForeignKey(Ads, models.DO_NOTHING, db_column='Ad_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'meta'


class Province(models.Model):
    province_id = models.AutoField(db_column='Province_ID', primary_key=True)  # Field name made lowercase.
    province_name = models.CharField(db_column='Province_Name', unique=True, max_length=55)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'province'
        
    def __str__(self) :
        return self.province_name


class ReportKind(models.Model):
    report_kind_id = models.AutoField(db_column='Report_Kind_ID', primary_key=True)  # Field name made lowercase.
    report_kind_name = models.CharField(db_column='Report_Kind_Name', max_length=55)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'report_kind'
        
    def __str__(self) :
        return self.report_kind_name
        
class Users(models.Model):
    user_id = models.AutoField(db_column='User_ID', primary_key=True)  # Field name made lowercase.
    user_status = models.CharField(db_column='User_Status', max_length=8)  # Field name made lowercase.
    first_name = models.CharField(db_column='First_Name', max_length=55)  # Field name made lowercase.
    last_name = models.CharField(db_column='Last_Name', max_length=55)  # Field name made lowercase.
    phone_number = models.CharField(db_column='Phone_Number', unique=True, max_length=55)  # Field name made lowercase.
    email = models.CharField(db_column='Email', unique=True, max_length=255)  # Field name made lowercase.
    city_id = models.IntegerField(db_column='City_ID')  # Field name made lowercase.
    profile_img = models.CharField(db_column='Profile_IMG', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    user_kind = models.CharField(db_column='User_Kind', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'users'
        
    def __str__(self) :
        return self.first_name+" "+self.last_name
    
class Business(models.Model):
    business_id = models.AutoField(db_column='Business_ID', primary_key=True)  # Field name made lowercase.
    business_name = models.CharField(db_column='Business_Name', max_length=55)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=255)  # Field name made lowercase.
    registeration_code = models.CharField(db_column='Registeration_Code', unique=True, max_length=55)  # Field name made lowercase.
    business_category = models.ForeignKey('BusinessCategory', models.DO_NOTHING, db_column='Business_Category_ID')  # Field name made lowercase.
    deleted_at = models.DateTimeField(db_column='Deleted_at', blank=True, null=True)  # Field name made lowercase.
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='User_ID')  # Field name made lowercase.
    city = models.ForeignKey('City', models.DO_NOTHING, db_column='City_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'business'
        
    


class BusinessCategory(models.Model):
    business_category_id = models.AutoField(db_column='Business_Category_ID', primary_key=True)  # Field name made lowercase.
    business_category_name = models.CharField(db_column='Business_Category_Name', unique=True, max_length=55)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'business_category'
        
    def __str__(self) :
        return self.business_category_name
    
class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'
# Create your models here.
