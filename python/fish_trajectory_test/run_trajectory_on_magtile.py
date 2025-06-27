import time
import csv
import signal
import sys
from TileController import TileController

# === Config ===
CSV_FILENAME = "trajectory.csv"
GRID_ROWS = 15
GRID_COLS = 15
POWER_LEVEL = 4095
STEP_DELAY = 0.3  # seconds between steps
PORT = "/dev/cu.usbmodem1301"     # change as needed

def load_indices(filename):
    indices = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            for cell in row:
                cell = cell.strip()
                if cell:
                    indices.append(int(cell))
    return indices

def index_to_coord(index, cols):
    return divmod(index-1, cols)

def turn_off_all_coils(controller):
    print("Turning off all coils...")
    width = controller.read_width()
    height = controller.read_height()
    for row in range(height * 3):
        for col in range(width * 3):
            try:
                controller.set_power(row, col, 0)
                # print(f"Turned off coil at ({row}, {col})")
            except ValueError as e:
                print(f"Failed to turn off coil at ({row}, {col}): {e}")
    print("All coils should now be off")

def print_grid(current_row, current_col, next_row, next_col, rows, cols):
    """Prints a grid with the current (red) and next (green) positions marked."""
    for r in range(rows):
        row_str = ""
        for c in range(cols):
            if r == current_row and c == current_col:
                row_str += " \033[31mX\033[0m"  # Red X for current
            elif r == next_row and c == next_col:
                row_str += " \033[32mO\033[0m"  # Green O for next
            else:
                row_str += " ."
        print(row_str)
    print("\n" + "-" * (cols * 2))

def run_trajectory(controller, indices, grid_cols):
    for i, index in enumerate(indices):
        row, col = index_to_coord(index, grid_cols)
        if i + 1 < len(indices):
            next_row, next_col = index_to_coord(indices[i + 1], grid_cols)
        else:
            next_row, next_col = -1, -1  # No next position
        print("\033c", end="")  # Clear screen (ANSI escape code)
        print(f"[{i+1}/{len(indices)}] Activating ({row}, {col})")
        print_grid(row, col, next_row, next_col, GRID_ROWS, GRID_COLS)
        controller.set_power(row, col, POWER_LEVEL)
        time.sleep(STEP_DELAY)
        # input("Press Enter to continue...")
        controller.set_power(row, col, 0)
    print("Trajectory complete.")

def turn_on_all_test_leds(controller):
    print("Turning on all test LEDs...")
    addresses = controller.read_address_list()
    for address in addresses:
        try:
            controller.test_led_enable(address)
        except ValueError as e:
            print(f"Failed to enable test LED at address {address}: {e}")
    print("All test LEDs should now be on")

def turn_off_all_test_leds(controller):
    print("Turning off all test LEDs...")
    addresses = controller.read_address_list()
    for address in addresses:
        try:
            controller.test_led_disable(address)
        except ValueError as e:
            print(f"Failed to disable test LED at address {address}: {e}")
    print("All test LEDs should now be off")

if __name__ == "__main__":
    try:
        with TileController(PORT) as controller:
            print("Connected to controller.")
            turn_on_all_test_leds(controller)
            indices = load_indices(CSV_FILENAME)

            try:
                run_trajectory(controller, indices, GRID_COLS)
            except KeyboardInterrupt:
                print("\nInterrupted. Cleaning up...")
            except Exception as e:
                print(f"Error during trajectory execution: {e}")
            finally:
                # Always clean up
                turn_off_all_coils(controller)
                turn_off_all_test_leds(controller)

    except Exception as e:
        print(f"Fatal error: {e}")
