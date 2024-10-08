function initializeMonthSwitcher(switcher) {
    let currentMonthIndex = switcher.querySelectorAll('.month-display').length - 1;
    const months = switcher.querySelectorAll('.month-display');
    const prevButton = switcher.querySelector('#prev');
    const nextButton = switcher.querySelector('#next');

    function updateMonthDisplay() {
        months.forEach((month, index) => {
            month.style.display = index === currentMonthIndex ? 'inline' : 'none';
        });
        prevButton.disabled = currentMonthIndex === 0;
        nextButton.disabled = currentMonthIndex === months.length - 1;

        const urlParams = new URLSearchParams(window.location.search);
        const sectionId = urlParams.get('id');

        // Get selected month and year from the element
        const selectedMonthElement = months[currentMonthIndex];
        const monthData = selectedMonthElement.dataset.month;
        const yearData = selectedMonthElement.dataset.year;

        drawStatisticPieChart(
            `/get-section-stats/?id=${sectionId}&month=${monthData}&year=${yearData}`,
            'month-chart'
        )
    }

    function changeMonth(step) {
        currentMonthIndex += step;
        updateMonthDisplay();
    }

    prevButton.addEventListener('click', () => changeMonth(-1));
    nextButton.addEventListener('click', () => changeMonth(1));

    updateMonthDisplay();
}

document.addEventListener('DOMContentLoaded', function() {
    const observer = new MutationObserver((mutations, observer) => {
        const monthSwitchers = document.querySelectorAll('.month-switcher');
        if (monthSwitchers.length > 0) {
            monthSwitchers.forEach(initializeMonthSwitcher);
            observer.disconnect();
        }
    });
    observer.observe(document.body, { childList: true, subtree: true });

    const monthSwitchers = document.querySelectorAll('.month-switcher');
    if (monthSwitchers.length > 0) {
        monthSwitchers.forEach(initializeMonthSwitcher);
    }
});