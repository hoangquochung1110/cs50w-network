import {getPosts, performFollow, getHostUser, createNewPost} from './utils.js';

const is_authenticated = JSON.parse(document.querySelector("#request_user_is_authenticated").textContent);

const allPostsContainer = document.querySelector('.all-posts');
const followingPostsContainer = document.querySelector('.following-posts');
const overlay = document.querySelector('.overlay');
const userProfilePopup = document.querySelector('.user-profile-popup');

document.addEventListener('DOMContentLoaded', function() {
    if (allPostsContainer){
        getPosts('/posts/', allPostsContainer);
        allPostsContainer.addEventListener('click', showUserProfilePopup);
    } else if (followingPostsContainer){
        getPosts('posts/following/', followingPostsContainer);
        followingPostsContainer.addEventListener('click', showUserProfilePopup);
    } else{
        throw new Error('Can not load page at the moment')
    }

    if (is_authenticated){
        const response = getHostUser();
        response.then(
            data => {
                sessionStorage.setItem('user_id', data[0]['id']);
            }
        )
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
    const followers_count = document.querySelector('#user-profile-popup__followers');
    const following_count = document.querySelector('#user-profile-popup__following');
    const posts_count = document.querySelector('#user-profile-popup__num_of_posts');

    const target_user_id = target.dataset.userid;
    const host_user_id = sessionStorage.getItem('user_id');

    const followBtn = document.querySelector('.follow-btn');
    followBtn.style.display = 'inline-block'; // set the default display

    fetch(`/users/${target_user_id}`)
    .then(response => response.json())
    .then(result => {

        username.innerHTML = `<span style="font-weight:bold">${result['username']}</span>`;
        followers_count.innerHTML = `<span style="font-weight:bold">${result['followers_count']}</span> followers`;
        following_count.innerHTML = `<span style="font-weight:bold">${result['following_count']}</span> following`;
        posts_count.innerHTML = `<span style="font-weight:bold">${result['posts_count']}</span> posts`;

        if (host_user_id == target_user_id) followBtn.style.display = 'none';   // unable to follow yourself
        else {
            result['followers'].forEach(follower => {
                if (follower['id'] == host_user_id){
                    followBtn.innerHTML = `Following <span class="material-icons md-15">done</span>`; 
                    followBtn.disabled = true; // unable to follow more than once
                } 
            });
        }


    })

    // listen for event clicking Timeline
    const userTimelineBtn = document.querySelector('#user-profile-popup__timeline-btn');
    userTimelineBtn.addEventListener('click', () => {
        window.location.href = `/${target.innerText}`; // get the username of event.target then redirect to /username/ url
    })


    // listen for event following
    followBtn.addEventListener('click', () =>{
        performFollow(followBtn, target_user_id);
    })
}

