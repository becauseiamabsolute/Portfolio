function GetSignInDialog() {
    location.replace('login.html');
};

function RegRegirect() {
    location.replace('register.html');
};




function showpassword() {

    var password = document.getElementById('password1');
    var checkbox = document.querySelector('.checkbox1');

    if (checkbox.checked){
        password.type = 'text';
    }
    else {
        password.type = 'password';
    };
}