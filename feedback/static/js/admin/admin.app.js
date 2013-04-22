define(['admin/controllers'], function(controllers) {
  angular.module('admin', [])
    .config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
      $locationProvider.html5Mode(true);
      $routeProvider.when('/admin/projects', {
        templateUrl: '/static/templates/admin/dashboard.html',
        controller: controllers.AdminCtrls
      }).when('/admin/projects/new', {
        templateUrl: '/static/templates/admin/projects/new.html',
        controller: controllers.AdminCtrls
      }).when('/admin/statistics', {
        templateUrl: '/static/templates/admin/statistics.html',
        controller: controllers.AdminCtrls
      });
    }]);
});