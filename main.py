import time
from pynput import mouse, keyboard

recorded_events = []  # will store (timestamp, event_type, event_info)
recording = False
playback = False
stop_playback = False

# We track when we began recording to keep event times relative
start_time = 0.0

# We'll reference our listeners so we can manually stop them on ESC
m_listener = None
k_listener = None


def on_move(x, y):
    if recording:
        timestamp = time.time() - start_time
        recorded_events.append((timestamp, "move", (x, y)))


def on_click(x, y, button, pressed):
    if recording:
        timestamp = time.time() - start_time
        recorded_events.append((timestamp, "click", (x, y, button, pressed)))


def on_scroll(x, y, dx, dy):
    if recording:
        timestamp = time.time() - start_time
        recorded_events.append((timestamp, "scroll", (x, y, dx, dy)))


def on_press(key):
    global recording, playback, stop_playback, m_listener, k_listener

    # If we press ESC while recording, stop recording
    if key == keyboard.Key.esc:
        if recording:
            recording = False
            print("[INFO] Recording stopped.")
            # Manually stop our listeners so .join() returns
            if m_listener:
                m_listener.stop()
            if k_listener:
                k_listener.stop()
        elif playback:
            # If we press ESC while playing back, signal to stop playback
            stop_playback = True
            print("[INFO] Playback stop requested.")
            # We'll also stop the listener so we can keep reading console input
            if k_listener:
                k_listener.stop()

    if recording:
        # Only record key presses if recording is True
        timestamp = time.time() - start_time
        try:
            # Normal character
            recorded_events.append((timestamp, "press", (key.char,)))
        except AttributeError:
            # Special key (Shift, Ctrl, etc.)
            recorded_events.append((timestamp, "press", (str(key),)))


def on_release(key):
    if recording:
        timestamp = time.time() - start_time
        try:
            recorded_events.append((timestamp, "release", (key.char,)))
        except AttributeError:
            recorded_events.append((timestamp, "release", (str(key),)))


def record_events():
    global recorded_events, recording, start_time, m_listener, k_listener
    recorded_events.clear()

    # 3-second countdown
    for i in range(3, 0, -1):
        print(f"Starting recording in {i}...")
        time.sleep(1)

    recording = True
    start_time = time.time()

    print("[INFO] Recording started. Press ESC to stop recording.")

    with mouse.Listener(
        on_move=on_move, on_click=on_click, on_scroll=on_scroll
    ) as m, keyboard.Listener(on_press=on_press, on_release=on_release) as k:
        m_listener = m
        k_listener = k
        # Block until both listeners are fully stopped
        m_listener.join()
        k_listener.join()

    print("[INFO] Finished recording. Total events:", len(recorded_events))


def play_events(loop=False):
    """Replays the recorded events. If loop=True, it will keep looping until ESC is pressed."""
    global playback, stop_playback, k_listener
    if not recorded_events:
        print("[WARNING] No events to play back.")
        return

    # 3-second countdown before playback
    for i in range(3, 0, -1):
        print(f"Starting playback in {i}...")
        time.sleep(1)

    from pynput import mouse, keyboard

    mouse_controller = mouse.Controller()
    keyboard_controller = keyboard.Controller()

    playback = True
    stop_playback = False

    # We'll define a helper to perform a single event
    def handle_event(ev):
        (timestamp, etype, data) = ev
        if etype == "move":
            x, y = data
            mouse_controller.position = (x, y)
        elif etype == "click":
            x, y, button, pressed = data
            mouse_controller.position = (x, y)
            if pressed:
                mouse_controller.press(button)
            else:
                mouse_controller.release(button)
        elif etype == "scroll":
            x, y, dx, dy = data
            mouse_controller.position = (x, y)
            mouse_controller.scroll(dx, dy)
        elif etype == "press":
            (key_val,) = data
            if "Key." in key_val:
                # It's a special key
                k = getattr(keyboard.Key, key_val.split("Key.")[1], None)
                if k:
                    keyboard_controller.press(k)
            else:
                keyboard_controller.press(key_val)
        elif etype == "release":
            (key_val,) = data
            if "Key." in key_val:
                # It's a special key
                k = getattr(keyboard.Key, key_val.split("Key.")[1], None)
                if k:
                    keyboard_controller.release(k)
            else:
                keyboard_controller.release(key_val)

    # We'll also have a background listener to detect ESC and set stop_playback
    def on_press_stop(key):
        global stop_playback
        if key == keyboard.Key.esc:
            stop_playback = True
            print("[INFO] Playback stop requested.")
            return False  # stop this background listener

    # Start the listener in the background
    k_listener = keyboard.Listener(on_press=on_press_stop)
    k_listener.start()

    print("[INFO] Playback started. Press ESC to stop.")

    while True:
        start_replay_time = time.time()
        for event in recorded_events:
            if stop_playback:
                break
            current_time = time.time()
            event_offset = event[0]
            elapsed = current_time - start_replay_time
            if event_offset > elapsed:
                time.sleep(event_offset - elapsed)

            handle_event(event)

        if stop_playback:
            break
        if not loop:
            break

    playback = False
    k_listener.stop()
    print("[INFO] Playback finished.")


def main():
    while True:
        print("\nOptions:")
        print("1) Record events")
        print("2) Play recorded events once")
        print("3) Loop recorded events until ESC")
        print("4) Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            record_events()
        elif choice == "2":
            play_events(loop=False)
        elif choice == "3":
            play_events(loop=True)
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
