class Geohasher:
    # Custom Base32 alphabet (omits 'a', 'i', 'l', 'o' to avoid visual confusion)
    BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz"

    @staticmethod
    def encode(lat: float, lon: float, precision: int = 12) -> str:
        lat_interval = [-90.0, 90.0]
        lon_interval = [-180.0, 180.0]
        
        geohash = []
        bits = [16, 8, 4, 2, 1]
        
        bit = 0
        ch = 0
        even_bit = True # True for Longitude, False for Latitude

        while len(geohash) < precision:
            if even_bit:
                mid = (lon_interval[0] + lon_interval[1]) / 2
                if lon > mid:
                    ch |= bits[bit]
                    lon_interval[0] = mid
                else:
                    lon_interval[1] = mid
            else:
                mid = (lat_interval[0] + lat_interval[1]) / 2
                if lat > mid:
                    ch |= bits[bit]
                    lat_interval[0] = mid
                else:
                    lat_interval[1] = mid

            even_bit = not even_bit

            if bit < 4:
                bit += 1
            else:
                geohash.append(Geohasher.BASE32[ch])
                bit = 0
                ch = 0

        return "".join(geohash)

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    # Coordinates for the Golden Gate Bridge, San Francisco
    lat = 37.8199
    lon = -122.4783
    
    # Standard 9-character precision (approx 4.7 x 4.7 meters)
    result = Geohasher.encode(lat, lon, precision=9)
    
    # Mathematical proof of correct encoding
    assert result == "9q8zh4yvc", f"Geohash failed! Expected '9q8zh4yvc', got '{result}'"
    
    print(f"Python Geohashing Test Passed! (Result: {result})")