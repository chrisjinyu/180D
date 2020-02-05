import board
import neopixel
import time

pixels = neopixel.NeoPixel(board.D18, 12)
pixels.fill((255, 255, 255))

try:
    while True:
        pixels.fill((255,0,0))
        time.sleep(0.5)
        pixels.fill((0,255,0))
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nCleaning up")
    pixels.fill((0,0,0))
