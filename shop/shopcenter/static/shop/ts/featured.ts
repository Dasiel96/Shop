function featured(url: string){
    $(document).ready(() => {
        $(".item-grid-next-btn").click((event) => {
            event.stopPropagation()
            event.stopImmediatePropagation()
            console.log("working")
            const img = $(".ft-img")
            $.get(url, (data) => {
                img.attr("src", data.url)
            })
        })

        $(".item-grid-back-btn").click((event) => {
            event.stopPropagation()
            event.stopImmediatePropagation()

            const img = $(".ft-img")
            $.get(url, (data) => {
                img.attr("src", data.url)
            })
        })
    })
}