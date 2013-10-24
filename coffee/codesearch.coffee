app = angular.module "CodeSearch", ["ngSanitize"]


controller = app.controller "SearchCtrl", ($scope, $http, modalService) ->

    $scope.search =
        term: ""
        results: []
    $scope.modal = modalService

    $scope.do_search = ->
        q = $scope.search.term.trim()
        if q.length > 0
            result = $http
                method: "GET",
                url: window.urls.search,
                params: "q": q
            result.success (data) ->
                $scope.search.results = data
                return
        else
            $scope.search.results = []
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



controller.directive "popup", ($http, modalService) ->

    (scope, element, attrs) ->

        attrs.$observe "popup", ->
            element.bind "click", (event) ->
                event.preventDefault()

                result = $http
                    method: "GET",
                    url: attrs.popup

                result.success (data) ->
                    modalService.setTitle data.title
                    modalService.setBody data.body
                    modalService.setUrl data.url
                    modalService.show()
                    return
                return
            return
        return
