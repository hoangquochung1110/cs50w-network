import { performFollow, performUnfollow } from '../features/follow.js';
import { dropdown_on, dropdown_off } from '../features/follow.js';

const userProfilePopup = document.querySelector('.user-profile-popup');
const overlay = document.querySelector('.overlay');
const host_user_id = JSON.parse(document.querySelector("#user_id").textContent);
const followBtn = document.querySelector('.follow-btn');

// for timeline.html
// const visited_user_followers = JSON.parse(document.querySelector('#visited_user_followers').textContent);
const visited_user_followers = document.querySelector('#visited_user_followers') ? JSON.parse(document.querySelector('#visited_user_followers').textContent) : -1;
// const visited_user_id = JSON.parse(document.querySelector('#visited_user_id').textContent);
const visited_user_id = document.querySelector('#visited_user_id') ? JSON.parse(document.querySelector('#visited_user_id').textContent) : -1;

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

function createUserProfileHeader(){
    if (visited_user_id == host_user_id)    followBtn.style.display = 'none';
    else {
        visited_user_followers.forEach(follower => {
            if(follower['id'] == host_user_id){
                followBtn.innerHTML = `Following <span class="material-icons md-15">done</span>`;
                dropdown_on();
            }
        })
    }
    const unfollow = document.querySelector('.dropdown-content a');
    // If unfollow-btn ever rendered, listen for onClick event, otherwise skip it
    if (unfollow){
        unfollow.addEventListener('click', () => {
            performUnfollow(followBtn, visited_user_id);
            dropdown_off();
        })
    }
} 

export {showUserProfilePopup, hideUserProfilePopup, createUserProfileHeader };