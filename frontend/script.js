// ================= LOGIN =================

function login(){

    let username=document.getElementById("username").value;
    let password=document.getElementById("password").value;

    if(username=="admin" && password=="1234"){

        alert("Login Successful");

        window.location.href="home.html";

    }

    else{

        document.getElementById("message").innerHTML="Invalid User ID or Password";

    }

}


// ================= REGISTER =================

function registerUser(){

    let fullname=document.getElementById("fullname").value;

    let email=document.getElementById("email").value;

    let mobile=document.getElementById("mobile").value;

    let password=document.getElementById("password").value;

    let confirmPassword=document.getElementById("confirmPassword").value;


    if(fullname=="" || email=="" || mobile=="" || password=="" || confirmPassword==""){

        alert("Please fill all fields.");

        return;

    }


    if(password!=confirmPassword){

        alert("Passwords do not match.");

        return;

    }


    alert("Registration Successful!");

    window.location.href="login.html";

}
function changeLanguage() {

    let lang = document.getElementById("language").value;

    if (lang == "en") {

        document.getElementById("welcomeText").innerHTML = "Welcome Traveller 👋";
        document.getElementById("tagline").innerHTML = "Plan your dream vacation with AI.";
        document.getElementById("startBtn").innerHTML = "Start Planning";
        document.getElementById("tourTitle").innerHTML="🏛 Tourist Attractions";
document.getElementById("tourText").innerHTML="Discover famous tourist places.";

document.getElementById("hotelTitle").innerHTML="🏨 Hotels";
document.getElementById("hotelText").innerHTML="Find the best hotels within your budget.";

document.getElementById("transportTitle").innerHTML="🚖 Transport";
document.getElementById("transportText").innerHTML="Get transport recommendations.";

    }

    else if (lang == "hi") {

        document.getElementById("welcomeText").innerHTML = "🙏 नमस्ते यात्री";
        document.getElementById("tagline").innerHTML = "AI के साथ अपनी सपनों की यात्रा की योजना बनाएं।";
        document.getElementById("startBtn").innerHTML = "यात्रा शुरू करें";
        document.getElementById("tourTitle").innerHTML="🏛 पर्यटन स्थल";
document.getElementById("tourText").innerHTML="प्रसिद्ध पर्यटन स्थलों की खोज करें।";

document.getElementById("hotelTitle").innerHTML="🏨 होटल";
document.getElementById("hotelText").innerHTML="अपने बजट के अनुसार बेहतरीन होटल खोजें।";

document.getElementById("transportTitle").innerHTML="🚖 परिवहन";
document.getElementById("transportText").innerHTML="यात्रा के लिए परिवहन सुझाव प्राप्त करें।";

    }

    else if (lang == "mr") {

        document.getElementById("welcomeText").innerHTML = "🙏 नमस्कार प्रवासी";
        document.getElementById("tagline").innerHTML = "AI च्या मदतीने तुमच्या स्वप्नातील सहलीची योजना करा.";
        document.getElementById("startBtn").innerHTML = "प्रवास सुरू करा";
        document.getElementById("tourTitle").innerHTML="🏛 पर्यटन स्थळे";
document.getElementById("tourText").innerHTML="प्रसिद्ध पर्यटन स्थळांचा शोध घ्या.";

document.getElementById("hotelTitle").innerHTML="🏨 हॉटेल्स";
document.getElementById("hotelText").innerHTML="तुमच्या बजेटनुसार सर्वोत्तम हॉटेल शोधा.";

document.getElementById("transportTitle").innerHTML="🚖 वाहतूक";
document.getElementById("transportText").innerHTML="प्रवासासाठी वाहतुकीच्या शिफारसी मिळवा.";


    }

}
function changeTripLanguage(){

let lang=document.getElementById("language").value;

if(lang=="en"){

document.getElementById("tripTitle").innerHTML="✈ Plan Your Dream Trip";
document.getElementById("sourceLabel").innerHTML="Source City";
document.getElementById("destinationLabel").innerHTML="Destination City";
document.getElementById("startLabel").innerHTML="Start Date";
document.getElementById("endLabel").innerHTML="End Date";
document.getElementById("budgetLabel").innerHTML="Budget (₹)";
document.getElementById("travelerLabel").innerHTML="Number of Travelers";
document.getElementById("interestLabel").innerHTML="Travel Interest";
document.getElementById("transportLabel").innerHTML="Transport";
document.getElementById("hotelLabel").innerHTML="Hotel Preference";
document.getElementById("generateBtn").innerHTML="Generate AI Itinerary";

}

else if(lang=="hi"){

document.getElementById("tripTitle").innerHTML="✈ अपने सपनों की यात्रा की योजना बनाएं";
document.getElementById("sourceLabel").innerHTML="प्रस्थान शहर";
document.getElementById("destinationLabel").innerHTML="गंतव्य शहर";
document.getElementById("startLabel").innerHTML="प्रारंभ तिथि";
document.getElementById("endLabel").innerHTML="समाप्ति तिथि";
document.getElementById("budgetLabel").innerHTML="बजट (₹)";
document.getElementById("travelerLabel").innerHTML="यात्रियों की संख्या";
document.getElementById("interestLabel").innerHTML="यात्रा रुचि";
document.getElementById("transportLabel").innerHTML="यातायात";
document.getElementById("hotelLabel").innerHTML="होटल पसंद";
document.getElementById("generateBtn").innerHTML="AI यात्रा योजना बनाएं";

}

else if(lang=="mr"){

document.getElementById("tripTitle").innerHTML="✈ तुमच्या स्वप्नातील सहलीची योजना करा";
document.getElementById("sourceLabel").innerHTML="प्रस्थान शहर";
document.getElementById("destinationLabel").innerHTML="गंतव्य शहर";
document.getElementById("startLabel").innerHTML="सुरुवातीची तारीख";
document.getElementById("endLabel").innerHTML="समाप्तीची तारीख";
document.getElementById("budgetLabel").innerHTML="बजेट (₹)";
document.getElementById("travelerLabel").innerHTML="प्रवाशांची संख्या";
document.getElementById("interestLabel").innerHTML="प्रवासाची आवड";
document.getElementById("transportLabel").innerHTML="वाहतूक";
document.getElementById("hotelLabel").innerHTML="हॉटेल पसंती";
document.getElementById("generateBtn").innerHTML="AI सहल योजना तयार करा";

}

}