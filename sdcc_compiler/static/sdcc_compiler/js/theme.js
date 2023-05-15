const theme_icon = document.getElementById("theme-icon");
const current_theme = localStorage.getItem("theme");

if (current_theme === "light") {
    theme_icon.className = "fa-regular fa-moon";
    document.body.classList.toggle("light-theme");
}

theme_icon.onclick = function () {
    document.body.classList.toggle("light-theme");
    if (document.body.classList.contains("light-theme")) {
        localStorage.setItem("theme", "light");
        theme_icon.className = "fa-regular fa-moon";
    } else {
        localStorage.setItem("theme", "dark");
        theme_icon.className = "fa-regular fa-sun";
    }
}