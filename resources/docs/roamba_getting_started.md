# R.O.A.M-B.A
The Robotic Observation and Autonomous Mobility Boundary Analyzer (R.O.A.M-B.A) is a group project for Purdue University ECE 568 Embedded Systems. The system uses a off-the-shelf robot kit that comes complete with an Arduino Uno R3 and all sensors and servos needed to drive the robot[1]. Additionally, we use a Raspberry Pi 4 hooked to the kit's webcam for visual recognition of path and obstacles.

[1] https://us.elegoo.com/products/elegoo-smart-robot-car-kit-v-4-0
[2] https://www.raspberrypi.com/products/raspberry-pi-4-model-b/

# Getting Started
## Arduino
1. Install [Arduino IDE v2.3.8](https://github.com/arduino/arduino-ide/releases/tag/2.3.8)
2. Update IDE to include Arduino AVR Boards (core) which includes the build tools needed for the Uno R3
3. Using the IDE library manager, add libraries:
    - IRremote
    - FastLED
    - MPU6050 by Electronic Cats
4. Sketch -> Verify/Compile
5. On the Uno's top board, move the switch from "Cam" to "Upload"
6. In the IDE, select "Upload"

## Raspberry Pi Fresh Start
1. Power on the Raspberry Pi
2. Connect the pi, either through Pi Connect, using headless setup, or via an HDMI cable
3. Open a terminal on the pi
4. Copy or clone the ROAM-BA repo to the pi. For the purpose of these instructions, I put the repo at `~/git_repos/roamba`
5. Navigate to the repo location in the terminal and create a python virtual environment:
```sh
cd ~/git_repos/roamba
python -m venv .venv
```
- you can check whether this succeeded by typing `ls -a` in the terminal. This should display all hidden directories, including a newly created `.venv` directory
6. Run the python virtual environment (you will have to do this every time you connect to the pi):
```sh
source ./.venv/bin/activate
```
- NOTE: there is no file extension on the activate script in Linux
- Side NOTE: Running virtual environments depends on the operating system. To run a virtual env scripts local to Windows, run: `./.venv/Scripts/activate.ps1` if in powershell or `./.venv/Scripts/activate.sh` if in git bash
7. Change Directory down to the vision_sys folder, and install packages using pip:
```sh
cd ~/git_repos/roamba/vision_sys
pip install -r requirements.txt
```
- NOTE: Make sure the raspberry pi is connected to the internet, otherwise these installs will fail
8. OpenCV versions 4.13 and newer do not include fonts, so create a directory to hold them, then copy them over to the venv openCV package:
```sh
mkdir ~/git_repos/roamba/.venv/lib/python3.13/site-packages/cv2/qt/fonts
cp /usr/share/fonts/truetype/dejavu/*.ttf ~/git_repos/roamba/.venv/lib/python3.13/site-packages/cv2/qt/fonts
```
- NOTE: you can find your venv path information by running the venv environment (step 6), then running the `which python` command
9. There is a bug where OpenCV will not be able to find qt plugin "wayland". To fix permanantly, run:
```sh
echo 'export QT_QPA_PLATFORM=xcb' >> ~/.bashrc
source ~/.bashrc
```
- You can verify this command worked by looking at the end of the bashrc file by running `tail ~/.bashrc`


Or to fix temporarily (this setting does not persist between power cycles), run:
```sh
export QT_QPA_PLATFORM=xcb
```

8. Done! Test OpenCV was installed correctly by running the ColorPicker script:
```sh
cd ~/git_repos/roamba/vision_sys
python ColorPickerScript.py
```
- This should pop up two windows with a test video and color sliders
- NOTE: the ColorPickerScript.py has relative paths, and so must be run from the vision_sys directory

## SSH Remote Session
To run the robot remotely, you can ssh into the pi when connected to the Elegoo wifi:
0. Power on your pi and the robot, so the camera Elegoo wifi is running and discoverable
1. On your remote computer, open a command prompt or terminal and verify ssh is installed by running:
```sh
ssh
```
- If ssh is not installed, try a different terminal/command prompt program (like powershell), or install [open-ssh](https://www.openssh.org/)
- You may need to create an ssh public key. Follow the github instructions on how to [create one](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
2. On your raspberry pi, connect to the Elegoo wifi, then find your IP address by running:
```sh
hostname -I
```
- For the purposes of these instructions, I will use `192.168.4.2`
3. On your pi, identify your username (in the terminal, it should be in green text with the format: `myusername@raspberrypiname`)
4. On your remote computer, connect to the Elegoo Wifi, then run ssh in command prompt or terminal:
```sh
ssh -X myusername@192.168.4.2
```
- type your raspberry pi account password when prompted. If you do not have a password, leave blank and hit 'enter'
- You will be prompted to save the connection to known_hosts. Type 'y' to confirm.
    - Side NOTE: known_hosts is a human-readable file on your remote computer at ~/.ssh/known_hosts. If you want to delete this ssh key later, edit the known_hosts file and delete the line corresponding to the IP address you connected to
- NOTE: the `-X` command is needed to forward pop-up windows from the OpenCV qt windows to the client computer ssh session
5. You're now remotely logged in to the pi! 
6. Change directory to the location of your roamba repo, and run your python virtual environment:
```sh
cd ~/git_repos/roamba
source ./.venv/bin/activate
```
7. Test out the webcam live stream by running MainRobotLane.py:
```sh
python ~/git_repos/roamba/vision_sys/MainRobotLane.py
```
- This should pop up a window with a color slider, a window with the live webcam feed, and should print a single line live-update of the curve degree output in the terminal
8. Exit the ssh session by typing `exit` in the remote computer terminal

## Debug Web Server
This puts out commands that can be read by ControlMain.ino
1. pip install flask pyserial