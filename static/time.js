let months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
let days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
function get_time(input) {
    var currentTime = new Date()
    var year = parseInt(currentTime.getFullYear())
    var month = parseInt(currentTime.getMonth())
    var day = parseInt(currentTime.getDate())
    var hour = parseInt(currentTime.getHours())
    var minutes = parseInt(currentTime.getMinutes())
    var seconds = parseInt(currentTime.getSeconds())
    let initial = input.split(" ")
    let date = initial[0].split("-")
    let time = initial[1].split(":")
    var old_year = parseInt(date[0])
    var old_month = parseInt(date[1])
    var old_day = parseInt(date[2])
    var old_hour = parseInt(time[0])
    var old_minutes = parseInt(time[1]).toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping: false})
    var old_seconds = parseInt(time[2])
    old_hour = parseInt(old_hour)+1
    if (old_hour > 23){
        old_hour-=23;
    }
    if (year == old_year) {
        if (month + 1 == old_month) {
            if (day == old_day) {
                if (hour == old_hour){
                    if (minutes == old_minutes) {
                        if ((seconds - old_seconds) < 2){
                            result = "Just Now"
                        }
                        else {
                            result = (seconds - old_seconds) + " Seconds ago."
                        }
                        
                    }
                    else {
                        if ((minutes - old_minutes) < 2){
                            result = "1 Minute ago."
                        }
                        else {
                            result = (minutes - old_minutes) + " Minutes ago."
                        }
                    }
                }
                else {
                    if ((hour - old_hour) < 2){
                        result = "1 Hour ago."
                    }
                    else {
                        result = (hour - old_hour) + " Hours ago."
                    }
                }
            }
            else if ((day - old_day)  < 2) {
                result = "Yesterday at " + old_hour + ":" + old_minutes
            }
            else if ((day - old_day)  < 7) {
                let c_day = currentTime.getDay()
                c_day = c_day - (day - old_day)
                if (c_day < 0) {
                    c_day += 6
                }
                c_day = days[c_day]
                result = c_day + " at " + old_hour + ":" + old_minutes
            }
            else {
                result = months[old_month - 1] + " " + old_day + " at " + old_hour + ":" + old_minutes
            }
        }
        else {
            result = months[old_month - 1] + " " + old_day + " at " + old_hour + ":" + old_minutes
        }
    }
    else {
        result = months[old_month - 1] + " " + old_day + ", " + old_year + " at " + old_hour + ":" + old_minutes
    }
    return (result)
}