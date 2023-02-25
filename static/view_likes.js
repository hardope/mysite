/* Function to pop up view to display likes for a specific post */

function view_likes(input) {
    let a = 0
    let viewer = document.getElementById("like_viewer")
    let viewer_body = document.getElementById("viewer_body")

    /* Display Box */
    viewer.style.display = "block"
    let url = window.location.origin
    let request = new XMLHttpRequest();
    /* Fetch List of users */
    request.open("GET", url + "/view_likes/" + input);
    request.send();
    request.onload = () => {
        if (request.status === 200) {
            viewer_body.innerHTML = ""
           for (let obj of JSON.parse(request.response)) {
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
                name_link.setAttribute('href', "/profile/" + obj)
                name.setAttribute('style', 'margin-left: 10px; margin-top: 30px;')
                name_link.appendChild(name)
                v_cont.appendChild(name_link)
                viewer_body.appendChild(v_cont)

                a+=1
            }
            /* If there are no likes */
            if (a == 0) {
                let viewer = document.getElementById("viewer_body")
                let no_like = document.createElement('p')
                no_like.textContent = 'No Likes Yet'
                viewer.appendChild(no_like)
            }
        }
    }
}
/* Close Pop Up */
function close_likes() {
    let viewer = document.getElementById("like_viewer")
    let viewer_body = document.getElementById("viewer_body")
    viewer.style.display = "none"
    viewer_body.innerHTML = ""
}