const csrftoken = Cookies.get('csrftoken');
const host_user_id = JSON.parse(document.querySelector("#user_id").textContent);

function getPosts(request_url, page, container){
    fetch(request_url+`?page=${page}`)
    .then(response => {
        if(response.ok){
            return response.json();
        } else {
            window.location.href = '/pagenotfound';
            throw new Error('Sorry, something went wrong !');
        }
    })
    .then(data => {
        container.innerHTML = ''; // clear .all-posts for every time reloading the page. Is there better way to handle this ?
        paginatePosts(data, request_url, page, container);
        data['results'].forEach(post => populatePost(post, container))
    })
    .catch((error) => {
        console.error('Error: ', error);
    });
}

function paginatePosts(data, request_url, page, container){
    /*
    data: JSON response
    */
    const pagination = document.querySelector('.pagination');
    pagination.innerHTML = ''; // clear previous DOMs

    if (data['previous'] != null){
        const previous = document.createElement('li');
        previous.classList.add('page-item'); // Bootstrap class

        const previousLink = document.createElement('a');
        previousLink.addEventListener('click', (e) =>{
            getPosts(request_url, page-1,container);
        })
        previousLink.innerHTML = 'Previous';

        previous.appendChild(previousLink);
        pagination.appendChild(previous);
    }

    const ithPageItem = document.createElement('li');
    ithPageItem.classList.add('page-item');
    ithPageItem.innerHTML = `${page}`;
    pagination.appendChild(ithPageItem);

    if (data['next'] != null){
        const next = document.createElement('li');
        next.classList.add('page-item'); // Bootstrap class

        const nextLink = document.createElement('a');
        nextLink.addEventListener('click', (e) =>{
            getPosts(request_url, page+1,container);
        })
        nextLink.innerHTML = 'Next';

        next.appendChild(nextLink);
        pagination.appendChild(next);
    }
    
}

function populatePost(item, parentContainer){
    // create headContainer that has 2 child elements: poster and editBtn
    const headerContainer = document.createElement('div');
    headerContainer.className = 'post__header';
    createPostHeader(item, headerContainer);

    // create bodyContainer that has 2 child elements: content and timestamp
    const bodyContainer = document.createElement('div');
    bodyContainer.className = 'post__body';
    createPostBody(item, bodyContainer);

    // create footerContainer that has 2 child elements: likeBtn and likes
    const footerContainer = document.createElement('div');
    footerContainer.className = 'post__footer';
    createPostFooter(item, footerContainer);

    // create postContainer that have 3 child elements: headerContainer, bodyContainer and footerContainer
    //const postContainer = document.createElement('div');
    let postContainer = document.createElement('div');
    postContainer.className = 'post';
    postContainer.dataset.id = item['id']; // assign post id to div `post` for CRUD purposes
    [headerContainer, bodyContainer, footerContainer].forEach(element => postContainer.appendChild(element));

    parentContainer.appendChild(postContainer);
    
}

function createPostHeader(item, headerContainer){
    // PostHead: an element container containing username, email address, timestamp and (optional) edit button
    // Verify if currently signed in user is the owner of the current post to construct the button
    // render username, email address
    const poster = document.createElement('h6');
    poster.dataset.userid = item['publisher']['id'];
    poster.className = 'post__poster';
    poster.innerHTML = `${item['publisher']['username']}`;

    // render button to edit the post if current user owns this post
    if (host_user_id==item['publisher']['id']){
        const editBtn = document.createElement('button');
        editBtn.className = 'post__edit-btn';
        editBtn.dataset.id = item['id'];
        editBtn.innerHTML = `<span class="material-icons md-15">edit</span>`
        editBtn.title = 'Edit Post';
        editBtn.addEventListener('click', updatePost);
        [poster, editBtn].forEach(element => headerContainer.appendChild(element));
    } else{
        headerContainer.appendChild(poster);
    }
}

function createPostBody(item, bodyContainer){
    // create content text of the post
    const postContent = document.createElement('div');
    postContent.className = 'post__content';
    postContent.innerHTML = item['content'];

    const postTimestamp = document.createElement('div');
    postTimestamp.className = 'post__timestamp';
    postTimestamp.innerHTML = localizeDatetime(item['creation_date']);

    [postContent, postTimestamp].forEach(element => bodyContainer.appendChild(element));
}

