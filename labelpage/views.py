import plotly.graph_objs as go
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .forms import LabelForm
from .models import Label
from homepage.models import CsvData
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse
import logging
import json
import os

logger = logging.getLogger('labelpage')

#Label
@login_required(login_url='login')
def label_view(request, csv_id):
    logger.debug(f"访问 label_view, csv_id: {csv_id}")

    csv_data = get_object_or_404(CsvData, id=csv_id, user=request.user)

    # 获取当前用户的标签（如果已存在）
    label = Label.objects.filter(csv_data=csv_data, labeled_by=request.user).first()
    if label:
        logger.debug(f"找到现有标签: {label}")
    else:
        logger.debug("当前 CsvData 没有标签")


    # 生成 Plotly 图表
    try:
        time_samples = list(map(float, csv_data.time_samples.split(',')))
        flowrate_samples = list(map(float, csv_data.flowrate_samples.split(',')))
    except Exception as e:
        messages.error(request, f'Data parsing error: {e}')
        logger.error(f'Data parsing error: {e}')
        return redirect('label_redirect')

    # 创建图表
    fig = go.Figure()
    # 添加尿流曲线
    fig.add_trace(
        go.Scatter(
            x=time_samples,
            y=flowrate_samples,
            mode='lines',
            name='Urine Flow Curve',
            line=dict(color='blue')  # 可选：设置线条颜色
        )
    )

    # 更新图表布局，固定轴范围
    fig.update_layout(
        title="Urine Flow Rate Over Time",
        xaxis=dict(
            title="Time (s)",
            range=[0, 120],           # 固定 x 轴范围为 0 到 120 秒
            tick0=0,                  # 可选：设置刻度起始点
            dtick=5,                 # 可选：设置刻度间隔
            zeroline=True,            # 可选：显示零线
            zerolinewidth=2,
            zerolinecolor='Gray'
        ),
        yaxis=dict(
            title="Flow Rate (mL/s)",
            range=[0, 45],            # 固定 y 轴范围为 0 到 50 mL/s
            tick0=0,                  # 可选：设置刻度起始点
            dtick=5,                 # 可选：设置刻度间隔
            zeroline=True,            # 可选：显示零线
            zerolinewidth=2,
            zerolinecolor='Gray'
        ),
        width=580,                      # 可选：调整图表宽度
        height=380,                     # 可选：调整图表高度
        template='plotly_white'         # 可选：设置图表模板
    )

    # 可选：添加网格线
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

    # 生成 HTML
    graph_html = fig.to_html(full_html=False)

    all_labeled = False  # 初始化标志

    # 处理 POST 请求，保存标签
    if request.method == 'POST':
        form = LabelForm(request.POST, instance=label, csv_data=csv_data, user=request.user)
        if form.is_valid():
            label_instance = form.save(commit=False)
            label_instance.csv_data = csv_data
            label_instance.labeled_by = request.user
            label_instance.label_time = timezone.now()
            label_instance.save()

            logger.debug(f"标签保存成功: {label_instance}")

            # 更新Session中的最近标记条目
            request.session['last_labeled_csv_id'] = csv_id
            logger.debug(f"更新 session last_labeled_csv_id 为: {csv_id}")

            messages.success(request, 'Tags saved successfully.')
            logger.debug(f"标签保存成功 for user {request.user.username} on csv_id {csv_id}")

            # 获取下一张的 CSV ID
            csv_ids = list(CsvData.objects.filter(user=request.user).order_by('image_number').values_list('id', flat=True))
            try:
                current_index = csv_ids.index(csv_id)
            except ValueError:
                current_index = -1

            next_csv_id = csv_ids[current_index + 1] if current_index < len(csv_ids) - 1 else None
            logger.debug(f"current_index: {current_index}, next_csv_id: {next_csv_id}")

            if next_csv_id:
                return redirect('label', csv_id=next_csv_id)
            else:
                messages.success(request, 'Thank you for your time! You have completed all the labeling tasks.')
                all_labeled = True
        else:
            logger.debug(f"Form errors: {form.errors}")
            messages.error(request, 'Failed to save tags. Please check your input.')
            logger.debug(f"标签保存失败 for user {request.user.username} on csv_id {csv_id}")
            logger.debug(f"Form errors: {form.errors}")
    else:
        form = LabelForm(instance=label, csv_data=csv_data, user=request.user)
        logger.debug("处理 GET 请求，显示表单")

    # 计算标注进度
    total_entries = CsvData.objects.filter(user=request.user).count()
    labeled_entries = Label.objects.filter(csv_data__user=request.user).count()
    progress = f"{labeled_entries}/{total_entries} Marked"
    logger.debug(f"标注进度: {progress}")

    # 获取当前用户所有的 CsvData，按 image_number 顺序
    all_csv = CsvData.objects.filter(user=request.user).order_by('image_number')

    # 获取所有与当前用户相关的 Label，并组织成字典
    labels = Label.objects.filter(csv_data__in=all_csv, labeled_by=request.user)
    label_dict = {label.csv_data_id: label for label in labels}
    logger.debug(f"标签字典创建完成，包含 {len(label_dict)} 个条目")

    # 获取 Session 中的最近标记的 CsvData ID
    last_labeled_csv_id = request.session.get('last_labeled_csv_id', None)
    logger.debug(f"last_labeled_csv_id: {last_labeled_csv_id}")

    # 获取当前 CsvData ID
    current_csv_id = csv_id
    
    # 获取用户所有 CsvData 的 ID 列表，按 image_number 顺序
    csv_ids = list(all_csv.values_list('id', flat=True))
    try:
        current_index = csv_ids.index(csv_id)
    except ValueError:
        current_index = -1

    # 获取上一张和下一张的 CsvData ID
    previous_csv_id = csv_ids[current_index - 1] if current_index > 0 else None
    next_csv_id = csv_ids[current_index + 1] if current_index < len(csv_ids) - 1 else None
    logger.debug(f"previous_csv_id: {previous_csv_id}, next_csv_id: {next_csv_id}")


    # 获取第一张和最后一张的 CsvData ID
    first_csv_id = csv_ids[0] if csv_ids else None
    last_csv_id = csv_ids[-1] if csv_ids else None
    logger.debug(f"first_csv_id: {first_csv_id}, last_csv_id: {last_csv_id}")


    # 检查用户是否有任何标记条目
    has_labels = Label.objects.filter(labeled_by=request.user).exists()
    logger.debug(f"用户是否有标记条目: {has_labels}")

    context = {
        'graph_html': graph_html,  # 图表HTML
        'csv_data': csv_data,
        'form': form,
        'user': request.user,
        'progress': progress,
        'previous_csv_id': previous_csv_id,
        'next_csv_id': next_csv_id,
        'first_csv_id': first_csv_id,
        'last_csv_id': last_csv_id,
        'all_csv': all_csv,
        'last_labeled_csv_id': last_labeled_csv_id,
        'current_csv_id': current_csv_id,
        'label_dict': label_dict,  # 传递标签字典
    }
    # 如果 all_labeled 标志存在，则添加到上下文
    if 'all_labeled' in locals():
        context['all_labeled'] = all_labeled
    
    logger.debug("渲染模板完成，返回响应")
    return render(request, 'label.html', context)


