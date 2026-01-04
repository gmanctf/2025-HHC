import socketio, re, threading, sys
import time

# Create a Socket.IO client
sio = socketio.Client(reconnection=False)

# Clean ANSI encoding
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def clean(text): return ansi_escape.sub('', text)

# global variable to track state, resolve race condition for Q3 and finish keepalive thread
waiting_for_q3_completion = False
q4_detected = False
q4_answer_sent = False
challenge_complete = False
keep_alive_timer = None


# Define handler functions
def handle_connect():
    print("Connected to server")

def handle_disconnect():
    print("Disconnected from server")
    # If challenge is complete, exit the script
    if challenge_complete:
        print("Challenge completed successfully! Exiting script.")
        # Cancel any pending keep-alive timer
        global keep_alive_timer
        if keep_alive_timer:
            keep_alive_timer.cancel()

def handle_data(data):
    # Declare global variables
    global waiting_for_q3_completion, q4_detected, q4_answer_sent, challenge_complete

    text = clean(data)
    print("Server says:", text)
    
    # Send "y" to start challenge
    if "Type [y]es to begin" in data:
        print("Sending 'y'")
        sio.emit("input", "y\n")
    
    # Question 1
    if "Run a default nmap scan of 127.0.12.25" in text:
        print("Answering step 1")
        sio.emit("input", "nmap 127.0.12.25\n")

    # Question 2
    elif "Run an nmap scan of all TCP ports on 127.0.12.25" in text:
        print("Answering step 2")
        sio.emit("input", "nmap 127.0.12.25 -p-\n")
    
    # Question 3
    elif "Scan the range 127.0.12.20 - 127.0.12.28" in text:
        print("Answering step 3")
        waiting_for_q3_completion = True
        q4_detected = False
        q4_answer_sent = False
        sio.emit("input", "nmap 127.0.12.20-28 -p-\n")
    
    # Question 4 - just set a flag when we see it, don't answer yet
    elif "What service is running on 127.0.12.25 TCP port 8080" in text:
        print("Q4 detected - waiting for scan to complete")
        q4_detected = True
    
    # Detect when nmap scan is completely finished
    if "Nmap done:" in text and waiting_for_q3_completion:
        print("Q3 scan completed")
        waiting_for_q3_completion = False
        # If Q4 was already detected, send the answer now
        if q4_detected and not q4_answer_sent:
            print("Sending Q4 answer after scan completion")
            time.sleep(1)  # Give the terminal a moment to be ready
            sio.emit("input", "nmap -sV 127.0.12.25 -p 8080\n")
            q4_answer_sent = True
    
    # If Q4 appears after scan is already done, answer immediately
    elif "What service is running on 127.0.12.25 TCP port 8080" in text and not waiting_for_q3_completion and not q4_answer_sent:
        print("Q4 detected after scan completion - answering immediately")
        sio.emit("input", "nmap -sV 127.0.12.25 -p 8080\n")
        q4_answer_sent = True
    
    # Question 5
    elif "Use the ncat tool to connect to TCP port 24601" in text:
        print("Answering step 5")
        sio.emit("input", "nc 127.0.12.25 24601\n")
    
    # Final exit
    elif "Congratulations, you finished the Intro to Nmap" in text:
        print("Exiting challenge")
        challenge_complete = True
        sio.emit("input", "exit\n")

# Keep-alive every 5 seconds
def keep_alive():
    # Only send keep-alive if challenge is not complete
    if not challenge_complete:
        sio.emit("2")
        global keep_alive_timer
        keep_alive_timer = threading.Timer(5, keep_alive)
        keep_alive_timer.daemon = True
        keep_alive_timer.start()

sio.on("connect", handle_connect)
sio.on("disconnect", handle_disconnect)
sio.on("data", handle_data)

# Connect to the server
sio.connect(
    "https://hhc25-wetty-prod.holidayhackchallenge.com/?challenge=termNmap",
    transports=["websocket"]
)

# Start keep-alive
keep_alive()

# Keep the script running
sio.wait()

# Finish
sys.exit(0)
