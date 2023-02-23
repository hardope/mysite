let react = ""
function load() {
    let a = 1
    let url = window.location.origin
    let request = new XMLHttpRequest();
    let body = document.querySelector('#body');
    request.open("GET", url + "/posts/open");
    request.send();
    request.onload = () => {
       if (request.status === 200) {
            let body = document.querySelector('#body');
            for (let obj of JSON.parse(request.response)) {
                var name_container = document.createElement('div')
                var name_link = document.createElement('a')
                name_container.setAttribute('class', 'name_container')
                name_link.setAttribute('style', 'display: inline-flex;')
                pic = document.createElement('img')
                pic.setAttribute('src', '/static/favicon.ico')
                pic.setAttribute('style', 'width: 50px; border-radius: 25px; margin-top: 20px; margin-left: 30px')
                name_link.appendChild(pic)
                var name = document.createElement('div');
                name.setAttribute('class', 'p')
                name.textContent = obj[1];
                name_link.setAttribute('href', "/profile/" + obj[1])
                name.setAttribute('style', 'margin-left: 10px; margin-top: 30px;')
                name_link.appendChild(name)
                name_container.appendChild(name_link)
                body.appendChild(name_container)
                var time = document.createElement('p');
                time.setAttribute('style', 'margin-top: -10px; margin-left: 30px; font-size: 15px !important;')
                time.setAttribute('class', 'a')
                time.textContent = get_time(obj[3]);
                body.appendChild(time);
                var tag = document.createElement('div');
                tag.textContent = obj[2];
                tag.setAttribute('class', 'div')
                body.appendChild(tag);
                if (obj[7] === "True"){
                    let link = document.createElement('a');
                    link.setAttribute("href", '/static/'+ obj[0] +'.jpg')
                    var pic = document.createElement('img');
                    pic.setAttribute('src', '/static/'+ obj[0] +'.jpg')
                    link.appendChild(pic)
                    body.appendChild(link)
                }
                var container = document.createElement('div');
                container.setAttribute('class', 'container')
                var react = document.createElement('p')
                react.setAttribute('class', 'react')
                react.setAttribute('value', obj[5])
                react.setAttribute('id', obj[0])
                react.setAttribute('style', 'inline')
                react.setAttribute('onclick', 'like(' + obj[0] + ')')
                react.textContent = obj[4];
                container.appendChild(react)
                var link = document.createElement('a')
                link.setAttribute('href', '/comment/' + obj[0])
                var comment = document.createElement('p')
                comment.setAttribute('class', 'comment')
                comment.setAttribute('style', 'inline')
                comment.textContent = obj[6] + ' 💬';
                link.appendChild(comment)
                container.appendChild(link)
                body.appendChild(container)

                a+=1
            }
       }
    }

}

document.addEventListener("DOMContentLoaded", load)