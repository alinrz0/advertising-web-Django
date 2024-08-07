# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AdCategory(models.Model):
    ad_category_id = models.AutoField(db_column='Ad_Category_ID', primary_key=True)  # Field name made lowercase.
    category_name = models.CharField(db_column='Category_Name', max_length=55)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ad_category'


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
    suporter = models.ForeignKey('Users', models.DO_NOTHING, db_column='Suporter_ID')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=10, blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=1000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ad_status'


class Ads(models.Model):
    ad_id = models.AutoField(db_column='Ad_ID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=55)  # Field name made lowercase.
    ad_status = models.CharField(db_column='Ad_STATUS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    info = models.CharField(db_column='INFO', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    add_time = models.DateTimeField(db_column='Add_Time', blank=True, null=True)  # Field name made lowercase.
    price = models.IntegerField(db_column='Price')  # Field name made lowercase.
    city_id = models.IntegerField(db_column='City_ID')  # Field name made lowercase.
    category = models.ForeignKey(AdCategory, models.DO_NOTHING, db_column='Category_ID')  # Field name made lowercase.
    views = models.IntegerField(db_column='Views', blank=True, null=True)  # Field name made lowercase.
    identifier = models.CharField(db_column='Identifier', max_length=8, blank=True, null=True)  # Field name made lowercase.
    deleted_at = models.DateTimeField(db_column='Deleted_at', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ads'


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


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


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


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


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


class City(models.Model):
    city_id = models.AutoField(db_column='City_ID', primary_key=True)  # Field name made lowercase.
    city_name = models.CharField(db_column='City_Name', max_length=55)  # Field name made lowercase.
    province = models.ForeignKey('Province', models.DO_NOTHING, db_column='Province_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'city'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


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


class ReportKind(models.Model):
    report_kind_id = models.AutoField(db_column='Report_Kind_ID', primary_key=True)  # Field name made lowercase.
    report_kind_name = models.CharField(db_column='Report_Kind_Name', max_length=55)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'report_kind'


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
