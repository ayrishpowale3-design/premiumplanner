fetch("http://127.0.0.1:5000/trip-history")
  .then((response) => response.json())
  .then((trips) => {
    const tripList = document.getElementById("tripList");

    if (trips.length === 0) {
      tripList.innerHTML = "<h3>No Trips Saved Yet</h3>";
      return;
    }

    trips.forEach((trip) => {
      const favoriteButton = trip.is_favorite
        ? "❤️ Remove Favorite"
        : "🤍 Add to Favorites";

      tripList.innerHTML += `
        <div class="trip-card">

            <h2>${trip.source} ➜ ${trip.destination}</h2>

            <p>📅 ${trip.start_date} - ${trip.end_date}</p>

            <p>💰 ${trip.budget}</p>

            <p>🚗 ${trip.transport}</p>

            <p>❤️ ${trip.interest}</p>

            <p>🏨 ${trip.hotel}</p>

            <button onclick="favoriteTrip(${trip.id})">
                ${favoriteButton}
            </button>

            <button onclick="deleteTrip(${trip.id})">
                🗑 Delete Trip
            </button>

            <hr>

        </div>
      `;
    });
  });


function favoriteTrip(id) {
  fetch(`http://127.0.0.1:5000/favorite-trip/${id}`, {
    method: "POST",
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        location.reload();
      }
    });
}


function deleteTrip(id) {
  if (!confirm("Delete this trip?")) return;

  fetch(`http://127.0.0.1:5000/delete-trip/${id}`, {
    method: "DELETE",
  }).then(() => {
    location.reload();
  });
}