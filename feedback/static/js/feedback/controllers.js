define(['fn', 'commons/notification'], function(fn, notification) {
  function GlobalCtrl($scope, $http, $location, $window, $routeParams) {
    var path = $location.path();
    $scope.projects = [];
    $scope.pathVariables = {};
    $scope.navigation = path.split('/').length > 1 ? path.split('/')[1] : 'projects';

    loadProjects();

    function loadProjects() {
      $http.get('/api/v1/projects/').success(function(json) {
        $scope.projects = json.items;
        if ($scope.projects == null || $scope.projects.length == 0) {
          notification.error('등록된 프로젝트가 없어 티켓을 등록할 수 없습니다. 먼저, 등록하신 후에 이용해주세요.');
          notification.info('프로젝트 등록은 <a href="/admin/projects">이 페이지 (링크)</a>에서 등록 가능합니다.');
        }
      });
    };

    $scope.admin = function() {
      $window.location = '/admin/projects';
    }

    $scope.showTickets = function() {
      $location.path('/projects');
    };

    $scope.newTicket = function() {
      $location.path('/tickets/new');
    };

    $scope.isActive = function(type, id) {
      if (type == 'path') {
        return id == $location.path();
      } else if (type == 'nav') {
        return id == $scope.navigation;
      }
    };
  };
  GlobalCtrl.$inject = ['$scope', '$http', '$location', '$window', '$routeParams'];

  function NewTicketCtrl($scope, $http, $location, $routeParams) {
    $scope.ticket = {};
    $scope.errors = null;

    $scope.hasError = function(field) {
      return $scope.errors && $scope.errors[field];
    };

    $scope.submit = function() {
      var ticket = $scope.ticket;
      $http.post('/api/v1/tickets/', ticket).success(function(json) {
        $location.path('/projects');
        notification.success('티켓이 등록되었습니다.');
      }).error(function(json) {
        notification.error('티켓이 등록되지 않았어요. 부족한 내용을 채워주세요.');
        $scope.errors = json.errors;
      });
    };

    $scope.cancel = function() {
      $location.path('/').replace();
    };
  };
  NewTicketCtrl.$inject = ['$scope', '$http', '$location', '$routeParams'];

  function TicketsCtrl($scope, $http, $location, $routeParams, $cookieStore) {
    $scope.tickets = [];
    $scope.meta = {
      loading: false
      , loadGauge: 0
      , continuation: null
    };
    $scope.pathVariables['project'] = $routeParams.id;
    loadTickets();

    $scope.toggle = function(ticket) {
      if (!ticket._meta.expand) {
        ticket._meta.expand = false;
      }
      ticket._meta.expand = !ticket._meta.expand;
    };

    $scope.isChecked = function(ticket) {
      if (ticket && ticket.id) {
        return $cookieStore.get('ticket:'+ticket.id) == '1';
      }
      return false;
    };

    $scope.like = function(ticket) {
      if ($scope.isChecked(ticket)) {
        notification.info('이미 추천했어요.');
        return;
      }
      $http({method: 'PUT', url: '/api/v1/tickets/'+ticket.id+'/connects?op=like'}).success( function(json) {
        $cookieStore.put('ticket:'+ticket.id, '1');
        notification.success('추천했어요.');
        ticket.connects = parseInt(ticket.connects) + 1;
      }).error(function(json) {
        notification.error('추천이 되지 않았습니다. 잠시 후 다시 시도해주세요.');
      });
    };

    $scope.moreTickets = function() {
      loadTickets();
    };

    $scope.collapse = function(ticket) {
      ticket._meta.expand = false;
    };
    $scope.expand = function(ticket) {
      ticket._meta.expand = true;
    };

    function loadTickets() {
      var params = {};
      if ($routeParams.id) {
        params = {project_id: $routeParams.id};
      }
      if ($scope.meta.continuation) {
        params.max_id = $scope.meta.continuation;
      }

      var TIMES = 10;
      var repeat = fn.repeat(function(remain) {
        if (remain == 1) {
          $scope.meta.loading = false;
          $scope.meta.loadGauge = 0;
        }
        $scope.meta.loadGauge = 100 - (remain - 1) * 10;
        if (remain < TIMES / 2) {
          // slow ajax loads. interval * TIMES / 2 (ms)
          $scope.meta.loading = true;
          $scope.$digest();
        }
      }, {interval: 20, times: TIMES});

      var MAX_LENGTH = 300; // limit
      $http({method: 'get', url: '/api/v1/tickets/', params: params}).success(function(json) {
        var tickets = json.items.map(function(i) {
          i.summary = i.description && i.description.length > MAX_LENGTH ?
              i.description.substring(0, MAX_LENGTH) + ' ...' : i.description;
          i.summary = i.summary.replace(/<[\/a-zA-Z0-9]+>/g, ' ');
          i._meta = {};
          return i;
        });
        $scope.tickets = $scope.tickets.concat(tickets);
        $scope.meta.continuation = json.continuation;
        repeat.stop(function() {
          $scope.meta.loading = false;
        });
      });
    };
  };
  TicketsCtrl.$inject = ['$scope', '$http', '$location', '$routeParams', '$cookieStore'];

  function FeedbackCtrls($scope) {
    $scope.TicketsCtrl = TicketsCtrl;
    $scope.NewTicketCtrl = NewTicketCtrl;
    $scope.GlobalCtrl = GlobalCtrl;
  };
  FeedbackCtrls.$inject = ['$scope'];

  return {
    FeedbackCtrls: FeedbackCtrls
  }
});