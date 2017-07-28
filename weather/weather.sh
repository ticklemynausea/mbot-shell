#!/bin/bash

temp() {
  python -c 'import json; import sys; print json.load(sys.stdin)["query"]["results"]["channel"]["item"]["condition"]["temp"]'
}
humidity() {
  python -c 'import json; import sys; print json.load(sys.stdin)["query"]["results"]["channel"]["atmosphere"]["humidity"]'
}
wind() {
  python -c 'import json; import sys; print json.load(sys.stdin)["query"]["results"]["channel"]["wind"]["speed"]'
}
city() {
  python -c 'import json; import sys; print json.load(sys.stdin)["query"]["results"]["channel"]["item"]["title"]'
}
condition() {
  python -c 'import json; import sys; print json.load(sys.stdin)["query"]["results"]["channel"]["item"]["condition"]["text"]'
}
sunrise() {
  python -c 'import json; import sys; print json.load(sys.stdin)["query"]["results"]["channel"]["astronomy"]["sunrise"]'
}
sunset() {
  python -c 'import json; import sys; print json.load(sys.stdin)["query"]["results"]["channel"]["astronomy"]["sunset"]'
}

TEMP=$(curl -sf "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22$1%22)%20and%20u%3D%22c%22&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys" | temp)
HUMIDITY=$(curl -sf "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22$1%22)%20and%20u%3D%22c%22&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys" | humidity)
CITY=$(curl -sf "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22$1%22)%20and%20u%3D%22c%22&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys" | city)
WIND=$(curl -sf "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22$1%22)%20and%20u%3D%22c%22&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys" | wind)
CONDITION=$(curl -sf "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22$1%22)%20and%20u%3D%22c%22&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys" | condition)
SUNRISE=$(curl -sf "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22$1%22)%20and%20u%3D%22c%22&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys" | sunrise)
SUNSET=$(curl -sf "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22$1%22)%20and%20u%3D%22c%22&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys" | sunset)



echo "$CITY Temperature: $TEMP Cยบ  Condition: $CONDITION  Humidity: $HUMIDITY%  Wind: $WIND km/h  Sunrise/Sunset: $SUNRISE/$SUNSET"
