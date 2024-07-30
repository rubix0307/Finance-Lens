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
                    total_usd: categoryData.total_usd,
                    currencies: categoryData.currencies
                });
            }
        });

        // Create data set with preprocessed data
        var dataSet = anychart.data.set(processedData);

        // Create column chart
        var chart = anychart.column();
        chart.animation(true);
        chart.padding(10);

        chart.yAxis(false);
        chart.xAxis().title('Month').stroke('black', 2);
        chart.xAxis().ticks().enabled(false);

        // Force chart to stack values by Y scale
        chart.yScale().stackMode('value');

        if (title) {
            chart.title(title);
        }

        // Create data-area and set background settings
        chart
            .dataArea()
            .background()
            .enabled(true)
            .fill('#456')
            .corners(25, 25, 0, 0);

        // Set grid settings
        chart
            .xGrid()
            .stroke('#fff .1')
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
                    value: categoryData.total_usd,
                    category: category,
                    currencies: categoryData.currencies
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
                var currencyText = Object.keys(currencies).map(function(key) {
                    return key + ": " + currencies[key];
                }).join(", ");
                return this.getData('category') + "\n" + currencyText;
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
            .fontSize(13)
            .fontColor('white')
            .positionMode('inside')
            .margin({ top: 15 });

        chart.container(container);

        // Initiate chart drawing
        chart.draw();
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