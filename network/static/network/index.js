import {getPosts, fetchHostUser} from './utils.js';

const allPostContainer = document.querySelector('.all-posts');
const overlay = document.querySelector('.overlay');
const userProfilePopup = document.querySelector('.user-profile-popup');

document.addEventListener('DOMContentLoaded', function() {

    const newPostForm = document.querySelector('#new-post__form');
    console.log(newPostForm);
    console.log('running index.html');
    getPosts('/posts/', allPostContainer);
    newPostForm.addEventListener('submit', handleNewPost);
    allPostContainer.addEventListener('click', showUserProfilePopup);
    overlay.addEventListener('click', hideUserProfilePopup);
});






/*
TODO: HANDLE DUPLICATE ITEMS
postsList = fetch('/posts/'); // get new, updated list of posts

allPost = querySelector('.all-post');
allPost.innerHTML = postsList.map(post, i) => renderPost()       <---- reassign allPost.innerHTML
*/

async function handleNewPost(e){
    e.preventDefault();
    //console.log(e.target);

    // TODO: consider if keep userID in global scope
    const response = await fetchHostUser();
    const userID = response[0]['id'];

    // get csrf token to attach to request
    const csrftoken = Cookies.get('csrftoken');
    fetch(`/users/${userID}/posts/`,{
        method: 'POST',
        body: JSON.stringify({
            "content": document.querySelector('#new-post__body').value,
            "publisher": userID,
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        }
    })
    .then(response => response.json())
    .then(result => {
        getPosts('/posts/', allPostContainer);
    })
    .catch((error) => {
        console.error('Error: ', error);
    });

    // clear input
    this.reset();
}

function showUserProfilePopup(e){
    // function to render a pop-up user profile card and handle overlay effect

    let target = e.target;
    console.log(target);

    // event delegation
    if (target.className != 'post__poster'){
        return; // Skip if the trigger DOM element is not post__poster
    }

    // make user-profile-popup overlap container
    userProfilePopup.classList.add('user-profile-popup--active');
    overlay.style.display = 'block';

    createUserProfile(target);

}

function hideUserProfilePopup(){
    // function to hide a pop-up user profile card

    userProfilePopup.classList.remove('user-profile-popup--active');
    overlay.style.display = 'none';
}

async function createUserProfile(target){
    // target: DOM element that triggered the event
    const username = document.querySelector('#user-profile-popup__username');
    /*
    const emailAddress = document.querySelector('#user-profile__email-address');
    const age = document.querySelector('#user-profile__age');
    const gender = document.querySelector('#user-profile__gender');
    */
    const followers_count = document.querySelector('#user-profile-popup__followers');
    const following_count = document.querySelector('#user-profile-popup__following');
    const posts_count = document.querySelector('#user-profile-popup__num_of_posts');

    let targetUserID = target.dataset.userid;

    const response = await fetchHostUser();
    const hostUserID = response[0]['id'];
    const followBtn = document.querySelector('.follow-btn');
    followBtn.style.display = 'inline-block'; // set the default display

    console.log(hostUserID, targetUserID);
    if (hostUserID == targetUserID){
        followBtn.style.display = 'none';   // unable to follow yourself
    }

    fetch(`/users/${targetUserID}`)
    .then(response => response.json())
    .then(result => {
        username.innerHTML = `<span style="font-weight:bold">${result['username']}</span>`;
        /*
        emailAddress.innerHTML = result['email'];
        age.innerHTML =  `${result['age']} years old`;
        gender.innerHTML = result['gender'];
        */
        followers_count.innerHTML = `<span style="font-weight:bold">${result['followers_count']}</span> followers`;
        following_count.innerHTML = `<span style="font-weight:bold">${result['following_count']}</span> following`;
        posts_count.innerHTML = `<span style="font-weight:bold">${result['posts_count']}</span> posts`;

    })

    // listen for event clicking Timeline
    const userTimelineBtn = document.querySelector('#user-profile-popup__timeline-btn');
    userTimelineBtn.addEventListener('click', () => {
        window.location.href = `/${target.innerText}`; // get the username of event.target then redirect to /username/ url
    })
}

