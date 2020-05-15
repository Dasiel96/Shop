"use strict";
function item(urls) {
    $(document).ready(() => {
        $(".add-cart").click(function () {
            const img_name = this.getAttribute("data-img");
            if (img_name) {
                $.post(urls.add_url, { "img_name": img_name }, (data) => {
                    window.location.href = data["url"];
                });
            }
        });
    });
}
