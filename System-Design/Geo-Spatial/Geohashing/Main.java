public class Main {
    static class Geohasher {
        private static final String BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz";

        public static String encode(double lat, double lon, int precision) {
            double[] latInterval = {-90.0, 90.0};
            double[] lonInterval = {-180.0, 180.0};
            
            StringBuilder geohash = new StringBuilder();
            int[] bits = {16, 8, 4, 2, 1};
            
            int bit = 0;
            int ch = 0;
            boolean evenBit = true;

            while (geohash.length() < precision) {
                if (evenBit) {
                    double mid = (lonInterval[0] + lonInterval[1]) / 2;
                    if (lon > mid) {
                        ch |= bits[bit];
                        lonInterval[0] = mid;
                    } else {
                        lonInterval[1] = mid;
                    }
                } else {
                    double mid = (latInterval[0] + latInterval[1]) / 2;
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
                    geohash.append(BASE32.charAt(ch));
                    bit = 0;
                    ch = 0;
                }
            }

            return geohash.toString();
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        double lat = 37.8199;
        double lon = -122.4783;
        
        String result = Geohasher.encode(lat, lon, 9);
        
        if (result.equals("9q8zh4yvc")) {
            System.out.println("Java Geohashing Test Passed! (Result: " + result + ")");
        } else {
            System.err.println("Failed! Got " + result);
            System.exit(1);
        }
    }
}