export function performLike(event){
    const csrftoken = Cookies.get('csrftoken');

    const likeBtn = event.target;
    const liked = likeBtn.dataset.liked;
    const postID = likeBtn.dataset.id;

    let request_url = '';
    if(liked=='false'){ // perform unlike
        request_url = `/posts/${postID}/unlike/`;
    }else if(liked=='true'){ // perform like
        request_url = `/posts/${postID}/like/`;
    }
    fetch(request_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        }
    })
    .then(response => {
        if(response.ok) return response.json()
    })
    .then(JSONResponse => {
        likeBtn.innerHTML = `<span class="material-icons md-15">favorite</span>${JSONResponse['like']}`;
    })
}
