document.addEventListener('input', function (event) {
    if (event.target.matches('.receipt .products-list .product .column.price input[type="number"]')) {
        updateTotalPrice(event.target.closest('.receipt'));
    }
});


function updateTotalPrice(receipt) {
    let totalPrice = 0;
    receipt.querySelectorAll('.products-list .product .column.price input[type="number"]').forEach(input => {
        totalPrice += parseFloat(input.value) || 0;
    });

    let totalElement = receipt.querySelector('.receipt .product .column.price.total span');
    if (totalElement) {
        totalElement.textContent = totalPrice.toFixed(2);
    }
}


document.addEventListener('DOMContentLoaded', function () {
    // Обновляем все существующие элементы с классом .receipt
    document.querySelectorAll('.receipt').forEach(receipt => {
        updateTotalPrice(receipt);
    });

    // Создаем MutationObserver для отслеживания изменений в DOM
    const observer = new MutationObserver(function(mutationsList) {
        for (let mutation of mutationsList) {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === Node.ELEMENT_NODE && node.classList.contains('receipt')) {
                        updateTotalPrice(node);

                        if (node.getAttribute('data-isupdated') === '1') {
                            updateButtonText(node)
                        }
                    }
                });
            }
        }
    });

    // Настройки для наблюдения: следить за добавлением дочерних элементов
    const config = { childList: true, subtree: true };

    // Запускаем наблюдателя на document.body
    observer.observe(document.body, config);
});