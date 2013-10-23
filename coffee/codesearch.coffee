app = angular.module "CodeSearch", ["ngSanitize"]


controller = app.controller "SearchCtrl", ($scope, $http) ->

    $scope.model =
        term: ""
        #$scope.modal = modalService

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



modalController = app.controller "ModalCtrl", ($scope, modalService) ->
    $scope.modal = modalService
    return


modalController.factory "modalService", ->
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



modalController.directive "popup", ($http, modalService) ->

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
