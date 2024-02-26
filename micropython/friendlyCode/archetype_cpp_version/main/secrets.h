#ifndef SECRETS_H
#define SECRETS_H

#define MY_SSID "Aulas EICT"
#define MY_PASSWORD "eict1234"
#define PING_URLS ["www.google.com", "www.facebook.com", "www.twitter.com"]

extern const String API_URL  = "192.168.1.133"; 
extern const uint   API_PORT = 8080;
#define API_ENDPOINT "/api/data"
#define API_USERNAME "admin"
#define API_PASSWORD "admin"

extern const String TEMPERATURE_UIID = "3a56695b-005c-48d3-8005-a76f5d0dc9f6";
extern const String HUMIDITY_UIID = "5d706a1a-86b0-4bca-b2c8-6a9e52107f27";
extern const String CROP_UIID = "5d706a1a-86b0-4bca-b2c8-6a9e52107f27";

#endif // SECRETS_H