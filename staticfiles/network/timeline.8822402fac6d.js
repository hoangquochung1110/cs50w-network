import { performFollow } from "./features/follow.js"
import { getPosts } from "./components/post.js";
import { createUserProfileHeader } from "./components/userprofile.js";
import { dropdown_on } from "./features/follow.js";

const visited_user_id = JSON.parse(document.querySelector('#visited_user_id').textContent);

const followBtn = document.querySelector('.follow-btn');

document.addEventListener('DOMContentLoaded', function() {
    const userPostsContainer = document.querySelector('.user-posts');
    getPosts(`/users/${visited_user_id}/posts/`, 1, userPostsContainer);
    createUserProfileHeader();
    followBtn.addEventListener('click', function(){
        console.log('hii thee');
        performFollow(followBtn, visited_user_id);
        dropdown_on();
    })
});

