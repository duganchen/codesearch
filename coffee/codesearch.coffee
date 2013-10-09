$ ->

    display_url = (id) ->
        $("#display-url").text().slice(0, -1) + id

    ajax_display_url = (id) ->
        $("#display-ajax-url").text().slice(0, -1) + id

    search_url = $('#search-url').text()

    basename = (path) ->
        splits = path.split('/')
        length = splits.length
        splits[splits.length - 1]

    popup = (link_target) ->
        id = $(link_target).data('id')
        my_display_url = display_url(id)
        my_ajax_url = ajax_display_url(id)
        title = basename $(link_target).text()
        event.preventDefault()

        $.ajax
            url: my_ajax_url
            cache: false
            success: (data) ->
                $(".modal-title").text title
                $("#link").attr "href", my_display_url
                $('.modal-body').html(data)
                $('#myModal').modal(show=true)
                return
        return

    $("ul").click (event) ->
        if $(event.target).prop("tagName") is "A"
            event.preventDefault()
            popup(event.target)
        return

    search = (event) ->
        term = escape $.trim $(event.target).val()

        if not term
            $("ul").empty()
            return

        populate = (data) ->
            $("ul").empty()
            for result in data
                url = display_url(result.id)
                li = "<li class=\"list-group-item\"><a href=\"#{url}\" data-id=\"#{result.id}\">#{result.path}</a></li>"
                $("ul").append li
            return

        $.ajax
            url: "#{search_url}?q=#{term}"
            dataType: "json"
            success: populate
        return

    $('input[type="search"]').keyup search
    return
