
angular.module('cdat', ['ngWebworker'])
.controller('CDATControl', function($scope, $http, $timeout, Webworker) {

    $scope.init = function(){
        console.log('[+] Initializing CDAT window');
        $scope.boxfill = {
            "boxfill": {
                "test": {
                    "boxfill_type": "linear", 
                    "color_1": 16, 
                    "color_2": 239, 
                    "colormap": null, 
                    "datawc_calendar": 135441, 
                    "datawc_timeunits": "days since 2000", 
                    "datawc_x1": 1e+20, 
                    "datawc_x2": 1e+20, 
                    "datawc_y1": 1e+20, 
                    "datawc_y2": 1e+20, 
                    "ext_1": false, 
                    "ext_2": false, 
                    "fillareacolors": null, 
                    "fillareaindices": [1], 
                    "fillareaopacity": [], 
                    "fillareastyle": "solid", 
                    "legend": null, 
                    "level_1": 1e+20, 
                    "level_2": 1e+20, 
                    "levels": [1e+20, 1e+20], 
                    "missing": 1, 
                    "projection": "linear", 
                    "xaxisconvert": "linear", 
                    "xmtics1": "", 
                    "xmtics2": "", 
                    "xticlabels1": "*", 
                    "xticlabels2": "*", 
                    "yaxisconvert": "linear", 
                    "ymtics1": "", 
                    "ymtics2": "", 
                    "yticlabels1": "*", 
                    "yticlabels2": "*"
                }
            }
        };
        $scope.selected_source = undefined;
        $scope.data_options = undefined;
        $scope.get_user();
        $scope.load_user_data();
        $scope.d_limit = 10;
        $('.collapsible').collapsible({
            accordion : false
        });
    }

    $scope.visualize_nc = (filename, run_name) => {
        var name_split = run_name.split('_');
        var run_id = name_split.last();
        var run_name = run_split.splice(0, name_split.length - 2).join('');
        $http({
            url: '/cdat/get_provenance/',
            method: 'POST',
            headers: {
              'X-CSRFToken' : $scope.get_csrf()
            },
            data: {
                'file_name': file_name,
                'run_name': run_name,
                'run_id': run_id
            }
        }).then((res) => {
            console.log(res.data);
            var vizContainer = $('#vizContainer');
            var parent = vizContainer.parents('.lm_content');
            var width = parent.width();
            var height = parent.height();
            vizContainer.width(width);
            vizContainer.height(height);
            $scope.canvas = VCS.init('#vizContainer');
            $scope.canvas.plot(res.data, $scope.boxfill);
        }).catch((res) => {
            console.log(res);
        });
    }

    $scope.select_source = (source) => {
        $scope.selected_source = source;
        if(source == 'diagnostic'){
            $scope.load_diagnostic_data();
        }
        else if(source == 'model'){
            $scope.load_model_data();
        } else {
            console.log('Unrecognized source: ' + source);
            return;
        }
    }

    $scope.load_diagnostic_data = () => {
        // load users available diagnostic data
        $scope.select_data = $scope.user_data[window.ACMEDashboard.user]['diagnostic_output'];
        $scope.select_data_keys = Object.keys($scope.select_data);
    };

    $scope.load_model_data = () => {
        // load users available model data
        $scope.select_data = $scope.user_data[window.ACMEDashboard.user]['model_output'];
        $scope.select_data_keys = Object.keys($scope.select_data);
    };

    $scope.increase_d_limit = (all) => {
        if(all){
            $scope.d_limit = $scope.selected_data_options.length;
        } else {
            $scope.d_limit += 10;
        }
    }

    $scope.select_data_option = (data) => {
        if($scope.selected_data_option == data){
            return;
        } else {
            $scope.selected_data_option = data;
            $scope.selected_data_options = [];
            for(k in $scope.select_data[data]['amwg']){
                if(k.endsWith('.nc')){
                    $scope.selected_data_options.push(k);
                }
            }
            $('.collapsible').collapsible({
                accordion : false
            });
        }

    }

    $scope.load_user_data = () => {
        if(window.ACMEDashboard.user_data){
            return;
        } else {
            window.ACMEDashboard.user_data = 'pending';
        }
        var worker = Webworker.create(window.ACMEDashboard.ajax, {async: true });
        var data = {
            'url': 'http://aims2.llnl.gov:8000/esgf/get_user_data',
            'method': 'GET'
        };
        worker.run(data).then((result) => {
            $scope.user_data = JSON.parse(result);
            window.ACMEDashboard.user_data = $scope.user_data;
        }).catch((res) => {
            console.log(res);
        });
    }

    $scope.get_user = () => {
        if(window.ACMEDashboard.user){
            return;
        } else {
            window.ACMEDashboard.user = 'pending';
        }
        var worker = Webworker.create(window.ACMEDashboard.ajax, {async: true });
        var data = {
            'url': 'http://aims2.llnl.gov:8000/run_manager/get_user/',
            'method': 'GET'
        };
        worker.run(data).then((result) => {
            window.ACMEDashboard.user = result;
        }).catch((res) => {
            console.log(res);
        });
    }

    $scope.get_csrf = () => {
      var cookieValue = null;
      var name = 'csrftoken';
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
    }
})
.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    return $interpolateProvider.endSymbol(']]');
});
