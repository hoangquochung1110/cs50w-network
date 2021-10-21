import {getPosts} from "./utils.js"

document.addEventListener('DOMContentLoaded', function() {
    const userPostsContainer = document.querySelector('.user-posts');
    const visited_user_id = JSON.parse(document.querySelector('#visited_user_id').textContent);
    getPosts(`/users/${visited_user_id}/posts/`, userPostsContainer);
    /*
        REQUEST_URL
        get_post(REQUEST_URL, container)
    */
});
