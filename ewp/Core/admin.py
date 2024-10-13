from django.contrib import admin
from .models import Profile

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'phone_number', 'date_of_birth', 'created_at')
    list_filter = ('created_at', 'date_of_birth')
    search_fields = ('user__username', 'bio', 'phone_number')
    ordering = ('created_at',)
    readonly_fields = ('created_at',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user') 

admin.site.register(Profile, ProfileAdmin)
