(function () {
    'use strict';

    window.addEventListener('DOMContentLoaded', function () {
        document.querySelector('form').addEventListener('submit', function () {
            document.querySelector("input[type=search]").readOnly = true;
            document.querySelector("button[type=submit]").disabled = true;
            document.querySelector("img").classList.remove("hidden");
        });
    });

    /*
    Restore the page when the back button is pressed.
    see: http://stackoverflow.com/a/201406
    */
    window.addEventListener("unload", function () { return; });
}());
