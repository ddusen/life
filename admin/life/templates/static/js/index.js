$(document).ready(function() {
  // api request
  function httpGet(reqUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", reqUrl, false); // false for synchronous request
    xmlHttp.send(null);
    return JSON.parse(xmlHttp.responseText);
  };
  var responseText = httpGet('/api/index');

  // annual time
  function annualTime(timeData) {
    document.getElementById('validTimeRate').innerHTML = timeData['valid_time_rate'];
    document.getElementById('invalidTimeRate').innerHTML = timeData['invalid_time_rate'];
    document.getElementById('studyTime').innerHTML = timeData['study_time_amount'];
    document.getElementById('codingTime').innerHTML = timeData['coding_time_amount'];
    document.getElementById('fitnessTime').innerHTML = timeData['fitness_time_amount'];
    document.getElementById('sleepTime').innerHTML = timeData['sleep_time_amount'];
    // common options for common style
    var options = {
      showArea: true,
      low: 0,
      high: timeData['max_amount'],
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
          return value;
        },
        scaleMinSpace: 40
      },
      plugins: [Chartist.plugins.tooltip()]
    };

    //day data
    var dayLabelList = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    // var dayLabelList = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'];   
    var daySeries1List = {
      name: '有效时间(时)',
      data: timeData['valid_time'],
    };
    var daySeries2List = {
      name: '无效时间(时)',
      data: timeData['invalid_time'],
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
      var clickli = clickli || (0, _jquery2.default)("#annualTime .product-filters").find(".active");

      var chartId = clickli.attr("href");
      newScoreLineChart(chartId, dayLabelList, daySeries1List, daySeries2List, options);
    };

    //default create chart whithout click
    createKindChart();

    //create for click
    (0, _jquery2.default)(".product-filters li a").on("click", function() {
      createKindChart((0, _jquery2.default)(this));
    });

    //study time bar data
    var studyTimeBarData = {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      series: timeData['study_time_bar'],
    };
    //coding time bar data
    var codingTimeBarData = {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      series: timeData['coding_time_bar'],
    };
    //fitness time bar data
    var fitnessTimeBarData = {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      series: timeData['fitness_time_bar'],
    };
    //sleep time bar data
    var sleepTimeBarData = {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      series: timeData['sleep_time_bar'],
    };
    var barsData = [studyTimeBarData, codingTimeBarData, fitnessTimeBarData, sleepTimeBarData];

    //Common OverlappingBarsOptions
    var overlappingBarsOptions = {
      low: 0,
      high: timeData['max_amount'],
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

    (0, _jquery2.default)("#annualTimeData .ct-chart").each(function(index) {
      createBar(this, barsData[index], overlappingBarsOptions, responsiveOptions);
    });
  };
  annualTime(responseText['annual_time']);

  // annual consume
  function annualConsume(consumeData) {
    //table
    var tableData = consumeData['consume_data_table'];
    var tableNode = document.getElementById('consumeTable');
    var new_node = ''
    for (var i = 0; i < tableData.length; i++) {
      new_node += '<tr><td><img src="' + tableData[i]['icon'] + '" title="' + tableData[i]['category'] + '" alt="' + tableData[i]['category'] + '"></td><td>' + tableData[i]['category'] + '</td><td>' + tableData[i]['amount'] + '</td></tr>';
    }
    tableNode.innerHTML = new_node;

    //pie
    Morris.Donut({
      resize: true,
      element: 'annualConsumePieChart',
      data: consumeData['consume_data_pie'],
      // colors: ['#f96868', '#62a9eb', '#f3a754'],
      colors: ['#589FFC', '#28C7B7', '#28D17C', '#FFDC2E', '#FF666B', '#A57AFA'],
    });

    new Chartist.Bar('#annualConsumeBarChart', {
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
  function annualKeywords(keywordsData) {
    //table
    var tableData = keywordsData;
    var tableNode = document.getElementById('keywordsTable');
    var new_node = ''
    for (var i = 0; i < tableData.length; i++) {
      new_node += '<tr><td><img src="' + tableData[i]['icon'] + '" title="' + tableData[i]['keywords'] + '" alt="' + tableData[i]['keywords'] + '"><span class="country-name">' + tableData[i]['keywords'] + '</span></td><td>' + tableData[i]['count'] + '</td><td><div class="progress progress-xs mb-0"><div class="progress-bar progress-bar-info bg-blue-600" style="width: ' + tableData[i]['rate'] + '%" aria-valuemax="100" aria-valuemin="0" aria-valuenow="' + tableData[i]['rate'] + '" role="progressbar"></div></div><span class="progress-percent">' + tableData[i]['rate'] + '%</span></td></tr>';
    }
    tableNode.innerHTML = new_node;
  };
  annualKeywords(responseText['annual_keywords'])
});