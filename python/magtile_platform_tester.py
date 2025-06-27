from TileController import TileController
import time
import signal
import sys

# Global variable to store the controller
controller = None

def signal_handler(sig, frame):
    print('\nKeyboard interrupt received. Cleaning up...')
    if controller:
        turn_off_all_test_leds(controller)
        turn_off_all_coils(controller)
    sys.exit(0)

def snake_pattern_test(controller, delay_time=0.25):
    # Read the width and height
    width = controller.read_width()
    height = controller.read_height()
    
    print(f"Array dimensions: {width}x{height}")
    
    # Define the maximum power level
    max_power = 4095
    
    # Iterate through the coils in a snaking pattern
    for row in range(height * 3):
        # Determine the direction for this row
        if row % 2 == 0:
            col_range = range(width * 3)
        else:
            col_range = range(width * 3 - 1, -1, -1)
        
        for col in col_range:
            print(f"Activating coil at ({row}, {col})")
            
            # Turn on the coil
            controller.set_power(row, col, max_power)
            
            # Wait for the specified delay time
            # time.sleep(delay_time)
            input("Press Enter to continue")
            # input("", end='')  # Wait for user input to continue
            
            # Turn off the coil
            controller.set_power(row, col, 0)
            
    print("Test completed")

def turn_on_all_test_leds(controller):
    print("Turning on all test LEDs...")
    addresses = controller.read_address_list()
    for address in addresses:
        try:
            controller.test_led_enable(address)
            # print(f"Enabled test LED at address {address}")
        except ValueError as e:
            print(f"Failed to enable test LED at address {address}: {e}")
    print("All test LEDs should now be on")

def turn_off_all_test_leds(controller):
    print("Turning off all test LEDs...")
    addresses = controller.read_address_list()
    for address in addresses:
        try:
            controller.test_led_disable(address)
            # print(f"Disabled test LED at address {address}")
        except ValueError as e:
            print(f"Failed to disable test LED at address {address}: {e}")
    print("All test LEDs should now be off")

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

# Main execution
if __name__ == "__main__":
    # Replace '/dev/tty.usbmodem101' with the appropriate port for your Arduino
    # port = '/dev/tty.usbmodem1101'
    port = '/dev/cu.usbmodem1301'

    print(f"Connecting to MagTile1 controller on port: {port}")
    
    # Set up the signal handler for keyboard interrupt
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        with TileController(port) as controller:
            # Store the controller in the global variable
            globals()['controller'] = controller
            
            print("Turning on test LEDs")
            turn_on_all_test_leds(controller)
            print("All coils will be tested one by one. Ensure each coil is working by monitoring the power supply current or using a magnet to feel the force from the coil.")
            input("Press Enter to begin")
            print("Starting snake pattern test...")
            snake_pattern_test(controller)
            print("Turning off test LEDs")
            turn_off_all_test_leds(controller)
    except Exception as e:
        print(f"An error occurred: {e}")
        if controller:
            turn_off_all_test_leds(controller)
            turn_off_all_coils(controller)
    finally:
        # Reset the global controller variable
        globals()['controller'] = None