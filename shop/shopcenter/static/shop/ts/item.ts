interface Urls1 {
    [key: string]: string
}

function item(urls: Urls1){
    $(document).ready(() => {
        $(".add-cart").click(function() {
            const img_name = this.getAttribute("data-img")
            if(img_name){
                $.post(urls.add_url, {"img_name": img_name}, (data) => {
                    window.location.href = data["url"]
                })
            }
        })
    })
}