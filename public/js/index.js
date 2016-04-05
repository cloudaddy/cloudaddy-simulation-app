$(function() {
  var btnStopTesting = $('#btnStopTesting');
  var btnStartTesting = $('#btnStartTesting');
  var refreshInterval;
  var dataTable;

  btnStopTesting.click(function() {
    $.get('/stop-testing').done(function() {
      clearInterval(refreshInterval);
      btnStartTesting.prop('disabled', false).text(
        'Start Load Testing');
      btnStopTesting.prop('disabled', true);
    })
  });

  $('#testing-form').submit(function(env) {

    var formData = {
      'numberOfConcurrentUsers': $(
        'input[name=numberOfConcurrentUsers]').val(),
      'numberOfJobsPerUser': $('input[name=numberOfJobsPerUser]').val()
    };

    $.post('/start-testing', formData).done(function(data) {
      btnStartTesting.prop('disabled', true).text('Testing...');
      btnStopTesting.prop('disabled', false);

      // start to show stats

      refreshInterval = setInterval(function() {
        $.get('/stats/requests').done(function(data) {
          // console.log(data);
          var statsData = JSON.parse(data).stats;
          if (!dataTable) {
            dataTable = $('#data-table').bootstrapTable({
              columns: [{
                field: 'name',
                title: 'Name'
              }, {
                field: 'avg_content_length',
                title: 'Average Content Length'
              }, {
                field: 'avg_response_time',
                title: 'Average Response Time'
              }, {
                field: 'current_rps',
                title: 'Current RPS'
              }, {
                field: 'max_response_time',
                title: 'Max Response Time'
              }, {
                field: 'median_response_time',
                title: 'Median Response Time'
              }, {
                field: 'min_response_time',
                title: 'Min Response Time'
              }, {
                field: 'method',
                title: 'Method'
              }, {
                field: 'num_failures',
                title: 'Num Failures'
              }, {
                field: 'num_requests',
                title: 'Num Requests'
              }],
              data: statsData
            });
          } else {
            $(dataTable).bootstrapTable('load', statsData);
          }
        })

      }, 2000);

    });

    env.preventDefault();
  })
});
