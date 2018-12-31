$(document).ready(function() {
  $("#dataTables").DataTable({
    "scrollX": false,
    "scrollY": false,
    "ordering": true,
    "searching": true,
    "processing": true,
    "serverSide": true,
    "columns": [
      { "data": "pubtime" },
      { "data": "mood" },
      { "data": "mood_keywords" },
      { "data": "consume" },
      { "data": "consume_keywords" },
      { "data": "time_keywords" },
    ],
    "columnDefs": [
      { "width": "10%", "targets": 0 },
      {
        "targets": [1],
        "width": "11%",
        "data": "mood",
        "render": function(data, type, full) {
          if (data < 10) {
            color = 'danger';
          } else if (data < 40) {
            color = 'warning';
          } else if (data < 70) {
            color = 'primary';
          } else {
            color = 'success';
          }
          return '<div class="progress progress-xs mb-0 "><div class="progress-bar progress-bar-' + color + '" style="width: ' + data + '%"></div></div>';
        },
      },
      { "width": "10%", "targets": 2 },
      { "width": "9%", "targets": 3 },
      { "width": "25%", "targets": 4 },
      { "width": "35%", "targets": 5 },
    ],
    "ajax": "/api/data",
    "language": {
      "url": "/templates/static/data/Chinese.lang"
    },
  });
});