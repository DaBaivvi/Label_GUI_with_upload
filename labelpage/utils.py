# labelpage/utils.py

import pandas as pd
import os
from django.conf import settings
from homepage.models import CsvData
from django.db import transaction
import logging

logger = logging.getLogger('labelpage')


def import_csv_for_user(user, csv_file_path):
    """
    导入用户的 CSV 数据到数据库。
    """
    logger.debug(f"开始为用户 {user.username} 导入 CSV 数据")
    print(f"开始为用户 {user.username} 导入 CSV 数据")  # 调试信息
    logger.debug(f"CSV 文件路径: {csv_file_path}")
    
    if not os.path.exists(csv_file_path):
        print(f"CSV 文件不存在: {csv_file_path}")
        logger.error(f"CSV 文件不存在: {csv_file_path}")
        return
    
    try:
        df = pd.read_csv(csv_file_path)
        
        required_columns = [
            'Time samples', 'Flowrate samples', 'Maximal Flow Rate (ml/s)',
            'Average Flow Rate(ml/s)', 'Increase Time (s)',
            'Total Volume Voided (ml)', 'Total Voiding Time (s)', 'Total Flow Time (s)',
            'Image Filename', 'Sex', 'Age' 
        ]
        
        for col in required_columns:
            if col not in df.columns:
                raise KeyError(f"缺少必需的列: {col}")
        
        with transaction.atomic():
            for index, row in df.iterrows():
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
                image_number = index + 1  # 根据实际情况调整
                
                if CsvData.objects.filter(image_filename=image_filename, user=user).exists():
                    print(f"跳过重复的 image_filename: {image_filename}")
                    continue
                
                # 处理 time_samples
                if isinstance(time_samples, list):
                    time_samples = ','.join(map(str, time_samples))
                elif isinstance(time_samples, (float, int)):
                    time_samples = str(time_samples)
                else:
                    time_samples = str(time_samples)

                # 处理 flowrate_samples
                if isinstance(flowrate_samples, list):
                    flowrate_samples = ','.join(map(str, flowrate_samples))
                elif isinstance(flowrate_samples, (float, int)):
                    flowrate_samples = str(flowrate_samples)
                else:
                    flowrate_samples = str(flowrate_samples)
                
                # 获取相对于 MEDIA_ROOT 的路径
                relative_csv_path = os.path.relpath(csv_file_path, settings.MEDIA_ROOT)
                
                CsvData.objects.create(
                    user=user,
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
                    csv_file=relative_csv_path
                )
            
        print(f"成功为用户 {user.username} 导入 CSV 数据。")
        logger.debug(f"成功为用户 {user.username} 导入 CSV 数据。")
    
    except KeyError as e:
        print(f"CSV 解析错误: {e}")
        logger.error(f"CSV 解析错误: {e}")
    except Exception as e:
        print(f"导入 CSV 数据时出错: {e}")
        logger.error(f"导入 CSV 数据时出错: {e}")