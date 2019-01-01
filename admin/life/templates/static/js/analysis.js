$(document).ready(function() {
  new Chartist.Bar("#widgetOverallViews .small-bar-one", {
    labels: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
    series: [
      [120, 60, 100, 50, 40, 120, 80, 130]
    ]
  }, {
    low: 0,
    fullWidth: true,
    chartPadding: {
      top: -10,
      right: 0,
      bottom: 0,
      left: 0
    },
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
    plugins: [Chartist.plugins.tooltip()]
  });

  new Chartist.Bar("#widgetOverallViews .small-bar-two", {
    labels: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
    series: [
      [50, 90, 30, 90, 130, 40, 120, 90]
    ]
  }, {
    low: 0,
    fullWidth: true,
    chartPadding: {
      top: -10,
      right: 0,
      bottom: 0,
      left: 0
    },
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
    plugins: [Chartist.plugins.tooltip()]
  });

  new Chartist.Line("#widgetOverallViews .line-chart", {
    labels: ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'],
    series: [
      [20, 50, 70, 110, 100, 200, 230],
      [50, 80, 140, 130, 150, 110, 160]
    ]
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
      showLabel: true,
      showGrid: false,
      offset: 30
    },
    axisY: {
      showLabel: true,
      showGrid: true,
      offset: 30
    },
    plugins: [Chartist.plugins.tooltip()]
  });
});