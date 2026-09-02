// ================= LOGIN =================

async function login() {
  let email = document.getElementById("username").value;
  let password = document.getElementById("password").value;

  let response = await fetch("/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email: email,
      password: password,
    }),
  });

  let result = await response.json();

  if (result.success) {
    alert("Login Successful");

    window.location.href = "home.html";
  } else {
    document.getElementById("message").innerHTML = "Invalid Email or Password";
  }
}

// ================= REGISTER =================
async function registerUser() {
  let fullname = document.getElementById("fullname").value;
  let email = document.getElementById("email").value;
  let mobile = document.getElementById("mobile").value;
  let password = document.getElementById("password").value;
  let confirmPassword = document.getElementById("confirmPassword").value;

  if (
    fullname == "" ||
    email == "" ||
    mobile == "" ||
    password == "" ||
    confirmPassword == ""
  ) {
    alert("Please fill all fields.");
    return;
  }

  if (password != confirmPassword) {
    alert("Passwords do not match.");
    return;
  }

  let response = await fetch("/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      fullname: fullname,
      email: email,
      mobile: mobile,
      password: password,
    }),
  });

  let result = await response.json();

  if (result.success) {
    alert("Registration Successful!");

    window.location.href = "login.html";
  } else {
    alert(result.message);
  }
}

