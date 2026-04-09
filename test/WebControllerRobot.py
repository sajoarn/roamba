# This is a web controller for the robot, just to move the robot around.
# To connect use the given IP address that includes port 5000, example http://192.168.1.129:5000/
# The website has Robot Control Dashboard (still work in progress) 
# and Custom Commands, this is what was used during my test
# Rotate Left, Rotate Right requires angle (default if 45 degrees)
# Forward, Reverse requires movement duration (default is 1000 ms)
# To get this running for testing use in RPi terminal:
# pip install flask 
# pip install pyserial
# The Raspberry Pi is connected to Arduino via USB
from flask import Flask, render_template_string, request
import serial
import time

# ---- Serial connection to Arduino ----
arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=0.1)
time.sleep(2)

def send_command(cmd, value=None):
    if value is None:
        msg = f"{cmd}\n"
    else:
        msg = f"{cmd}:{value}\n"
    arduino.write(msg.encode())
    print("Sent:", msg.strip())

# ---- Flask App ----
app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Robot Control Dashboard</title>
    <style>
        body { font-family: Arial; text-align: center; background: #f0f0f0; }
        button { width: 150px; height: 60px; font-size: 20px; margin: 10px; }
        input { font-size: 20px; width: 100px; }
        .container { margin-top: 40px; }
    </style>
</head>
<body>

<h1>Robot Control Dashboard</h1>

<div class="container">
    <form method="POST">
        <button name="cmd" value="F">Forward</button><br>
        <button name="cmd" value="L">Left</button>
        <button name="cmd" value="S">Stop</button>
        <button name="cmd" value="R">Right</button><br>
        <button name="cmd" value="B">Reverse</button>
    </form>
</div>

<h2>Custom Commands</h2>
<form method="POST">
    <label>Angle:</label>
    <input type="number" name="angle" value="45">
    <button name="cmd" value="L">Rotate Left</button>
    <button name="cmd" value="R">Rotate Right</button>
</form>

<form method="POST">
    <label>Duration (ms):</label>
    <input type="number" name="duration" value="1000">
    <button name="cmd" value="F">Forward</button>
    <button name="cmd" value="B">Reverse</button>
</form>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def control():
    if request.method == "POST":
        cmd = request.form.get("cmd")

        # Angle commands
        if cmd in ["L", "R"] and "angle" in request.form:
            angle = request.form.get("angle")
            send_command(cmd, angle)
        
        # Duration commands
        elif cmd in ["F", "B"] and "duration" in request.form:
            duration = request.form.get("duration")
            send_command(cmd, duration)

        # Simple commands (Stop)
        else:
            send_command(cmd)

    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)