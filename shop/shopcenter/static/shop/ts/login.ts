function login(url: string){
    $(document).ready(() => {
        $(".form-content-login-button").on("click", function(event){
            document.location.href = url
        })

        $(".form-content-create-button").on("click", (event) => {
            document.location.href = url
        })
    })
}