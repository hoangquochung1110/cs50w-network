async function fetchUserID(){
    const response = await fetch('http://127.0.0.1:8000/users/');
    const result = await response.json();
    return result
}

function getPosts(){
    fetch('http://127.0.0.1:8000/posts/')
    .then(response => response.json())
    .then(posts => {
        posts.forEach(post => populatePost(post))
    })
}

function localize_datetime(dt){
    // get UTC datetime from server, convert to user's local time
    // dt: String
    // desired format: /date/ + /time/
    let local_dt = new Date(dt);
    return local_dt.toLocaleString();
}

function populatePost(item){
    const allPostContainer = document.querySelector('.all-posts');
    //console.log(item);
    /*
        allPostContainer
            postContainer
                headContainer
                contentContainer
                footerContainer

    */

    // create headContainer that has 2 child elements: poster and editBtn
    const headContainer = document.createElement('div');
    headContainer.className = 'post__head';
    createPostHead(item, headContainer);


    // create content text of the post
    const postContent = document.createElement('div');
    postContent.className = 'post__content';
    postContent.innerHTML = item['content'];

    // create footerContainer that has 2 child elements: likeBtn and likes
    const footerContainer = document.createElement('div');
    footerContainer.className = 'post__footer';
    createPostFooter(item, footerContainer);

    // create postContainer that have 3 child elements: headContainer, postContent and likeContainer
    const postContainer = document.createElement('div');
    postContainer.className = 'post';
    postContainer.dataset.id = item['id']; // assign post id to div `post` for CRUD purposes
    [headContainer, postContent, footerContainer].forEach(element => postContainer.appendChild(element));

    allPostContainer.appendChild(postContainer);

}

async function createPostHead(item, headContainer){
    // PostHead: an element container containing username, email address, timestamp and (optional) edit button
    // Verify if signed in user is the owner of the current post to construct the button
    const response = await fetchUserID();
    const userID = response[0]['id'];
    //console.log(userID);

    // render username, email address
    const poster = document.createElement('div');
    poster.style.display = 'inline';
    poster.innerHTML = `<span style="font-weight:bold">${item['publisher']['username']}</span> ${item['publisher']['email']} ◦ ${localize_datetime(item['published'])}`;

    // render button to edit the post if current user owns this post
    if (item['publisher']['id'] == userID){
        const editBtn = document.createElement('button');
        editBtn.className = 'post__edit-btn';
        editBtn.dataset.id = item['id'];
        editBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil" viewBox="0 0 16 16"><path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325z"/></svg>`
        editBtn.addEventListener('click', update_post);
        [poster, editBtn].forEach(element => headContainer.appendChild(element));
    } else{
        headContainer.appendChild(poster);
    }
}

function createPostFooter(item, footerContainer){
    // create likeContainer that has 2 child elements: postLikeBtn and postLikes
    const likeBtn = document.createElement('button');
    likeBtn.className = 'post__like-btn';
    likeBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16"><path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/></svg>`;


    const likes = document.createElement('div');
    likes.className = 'post__likes';
    likes.innerHTML = item['like'];

    [likeBtn, likes].forEach(element => footerContainer.appendChild(element))
}

function update_post(e){
    console.log(e.target.parentNode.dataset.id);
    const editBtn = e.target.parentNode;
    const postContainer = document.querySelector(`.all-posts div[data-id="${e.target.parentNode.dataset.id}"]`);
    console.log(postContainer);
}

function handleNewPost(e){
    e.preventDefault();
    console.log(e.target);
}

document.addEventListener('DOMContentLoaded', function() {
    const newPostForm = document.querySelector('.new-post__form');

    getPosts();
    newPostForm.addEventListener('submit', handleNewPost)
});