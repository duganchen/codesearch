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

        id = $(this).data('id')
        my_display_url = display_url(id)
        my_ajax_url = ajax_display_url(id)

        title = basename $(event.target).text()

        event.preventDefault()

        jQuery.ajax
            url: my_ajax_url
            cache: false
            success: (data) ->
                $(".modal-title").text title
                $("#link").attr "href", my_display_url
                $('.modal-body').html(data)
                $('#myModal').modal(show=true)
                return
        return

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
            return

        jQuery.ajax
            url: "#{search_url}?q=#{term}"
            dataType: "json"
            success: populate
        return

    jQuery('input[type="search"]').keyup search
    jQuery('input[type="search"]').change search
    return
