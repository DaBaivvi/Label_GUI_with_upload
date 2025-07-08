from django.contrib import admin
from .models import Label

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user', 'label_type', 'abnormal_subtype', 'labeled_by', 'label_time')
    list_filter = ('label_type', 'abnormal_subtype', 'labeled_by')
    search_fields = ('labeled_by__username', 'label_type', 'csv_data__image_number',)
    
    def get_user(self, obj):
            return obj.labeled_by.username if obj.labeled_by else "No User"
    get_user.short_description = 'User'