@login_required(login_url='login')
def load_resource_csvs(request):
    """
    获取当前用户尚未标注的 CsvData并重定向到标注视图。
    """
    # 获取当前用户所有 CsvData
    resource_csvs = CsvData.objects.filter(user=request.user).order_by('image_number')

    # 查找用户尚未标记的 CsvData
    unlabelled_csvs = resource_csvs.exclude(labels__labeled_by=request.user)

    if unlabelled_csvs.exists():
        # 获取第一个未标记的 CsvData
        next_csv = unlabelled_csvs.first()
        return redirect('label', csv_id=next_csv.id)
    else:

        return redirect('label.html') 
    

@login_required(login_url='login')
def go_to_last_labeled_view(request):
    """
    重定向到用户最后标记的 CsvData 视图。
    """
    last_labeled_csv_id = request.session.get('last_labeled_csv_id', None)
    if last_labeled_csv_id:
        return redirect('label', csv_id=last_labeled_csv_id)
    else:
        messages.info(request, 'No labeled entries found.')
        return redirect('label.html')

    


@login_required(login_url='login')
def label_redirect_view(request):
    """
    登录后重定向到下一个未标注的 CsvData 视图。
    """
    # 获取当前用户已标注的 CsvData ID 列表
    labeled_ids = Label.objects.filter(labeled_by=request.user).values_list('csv_data_id', flat=True)
    
    # 获取下一个未标注的 CsvData，按 image_number 顺序
    csv_data = CsvData.objects.filter(user=request.user).exclude(id__in=labeled_ids).order_by('image_number').first()
    
    if csv_data:
        return redirect('label', csv_id=csv_data.id)
    else:
        return render(request, 'label.html')




