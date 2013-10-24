app = angular.module "CodeSearch", ["ngSanitize"]


controller = app.controller "SearchCtrl", ($scope, modalService, resultsService) ->

    $scope.results = resultsService
    $scope.modal = modalService
    $scope.search =
        term: ""
    return


controller.directive "codesearchSearch", ($http, resultsService) ->

    (scope, element, attrs) ->

        element.on "keyup", (event) ->

            q = escape event.target.value.trim()
            if q.length > 0
                result = $http
                    method: "GET",
                    url: attrs.codesearchSearch,
                    params: "q": q
                result.success (data) ->
                    resultsService.setResults data
                    return
            else
                resultsService.setResults []
            return


controller.factory "resultsService", ->

    _results = []

    getResults: ->
        return _results
    setResults: (value) ->
        _results = value
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



controller.directive "codesearchPopup", ($http, modalService) ->

    (scope, element, attrs) ->

        element.on "click", (event) ->
            event.preventDefault()

            result = $http
                method: "GET",
                url: attrs.codesearchPopup

            result.success (data) ->
                modalService.setTitle data.title
                modalService.setBody data.body
                modalService.setUrl data.url
                modalService.show()
                return
            return
        return
