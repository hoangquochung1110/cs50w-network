import fixNav from "./features/stickyNav.js";

const nav = document.querySelector('.navbar');
let topOfNav = nav.offsetTop; // assign to a let to avoid layout thrashing
const offsetHeight = nav.offsetHeight;

window.addEventListener('scroll', () => {
    fixNav(nav, topOfNav, offsetHeight);
})
