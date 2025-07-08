# labelpage/signals.py
print("labelpage.signals 已加载")  # 调试信息
import shutil
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User
from homepage.models import CsvData
from labelpage.utils import import_csv_for_user
import logging

logger = logging.getLogger('labelpage')


@receiver(post_save, sender=User)
def create_csv_for_user(sender, instance, created, **kwargs):
    if created:
        logger.debug(f"新用户创建: {instance.username}")
        print(f"新用户创建: {instance.username}")  # 调试信息

        original_file_path = os.path.join(settings.MEDIA_ROOT, 'flowrate_parameters.csv')
        user_directory = os.path.join(settings.MEDIA_ROOT, f'user_{instance.id}/csv_files/')
        os.makedirs(user_directory, exist_ok=True)

        user_file_path = os.path.join(user_directory, f'user_{instance.id}_flowrate_parameters.csv')

        if not os.path.exists(original_file_path):
            logger.error(f"原始 CSV 文件不存在: {original_file_path}")
            print(f"原始 CSV 文件不存在: {original_file_path}")
            return

        if not os.path.exists(user_file_path):
            shutil.copy(original_file_path, user_file_path)
            logger.debug(f"复制 CSV 文件到用户目录: {user_file_path}")
            print(f"复制 CSV 文件到用户目录: {user_file_path}")

        # 导入 CSV 数据
        import_csv_for_user(instance, user_file_path)