app = angular.module "CodeSearch", ["ngSanitize"]


controller = app.controller "SearchCtrl", ($scope, $http, modalService) ->

    $scope.model =
        term: ""
    $scope.modal = modalService

    $scope.search = ->
        q = $scope.model.term.trim()
        if q.length > 0
            result = $http
                method: "GET",
                url: window.urls.search,
                params: q: "q"
            result.success (data) ->
                $scope.results = data
        else:
            $scope.results = []
        return
    return


controller.factory "modalService", ->
    href = "#"
    title = ""
    body = ""

    getUrl: -> href,
    getTitle: -> title
    getBody: -> body
    setTitle: (newTitle) ->
        title = newTitle
    setUrl: (newUrl) ->
        href = newUrl
    setBody: (newBody) ->

        body = newBody
    show: ->
        $('#myModal').modal(show=true)


controller.directive "popup", ($http) ->

    (scope, element) ->

        element.bind "click", (event) ->
            event.preventDefault()

            result = $http
                method: "GET",
                url: event.target.dataset.ajaxUrl

            result.success (data) ->
                scope.modal.setTitle data.title
                scope.modal.setBody data.body
                scope.modal.setUrl data.url
                scope.modal.show()
            return
        return
