let months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

function get_time(input) {
    var currentTime = new Date()
    var year = currentTime.getFullYear()
    let initial = input.split(" ")
    let time = initial[1]
    let date = initial[0]
    date = date.split("-")
    time = time.slice(0, -3);
    time = time.split(":")
    time[0] = parseInt(time[0])+1
    if (time[0] > 23){
        time[0]-=23;
    }
    date[1] = months[parseInt(date[1]) - 1]
    date.push(date.shift())
    date = date.toString()
    date = date.replace(year.toString(), "")
    date = date.replace(",", " ")
    time = time.toString()
    time = time.replace(",", ':')
    result = date + " " + time
    return (result)
}