function createPostFooter(item, footerContainer){
    // create likeContainer that has 1 child elements: postLikeBtn
    const likeBtn = document.createElement('button');
    if (host_user_id == -1){    // user is anonymous
        likeBtn.disabled = true;
    }
    likeBtn.className = 'post__like-btn';
    likeBtn.innerHTML = `<span class="material-icons md-15">favorite</span>${item['like']}`;
    likeBtn.dataset.id = item['id'];
    likeBtn.dataset.liked = 'false'; // default value

    item['liked_by'].forEach(liker => {
        if (liker['id'] == host_user_id) {
            decorateLikeButton(likeBtn, 'false'); // warning: possible bug. Must test it later
        }
    })
    likeBtn.addEventListener('click', (event) => {
        decorateLikeButton(likeBtn, likeBtn.dataset.liked);
        performLike(event);
    });

    footerContainer.appendChild(likeBtn);
}

function localizeDatetime(dt){
    // dt: String
    // get UTC datetime from server, convert to user's local time. Returned format: /date/ + /time/
    let local_dt = new Date(dt);
    return local_dt.toLocaleString();
}

function createNewPost(e){
    e.preventDefault();

    fetch(`/users/${host_user_id}/posts/`,{
        method: 'POST',
        body: JSON.stringify({
            "content": document.querySelector('#new-post__body').value,
            "publisher": host_user_id,
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        }
    })
    .then(response => {
        if(response.ok){
            window.location.href = `/`;
        }
    })
    .catch((error) => {
        console.error('Error: ', error);
    });

    // clear input
    this.reset();
}

function updatePost(e){
    // handle popup effect
    console.log(e.target);
    const editForm = document.querySelector('.edit-post');
    const overlay = document.querySelector('.overlay');
    editForm.classList.add('user-profile-popup--active');
    overlay.style.display = 'block';

    const postID = e.target.dataset.id;
    const postContainer = document.querySelector(`.post[data-id="${postID}"]`);
    const original_content = postContainer.querySelector('.post__content').innerHTML;

    const editFormBody = editForm.querySelector('#edit-post__body');
    editFormBody.innerHTML = original_content;

    const editFormBtn = editForm.querySelector('#edit-post__btn');

    editFormBtn.addEventListener('click', () => {
        fetch(`/posts/${postID}/`, {
            method: 'PATCH',
            body: JSON.stringify({
                "content": editFormBody.value,
            }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            }
        })
        .catch((error) => {
            console.error('Error: ', error);
        });
    })
}

function performFollow(button, user_id){
    // get csrf token to attach to request
    fetch(`/users/${user_id}/follow/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        }
    })
    .then(response => {
        if(response.ok){
            return response.json()
        }else {
            throw new Error('Sorry, something went wrong !');
        }
    })
    .then(JSONResponse =>{
        button.innerHTML = `Following <span class="material-icons md-15">done</span>`;
        const followersCount = document.querySelector('.followers-count');
        followersCount.innerHTML = `${JSONResponse['followers_count']} Followers`;
    })
}

function performUnfollow(button, user_id){
    fetch(
        `/users/${user_id}/unfollow/`,{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            }
        }
    )
    .then(response => {
        if(response.ok){
            return response.json()
        }else {
            throw new Error('Sorry, something went wrong !');
        }
    })
    .then(JSONResponse => {
        button.innerHTML = 'Follow';
        const followersCount = document.querySelector('.followers-count');
        followersCount.innerHTML = `${JSONResponse['followers_count']} Followers`;
    })
}

function performLike(event){
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

function decorateLikeButton(btn, liked){
    if (liked=='true'){ 
        // liked the post already
        btn.classList.remove('like-btn-active');
        btn.dataset.liked = 'false';
    } else{
        // not liking the post
        btn.classList.add('like-btn-active');
        btn.dataset.liked = 'true';
    }
}

export {getPosts, performFollow, performUnfollow, createNewPost};