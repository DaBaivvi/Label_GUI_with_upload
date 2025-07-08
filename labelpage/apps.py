from django.apps import AppConfig


class LabelpageConfig(AppConfig):
    
    name = 'labelpage'
    
    def ready(self):
        print("labelpage.apps.LabelpageConfig.ready() 被调用")  # 调试信息
        import labelpage.signals  # 导入信号处理器