from django import forms
from django.contrib import admin
from . import models
from datetime import datetime
from django.contrib.auth import get_user_model


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
    fields = ('note', 'suporter')
    extra=1
    
class AdsAdmin(admin.ModelAdmin):
    readonly_fields = ('title', 'info', 'add_time', 'price', 'city_id', 'category', 'views', 'identifier')
    fields = ('ad_status',) + readonly_fields
    list_display = ["title"]
    inlines = [AdStatusInline]
    def has_add_permission(self, request):
        return False
    
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.ad = form.instance
            instance.suporter = request.user
            instance.status = form.instance.ad_status
            instance.edit_time=datetime.now()
            instance.save()
        formset.save_m2m()
        

admin.site.register(models.Ads, AdsAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display=["first_name" ,"last_name"]
admin.site.register(models.Users,UserAdmin)