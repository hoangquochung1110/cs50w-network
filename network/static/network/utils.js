const csrftoken = Cookies.get('csrftoken');
const PAGESIZE = 10; // display 10 item per page

function getPosts(request_url, page, container){
    fetch(request_url+`?page=${page}`)
    .then(response => response.json())
    .then(data => {
        container.innerHTML = ''; // clear .all-posts for every time reloading the page. Is there better way to handle this ?
        paginatePosts(data, request_url, page, container);
        data['results'].forEach(post => populatePost(post, container))
    })
}

function paginatePosts(data, request_url, page, container){
    /*
    data: JSON response
        PAGE 1: previous:null current:1 next:data['next']

        PAGE 2: previous:data['previous'] current:2 next:data['next']

        PAGE 3: previous:data['previous'] current:2 next:null
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

async function getHostUser(){
    // get data of the currently signed in user
    const response = await fetch('http://127.0.0.1:8000/users/');
    const result = await response.json();
    return result
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
    //poster.style.display = 'inline';
    poster.innerHTML = `${item['publisher']['username']}`;

    // render button to edit the post if current user owns this post
    const host_user_id = sessionStorage.getItem('user_id')
    if (host_user_id!= null && host_user_id==item['publisher']['id']){
        const editBtn = document.createElement('button');
        editBtn.className = 'post__edit-btn';
        editBtn.dataset.id = item['id'];
        editBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil" viewBox="0 0 16 16"><path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325z"/></svg>`
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
    const host_user_id = sessionStorage.getItem('user_id');

    if (host_user_id != null){
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
    // get UTC datetime from server, convert to user's local time
    // dt: String
    // desired format: /date/ + /time/
    let local_dt = new Date(dt);
    return local_dt.toLocaleString();
}

function createNewPost(e){
    e.preventDefault();
    const host_user_id = sessionStorage.getItem('user_id');

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
    .then(response => response.json())
    .then(result => {
        window.location.href = `/`;
    })
    .catch((error) => {
        console.error('Error: ', error);
    });

    // clear input
    this.reset();
}

function updatePost(e){
    // handle popup effect
    const editForm = document.querySelector('.edit-post');
    const overlay = document.querySelector('.overlay');
    editForm.classList.add('user-profile-popup--active');
    overlay.style.display = 'block';

    const postID = e.target.parentNode.dataset.id
    const postContainer = document.querySelector(`.all-posts div[data-id="${postID}"]`);
    console.log(postContainer);
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
        .then(response => response.json())
        .then(result => {
            console.log(result);
        })
        .catch((error) => {
            console.error('Error: ', error);
        });
    
        // clear input
        this.reset();

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
    .then(data =>{
        button.innerHTML = `Following <span class="material-icons md-15">done</span>`; 
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
        button.innerHTML = 'Follow';
    })
}

function performLike(event){
    const likeBtn = event.target;
    const liked = likeBtn.dataset.liked;
    const postID = likeBtn.dataset.id;

    let request_url = '';
    console.log(event.target, 'target');
    if(liked=='false'){
        // perform unlike
        request_url = `/posts/${postID}/unlike/`;
    }else if(liked=='true'){
        // perform like
        request_url = `/posts/${postID}/like/`;
    }
    fetch(request_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        }
    })
    .then(response => response.json())
    .then(data => {
        likeBtn.innerHTML = `<span class="material-icons md-15">favorite</span>${data['like']}`;

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

export {getPosts, getHostUser, performFollow, performUnfollow, createNewPost};