#ifndef SECRETS_H
#define SECRETS_H

#define MY_SSID "ArchLinux"
#define MY_PASSWORD "nuncaheusadoarch"
#define PING_URLS ["www.google.com", "www.facebook.com", "www.twitter.com"]

extern const uint   API_PORT  = 8000;
extern const String API_URL   = "192.168.0.110"; 
extern const String API_CREDS = "{\"username\":\"admin\", \"password\":\"admin\"}";

#define HTTP_TIMEOUT 1000
#define API_ENDPOINT "/api/measurement/write_batch/"
#define API_LOGIN_ENDPOINT "/api/user/login/"

extern const String TEMPERATURE_UIID = "\"3a56695b-005c-48d3-8005-a76f5d0dc9f6\"";
extern const String HUMIDITY_UIID = "\"5d706a1a-86b0-4bca-b2c8-6a9e52107f27\"";
extern const String CROP_UIID = "\"5d706a1a-86b0-4bca-b2c8-6a9e52107f27\"";

#endif // SECRETS_H