import os
import django

# 设置 DJANGO_SETTINGS_MODULE 环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Label_GUI.settings")

# 初始化 Django
django.setup()

import os
from django.conf import settings
from homepage.models import CsvData

def cleanup_orphan_files():
    media_root = settings.MEDIA_ROOT
    csv_files = set(CsvData.objects.values_list('csv_file', flat=True))

    for root, dirs, files in os.walk(os.path.join(media_root, 'user_')):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, media_root)
            if relative_path not in csv_files:
                os.remove(file_path)
                print(f"已删除孤立文件: {file_path}")

if __name__ == "__main__":
    cleanup_orphan_files()