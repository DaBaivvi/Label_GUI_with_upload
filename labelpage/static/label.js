document.addEventListener('DOMContentLoaded', function() {
    const labelTypeRadios = document.querySelectorAll('input[name="label_type"]');
    const abnormalSubtypeDiv = document.getElementById('abnormal-subtype');

    labelTypeRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'abnormal') {
                abnormalSubtypeDiv.style.display = 'block';
            } else {
                abnormalSubtypeDiv.style.display = 'none';
                // 清除异常子类型的值，以防止提交时的验证错误
                const abnormalSubtypeField = document.getElementById('id_abnormal_subtype');
                if (abnormalSubtypeField) {
                    abnormalSubtypeField.value = '';
                }
            }
        });
    });

    // 初始化显示
    const selectedLabelType = document.querySelector('input[name="label_type"]:checked');
    if (selectedLabelType && selectedLabelType.value === 'abnormal') {
        abnormalSubtypeDiv.style.display = 'block';
    }

});