document.addEventListener('DOMContentLoaded', function(){
        let username = "{{username}}"
        var list;
        var newlist;
        let url = window.location.origin
        let months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

        let request = new XMLHttpRequest();
        request.open("GET", url + "/api/{{recipient}}");
        request.send();
        request.onload = () => {
            if (request.status === 200) {
                let body = document.querySelector('#body');
                list = JSON.parse(request.response);
                newlist = list;
                for (let obj of JSON.parse(request.response)) {
                    if (obj[1] === username ) {
                            var tag = document.createElement('p');
                            tag.textContent = obj[3]
                            tag.setAttribute('class', 'from-me margin-b_none')
                            tag.setAttribute('style', 'font-size: 20px;')
                            body.appendChild(tag);
                            var date = document.createElement('small')
                            date.textContent = get_time(obj[4])
                            date.setAttribute('style', 'text-align: right; font-size: 15px !important')
                            body.appendChild(date)
                    } else {
                            var tag = document.createElement('p');
                            tag.textContent = obj[3]
                            tag.setAttribute('class', 'from-them')
                            tag.setAttribute('style', 'font-size: 20px;')
                            body.appendChild(tag);
                            var date = document.createElement('small')
                            date.textContent = get_time(obj[4])
                            date.setAttribute('style', 'text-align: left; font-size: 15px !important')
                            body.appendChild(date)
                    }
                }
                window.scrollTo(0, 10000);
            }
        }
        function refresh() {
            let request = new XMLHttpRequest();
            request.open("GET", url + "/api/{{recipient}}");
            request.send();
            request.onload = () => {
                if (request.status === 200) {
                    newlist = JSON.parse(request.response);
                    if (newlist.length > list.length){
                        var count = newlist.length - list.length;
                        for (let i = list.length -1; i < newlist.length-1; i++){
                            if (newlist[i+1][1] === username ) {
                                var tag = document.createElement('p');
                                tag.textContent = newlist[i+1][3];
                                tag.setAttribute('class', 'from-me')
                                tag.setAttribute('style', 'font-size: 20px;')
                                body.appendChild(tag);
                                var date = document.createElement('small')
                                date.textContent = get_time(newlist[i+1][4]);
                                date.setAttribute('style', 'text-align: right; font-size: 15px !important')
                                body.appendChild(date)
                            } else{
                                var tag = document.createElement('p');
                                tag.textContent = newlist[i+1][3];
                                tag.setAttribute('class', 'from-them')
                                tag.setAttribute('style', 'font-size: 20px;')
                                body.appendChild(tag);
                                var date = document.createElement('small')
                                date.textContent = get_time(newlist[i+1][4]);
                                date.setAttribute('style', 'text-align: left; font-size: 15px !important')
                                body.appendChild(date)
                            }
                        }
                        list = newlist;
                        window.scrollTo(0, 10000);
                    }
                }
            }
        }
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
        setInterval(refresh, 1000);
        document.querySelector('#submit').disabled = true;

        document.querySelector('#message').onkeyup = () => {
            if (document.querySelector('#message').value.length > 0){
                document.querySelector('#submit').disabled = false;
            }
            else {
                document.querySelector('#submit').disabled = true;
            }
        }
        document.querySelector('#form').onsubmit = () => {
            let message = document.querySelector('#message').value;
            let newmessage = new XMLHttpRequest();
            var formdata = new FormData()
            formdata.append("message", message)
            newmessage.open("POST", url + "/messages/{{recipient}}");
            newmessage.send(formdata);
            document.querySelector('#message').value = '';
            document.querySelector('#submit').disabled = true;
            return false
        }
    });