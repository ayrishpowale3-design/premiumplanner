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
async function loadTrips() {

    try {

        const response = await fetch("/trip-history");

        const trips = await response.json();

        const container =
            document.getElementById("tripsContainer");

        if (!container) {
            return;
        }

        if (trips.length === 0) {

            container.innerHTML =
                "<h3>No trips saved yet.</h3>";

            return;
        }

        let html = "";

        trips.forEach(function(trip) {

            html += `

                <div class="service-box">

                    <h2>
                        ✈ ${trip.source}
                        → ${trip.destination}
                    </h2>

                    <p>
                        📅 ${trip.start_date}
                        → ${trip.end_date}
                    </p>

                    <p>
                        👥 Travelers:
                        ${trip.travellers}
                    </p>

                    <p>
                        💰 Budget:
                        ₹${trip.budget}
                    </p>

                    <p>
                        🚗 Transport:
                        ${trip.transport}
                    </p>

                    <p>
                        🏨 Hotel:
                        ${trip.hotel}
                    </p>

                    <p>
                        ❤️ Favorite:
                        ${trip.is_favorite ? "Yes" : "No"}
                    </p>

                    <button
                        onclick="favoriteTrip(${trip.id})">
                        ❤️ Favorite
                    </button>

                    <button
                        onclick="deleteTrip(${trip.id})">
                        🗑 Delete
                    </button>

                </div>

            `;

        });

        container.innerHTML = html;

    } catch (error) {

        console.error(error);

        document.getElementById("tripsContainer").innerHTML =
            "<p>Unable to load trips.</p>";
    }
}


async function favoriteTrip(id) {

    await fetch(
        "/favorite-trip/" + id,
        {
            method: "POST"
        }
    );

    loadTrips();
}


async function deleteTrip(id) {

    if (!confirm("Delete this trip?")) {
        return;
    }

    await fetch(
        "/delete-trip/" + id,
        {
            method: "DELETE"
        }
    );

    loadTrips();
}


window.onload = loadTrips;