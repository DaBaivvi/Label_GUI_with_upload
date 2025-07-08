document.addEventListener('DOMContentLoaded', function() {
    // 获取表单并监听提交事件
    const form = document.getElementById('RegisterForm');
    form.addEventListener('submit', function(event) {
        event.preventDefault();  // 阻止默认表单提交行为

        const formData = new FormData(form);

        // 使用 fetch 提交表单数据
        fetch(form.action, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())  // 解析响应为 JSON
        .then(data => {
            if (data.status === 'success') {
                // 显示成功消息
                alert('Account has been created successfully. Please log in, ' + data.username);

                // 重定向到 next 页面或默认页面
                if (data.next) {
                    window.location.href = data.next;  // 重定向到 next 页面
                } else {
                    window.location.href = '/';  // 默认重定向到主页
                }
            } else {
                // 如果注册失败，显示错误信息
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);  // 错误处理
        });
    });
});