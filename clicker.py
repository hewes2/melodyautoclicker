import pyautogui
import json
import time
from pynput import mouse

POINTS_FILE = "points.json"
DEFAULT_INTERVAL = 0.3

def record_points(n=7, filename=POINTS_FILE):
    print(f"Recording {n} points.")
    print("Move your mouse to the location and press Enter in this terminal.")
    points = []
    try:
        for i in range(n):
            input(f"\nPoint {i+1}: move mouse to the spot, then press Enter...")
            x, y = pyautogui.position()
            print(f"Captured point {i+1}: ({x}, {y})")
            points.append({"x": x, "y": y})
        with open(filename, "w") as f:
            json.dump(points, f, indent=2)
        print(f"\nSaved {n} points to {filename}")
        return points
    except KeyboardInterrupt:
        print("\nRecording cancelled by user.")
        return points

def load_points(filename):
    with open(filename, "r") as f:
        return json.load(f)

def play_melody(sequence, points, interval=0.3):
    # Wait for initial click to start
    print("\nClick anywhere to start the 3-second countdown...")
    def on_click(x, y, button, pressed):
        if pressed:
            return False
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

    # 3-second countdown
    for i in range(3, 0, -1):
        print(f"Starting in {i}...")
        time.sleep(1)
    time.sleep(0.1)
    print("Go!")

    # Playback loop
    for i, symbol in enumerate(sequence):
        if symbol == "0":
            print(f"Step {i+1}: rest")
            time.sleep(interval)
        elif symbol == "8":
            print(f"Step {i+1}: small extra pause 0.05s")
            time.sleep(0.05)
        elif symbol == "9":
            adjusted = max(interval - 0.06, 0)  # ensure non-negative
            print(f"Step {i+1}: short pause interval-0.01 = {adjusted:.3f}s")
            time.sleep(adjusted)
        else:
            index = int(symbol) - 1
            if 0 <= index < len(points):
                x, y = points[index]["x"], points[index]["y"]
                print(f"Step {i+1}: clicking point {symbol} at ({x}, {y})")
                pyautogui.moveTo(x, y)  # instant move
                pyautogui.click()
            else:
                print(f"Step {i+1}: invalid point {symbol}")
            time.sleep(interval)


def measure_click_intervals(num_clicks=5):
    """
    Waits for `num_clicks` and returns a list of intervals between consecutive clicks.
    For 5 clicks, returns 4 intervals.
    """
    click_times = []

    def on_click(x, y, button, pressed):
        if pressed:
            click_times.append(time.time())
            print(f"Click {len(click_times)} recorded at {click_times[-1]:.3f}s")
            if len(click_times) >= num_clicks:
                return False  # stop listener

    print(f"Please click {num_clicks} times to measure intervals...")
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

    # compute intervals between consecutive clicks
    intervals = [click_times[i+1] - click_times[i] for i in range(len(click_times)-1)]
    return intervals

if __name__ == "__main__":
    print("Click 1 for record, 2 to input a melody or 3 to measure an interval: ")
    num = int(input())
    if num == 1:
        record_points()
    elif num == 2:
        points = load_points(POINTS_FILE)
        melody = input("Which melody should i play? (1-13): ")
        match melody:
            case "8":
                sequence= "602345602020887034567020208850865434954323943212"
                interval = 0.102
            case "9":
                sequence = ""
                interval = 0.1
            case __:
                #sequence = input("Enter rhythm (use 1–7 for points, 0 for rest, 8 for little more pause, 9 for some less pause): ").strip()
                sequence = ("706054004030210045005600670077654044321357").strip()
                interval = input(f"Interval per step in seconds (default {DEFAULT_INTERVAL}): ").strip()
                interval = float(interval) if interval else DEFAULT_INTERVAL
        play_melody(sequence, points, interval)
    elif num == 3:
        # Example usage
        intervals = measure_click_intervals()
        for i, t in enumerate(intervals):
            print(f"Interval {i+1}: {t:.3f} seconds")
    else:
        print("rtfm")
