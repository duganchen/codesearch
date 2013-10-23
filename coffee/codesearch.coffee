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
                return
        else
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
        return
    setUrl: (newUrl) ->
        href = newUrl
        return
    setBody: (newBody) ->
        body = newBody
        return
    show: ->
        $('#myModal').modal(show: true)
        return


controller.directive "popup", ($http) ->

    (scope, element, attrs) ->

        attrs.$observe "popup", ->
            element.bind "click", (event) ->
                event.preventDefault()

                result = $http
                    method: "GET",
                    url: attrs.popup

                result.success (data) ->
                    scope.modal.setTitle data.title
                    scope.modal.setBody data.body
                    scope.modal.setUrl data.url
                    scope.modal.show()
                return
            return
        return
