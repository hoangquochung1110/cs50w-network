const followBtn = document.querySelector('.follow-btn');
const csrftoken = Cookies.get('csrftoken');

// dropdown: an element to display follow/unfollow button
function dropdown_on(){
    const dropdown = document.querySelector('.dropdown'); // turn on hover effect
    dropdown.prepend(followBtn);
}

function dropdown_off(){
    const userProfileUsername = document.querySelector('#user-profile-header__username');
    userProfileUsername.after(followBtn);
}

function performFollow(button, user_id){
    // get csrf token to attach to request
    fetch(`/users/${user_id}/follow/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        }
    })
    .then(response => {
        if(response.ok){
            return response.json()
        }else {
            throw new Error('Sorry, something went wrong !');
        }
    })
    .then(JSONResponse =>{
        button.innerHTML = `Following <span class="material-icons md-15">done</span>`;
        const followersCount = document.querySelector('.followers-count');
        followersCount.innerHTML = `${JSONResponse['followers_count']} Followers`;
    })
}

function performUnfollow(button, user_id){
    fetch(
        `/users/${user_id}/unfollow/`,{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            }
        }
    )
    .then(response => {
        if(response.ok){
            return response.json()
        }else {
            throw new Error('Sorry, something went wrong !');
        }
    })
    .then(JSONResponse => {
        button.innerHTML = 'Follow';
        const followersCount = document.querySelector('.followers-count');
        followersCount.innerHTML = `${JSONResponse['followers_count']} Followers`;
    })
}

export { dropdown_on, dropdown_off, performFollow, performUnfollow }
