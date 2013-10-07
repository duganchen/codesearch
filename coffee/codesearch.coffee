jQuery ->
    search = (event) ->
        term = escape jQuery.trim $(event.target).val()

        if not term
            $("ul").empty()
            return

        populate = (data) ->
            jQuery("ul").empty()
            for filename in data
                li = "<li class=\"list-group-item\"><a href=\"/display?f=#{filename}\">#{filename}</a></li>"
                jQuery("ul").append li

        jQuery.getJSON "/search?q=#{term}", null, populate

    jQuery('input[type="search"]').keyup search
    jQuery('input[type="search"]').change search
