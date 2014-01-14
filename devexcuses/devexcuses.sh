#!/bin/sh
curl -s http://developerexcuses.com/ | grep -oP "<a href=\"/\"[^>]*>\K.*(?=</a)"
