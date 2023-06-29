window.addEventListener('load', () => {
    const darkSwitch = document.getElementById('toggleDarkMode');
    if (localStorage.getItem('darkMode') === 'enabled') {
        document.body.classList.add('dark-mode');
        darkSwitch.dataset.dark = "true";
        darkSwitch.innerText = "Toggle Light Mode";
    }
    darkSwitch.addEventListener('click', () => {
        if (darkSwitch.dataset.dark == "false") {
            document.body.classList.add('dark-mode');
            localStorage.setItem('darkMode', 'enabled');
            darkSwitch.dataset.dark = "true";
            darkSwitch.innerText = "Toggle Light Mode";
        } else {
            document.body.classList.remove('dark-mode');
            localStorage.removeItem('darkMode');
            darkSwitch.dataset.dark = "false";
            darkSwitch.innerText = "Toggle Dark Mode";
        }
    });
});
