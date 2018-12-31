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
      return JSON.parse(xmlHttp.responseText);
    };
    var responseText = httpGet('/api/index');

    // Top Line Chart With Tooltips
    function annualTime(timeData) {
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

    // annual consume
    function annualConsume(consumeData) {
      //table
      var tableData = consumeData['consume_data_table'];
      var tableNode = document.getElementById('consumeTable');
      var new_node = ''
      for (var i = 0; i < tableData.length; i++) {
        new_node += '<tr><td><img src="'+ tableData[i]['icon'] +'" title="'+ tableData[i]['category'] +'" alt="'+ tableData[i]['category'] +'"></td><td>'+ tableData[i]['category'] +'</td><td>'+ tableData[i]['amount'] +'</td></tr>';
      }
      tableNode.innerHTML = new_node;

      //pie
      Morris.Donut({
        resize: true,
        element: 'annumalConsumePieChart',
        data: consumeData['consume_data_pie'],
        // colors: ['#f96868', '#62a9eb', '#f3a754'],
        colors: ['#3E8EF7', '#17B3A3', '#11C26D', '#FFCD17', '#FF4C52', '#9463F7'],
      });

      new Chartist.Bar('#annumalConsumeBarChart', {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        // labels: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
        series: consumeData['consume_data_bar'],
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
    };
    annualConsume(responseText['annual_consume']);

    // annual mood keywords
    function annualKeywords(keywordsData){
       //table
      var tableData = keywordsData;
      var tableNode = document.getElementById('keywordsTable');
      var new_node = ''
      for (var i = 0; i < tableData.length; i++) {
        new_node += '<tr><td><img src="'+ tableData[i]['icon'] +'" title="'+ tableData[i]['keywords'] +'" alt="'+ tableData[i]['keywords'] +'"><span class="country-name">'+ tableData[i]['keywords'] +'</span></td><td>'+ tableData[i]['count'] +'</td><td><div class="progress progress-xs mb-0"><div class="progress-bar progress-bar-info bg-blue-600" style="width: '+ tableData[i]['rate'] +'%" aria-valuemax="100" aria-valuemin="0" aria-valuenow="'+ tableData[i]['rate'] +'" role="progressbar"></div></div><span class="progress-percent">'+ tableData[i]['rate'] +'%</span></td></tr>';
      }
      tableNode.innerHTML = new_node;
    };
    annualKeywords(responseText['annual_keywords'])
  })();
});