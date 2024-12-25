// Initialize the map and handle other logic
var map = L.map('map').setView([14.565111, 121.029889], 12); // Example coordinates (Makati)

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

fetch('/get_stores')
  .then(response => response.json())
  .then(data => {
    data.forEach(function(store) {
      L.marker([store.lat, store.lng])
        .addTo(map)
        .bindPopup("<b>" + store.name + "</b><br>Lat: " + store.lat + ", Lng: " + store.lng);
    });
  })
  .catch(error => console.error("Error fetching stores:", error));

document.getElementById('addressForm').addEventListener('submit', function(event) {
  event.preventDefault();
  var address = document.getElementById('address').value;

  fetch('/recommend_store', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ address: address }),
  })
  .then(response => response.json())
  .then(data => {
    if (data.nearest_store) {
      document.getElementById('nearestStore').innerText = "Nearest Store: " + data.nearest_store.name;
      document.getElementById('distance').innerText = "Distance: " + data.distance_km + " km";
    } else {
      document.getElementById('nearestStore').innerText = "Error: " + data.error;
    }
  })
  .catch(error => console.error("Error finding nearest store:", error));
});
