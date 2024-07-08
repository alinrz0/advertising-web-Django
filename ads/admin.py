from django import forms
from django.contrib import admin
from . import models
from datetime import datetime
from django.contrib.auth import get_user_model
from django.db.models import Case, When, Value

class AdCategoryAdmin(admin.ModelAdmin):
    list_display=["category_name"]
admin.site.register(models.AdCategory,AdCategoryAdmin)

class BusinessCategoryAdmin(admin.ModelAdmin):
    list_display=["business_category_name"]
admin.site.register(models.BusinessCategory,BusinessCategoryAdmin)

class CityAdmin(admin.ModelAdmin):
    list_display=["city_name","province"]
admin.site.register(models.City,CityAdmin)

class ProvinceAdmin(admin.ModelAdmin):
    list_display=["province_name"]
admin.site.register(models.Province,ProvinceAdmin)

class ReportKindAdmin(admin.ModelAdmin):
    list_display=["report_kind_name"]
admin.site.register(models.ReportKind,ReportKindAdmin)

class AdStatusInline(admin.TabularInline):
    model = models.AdStatus
    fields = ('note', 'status')
    extra=1
    can_delete=False

    def has_change_permission(self, request, obj=None):
        return False
    
class AdsOfUserInline(admin.TabularInline):
    model = models.AdsOfUsers
    fields = ('user',)
    readonly_fields=('user',)
    extra=1
    can_delete=False
    
class AdsOfBusinessInline(admin.TabularInline):
    model = models.AdsOfBusiness
    fields = ('business',)
    readonly_fields=('business',)
    extra=1
    can_delete=False
    
class AdsAdmin(admin.ModelAdmin):
    readonly_fields = ('ad_status','title', 'info', 'add_time', 'price', 'city_id', 'category', 'views', 'identifier')
    fields =  ('ad_status','title', 'info', 'add_time', 'price', 'city_id', 'category', 'views', 'identifier','deleted_at')
    list_display = ["title","ad_status"]
    inlines = [AdStatusInline,AdsOfUserInline,AdsOfBusinessInline]
    def has_add_permission(self, request):
        return False
    
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.ad = form.instance
            instance.suporter = request.user
            instance.edit_time=datetime.now()
            instance.save()
            form.instance.ad_status = instance.status
            form.instance.save()
        formset.save_m2m()
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by(
            Case(
                When(ad_status='WAITING', then=Value(0)),
                default=Value(1)
            ),
            'ad_status'
        )
        

admin.site.register(models.Ads, AdsAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display=["first_name" ,"last_name"]
admin.site.register(models.Users,UserAdmin)

class AdReportAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    readonly_fields=("note_report","report_kind","reporter","ad")
    
admin.site.register(models.AdReports,AdReportAdmin)