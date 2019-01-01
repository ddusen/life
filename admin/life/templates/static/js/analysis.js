$(document).ready(function() {
  // api request
  function httpGet(reqUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", reqUrl, false); // false for synchronous request
    xmlHttp.send(null);
    return JSON.parse(xmlHttp.responseText);
  };
  var responseText = httpGet('/api/analysis');

  // consume mood line chart
  function consumeMood(consumeMoodData) {
    new Chartist.Line("#consumeMoodLineChart .line-chart", {
      // labels: [],
      series: consumeMoodData['series'],
    }, {
      low: 0,
      showArea: false,
      showPoint: false,
      showLine: true,
      lineSmooth: false,
      fullWidth: true,
      chartPadding: {
        top: 0,
        right: 10,
        bottom: 0,
        left: 10
      },
      axisX: {
        showLabel: false,
        showGrid: false,
        offset: 20
      },
      axisY: {
        showLabel: false,
        showGrid: true,
        offset: 0
      },
      plugins: [Chartist.plugins.tooltip()]
    });
  };
  consumeMood(responseText['consume_mood']['month']);
  document.querySelector('#dayConsumeMood').addEventListener('click', function(event) {
    consumeMood(responseText['consume_mood']['day']);
  }, false);
  document.querySelector('#weekConsumeMood').addEventListener('click', function(event) {
    consumeMood(responseText['consume_mood']['week']);
  }, false);
  document.querySelector('#monthConsumeMood').addEventListener('click', function(event) {
    consumeMood(responseText['consume_mood']['month']);
  }, false);

});