const nav = document.querySelector('.navbar');
let topOfNav = nav.offsetTop; // assign to a let to avoid layout thrashing

window.addEventListener('scroll', () => {
    const offsetHeight = nav.offsetHeight;
    fixNav(nav, topOfNav, offsetHeight);
})

const fixNav = (nav, topOfNav, offsetHeight) => {
    const body = document.querySelector('.body');
    if(window.scrollY >= topOfNav){
        body.style.paddingTop = offsetHeight + 'px';
        nav.classList.add('fixed-nav');
    } else {
        body.style.paddingTop = 0;
        nav.classList.remove('fixed-nav');

    }
}
