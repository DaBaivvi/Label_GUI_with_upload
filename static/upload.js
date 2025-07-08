// 显示选择的文件名，并更新按钮文本
function showFileName(input) {
    const file = input.files[0];
    const fileNameArea = document.getElementById('fileNameArea');
    const chooseFileBtn = document.getElementById('chooseFileBtn');
    const uploadFileBtn = document.getElementById('uploadFileBtn');

    if (file) {
        // 检查文件大小（限制为 5MB）
        const maxSize = 5 * 1024 * 1024; // 5MB
        if (file.size > maxSize) {
            alert("File size exceeds the 5MB limit. Please select a smaller file.");
            input.value = ""; // 清空文件输入框
            fileNameArea.style.display = 'none';
            chooseFileBtn.textContent = 'Choose File';
            uploadFileBtn.style.display = 'none';
            return;
        }

        // 更新文件名显示区域
        fileNameArea.textContent = 'Selected File: ' + file.name;
        fileNameArea.style.display = 'inline'; // 显示文件名区域

        // 更新按钮文本为"更改文件"，并显示上传按钮
        chooseFileBtn.textContent = 'Change File';
        uploadFileBtn.style.display = 'inline'; // 显示上传按钮
    }
}

// 用户点击选择文件按钮时，触发文件选择框
document.getElementById('chooseFileBtn').addEventListener('click', function () {
    const fileInput = document.getElementById('fileInput');
    if (fileInput) {
        fileInput.click(); // 模拟点击文件选择框
    }
});

function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

// 用户点击上传文件按钮时，执行上传操作
function uploadFile() {
    const form = document.getElementById('UploadForm');
    const formData = new FormData(form);

    // 使用 fetch API 上传文件
    fetch(form.action, {
        method: 'POST',
        body: formData, // 发送表单数据（包括文件）
        headers: {
            'X-CSRFToken': getCsrfToken() // 添加 CSRF Token
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json(); // 解析响应为 JSON
    })
    .then(data => {
        console.log("Upload Response:", data); // 添加调试日志
        // 根据响应状态处理结果
        handleUploadResponse(data);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Upload failed. Please try again.');
    });
}

// 处理上传响应，根据响应内容执行相应的操作
function handleUploadResponse(response) {
    if (response.status === 'success') {
        // 上传成功，跳转到 label 页面
        alert('CSV file uploaded and saved successfully!');
        window.location.href = response.redirect_url; // 使用后端返回的跳转 URL
    } else {
        // 上传失败，显示后端返回的错误消息
        alert('Upload failed: ' + response.message);
        document.getElementById('fileInput').value = ''; // 清空文件输入框
        document.getElementById('fileNameArea').textContent = ''; // 清空文件名显示区域
        document.getElementById('fileNameArea').style.display = 'none'; // 隐藏文件名区域
        document.getElementById('chooseFileBtn').textContent = 'Choose File'; // 恢复按钮文本
        document.getElementById('uploadFileBtn').style.display = 'none'; // 隐藏上传按钮
    }
}