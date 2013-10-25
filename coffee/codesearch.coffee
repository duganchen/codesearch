app = angular.module "CodeSearch", ["ngSanitize", "ui.bootstrap"]


controller = app.controller "SearchCtrl", ($scope, $http) ->

    $scope.search =
        term: ""
        results: []

    $scope.modal =
        body: ""
        title: ""
        url: "#"

    return


controller.directive "codesearchQuery", ($http) ->
    templateUrl: "query.html"
    link: (scope, element, attrs) ->
        scope.perform = ->
          q = escape scope.search.term.trim()
          if q.length > 0
              result = $http
                  method: "GET",
                  url: attrs.codesearchQuery,
                  params: "q": q
              result.success (data) ->
                  scope.search.results = data
                  return
          else
              scope.search.results = []
          return


controller.directive "codesearchPopup", ($http, $modal) ->

    templateUrl: "popup.html"
    link: (scope, element) ->
        scope.popup = ($event) ->

            $event.preventDefault()

            result = $http
                method: "GET"
                url: scope.result.ajax_url

            result.success (data) ->
                scope.modal.title = data.title
                scope.modal.body = data.body
                scope.modal.url = data.url
                $modal.open
                    templateUrl: "modal.html"
                    scope: scope
                return
            return
