jQuery ->

    display_url = (id) ->
        jQuery("#display-url").text().slice(0, -1) + id

    ajax_display_url = (id) ->
        jQuery("#display-ajax-url").text().slice(0, -1) + id

    search_url = jQuery('#search-url').text()

    basename = (path) ->
        splits = path.split('/')
        length = splits.length
        splits[splits.length - 1]

    $("ul").on "click", "a", (event) ->

        event.preventDefault()

        id = $(this).data('id')
        my_display_url = display_url(id)
        my_ajax_url = ajax_display_url(id)

        $('#myModal').modal(show=true)

        title = basename $(event.target).text()

        $.get my_ajax_url, null, (data) ->
            $(".modal-title").text title
            $("#link").attr "href", my_display_url
            $('.modal-body').html(data)
            $('#myModal').modal(show=true)

    search = (event) ->
        term = escape jQuery.trim $(event.target).val()

        if not term
            $("ul").empty()
            return

        populate = (data) ->
            jQuery("ul").empty()
            for result in data
                url = display_url(result.id)
                li = "<li class=\"list-group-item\"><a href=\"#{url}\" data-id=\"#{result.id}\">#{result.path}</a></li>"
                jQuery("ul").append li

        jQuery.getJSON "#{search_url}?q=#{term}", null, populate

    jQuery('input[type="search"]').keyup search
    jQuery('input[type="search"]').change search
