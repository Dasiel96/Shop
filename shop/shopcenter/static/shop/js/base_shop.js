"use strict";
let search_bar = null;
let is_ready = false;
function base_shop(url) {
    $(document).ready(() => {
        $("#search-button").click(() => {
            console.log("working");
            console.log($("#search-box").val());
            $.ajax({
                type: "POST",
                url: url.search_url,
                data: { "search string": $("#search-box").val() },
                success: (data) => {
                    window.location.href = data.url;
                },
                error: (s, e, t) => {
                    console.log(s.statusCode);
                }
            });
        });
        $(".item-grid-product-img").click(function (event) {
            event.stopPropagation();
            event.stopImmediatePropagation();
            const img_path = this.getAttribute("src").split("/");
            const img_name = img_path[img_path.length - 1];
            console.log("working", img_name);
            if (img_name) {
                console.log(img_name, url.item_url);
                $.post(url.item_url, { "item_name": img_name }, function (data) {
                    window.location.href = data["url"];
                });
            }
        });
    });
}
