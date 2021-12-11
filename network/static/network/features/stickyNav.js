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

export default fixNav;