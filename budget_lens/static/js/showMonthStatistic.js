async function drawStatisticPieChart(dataUrl, container, title) {

    var rawData = await getData(dataUrl);

    anychart.onDocumentReady(function () {
        var processedData = [];

        rawData.forEach(function(item) {
            for (var category in item.categories) {
                var categoryData = item.categories[category];
                processedData.push({
                    x: categoryData.name,
                    value: categoryData.selected_currency_total_price,
                    currencies: categoryData.currencies,
                    base_currency: item.base_currency,
                });
            }
        });

        var chart = anychart.pie(processedData);
        chart.background().fill("var(--tg-theme-bg-color)");
        chart.animation(false);
        chart.padding(10, 5, 5, 5);

        chart.labels().enabled(true);
        chart.labels().format(function() {
            return this.x + ' (' + this.value + ')';
        });
        chart.labels().position('outside');
        chart.labels().padding(4);
        chart.labels().textOverflow('ellipsis');

        if (title) {
            chart.title(title);
        }

        chart.tooltip().format(function() {
            var currencies = this.getData('currencies');
            var baseCurrency = this.getData('base_currency');
            var currencyText = Object.keys(currencies).map(function(key) {
                return key + ": " + currencies[key];
            }).join("\n");
            return this.x + "\n" + currencyText + "\n------------" + "\n" + `≈ ${this.value} ${baseCurrency}`;
        });


        chart
            .legend()
            .enabled(true)
            .fontSize(16)
            .fontColor('var(--tg-theme-text-color);')
            .positionMode('outside')
            .itemsLayout('horizontalExpandable')
            .position('bottom');

        document.getElementById(container).innerHTML = '';
        chart.container(container);
        chart.draw();
    });
}