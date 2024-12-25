from flask import Flask, request, jsonify, render_template
from geopy.distance import geodesic
import ssl
from urllib.request import build_opener, HTTPSHandler, Request
import json

# Flask app setup
app = Flask(__name__)

# Sample store data (latitude, longitude)
stores = [
    { "id": 1, "name": "G6 cafe EDSA Guadalupe Branch", "lat": 14.564667, "lng": 121.045167 },
    { "id": 2, "name": "G6 cafe Makati Ave. Branch", "lat": 14.565111, "lng": 121.029889 },
    { "id": 3, "name": "G6 cafe Timog Ave., Quezon City Branch", "lat": 14.634907, "lng": 121.037490 },
    { "id": 4, "name": "G6 cafe UST Branch", "lat": 14.611944, "lng": 120.988250 },
    { "id": 5, "name": "G6 cafe Caloocan Branch", "lat": 14.651833, "lng": 120.977083 },
    { "id": 6, "name": "Karuhatan, Valenzuela City", "lat": 14.683806, "lng": 120.977361 },
    { "id": 7, "name": "Valenzuela", "lat": 14.705417, "lng": 120.989417 },
    { "id": 8, "name": "Tondo, Manila", "lat": 14.607000, "lng": 120.966861 },
    { "id": 9, "name": "Malabon", "lat": 14.660417, "lng": 120.951389 },
    { "id": 10, "name": "Marilao", "lat": 14.765312502225738, "lng": 120.96303895378405 },
    { "id": 11, "name": "Maginhawa", "lat": 14.646462329467116, "lng": 121.05994100960814 },
    { "id": 12, "name": "Eastwood, Quezon City", "lat": 14.610476961805494, "lng": 121.08137521324323 },
    { "id": 13, "name": "Tomas Morato Ave., Quezon City", "lat": 14.637358481410566, "lng": 121.03574659070495 },
    { "id": 14, "name": "East Kapitolyo, Pasig City", "lat": 14.569904297281166, "lng": 121.06023714392221 },
    { "id": 15, "name": "Fairview Terraces, Quezon City", "lat": 14.735937949695424, "lng": 121.060}
]


# Function to find the nearest store based on user's location
def find_nearest_store(user_location):
    nearest_store = None
    min_distance = float('inf')
    for store in stores:
        store_location = (store['lat'], store['lng'])
        distance = geodesic(user_location, store_location).kilometers
        if distance < min_distance:
            min_distance = distance
            nearest_store = store
    return nearest_store, min_distance


# Function to get coordinates from an address with SSL verification bypass
def get_coordinates(address):
    try:
        # Bypass SSL verification
        ssl_context = ssl._create_unverified_context()
        opener = build_opener(HTTPSHandler(context=ssl_context))

        # Prepare URL and request
        base_url = "https://nominatim.openstreetmap.org/search"
        params = f"?q={address}&format=json&limit=1"
        url = f"{base_url}{params}"
        request = Request(url)

        # Make the request and parse the response
        response = opener.open(request)
        data = json.loads(response.read().decode())

        if data:
            location = data[0]
            return float(location["lat"]), float(location["lon"])
        return None
    except Exception as e:
        print(f"Error getting coordinates: {e}")
        return None


# Route for the main page (index page)
@app.route('/')
def index():
    return render_template('index.html')  # Ensure you have an index.html in the templates folder


# Route for recommending stores based on user address
@app.route('/recommend_store', methods=['POST'])
def recommend_store():
    data = request.json
    address = data.get("address")

    if not address:
        return jsonify({"error": "No address provided."}), 400

    user_location = get_coordinates(address)

    if not user_location:
        return jsonify({"error": "Address not found."}), 400

    store, distance = find_nearest_store(user_location)
    if store:
        return jsonify({
            "nearest_store": store,
            "distance_km": round(distance, 2)
        })
    return jsonify({"error": "No stores found."}), 404


# Route to get all stores for rendering on the map
@app.route('/get_stores', methods=['GET'])
def get_stores():
    return jsonify(stores)


# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True)
