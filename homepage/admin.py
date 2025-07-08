# homepage/admin.py

from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from .models import CsvData
from labelpage.models import Label

class CsvDataResource(resources.ModelResource):
    # 定义一个自定义字段 'Labels' 来存储关联的 Label 类型
    Labels = fields.Field()

    # 定义一个自定义字段 'Username' 来显示用户的用户名
    Username = fields.Field(attribute='user__username', column_name='Username')

    class Meta:
        model = CsvData
        fields = (
            'image_number',
            'Username',
            'sex',
            'age',
            'Labels',
            'max_flow_rate',
            'average_flow_rate',
            'total_volume_voided',
            'increase_time',
            'total_voiding_time',
            'total_flow_time',
            'time_samples',
            'flowrate_samples',
            'image_filename',
        )
        export_order = (
            'image_number',
            'Username',
            'sex',
            'age',
            'Labels',
            'max_flow_rate',
            'average_flow_rate',
            'total_volume_voided',
            'increase_time',
            'total_voiding_time',
            'total_flow_time',
            'time_samples',
            'flowrate_samples',
            'image_filename',
        )

    #def dehydrate_Labels(self, obj):
        # 将关联的所有 Label 类型以逗号分隔的字符串形式返回
       # return ", ".join([label.label_type for label in obj.labels.all()])

    def dehydrate_Labels(self, obj):
            # 将关联的所有 Label 类型和 subtype 以逗号分隔的字符串形式返回
            return ", ".join([
                f"{label.get_label_type_display()} - {label.abnormal_subtype}" if label.label_type == 'abnormal' and label.abnormal_subtype
                else label.get_label_type_display()
                for label in obj.labels.all()
            ])
    
    

# 使用 @admin.register 装饰器注册 CsvDataAdmin
@admin.register(CsvData)
class CsvDataAdmin(ImportExportModelAdmin):
    resource_class = CsvDataResource

    list_display = (
        'image_number',
        'user',
        'get_labels',
        'sex',
        'age',
        'max_flow_rate',
        'average_flow_rate',
        'total_volume_voided',
        'increase_time',
        'total_voiding_time',
        'total_flow_time',
        # 保留 'id', 'created_at', 'updated_at' 如果需要在列表中显示
        'id',
        'created_at',
        'updated_at',
        'image_filename',
        'time_samples',
        'flowrate_samples',
    )
    #list_filter = ('user', 'created_at', 'updated_at')
    #search_fields = ('image_number', 'user__username')

    list_filter = ('user', 'labels__label_type', 'labels__abnormal_subtype', 'created_at', 'updated_at')
    search_fields = ('image_number', 'user__username', 'labels__label_type', 'labels__abnormal_subtype')

    def get_labels(self, obj):
        # 使用 label_type 和 abnormal_subtype 提取并格式化 Labels
        return ", ".join([
            f"{label.get_label_type_display()} - {label.abnormal_subtype}" if label.label_type == 'abnormal' and label.abnormal_subtype
            else label.get_label_type_display()
            for label in obj.labels.all()
        ])
    get_labels.short_description = 'Labels'

    # 优化查询以提高性能
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('labels')





    #def get_labels(self, obj):
        #return ", ".join([label.label_type for label in obj.labels.all()])
    #get_labels.short_description = 'Labels'