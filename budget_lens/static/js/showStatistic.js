async function drawStatisticChart(dataUrl, container, title) {
    var rawData = await getData(dataUrl);
    anychart.onDocumentReady(function () {
        // Get the raw data and preprocess it to a flat structure

        var processedData = [];

        rawData.forEach(function(item) {
            for (var category in item.categories) {
                var categoryData = item.categories[category];
                processedData.push({
                    month: item.month,
                    category: category,
                    total_base_currency: categoryData.total_base_currency,
                    currencies: categoryData.currencies,
                });
            }
        });

        // Create data set with preprocessed data
        var dataSet = anychart.data.set(processedData);

        // Create column chart
        var chart = anychart.column();
        chart.background().fill("var(--tg-theme-bg-color)");
        chart.animation(true);
        chart.padding(10, 5, 5, 5);

        chart.yAxis(true);
        chart.yAxis().stroke('var(--tg-theme-hint-color)', 1);
        chart.yAxis().labels().format("{%Value}");

        chart.xAxis().title('Month').stroke('var(--tg-theme-hint-color)', 1);
        chart.xAxis().ticks().enabled(false);

        // Force chart to stack values by Y scale
        chart.yScale().stackMode("value");


        chart.labels().enabled(true);
        chart.labels().format(function() {
            return this.seriesName;
        });
        chart.labels().position('center');
        chart.labels().padding(4);
        chart.labels().textOverflow('ellipsis');

        if (title) {
            chart.title(title);
        }

        // Create data-area and set background settings
        chart
            .dataArea()
            .background()
            .enabled(true)
            .fill('var(--tg-theme-bg-color)')
            .corners(5, 5, 0, 0);

        // Set grid settings
        chart
            .xGrid()
            .stroke('transperent .1')
            .isMinor(true)
            .drawFirstLine(false)
            .drawLastLine(false);

        chart
            .yGrid()
            .stroke('#fff .1')
            .isMinor(true)
            .drawFirstLine(false)
            .drawLastLine(false);

        // Processed data series mapping
        var seriesMapping = {};
        rawData.forEach(function(item) {
            for (var category in item.categories) {
                if (!seriesMapping[category]) {
                    seriesMapping[category] = [];
                }
                var categoryData = item.categories[category];
                seriesMapping[category].push({
                    x: item.month,
                    value: categoryData.total_base_currency,
                    category: category,
                    currencies: categoryData.currencies,
                    base_currency: categoryData.base_currency,
                });
            }
        });

        // Create series for each category
        for (var category in seriesMapping) {
            var seriesData = anychart.data.set(seriesMapping[category]).mapAs({x: 'x', value: 'value'});
            var series = chart.column(seriesData);
            series.name(category);

            // Set tooltips
            series.tooltip().format(function() {
                var currencies = this.getData('currencies');
                var baseCurrency = this.getData('base_currency');
                var currencyText = Object.keys(currencies).map(function(key) {
                    return key + ": " + currencies[key];
                }).join("\n");
                console.log(this)
                return this.getData('category') + "\n" + currencyText + "\n------------"+ "\n" + `≈ ${this.value} ${baseCurrency}`;
            });
        }

        // Customize the X axis labels to show the month names
        chart.xAxis().labels().format(function() {
            var date = new Date(this.value);
            var options = { year: 'numeric', month: 'short' };
            return date.toLocaleDateString('en-US', options);
        });

        // Turn the legend on
        chart
            .legend()
            .enabled(true)
            .fontSize(16)
            .fontColor('var(--tg-theme-text-color);')
            .positionMode('inside')
            .margin({ top: 15 });

        chart.legend().background('var(--tg-theme-bg-color)');
        chart.legend().fontColor('var(--tg-theme-text-color)');


        chart.container(container);
        chart.draw();

        var legend = chart.legend();
        legend.positionMode("outside");
        legend.itemsLayout("horizontalExpandable");
        legend.position("bottom");

    });


    async function getData(url) {
        try {
            const response = await fetch(url);


            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }

            const data = await response.json();

            return data;
        } catch (error) {
            console.error('Произошла ошибка:', error);
        }
    }
}