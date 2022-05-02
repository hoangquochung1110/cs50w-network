import { getPosts, createNewPost } from './components/post.js';
import { showUserProfilePopup, hideUserProfilePopup } from './components/userprofile.js';

const FIRSTPAGE = 1;
const ANONYMOUSUSER = -1;

const host_user_id = JSON.parse(document.querySelector("#user_id").textContent);

const allPostsContainer = document.querySelector('.all-posts');
const followingPostsContainer = document.querySelector('.following-posts');
const overlay = document.querySelector('.overlay');

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

    if (host_user_id > ANONYMOUSUSER){ // user.is_authenticated == True
        const newPostForm = document.querySelector('#new-post__form');
        newPostForm.addEventListener('submit', createNewPost);
    }
    overlay.addEventListener('click', hideUserProfilePopup);
});
