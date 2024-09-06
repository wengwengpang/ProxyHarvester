document.addEventListener('DOMContentLoaded', function() {
    const proxyTable = document.getElementById('proxyTable');
    const searchInput = document.getElementById('searchInput');

    // 代理测试功能
    proxyTable.addEventListener('click', function(e) {
        if (e.target.classList.contains('test-proxy')) {
            const proxyId = e.target.dataset.proxyId;
            testProxy(proxyId);
        }
    });

    // 搜索功能
    searchInput.addEventListener('keyup', function() {
        const searchTerm = this.value.toLowerCase();
        const rows = proxyTable.getElementsByTagName('tr');

        for (let i = 1; i < rows.length; i++) {
            const row = rows[i];
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm) ? '' : 'none';
        }
    });

    // 排序功能
    proxyTable.querySelector('thead').addEventListener('click', function(e) {
        if (e.target.tagName === 'TH') {
            const th = e.target;
            const index = Array.from(th.parentNode.children).indexOf(th);
            sortTable(index);
        }
    });
});

function testProxy(proxyId) {
    fetch('/api/test_proxy', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({proxy_id: proxyId}),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`代理测试成功，延迟: ${data.latency}ms`);
        } else {
            alert('代理测试失败，已从数据库中删除');
            document.querySelector(`tr[data-proxy-id="${proxyId}"]`).remove();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('测试过程中发生错误');
    });
}

function sortTable(n) {
    // ... 实现表格排序逻辑 ...
}
