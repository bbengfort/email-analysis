#!/usr/bin/env python

import time
import random

Z = 208314

def crashed(num, Z=Z):
    return num >= Z

def search(Z=Z, factor=10, verbose=True):
    """
    Finds the number you're looking for.
    """

    # Initialize internal variables
    steps  = []
    index  = 1
    prev   = 0
    high   = 0
    start  = time.time()

    # Begin the search algorithm
    while True:
        steps.append(index) # Increment the number of steps
        try:
            # Does our current number crash us?
            if not crashed(index, Z):
                if verbose: print "%i UP!" % index
                prev = index # Save the previous state
                if high:
                    # Go halfway towards our bounding space
                    index = (index + high) / 2
                else:
                    # Improve exponentially to quickly find bounding space
                    index *= factor

            # We've seen a crash, the number is behind us.
            else:
                high = index # Save the highest seen bounding space
                if verbose: print "%i CRASHED!" % (index)

                # Go back half-way
                index = (index + prev) / 2

                # Termination condition
                if index <= prev:
                    if verbose: print "FOUND %i!" % (index)
                    break

            # Make it readable for humans
            if verbose: time.sleep(0.33)

        except KeyboardInterrupt:
            # Quit if requested
            break

    finit = time.time()
    delta = finit - start
    if verbose: print "Took %0.4f seconds and %i steps" % (delta, steps)
    return index, delta, steps

def test(numtests=2, factor=1000, start=2e4, end=2e7):
    results = []
    start_time = time.time()
    for i in xrange(numtests):
        z = random.randint(start, end)
        results.append(search(z, factor, False))
    finit = time.time()
    delta = finit - start_time

    steps = sum(len(x[2]) for x in results) / float(len(results))
    timed = sum(x[1] for x in results) / float(len(results))

    output = (
        "Max bound algorithm for %i tests with a factor of %i\n"
        "and a bound range of %i to %i\n"
        "took an average of %0.8f seconds and %i steps\n"
        "testing took %0.8f seconds"
    )

    print output % (numtests, factor, start, end, timed, steps, delta)

def visualize(z=None, factor=1000):
    import numpy as np
    import matplotlib.pyplot as plt

    z = z if z else random.randint(2e4, 2e7)
    index, delta, steps = search(z, factor, False)
    plt.plot(steps)
    plt.show()

if __name__ == '__main__':
    visualize()
