interface Urls2 {
    [key: string]: string
}

function shopping(url: Urls2){
    $(document).ready(() => {
        $(".item-grid-product-img").click(function()  {
            const img_path = this.getAttribute("src")!!.split("/")
            const img_name = img_path[img_path.length - 1]
            console.log("working", img_name)
            if(img_name){
                console.log(img_name, url.item_url)
                $.post(url.item_url, {"item_name": img_name}, function(data) {
                    window.location.href = data["url"]
                })
            }
        })
    })
}