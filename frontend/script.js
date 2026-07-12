function login(){

let user=document.getElementById("userid").value;
let pass=document.getElementById("password").value;

if(user=="admin" && pass=="1234")
{
    document.getElementById("message").style.color="green";
    document.getElementById("message").innerHTML="Login Successful!";
}
else
{
    document.getElementById("message").style.color="red";
    document.getElementById("message").innerHTML="Invalid User ID or Password";
}

}