app = angular.module "CodeSearch", ["ngSanitize"]


controller = app.controller "SearchCtrl", ($scope, $http, modalService) ->

    $scope.search =
        term: ""
        results: []
    $scope.perform = ->
       q = $scope.search.term.trim()
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

    $scope.modal = modalService

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
