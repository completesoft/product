from django.contrib import admin
from .models import Person, Residence_address, Experience, Education, MailToAddress, MailBackSettings, Location


class ResidenceInline(admin.TabularInline):
    model = Residence_address
    extra = 0


class ExpirienceInline(admin.StackedInline):
    model = Experience
    extra = 0
    fields = [
        ('exp_start_date', 'exp_end_date'),
        ('workplace', 'exp_position', 'exp_salary'),
        ('responsibility', 'reason_leaving')
    ]


class EducationInline(admin.TabularInline):
    model = Education
    extra = 0


class PersonAdmin(admin.ModelAdmin):
    inlines = [ResidenceInline, EducationInline, ExpirienceInline]

    # resource_class = PersonResource
    list_display = ['full_name', 'fill_date', 'position', 'email_send', 'fill_location']
    list_filter = ['fill_date', 'position']
    search_fields = ['full_name', 'position']


    fieldsets = [
        ('Личные данные:', {'fields':[('start', 'fill_location', 'source_about_as'), ('position', 'full_name', 'birthday'), 'gender', 'registration', 'residenceBool']}),
        ('Контакты:',{'fields':['phone']}),
        ('Семья:', {'fields': [('civil_status', 'quant_children')]}),
        ('Паспортные данные:', {'fields': ['passp_number', 'passp_issue', 'passp_date']}),
        ('Рекомендатель №1:', {'fields': [('ref1_full_name', 'ref1_position', 'ref1_workplace', 'ref1_phone')]}),
        ('Рекомендатель №2:', {'fields': [('ref2_full_name', 'ref2_position', 'ref2_workplace', 'ref2_phone')]}),
        ('Дополнительные сведения:', {'fields': ['army', 'army_id', 'driver_lic', 'car', 'advantage', 'disadvantage', 'convicted', 'illness', 'add_details', 'salary']}),
    ]



class MailToAddressAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email_address']


class MailBackSettingsAdmin(admin.ModelAdmin):
    list_display = ['id', 'email_host', 'email_host_user', 'email_use_tls', 'email_port', 'default']

class LocationAdmin(admin.ModelAdmin):
    list_display = ['loc_id', 'describe']
    filter_horizontal = ['mail_to']

admin.site.register(Location, LocationAdmin)
admin.site.register(Person, PersonAdmin)
# admin.site.register(Residence_address)
# admin.site.register(Experience)
# admin.site.register(Education)
admin.site.register(MailToAddress, MailToAddressAdmin)
admin.site.register(MailBackSettings, MailBackSettingsAdmin)


#############

from django.contrib import admin
from .models import CvStatusName, CvState


# class CvStateAdmin(admin.ModelAdmin):
#     list_display = ('full_name', 'position', 'status')


# admin.site.register(CvState, CvStateAdmin)
admin.site.register(CvStatusName)