#!/usr/bin/bash

echo "HEY! You shouldn't be here! If you are Frosty, then welcome back! Lets restore your access to the system..."
curl -X POST "$CHATBOT_URL/api/submit_ec87937a7162c2e258b2d99518016649" -H "Content-Type: Application/json" -d "{\"challenge_hash\":\"ec87937a7162c2e258b2d99518016649\"}"
echo "If you see no errors, the system should be unlocked for you now but they require root access."
echo -e "\nBut if you are not Frosty, please leave this place at once!"