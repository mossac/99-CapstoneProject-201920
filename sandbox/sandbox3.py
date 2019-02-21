# Put whatever you want in this module and do whatever you want with it.
# It exists here as a place where you can "try out" things without harm.

# James Kelley

import rosebot
import random

note = 600

while True:
    mono = random.randint(0, 2020)
    if mono > note:
        break
    print(mono)

print(mono, note)
