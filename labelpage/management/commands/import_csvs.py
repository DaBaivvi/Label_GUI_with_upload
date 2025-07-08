# labelpage/management/commands/import_csvs.py

from django.core.management.base import BaseCommand
from django.conf import settings
from homepage.models import CsvData
import pandas as pd
import os

class Command(BaseCommand):
    help = 'Import flowrate_parameters.csv from Resources directory into CsvData model as shared resource'

    def handle(self, *args, **kwargs):
        resources_dir = os.path.join(settings.BASE_DIR, 'Resources')
        filename = 'flowrate_parameters.csv'
        filepath = os.path.join(resources_dir, filename)

        if not os.path.exists(filepath):
            self.stdout.write(self.style.ERROR(f'CSV 文件不存在: {filepath}'))
            return

        # 检查是否已经导入
        if CsvData.objects.filter(image_filename=filename, is_resource=True).exists():
            self.stdout.write(self.style.NOTICE(f'共享资源 CSV 已存在: {filename}'))
            return

        try:
            df = pd.read_csv(filepath)

            # 定义所需的列
            required_columns = [
                'Time samples', 'Flowrate samples', 'Maximal Flow Rate (ml/s)',
                'Average Flow Rate(ml/s)', 'Increase Time (s)',
                'Total Volume Voided (ml)', 'Total Voiding Time (s)', 'Total Flow Time (s)',
                'Image Filename', 'Sex', 'Age'
            ]

            # 验证所需列是否存在
            for col in required_columns:
                if col not in df.columns:
                    raise KeyError(f"缺少必需的列: {col}")

            # 遍历每一行并创建 CsvData 实例
            for index, row in df.iterrows():
                # 提取行数据
                time_samples = row['Time samples']
                flowrate_samples = row['Flowrate samples']
                max_flow_rate = row['Maximal Flow Rate (ml/s)']
                average_flow_rate = row['Average Flow Rate(ml/s)']
                increase_time = row['Increase Time (s)']
                total_volume_voided = row['Total Volume Voided (ml)']
                total_voiding_time = row['Total Voiding Time (s)']
                total_flow_time = row['Total Flow Time (s)']
                image_filename = row['Image Filename']
                sex = row['Sex']        # 新增
                age = row['Age']


                # 在创建 CsvData 实例之前，检查 image_filename 是否已存在
                if CsvData.objects.filter(image_filename=image_filename).exists():
                    self.stdout.write(self.style.WARNING(f"跳过重复的 image_filename: {image_filename}"))
                    continue  # 跳过当前循环，处理下一行

                # 确保 'time_samples' 和 'flowrate_samples' 以逗号分隔的字符串形式存储
                # 根据您的 CSV 文件格式调整此部分
                if isinstance(time_samples, list):
                    time_samples = ','.join(map(str, time_samples))
                elif isinstance(time_samples, (float, int)):
                    time_samples = str(time_samples)
                else:
                    # 如果是字符串，不做处理
                    time_samples = str(time_samples)

                if isinstance(flowrate_samples, list):
                    flowrate_samples = ','.join(map(str, flowrate_samples))
                elif isinstance(flowrate_samples, (float, int)):
                    flowrate_samples = str(flowrate_samples)
                else:
                    # 如果是字符串，不做处理
                    flowrate_samples = str(flowrate_samples)

                # 生成唯一的 image_number
                existing_numbers = CsvData.objects.values_list('image_number', flat=True)
                if existing_numbers:
                    image_number = max(existing_numbers) + 1
                else:
                    image_number = 1

                # 创建 CsvData 实例
                try:
                    csv_data = CsvData.objects.create(
                        user=None,  # 共享资源 CSV 文件不关联特定用户
                        is_resource=True,
                        image_filename=image_filename,
                        image_number=image_number,
                        sex=sex,
                        age=age,
                        max_flow_rate=max_flow_rate,
                        max_flow_rate_unit='ml/s',
                        average_flow_rate=average_flow_rate,
                        average_flow_rate_unit='ml/s',
                        increase_time=increase_time,
                        increase_time_unit='s',
                        total_volume_voided=total_volume_voided,
                        total_volume_voided_unit='ml',
                        total_voiding_time=total_voiding_time,
                        total_voiding_time_unit='s',
                        total_flow_time=total_flow_time,
                        total_flow_time_unit='s',
                        time_samples=time_samples,
                        flowrate_samples=flowrate_samples,
                        csv_file=filename  # 存储文件名
                    )
                    self.stdout.write(self.style.SUCCESS(
                        f'成功导入共享资源 CSV: {filename}，图像编号={image_number}'
                    ))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"在 {filename} 的第 {index + 1} 行创建 CsvData 时出错: {e}"
                    ))
                    continue

        except KeyError as e:
            self.stdout.write(self.style.ERROR(f"CSV 解析错误: {e}"))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"读取 CSV 文件 {filename} 时出错: {e}"))
            return