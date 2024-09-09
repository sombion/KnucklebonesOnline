var loginForm = document.getElementById("login");
var registerForm = document.getElementById("register");
var toggleButton = document.getElementById("btn");

function register() {
    loginForm.style.left = "-400px";
    registerForm.style.left = "50px";
    toggleButton.style.left = "110px";
    toggleButton.style.width = "160px"
    
    registerForm.style.opacity = "1";
    loginForm.style.opacity = "0";
}

function login() {
    loginForm.style.left = "50px";
    registerForm.style.left = "450px";
    toggleButton.style.left = "0";
    toggleButton.style.width = "110px"
    

    loginForm.style.opacity = "1";
    registerForm.style.opacity = "0";
}
