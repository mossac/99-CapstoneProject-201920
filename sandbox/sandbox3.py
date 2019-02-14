# Put whatever you want in this module and do whatever you want with it.
# It exists here as a place where you can "try out" things without harm.

# James Kelley

# out 16 inches
# distance needed--0 inch

# at 16 inches--1 hz
# at 8 inches--2 hz
# at 4 inches--4 hz
# at 2 inches--8 hz

while True:

    starting_distance = self.robot.sensor.ir.get()

    initial = 1

    while True:
        rate = (starting_distance / dist) * increase
        print(rate)
