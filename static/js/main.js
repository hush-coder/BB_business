// 自动隐藏提示消息
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.remove();
            }, 300);
        }, 5000);
    });
});

// 表单验证
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
});

// 消息模态框自动聚焦
document.addEventListener('DOMContentLoaded', function() {
    const messageModals = document.querySelectorAll('.modal');
    messageModals.forEach(function(modal) {
        modal.addEventListener('shown.bs.modal', function() {
            const textarea = this.querySelector('textarea');
            if (textarea) {
                textarea.focus();
            }
        });
    });
});

// 表格排序
document.addEventListener('DOMContentLoaded', function() {
    const tables = document.querySelectorAll('table');
    tables.forEach(function(table) {
        const headers = table.querySelectorAll('th');
        headers.forEach(function(header, index) {
            header.style.cursor = 'pointer';
            header.addEventListener('click', function() {
                const rows = Array.from(table.querySelectorAll('tbody tr'));
                const direction = this.dataset.direction === 'asc' ? -1 : 1;
                this.dataset.direction = direction === 1 ? 'asc' : 'desc';
                
                rows.sort((a, b) => {
                    const aValue = a.cells[index].textContent;
                    const bValue = b.cells[index].textContent;
                    
                    if (!isNaN(aValue) && !isNaN(bValue)) {
                        return direction * (parseFloat(aValue) - parseFloat(bValue));
                    }
                    return direction * aValue.localeCompare(bValue);
                });
                
                const tbody = table.querySelector('tbody');
                tbody.innerHTML = '';
                rows.forEach(row => tbody.appendChild(row));
            });
        });
    });
}); 