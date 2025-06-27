import TileController

with TileController.TileController("/dev/tty.usbmodem101") as tc:
    print(tc.read_width())
    print(tc.read_height())
    print(tc.read_address_list())
    print(tc.scan_addresses())

    tc.blinkall_start()
    input("Press Enter to stop blinking")
    tc.blinkall_stop()