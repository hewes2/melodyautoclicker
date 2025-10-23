import pyautogui
import json
import time

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

def play_melody(sequence, points, interval=DEFAULT_INTERVAL):
    print(f"\nStarting melody in 3 seconds... switch to your target window now!")
    time.sleep(3)

    for i, symbol in enumerate(sequence):
        if symbol == "0":
            print(f"Step {i+1}: rest (no click)")
            time.sleep(interval)
            continue
        else:
            index = int(symbol) - 1
            if 0 <= index < len(points):
                x, y = points[index]["x"], points[index]["y"]
                print(f"Step {i+1}: clicking point {symbol} at ({x}, {y})")
                pyautogui.moveTo(x, y, duration=0.1)  # visible move
                pyautogui.click()
            else:
                print(f"Step {i+1}: invalid point {symbol}")
        time.sleep(interval)

if __name__ == "__main__":
    print("Click 1 for record or 2 to input a melody: ")
    num = int(input())
    if num == 1:
        record_points()
    elif num == 2:
        points = load_points(POINTS_FILE)
        sequence = input("Enter rhythm (use 1–7 for points, 0 for rest): ").strip()
        interval = input(f"Interval per step in seconds (default {DEFAULT_INTERVAL}): ").strip()
        interval = float(interval) if interval else DEFAULT_INTERVAL
        play_melody(sequence, points, interval)
    else:
        print("rtfm")
