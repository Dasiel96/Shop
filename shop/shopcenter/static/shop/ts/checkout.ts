let item_selected = 0
let item_to_run = 0
let run_counter = 0
let can_run = false
const run_speed_in_ms = 500
const msgs: Array<string> = [
    "Preparing your order for shipping",
    "Doing a quality check",
    "The order has been shipped",
    "The order is on its way",
    "Delivered!"
]

function getNumOfRunsInTimeFrame(seconds: number) {
    const runs_num_in_s = 1000 / run_speed_in_ms
    return seconds * runs_num_in_s
}
function checkout(url: string) {
    $(document).ready(() => {
        can_run = true
        $.post(url, {})
    })
}

setInterval(() => {
    if (can_run) {
        const prog_bar = $(".prog-bar")
        const prog_msg = $("#status-message")
        const prog_bar_child = $(prog_bar.children()[item_selected])
        if (item_selected < prog_bar.children().length && item_selected === item_to_run) {
            item_to_run++
            prog_bar_child.addClass("flash-anim")
            if (item_selected === 0) {
                prog_bar_child.addClass("first-child")
            }
            else if (item_selected === prog_bar.children().length - 1) {
                prog_bar_child.addClass("last_child")
            }
            prog_msg.text(msgs[item_selected])
        }
        else if (item_selected < prog_bar.children().length && run_counter >= getNumOfRunsInTimeFrame(60 * 2)) {
            prog_bar_child.removeClass("flash-anim")
            prog_bar_child.css("background-color", "red")
            item_selected += 1
            run_counter = 0
        }
        run_counter += 1
    }
}, run_speed_in_ms)