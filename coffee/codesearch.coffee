app = angular.module "CodeSearch", ["ngSanitize"]


controller = app.controller "SearchCtrl", ($scope, $http) ->

    $scope.search =
        term: ""
        results: []
    $scope.perform = ->
       q = escape $scope.search.term.trim()
       if q.length > 0
           result = $http
               method: "GET",
               url: window.search_url,
               params: "q": q
           result.success (data) ->
               $scope.search.results = data
               return
       else
           $scope.search.results = []
       return

    $scope.modal =
        body: ""
        title: "",
        url: "#"

    return


controller.directive "codesearchPopup", ($http) ->

    (scope, element, attrs) ->

        element.on "click", (event) ->
            event.preventDefault()

            result = $http
                method: "GET",
                url: attrs.codesearchPopup

            result.success (data) ->
                scope.modal.title = data.title
                scope.modal.body = data.body
                scope.modal.url = data.url
                $('#myModal').modal(show: true)
                return
            return
        return
