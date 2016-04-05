$(function() {
  var btnStopTesting = $('#btnStopTesting');
  var btnStartTesting = $('#btnStartTesting');
  var testingForm = $('#testing-form')[0];
  var inputNumberOfConcurrentUsers = $(
    'input[name=numberOfConcurrentUsers]');
  var inputNumberOfJobsPerUser = $('input[name=numberOfJobsPerUser]');
  var inputDaysDatesBack = $('input[name=daysDatesBack]');
  var refreshInterval;
  var dataTable;

  $('#preset-scenarios-container > li > a').click(function() {
    var numUsers = this.attributes["data-user"].value;
    var numReports = this.attributes["data-reports"].value;
    var daysDatesBack = this.attributes["data-date-back"].value;

    inputNumberOfConcurrentUsers.val(numUsers);
    inputNumberOfJobsPerUser.val(numReports);
    inputDaysDatesBack.val(daysDatesBack);
  });

  btnStopTesting.click(function() {
    $.get('/stop-testing').done(function() {
      clearInterval(refreshInterval);
      btnStartTesting.prop('disabled', false).text(
        'Start Load Testing');
      btnStopTesting.prop('disabled', true);
    })
  });

  btnStartTesting.click(function() {
    if (!testingForm.checkValidity()) {
      alert('Invalid parameters!');
      return;
    }

    var formData = {
      'numberOfConcurrentUsers': inputNumberOfConcurrentUsers.val(),
      'numberOfJobsPerUser': inputNumberOfJobsPerUser.val(),
      'daysDatesBack': inputDaysDatesBack.val()
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
  });

  $(window).on('beforeunload', function() {
    $.get('/stop-testing');
  });
});
