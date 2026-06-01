export class Geohasher {
    private static readonly BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz";

    public static encode(lat: number, lon: number, precision: number = 12): string {
        const latInterval = [-90.0, 90.0];
        const lonInterval = [-180.0, 180.0];
        
        let geohash = "";
        const bits = [16, 8, 4, 2, 1];
        
        let bit = 0;
        let ch = 0;
        let evenBit = true;

        while (geohash.length < precision) {
            if (evenBit) {
                const mid = (lonInterval[0] + lonInterval[1]) / 2;
                if (lon > mid) {
                    ch |= bits[bit];
                    lonInterval[0] = mid;
                } else {
                    lonInterval[1] = mid;
                }
            } else {
                const mid = (latInterval[0] + latInterval[1]) / 2;
                if (lat > mid) {
                    ch |= bits[bit];
                    latInterval[0] = mid;
                } else {
                    latInterval[1] = mid;
                }
            }

            evenBit = !evenBit;

            if (bit < 4) {
                bit++;
            } else {
                geohash += this.BASE32[ch];
                bit = 0;
                ch = 0;
            }
        }

        return geohash;
    }
}

// --- CI/CD Automated Test ---
const lat = 37.8199;
const lon = -122.4783;

const result = Geohasher.encode(lat, lon, 9);

if (result === "9q8zh4yvc") {
    console.log(`TypeScript Geohashing Test Passed! (Result: ${result})`);
} else {
    console.error(`Failed! Got ${result}`);
    process.exit(1);
}