function changeLanguage() {
  let lang = document.getElementById("language").value;

  if (lang == "en") {
    document.getElementById("welcomeText").innerHTML = "Welcome Traveller 👋";
    document.getElementById("tagline").innerHTML =
      "Plan your dream vacation with AI.";
    document.getElementById("startBtn").innerHTML = "Start Planning";
    document.getElementById("tourTitle").innerHTML = "🏛 Tourist Attractions";
    document.getElementById("tourText").innerHTML =
      "Discover famous tourist places.";

    document.getElementById("hotelTitle").innerHTML = "🏨 Hotels";
    document.getElementById("hotelText").innerHTML =
      "Find the best hotels within your budget.";

    document.getElementById("transportTitle").innerHTML = "🚖 Transport";
    document.getElementById("transportText").innerHTML =
      "Get transport recommendations.";
  } else if (lang == "hi") {
    document.getElementById("welcomeText").innerHTML = "🙏 नमस्ते यात्री";
    document.getElementById("tagline").innerHTML =
      "AI के साथ अपनी सपनों की यात्रा की योजना बनाएं।";
    document.getElementById("startBtn").innerHTML = "यात्रा शुरू करें";
    document.getElementById("tourTitle").innerHTML = "🏛 पर्यटन स्थल";
    document.getElementById("tourText").innerHTML =
      "प्रसिद्ध पर्यटन स्थलों की खोज करें।";

    document.getElementById("hotelTitle").innerHTML = "🏨 होटल";
    document.getElementById("hotelText").innerHTML =
      "अपने बजट के अनुसार बेहतरीन होटल खोजें।";

    document.getElementById("transportTitle").innerHTML = "🚖 परिवहन";
    document.getElementById("transportText").innerHTML =
      "यात्रा के लिए परिवहन सुझाव प्राप्त करें।";
  } else if (lang == "mr") {
    document.getElementById("welcomeText").innerHTML = "🙏 नमस्कार प्रवासी";
    document.getElementById("tagline").innerHTML =
      "AI च्या मदतीने तुमच्या स्वप्नातील सहलीची योजना करा.";
    document.getElementById("startBtn").innerHTML = "प्रवास सुरू करा";
    document.getElementById("tourTitle").innerHTML = "🏛 पर्यटन स्थळे";
    document.getElementById("tourText").innerHTML =
      "प्रसिद्ध पर्यटन स्थळांचा शोध घ्या.";

    document.getElementById("hotelTitle").innerHTML = "🏨 हॉटेल्स";
    document.getElementById("hotelText").innerHTML =
      "तुमच्या बजेटनुसार सर्वोत्तम हॉटेल शोधा.";

    document.getElementById("transportTitle").innerHTML = "🚖 वाहतूक";
    document.getElementById("transportText").innerHTML =
      "प्रवासासाठी वाहतुकीच्या शिफारसी मिळवा.";
  }
}
function changeTripLanguage() {
  let lang = document.getElementById("language").value;

  if (lang == "en") {
    document.getElementById("tripTitle").innerHTML = "✈ Plan Your Dream Trip";
    document.getElementById("sourceLabel").innerHTML = "Source City";
    document.getElementById("destinationLabel").innerHTML = "Destination City";
    document.getElementById("startLabel").innerHTML = "Start Date";
    document.getElementById("endLabel").innerHTML = "End Date";
    document.getElementById("budgetLabel").innerHTML = "Budget (₹)";
    document.getElementById("travelerLabel").innerHTML = "Number of Travelers";
    document.getElementById("interestLabel").innerHTML = "Travel Interest";
    document.getElementById("transportLabel").innerHTML = "Transport";
    document.getElementById("hotelLabel").innerHTML = "Hotel Preference";
    document.getElementById("generateBtn").innerHTML = "Generate AI Itinerary";
  } else if (lang == "hi") {
    document.getElementById("tripTitle").innerHTML =
      "✈ अपने सपनों की यात्रा की योजना बनाएं";
    document.getElementById("sourceLabel").innerHTML = "प्रस्थान शहर";
    document.getElementById("destinationLabel").innerHTML = "गंतव्य शहर";
    document.getElementById("startLabel").innerHTML = "प्रारंभ तिथि";
    document.getElementById("endLabel").innerHTML = "समाप्ति तिथि";
    document.getElementById("budgetLabel").innerHTML = "बजट (₹)";
    document.getElementById("travelerLabel").innerHTML = "यात्रियों की संख्या";
    document.getElementById("interestLabel").innerHTML = "यात्रा रुचि";
    document.getElementById("transportLabel").innerHTML = "यातायात";
    document.getElementById("hotelLabel").innerHTML = "होटल पसंद";
    document.getElementById("generateBtn").innerHTML = "AI यात्रा योजना बनाएं";
  } else if (lang == "mr") {
    document.getElementById("tripTitle").innerHTML =
      "✈ तुमच्या स्वप्नातील सहलीची योजना करा";
    document.getElementById("sourceLabel").innerHTML = "प्रस्थान शहर";
    document.getElementById("destinationLabel").innerHTML = "गंतव्य शहर";
    document.getElementById("startLabel").innerHTML = "सुरुवातीची तारीख";
    document.getElementById("endLabel").innerHTML = "समाप्तीची तारीख";
    document.getElementById("budgetLabel").innerHTML = "बजेट (₹)";
    document.getElementById("travelerLabel").innerHTML = "प्रवाशांची संख्या";
    document.getElementById("interestLabel").innerHTML = "प्रवासाची आवड";
    document.getElementById("transportLabel").innerHTML = "वाहतूक";
    document.getElementById("hotelLabel").innerHTML = "हॉटेल पसंती";
    document.getElementById("generateBtn").innerHTML = "AI सहल योजना तयार करा";
  }
}
async function generateTrip() {
  let source = document.getElementById("source").value;
  let destination = document.getElementById("destination").value;

  let startDate = document.getElementById("startDate").value;
  let endDate = document.getElementById("endDate").value;

  let budget = document.getElementById("budget").value;

  let travellers = document.getElementById("travellers").value;

  let interest = document.getElementById("interest").value;

  let transport = document.getElementById("transport").value;

  let hotel = document.getElementById("hotel").value;

  let response = await fetch("/generate-trip", {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      source: source,

      destination: destination,

      startDate: startDate,

      endDate: endDate,

      budget: budget,

      travellers: travellers,

      interest: interest,

      transport: transport,

      hotel: hotel,
    }),
  });

  let data = await response.json();

  localStorage.setItem("tripData", JSON.stringify(data));

  window.location.href = "itinerary.html";
}

window.onload = function () {
  if (window.location.pathname.includes("itinerary.html")) {
    let data = JSON.parse(localStorage.getItem("tripData"));

    if (!data) return;

    let hotelHTML = "";

    data.hotels.forEach(function (hotel) {
      hotelHTML += `<p>🏨 ${hotel}</p>`;
    });

    document.getElementById("hotelResult").innerHTML = hotelHTML;

    let placeHTML = "";

    data.places.forEach(function (place) {
      placeHTML += `<p>📍 ${place}</p>`;
    });

    document.getElementById("placeResult").innerHTML = placeHTML;

    document.getElementById("budgetResult").innerHTML = "₹" + data.budget;

    document.getElementById("itineraryResult").innerHTML = `
        <h3>Day 1</h3>
        Arrival & Hotel Check-in

        <br><br>

        <h3>Day 2</h3>
        Visit Tourist Attractions

        <br><br>

        <h3>Day 3</h3>
        Local Shopping & Departure
        `;
  }
};
