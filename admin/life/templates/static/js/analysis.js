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

  // sleep mood line chart
  function sleepMood(sleepMoodData) {
    new Chartist.Line("#sleepMoodLineChart .line-chart", {
      // labels: [],
      series: sleepMoodData['series'],
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
  sleepMood(responseText['sleep_mood']['month']);
  document.querySelector('#daySleepMood').addEventListener('click', function(event) {
    sleepMood(responseText['sleep_mood']['day']);
  }, false);
  document.querySelector('#weekSleepMood').addEventListener('click', function(event) {
    sleepMood(responseText['sleep_mood']['week']);
  }, false);
  document.querySelector('#monthSleepMood').addEventListener('click', function(event) {
    sleepMood(responseText['sleep_mood']['month']);
  }, false);

  // fitness mood line chart
  function fitnessMood(fitnessMoodData) {
    new Chartist.Line("#fitnessMoodLineChart .line-chart", {
      // labels: [],
      series: fitnessMoodData['series'],
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
  fitnessMood(responseText['fitness_mood']['month']);
  document.querySelector('#dayFitnessMood').addEventListener('click', function(event) {
    fitnessMood(responseText['fitness_mood']['day']);
  }, false);
  document.querySelector('#weekFitnessMood').addEventListener('click', function(event) {
    fitnessMood(responseText['fitness_mood']['week']);
  }, false);
  document.querySelector('#monthFitnessMood').addEventListener('click', function(event) {
    fitnessMood(responseText['fitness_mood']['month']);
  }, false);


  // study mood line chart
  function studyMood(studyMoodData) {
    new Chartist.Line("#studyMoodLineChart .line-chart", {
      // labels: [],
      series: studyMoodData['series'],
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
  studyMood(responseText['study_mood']['month']);
  document.querySelector('#dayStudyMood').addEventListener('click', function(event) {
    studyMood(responseText['study_mood']['day']);
  }, false);
  document.querySelector('#weekStudyMood').addEventListener('click', function(event) {
    studyMood(responseText['study_mood']['week']);
  }, false);
  document.querySelector('#monthStudyMood').addEventListener('click', function(event) {
    studyMood(responseText['study_mood']['month']);
  }, false);

  // work mood line chart
  function workMood(workMoodData) {
    new Chartist.Line("#workMoodLineChart .line-chart", {
      // labels: [],
      series: workMoodData['series'],
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
  workMood(responseText['work_mood']['month']);
  document.querySelector('#dayWorkMood').addEventListener('click', function(event) {
    workMood(responseText['work_mood']['day']);
  }, false);
  document.querySelector('#weekWorkMood').addEventListener('click', function(event) {
    workMood(responseText['work_mood']['week']);
  }, false);
  document.querySelector('#monthWorkMood').addEventListener('click', function(event) {
    workMood(responseText['work_mood']['month']);
  }, false);
});