document.addEventListener('input', function (event) {
    if (event.target.matches('.receipt .products-list .product .column.price input[type="number"]')) {
        updateTotalPrice(event.target.closest('.receipt'));
    }
});

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.receipt').forEach(receipt => {
        updateTotalPrice(receipt);
    });
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