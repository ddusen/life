(function(global, factory) {
  if (typeof define === "function" && define.amd) {
    define('/', ['jquery', 'Site'], factory);
  } else if (typeof exports !== "undefined") {
    factory(require('jquery'), require('Site'));
  } else {
    var mod = {
      exports: {}
    };
    factory(global.jQuery, global.Site);
    global.dashboardAnalytics = mod.exports;
  }
})(this, function(_jquery, _Site) {
  'use strict';

  var _jquery2 = babelHelpers.interopRequireDefault(_jquery);

  (0, _jquery2.default)(document).ready(function($$$1) {
    (0, _Site.run)();
  });

  (function() {

    // api request
    function httpGet(reqUrl) {
      var xmlHttp = new XMLHttpRequest();
      xmlHttp.open("GET", reqUrl, false); // false for synchronous request
      xmlHttp.send(null);
      return xmlHttp.responseText;
    };
    var responseText = httpGet('/api/index');

    // Top Line Chart With Tooltips
    function annualTime(responseText) {
      new Chartist.Bar('#weekStackedBarChart', {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        // labels: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
        series: [
          [
            301.9,
            1435.45,
            5317.98,
            2999.67,
            6248.36,
            3190.33,
            3295.59,
            3707.47,
            2778.14,
            4317.16,
            4671.26,
            3635.02,
          ],
          [
            6946.46,
            5812.91,
            1930.38,
            4248.69,
            1000.0,
            4058.03,
            3952.77,
            3540.89,
            4470.22,
            2931.2,
            2577.1,
            3613.34,
          ],
        ]
      }, {
        stackBars: true,
        axisY: {
          offset: 0
        },
        axisX: {
          offset: 60
        }
      }).on('draw', function(data) {
        if (data.type === 'bar') {
          data.element.attr({
            style: 'stroke-width: 20px'
          });
        }
      });

      // common options for common style
      var options = {
        showArea: true,
        low: 0,
        high: 8000,
        height: 240,
        fullWidth: true,
        axisX: {
          offset: 40
        },
        axisY: {
          offset: 30,
          labelInterpolationFnc: function labelInterpolationFnc(value) {
            if (value == 0) {
              return null;
            }
            return value / 1000 + 'k';
          },
          scaleMinSpace: 40
        },
        plugins: [Chartist.plugins.tooltip()]
      };

      //day data
      var dayLabelList = ['AUG 8', 'SEP 15', 'OCT 22', 'NOV 29', 'DEC 8', 'JAN 15', 'FEB 22', ''];
      var daySeries1List = {
        name: 'series-1',
        data: [0, 7300, 6200, 6833, 7568, 4620, 4856, 2998]
      };
      var daySeries2List = {
        name: 'series-2',
        data: [0, 3100, 7200, 5264, 5866, 2200, 3850, 1032]
      };

      //week data
      var weekLabelList = ['W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', ''];
      var weekSeries1List = {
        name: 'series-1',
        data: [0, 2400, 6200, 7833, 5568, 3620, 4856, 2998]
      };
      var weekSeries2List = {
        name: 'series-2',
        data: [0, 4100, 6800, 5264, 5866, 3200, 2850, 1032]
      };

      //month data
      var monthLabelList = ['AUG', 'SEP', 'OCT', 'NOV', 'DEC', 'JAN', 'FEB', ''];
      var monthSeries1List = {
        name: 'series-1',
        data: [0, 6400, 5200, 7833, 5568, 3620, 5856, 0]
      };
      var monthSeries2List = {
        name: 'series-2',
        data: [0, 3100, 4800, 5264, 6866, 3200, 2850, 1032]
      };

      var newScoreLineChart = function newScoreLineChart(chartId, labelList, series1List, series2List, options) {

        var lineChart = new Chartist.Line(chartId, {
          labels: labelList,
          series: [series1List, series2List]
        }, options);

        //start create
        lineChart.on('draw', function(data) {
          var elem, parent;
          if (data.type === 'point') {
            elem = data.element;
            parent = new Chartist.Svg(elem._node.parentNode);

            parent.elem('line', {
              x1: data.x,
              y1: data.y,
              x2: data.x + 0.01,
              y2: data.y,
              "class": 'ct-point-content'
            });
          }
        });
        //end create
      };

      //finally new a chart according to the state
      var createKindChart = function createKindChart(clickli) {
        var clickli = clickli || (0, _jquery2.default)("#productOverviewWidget .product-filters").find(".active");

        var chartId = clickli.attr("href");
        switch (chartId) {
          case "#scoreLineToDay":
            newScoreLineChart(chartId, dayLabelList, daySeries1List, daySeries2List, options);
            break;
          case "#scoreLineToWeek":
            newScoreLineChart(chartId, weekLabelList, weekSeries1List, weekSeries2List, options);
            break;
          case "#scoreLineToMonth":
            newScoreLineChart(chartId, monthLabelList, monthSeries1List, monthSeries2List, options);
            break;
        }
      };

      //default create chart whithout click
      createKindChart();

      //create for click
      (0, _jquery2.default)(".product-filters li a").on("click", function() {
        createKindChart((0, _jquery2.default)(this));
      });

      //Four Overlapping Bars Data
      var overlappingBarsDataOne = {
        labels: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
        series: [
          [3, 4, 6, 10, 8, 6, 3, 4],
          [2, 3, 5, 8, 6, 5, 4, 3]
        ]
      };
      var overlappingBarsDataTwo = {
        labels: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
        series: [
          [2, 4, 5, 10, 6, 8, 3, 5],
          [3, 5, 6, 5, 4, 6, 3, 3]
        ]
      };
      var overlappingBarsDataThree = {
        labels: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
        series: [
          [5, 2, 6, 7, 10, 8, 6, 5],
          [4, 3, 5, 6, 8, 6, 4, 3]
        ]
      };
      var barsData = [overlappingBarsDataOne, overlappingBarsDataTwo, overlappingBarsDataThree, overlappingBarsDataThree];

      //Common OverlappingBarsOptions
      var overlappingBarsOptions = {
        low: 0,
        high: 10,
        seriesBarDistance: 6,
        fullWidth: true,
        axisX: {
          showLabel: false,
          showGrid: false,
          offset: 0
        },
        axisY: {
          showLabel: false,
          showGrid: false,
          offset: 0
        },
        chartPadding: {
          //   top: 20,
          //   right: 115,
          //   bottom: 55,
          left: 30
        }
      };

      var responsiveOptions = [
        ['screen and (max-width: 640px)', {
          seriesBarDistance: 6,
          axisX: {
            labelInterpolationFnc: function labelInterpolationFnc(value) {
              return value[0];
            }
          }
        }]
      ];

      // create Four Bars
      var createBar = function createBar(chartId, data, options, responsiveOptions) {
        new Chartist.Bar(chartId, data, options, responsiveOptions);
      };

      (0, _jquery2.default)("#productOptionsData .ct-chart").each(function(index) {
        createBar(this, barsData[index], overlappingBarsOptions, responsiveOptions);
      });
    };
    annualTime(responseText);

    // Overlapping Bars One ~ Four
    function annualConsume(responseText) {
      Morris.Donut({
        resize: true,
        element: 'browersVistsDonut',
        data: [{
          label: 'Chrome',
          value: 4625,
        }, {
          label: 'Firfox',
          value: 1670
        }, {
          label: 'Safari',
          value: 1100
        }],
        colors: ['#f96868', '#62a9eb', '#f3a754'],
        // valueColors: ['#37474f', '#f96868', '#76838f']
      });
    };
    annualConsume(responseText);
  })();
});