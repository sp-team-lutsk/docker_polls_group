from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import StdUser, Profession, Faculty, Student


class StdUserAdmin(UserAdmin):
    model = StdUser

    list_display = ('email', 'username', 'is_staff', 'is_active', 'is_teacher', 'is_student')
    list_filter = ('email',)
    readonly_fields = ('date_joined', 'last_update', 'is_staff', 'is_active', 'is_admin',)
    
    fieldsets = (
            ('Personal Info', {
                'fields': ('email',
                           'username', 
                           'password', 
                           'first_name', 
                           'last_name',
                           'patronymic',
                           'bio',
                           'avatar',)
                }),
            ('Permissions', {
                'fields': ('is_active',
                           'is_staff',
                           'is_admin',
                           'is_student',
                           'is_teacher')
                }),
            ('Important Dates', {
                'fields': ('date_of_birth',
                           'date_joined',
                           'last_update',)
                }),
    )

    add_fieldsets = (
            (None, {
                'classes': ('wide', ),
                'fields': ('email',
                           'username',
                           'password1',
                           'password2',)
            }),
    )


admin.site.register(StdUser, StdUserAdmin)
admin.site.register(Student)

admin.site.register(Profession)
admin.site.register(Faculty)