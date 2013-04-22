/**
 * Administrator Controllers
 *
 * @author Daegeun Kim
 */
define(['commons/notification'], function(notification) {
  function GlobalCtrl($scope, $http, $location, $window) {
    $scope.home = function() {
      $window.location = '/';
    };
  };  
  GlobalCtrl.$inject = ['$scope', '$http', '$location', '$window'];

  function NewProjectCtrl($scope, $http, $location) {
    $scope.project = {};
    $scope.errors = {};

    $scope.submit = function() {
      $http({method: 'POST', url: '/admin/projects', data: $scope.project}).success(function(json) {
        notification.success('프로젝트가 등록되었습니다.');
        $location.path('/admin/projects');
      }).error(function(json) {
        notification.error('프로젝트이 등록되지 않았어요. 부족한 내용을 채워주세요.');
        $scope.errors = json.errors;
      });
    };

    $scope.cancel = function() {
      $location.path('/admin/projects');
    };
  };
  NewProjectCtrl.$inject = ['$scope', '$http', '$location'];

  function AdminCtrls($scope) {
    $scope.GlobalCtrl = GlobalCtrl;
    $scope.NewProjectCtrl = NewProjectCtrl;
  };
  AdminCtrls.$inject = ['$scope'];

  return {
    AdminCtrls: AdminCtrls
  };
});