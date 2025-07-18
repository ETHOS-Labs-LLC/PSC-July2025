import time
import board
import digitalio
import busio
from adafruit_rfm9x import RFM9x

# Initialize SPI bus
spi = busio.SPI(clock=board.GP10, MOSI=board.GP11, MISO=board.GP12)

# Initialize RFM95 LoRa
rfm95_cs = digitalio.DigitalInOut(board.GP5)
rfm95_reset = digitalio.DigitalInOut(board.GP6)

# LED for indicating activity
led = digitalio.DigitalInOut(board.GP3)
led.direction = digitalio.Direction.OUTPUT

# Function to blink LED
def blink_led(led, duration=0.1):
    led.value = True
    time.sleep(duration)
    led.value = False

# Get user input for frequency
try:
    frequency = float(input("Enter the frequency (902.0-928.9 MHz): "))
    if not (902 <= frequency <= 928):
        raise ValueError("Frequency must be between 902.0 and 928.9 MHz.")
except ValueError as e:
    print(f"Invalid frequency input: {e}")
    exit()

# Initialize RFM95 radio with the given frequency
try:
    rfm95 = RFM9x(spi, rfm95_cs, rfm95_reset, frequency)
    print(f"RFM95 initialized at {frequency} MHz")
except Exception as e:
    print(f"Failed to initialize RFM95: {e}")
    exit()

# Function to listen for packets
def listen_for_packets(radio, address, timeout=2):
    print(f"Listening on address {address} for {timeout} seconds...")
    radio.node = address  # Set the node address
    start_time = time.time()
    while time.time() - start_time < timeout:
        packet = radio.receive()
        if packet:
            try:
                # Decode and print the received packet
                data = packet.decode("utf-8")
                print(f"Received packet: {data} from address {packet[0]}")
            except Exception as e:
                print(f"Error decoding packet: {e}")
        time.sleep(0.1)  # Prevent CPU hogging

# Iterate through all possible node addresses (0-254)
for address in range(255):
    try:
        listen_for_packets(rfm95, address)
    except Exception as e:
        print(f"Error while listening on address {address}: {e}")
    blink_led(led, 0.2)
    time.sleep(0.5)  # Brief pause before moving to the next address

print("Brute force operation complete.")


