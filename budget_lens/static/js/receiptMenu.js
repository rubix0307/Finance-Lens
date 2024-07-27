function toggleConfirm(button) {
    const delBtn = button;
    const confirmBtn = button.nextElementSibling;

    delBtn.style.display = 'none';
    confirmBtn.style.display = 'block';

    // Через пол секунды
    setTimeout(() => {
        // Через 3 секунды вернуть всё обратно
        setTimeout(() => {
            delBtn.style.display = 'block';
            confirmBtn.style.display = 'none';
        }, 3000);
    }, 500);
}
function removeReceipt(confirmBtn) {
    const receipt = confirmBtn.closest('.receipt');
    if (receipt) {
        receipt.remove();
    }
}
