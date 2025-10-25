import os
import requests
import folium
from dotenv import load_dotenv 
load_dotenv()

# ───────────────────────────────────────────────
# 1. GOOGLE GEOCODING API  (replace Nominatim)
# ───────────────────────────────────────────────
def get_coordinates(postal_code, country):
    """
    Convert a postal code into (latitude, longitude)
    using Google Maps Geocoding API.
    """
    try:
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # store key in .env
        if not GOOGLE_API_KEY:
            raise ValueError("Missing Google API key. Set GOOGLE_API_KEY in environment.")

        address = f"{postal_code}, {country}"
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {"address": address, "key": GOOGLE_API_KEY}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data["status"] == "OK" and data["results"]:
            location = data["results"][0]["geometry"]["location"]
            lat, lon = location["lat"], location["lng"]
            print(f"✅ Coordinates found for {postal_code}, {country}: ({lat}, {lon})")
            return lat, lon
        else:
            print(f"⚠️ Google API could not find coordinates: {data['status']}")
            return None, None

    except Exception as e:
        print(f"[ERROR] Geocoding failed: {e}")
        return None, None


# ───────────────────────────────────────────────
# 2. Retrieve nearby hospitals from OpenStreetMap
# ───────────────────────────────────────────────
def get_hospitals(lat, lon, radius=5000):
    try:
        query = f"""
        [out:json][timeout:25];
        (
          node["amenity"="hospital"](around:{radius},{lat},{lon});
          way["amenity"="hospital"](around:{radius},{lat},{lon});
          relation["amenity"="hospital"](around:{radius},{lat},{lon});
        );
        out center;
        """
        url = "https://overpass-api.de/api/interpreter"
        response = requests.get(url, params={"data": query}, timeout=25)
        response.raise_for_status()

        data = response.json()
        hospitals = []
        for e in data.get("elements", []):
            name = e.get("tags", {}).get("name", "Unknown Hospital")
            lat_ = e.get("lat", e.get("center", {}).get("lat"))
            lon_ = e.get("lon", e.get("center", {}).get("lon"))
            if lat_ and lon_:
                hospitals.append({"name": name, "lat": lat_, "lon": lon_})

        print(f"✅ Found {len(hospitals)} hospitals nearby.")
        return hospitals

    except requests.exceptions.Timeout:
        print("[ERROR] Overpass API timed out.")
        return []
    except Exception as e:
        print(f"[ERROR] Failed to retrieve hospitals: {e}")
        return []


# ───────────────────────────────────────────────
# 3. Create map
# ───────────────────────────────────────────────
def create_map(lat, lon, hospitals, postal_code, country):
    try:
        fmap = folium.Map(location=[lat, lon], zoom_start=13, tiles="CartoDB positron")

        folium.Marker(
            [lat, lon],
            popup=f"{postal_code}, {country}\n(You are here)",
            icon=folium.Icon(color="blue", icon="home"),
        ).add_to(fmap)

        for h in hospitals:
            folium.Marker(
                [h["lat"], h["lon"]],
                popup=h["name"],
                icon=folium.Icon(color="red", icon="plus-sign"),
            ).add_to(fmap)

        output_dir = "static"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "hospitals_near_me.html")
        fmap.save(output_path)

        print(f"✅ Map saved at: {output_path}")
        return output_path

    except Exception as e:
        print(f"[ERROR] Failed to create map: {e}")
        return None


# ───────────────────────────────────────────────
# 4. Main
# ───────────────────────────────────────────────
if __name__ == "__main__":
    postal_code = input("Enter postal code: ").strip()
    country = input("Enter country name: ").strip()

    lat, lon = get_coordinates(postal_code, country)
    if not lat or not lon:
        print("❌ Failed to find coordinates. Try another postal code or country.")
        exit()

    hospitals = get_hospitals(lat, lon, radius=5000)
    for h in hospitals[:5]:
        print(f"🏥 {h['name']}")

    create_map(lat, lon, hospitals, postal_code, country)
