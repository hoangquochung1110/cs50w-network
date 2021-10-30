import {getPosts, performFollow, createNewPost} from './utils.js';

const FIRSTPAGE = 1;
const ANONYMOUSUSER = -1;

const host_user_id = JSON.parse(document.querySelector("#user_id").textContent);

const allPostsContainer = document.querySelector('.all-posts');
const followingPostsContainer = document.querySelector('.following-posts');
const overlay = document.querySelector('.overlay');
const userProfilePopup = document.querySelector('.user-profile-popup');

document.addEventListener('DOMContentLoaded', function() {

    if (allPostsContainer){
        getPosts('/posts/', FIRSTPAGE, allPostsContainer);
        allPostsContainer.addEventListener('click', showUserProfilePopup);
    } else if (followingPostsContainer){
        getPosts('posts/following/', FIRSTPAGE, followingPostsContainer);
        followingPostsContainer.addEventListener('click', showUserProfilePopup);
    } else{
        throw new Error('Can not load page at the moment')
    }

    if (host_user_id >= ANONYMOUSUSER){ // user.is_authenticated == True
        const newPostForm = document.querySelector('#new-post__form');
        newPostForm.addEventListener('submit', createNewPost);
        overlay.addEventListener('click', hideUserProfilePopup);
    }

});

function showUserProfilePopup(e){
    // function to render a pop-up user profile card and handle overlay effect
    // event delegation
    if (e.target.className != 'post__poster'){
        return; // Skip if the trigger DOM element is not post__poster
    }
    // make user-profile-popup overlap container
    userProfilePopup.classList.add('user-profile-popup--active');
    overlay.style.display = 'block';
    createUserProfilePopup(e.target);
}

function hideUserProfilePopup(){ 
    // function to hide a pop-up user profile card
    userProfilePopup.classList.remove('user-profile-popup--active');
    overlay.style.display = 'none';
}

function createUserProfilePopup(target){
    // target: DOM element that triggered the event
    const username = document.querySelector('#user-profile-popup__username');
    const followers_count = document.querySelector('.followers-count');
    const following_count = document.querySelector('.following-count');
    const posts_count = document.querySelector('.posts-count');

    const target_user_id = target.dataset.userid;
    const followBtn = document.querySelector('.follow-btn');
    followBtn.style.display = 'inline-block'; // set the default display
    followBtn.innerHTML = 'Follow';
    followBtn.disabled = false;

    fetch(`/users/${target_user_id}`)
    .then(response => {
        if(response.ok){
            return response.json()
        }
    })
    .then(JSONResponse => {
        username.innerHTML = `<span style="font-weight:bold">${JSONResponse['username']}</span>`;
        followers_count.innerHTML = `<span style="font-weight:bold">${JSONResponse['followers_count']}</span> followers`;
        following_count.innerHTML = `<span style="font-weight:bold">${JSONResponse['following_count']}</span> following`;
        posts_count.innerHTML = `<span style="font-weight:bold">${JSONResponse['posts_count']}</span> posts`;
        if (host_user_id == target_user_id) followBtn.style.display = 'none';   // unable to follow yourself
        else {
            JSONResponse['followers'].forEach(follower => {
                console.log(follower['id'],host_user_id);
                if (follower['id'] == host_user_id){
                    followBtn.innerHTML = `Following <span class="material-icons md-15">done</span>`; 
                    followBtn.disabled = true; // unable to follow more than once
                }
            });
        }
    })

    // listen for event clicking Timeline
    const userTimelineBtn = document.querySelector('.timeline-btn');
    userTimelineBtn.addEventListener('click', () => {
        window.location.href = `/${target.innerText}`; // get the username of event.target then redirect to /username/ url
    })

    // listen for event following
    followBtn.addEventListener('click', () =>{
        performFollow(followBtn, target_user_id);
    })
}

