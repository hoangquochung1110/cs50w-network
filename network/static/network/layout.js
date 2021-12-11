import fixNav from "./features/stickyNav.js";

const nav = document.querySelector('.navbar');
const searchInput = document.querySelector('.search');
let topOfNav = nav.offsetTop; // assign to a let to avoid layout thrashing
const offsetHeight = nav.offsetHeight;

const searchHandler = async (e) => {
    e.preventDefault();
    const queryString = e.target.value;
    if (queryString !== ''){
        console.log(queryString);
        const response = await fetch(`/users/?username__startswith=${queryString}`);
        const suggestions = await response.json();
        displayMatches(suggestions);
    } else {
        clearMatches();
    }

}

const displayMatches = (suggestions) => {
    const suggestionContainer = document.querySelector('.suggestions');
    const items = suggestions.map((item) => {
        return `
            <a href=${item.username} class="text-decoration-0 clr-bl">
                <li>
                    <div>${item.username}</div>
                </li>
            </a>
        `
    }).join('');
    suggestionContainer.innerHTML = items;
}

const clearMatches = () => {
    const suggestionContainer = document.querySelector('.suggestions');
    suggestionContainer.innerHTML = '';
}

window.addEventListener('scroll', () => {
    fixNav(nav, topOfNav, offsetHeight);
})

searchInput.addEventListener('change', searchHandler);
searchInput.addEventListener('keyup', searchHandler);

