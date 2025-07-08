# homepage/models.py

from django.db import models
from django.contrib.auth.models import User
import os


def user_csv_file_path(instance, filename):
    """
    文件将上传到 MEDIA_ROOT/user_<id>/csv_files/<filename>
    """
    return f'user_{instance.user.id}/csv_files/{filename}'

class CsvData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='csv_data', null=True, blank=True)
    
    image_filename = models.CharField(max_length=255)
    image_number = models.IntegerField()

    sex = models.CharField(max_length=20, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    
    max_flow_rate = models.FloatField()
    max_flow_rate_unit = models.CharField(max_length=20, default='ml/s')
    
    average_flow_rate = models.FloatField()
    average_flow_rate_unit = models.CharField(max_length=20, default='ml/s')
    
    increase_time = models.FloatField()
    increase_time_unit = models.CharField(max_length=20, default='s')
    
    total_volume_voided = models.FloatField()
    total_volume_voided_unit = models.CharField(max_length=20, default='ml')
    
    total_voiding_time = models.FloatField()
    total_voiding_time_unit = models.CharField(max_length=20, default='s')
    
    total_flow_time = models.FloatField()
    total_flow_time_unit = models.CharField(max_length=20, default='s')

    time_samples = models.TextField()         
    flowrate_samples = models.TextField()      
    
    # 存储 CSV 文件的字段（文件上传）
    csv_file = models.FileField(upload_to=user_csv_file_path, null=True, blank=True) 

    # 新增字段
    created_at = models.DateTimeField(auto_now_add=True)  # 记录创建时间
    updated_at = models.DateTimeField(auto_now=True)      # 记录更新时间

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'image_filename'], name='unique_user_csv')  # 每个用户和文件的组合唯一
        ]
    
    def get_label(self):  
        return self.labels.all()
    

    def __str__(self):
        return f"CSV {self.image_number} - {self.image_filename} for {self.user.username}"
    