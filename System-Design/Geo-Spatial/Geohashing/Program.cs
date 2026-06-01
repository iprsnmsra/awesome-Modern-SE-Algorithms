using System;
using System.Text;

public class Program {
    class Geohasher {
        private const string BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz";

        public static string Encode(double lat, double lon, int precision = 12) {
            double[] latInterval = { -90.0, 90.0 };
            double[] lonInterval = { -180.0, 180.0 };
            
            StringBuilder geohash = new StringBuilder();
            int[] bits = { 16, 8, 4, 2, 1 };
            
            int bit = 0;
            int ch = 0;
            bool evenBit = true;

            while (geohash.Length < precision) {
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
                    geohash.Append(BASE32[ch]);
                    bit = 0;
                    ch = 0;
                }
            }

            return geohash.ToString();
        }
    }

    // --- CI/CD Automated Test ---
    public static int Main() {
        double lat = 37.8199;
        double lon = -122.4783;
        
        string result = Geohasher.Encode(lat, lon, 9);
        
        if (result == "9q8zh4yvc") {
            Console.WriteLine($"C# Geohashing Test Passed! (Result: {result})");
            return 0;
        }
        
        Console.WriteLine($"Failed! Got {result}");
        return 1;
    }
}