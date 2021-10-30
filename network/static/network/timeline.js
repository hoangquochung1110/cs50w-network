import {getPosts, performFollow, performUnfollow} from "./utils.js"

const visited_user_id = JSON.parse(document.querySelector('#visited_user_id').textContent);
const visited_user_followers = JSON.parse(document.querySelector('#visited_user_followers').textContent);
const host_user_id = JSON.parse(document.querySelector("#user_id").textContent);

const followBtn = document.querySelector('.follow-btn');

document.addEventListener('DOMContentLoaded', function() {
    const userPostsContainer = document.querySelector('.user-posts');
    getPosts(`/users/${visited_user_id}/posts/`, 1, userPostsContainer);
    createUserProfileHeader();
    followBtn.addEventListener('click', function(){
        performFollow(followBtn, visited_user_id);
        dropdown_on();
    })
});

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

    // Listen for unfollow event
    const unfollow = document.querySelector('.dropdown-content a');
    if (unfollow){
        unfollow.addEventListener('click', () => {
            performUnfollow(followBtn, visited_user_id);
            dropdown_off();
        })
    }
}   

function dropdown_on(){
    const dropdown = document.querySelector('.dropdown'); // turn on hover effect
    dropdown.prepend(followBtn);
}

function dropdown_off(){
    const userProfileUsername = document.querySelector('#user-profile-header__username');
    userProfileUsername.after(followBtn);
}
