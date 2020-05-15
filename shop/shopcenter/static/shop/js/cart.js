"use strict";
let num_to_remove = {};
function cart(urls) {
    $(document).ready(() => {
        const btn = $(".cart-item-btn-sub");
        const num_input = $(".num-input");
        $(btn).on("click", function (event) {
            event.stopPropagation();
            event.stopImmediatePropagation();
            let base_id = this.getAttribute("id").substring(4);
            console.log(base_id, num_to_remove[base_id]);
            if (num_to_remove[base_id] !== null && num_to_remove[base_id] !== undefined) {
                $.ajax({
                    type: "POST",
                    url: urls.del_url,
                    data: { "src": base_id, "num_to_remove": num_to_remove[base_id] },
                    dataType: "json",
                    statusCode: {
                        200: (data) => {
                            $(this).parent().parent().remove();
                        }
                    }
                });
            }
        });
        $(num_input).on("click", function (event) {
            event.stopPropagation();
            event.stopImmediatePropagation();
            const base_id = this.getAttribute("id").substring(4);
            console.log(base_id);
            num_to_remove[base_id] = Number(num_input.val());
        });
        // btn.click(function () {
        //     const id = this.id
        //     console.log(id)
        //     if (id) {
        //         const base_id = id.substring(4)
        //         console.log(base_id, num_to_remove, val_id)
        //         if (!id) {
        //             $.post(urls.del_url, { "src": base_id, "num_to_remove": Number(num_to_remove) }, (data) => {
        //                 const div = $(`#div-${base_id}`)
        //                 if (data.remove && div) {
        //                     div.remove()
        //                 }
        //             })
        //         }
        //     }
        // })
    });
}
