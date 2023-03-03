document.addEventListener("DOMContentLoaded", function () {
     setInterval(notification, 2000)

})
function notification() {
     while (true) {
          let username = document.getElementById("trig_not").value

          let url = window.location.origin
          let request = new XMLHttpRequest();

          /* Fetch notification */

          request.open("GET", url + "/notification/" + username);
          request.send();
          request.onload = () => {
               a = 0
               if (request.status === 200) {
                    var data = JSON.parse(request.response)
                    if (data.length > 0) {
                         document.getElementById("bell").style.color = "red"
                    }
               }
          }
          break
     }
}

function notify() {
     input = ""
     let a = 0
     let not = document.getElementById("notify")
     let notify_body = document.getElementById("notify_body")
     input = document.getElementById("trig_not").value

     /* Display Box */
     not.style.display = "block"
     let url = window.location.origin
     let request = new XMLHttpRequest();
     /* Fetch notification */
     request.open("GET", url + "/notification/" + input);
     request.send();
     request.onload = () => {
          a = 0
          if (request.status === 200) {
               var data = JSON.parse(request.response)
               notify_body.innerHTML = ""
               not.style.display = "block"
               if (data.length > 0) {
                    document.getElementById("notify_header").innerHTML = "Unread Messages"
               }
               else {
                    document.getElementById("notify_header").innerHTML = "No New Messages"
               }

               for (let obj of data) {
                    /* Display Users */
                    var v_cont = document.createElement('div')
                    v_cont.setAttribute('class', 'v_cont')
                    var name_link = document.createElement('a')
                    name_link.setAttribute('style', 'display: inline-flex;')
                    pic = document.createElement('img')
                    pic.setAttribute('src', '/static/favicon.ico')
                    pic.setAttribute('style', 'width: 50px; border-radius: 25px; margin-top: 20px; margin-left: 30px')
                    name_link.appendChild(pic)
                    var name = document.createElement('div');
                    name.setAttribute('class', 'p')
                    name.textContent = obj;
                    name_link.setAttribute('href', "/chat/" + obj)
                    name.setAttribute('style', 'margin-left: 10px; margin-top: 30px;')
                    name_link.appendChild(name)
                    v_cont.appendChild(name_link)
                    notify_body.appendChild(v_cont)
               }
          }
     }

}
/* Close Pop Up */
function close_notify() {
     let notify = document.getElementById("notify")
     notify.style.display = "none"
}
