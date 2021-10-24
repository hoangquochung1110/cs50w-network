import {getPosts, perform_follow} from "./utils.js"

const visited_user_id = JSON.parse(document.querySelector('#visited_user_id').textContent);
const visited_user_followers = JSON.parse(document.querySelector('#visited_user_followers').textContent);

const host_user_id = sessionStorage.getItem('user_id');

const followBtn = document.querySelector('.follow-btn');

document.addEventListener('DOMContentLoaded', function() {
    const userPostsContainer = document.querySelector('.user-posts');
    getPosts(`/users/${visited_user_id}/posts/`, userPostsContainer);
    createUserProfileHeader();
    followBtn.addEventListener('click', function(){
        perform_follow(followBtn, visited_user_id);
    })
});

function createUserProfileHeader(){
    if (visited_user_id == host_user_id)    followBtn.style.display = 'none';
    else {
        visited_user_followers.forEach(follower => {
            if(follower['id'] == host_user_id){
                followBtn.innerHTML = `Following <span class="material-icons md-15">done</span>`;
                // const dropdown = document.querySelector('.dropdown'); // turn on hover effect
                // dropdown.classList.remove('un-hoverable'); // hover effect set none as default
            }
        })
    }

    // Listen for unfollow event
}   

function perform_unfollow(visited_user_id){
    const csrftoken = Cookies.get('csrftoken');

    fetch(
        `/users/${visited_user_id}/unfollow/`,{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            }
        }
    )
    .then(response => {
        followBtn.innerHTML = 'Follow';
    })
}