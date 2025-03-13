# Keyboard & Mouse Macro Recorder

A simple Python utility for recording and playing back keyboard and mouse actions.

## Features

- Record mouse movements, clicks, and scrolls
- Record keyboard presses and releases
- Play back recorded actions once or in a loop
- Stop recording or playback with ESC key

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/CuriouslyCory/keyboard-mouse-playback.git
   cd keyboard-mouse-playback
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the program with:
```
python main.py
```

### Menu Options

The program presents a simple menu with the following options:

1. **Record events** - Start recording mouse and keyboard actions
   - A 3-second countdown will begin
   - Press ESC to stop recording

2. **Play recorded events once** - Play back the recorded actions one time
   - A 3-second countdown will begin
   - Press ESC to stop playback

3. **Loop recorded events until ESC** - Play back the recorded actions repeatedly
   - A 3-second countdown will begin
   - Press ESC to stop playback

4. **Exit** - Quit the program

## Notes

- This program requires permission to monitor and control your mouse and keyboard
- Recordings are stored in memory and will be lost when the program exits
- Use responsibly and be careful with automated input playback

