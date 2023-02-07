# coalescer

Make sure you have Docker installed.

Then you can simply clone this repository and run build.sh

This project had several requirements from the "customer":
    (1) Dockerfile must udpate packages, create a new user, and run the app as the new user.
    (2) Docker image must have minimal layers and be as small as possible.
    (3) Create a bash/sh script to build the image and run the container to:
            a) process the input data.
            b) write the solution output data.
    (4) Application must parse input data and process it as follows:
            a) combine subnets on each line into least amount of possible subnets.
            b) format invalid data & coalesced data accordingly.
            c) the output solution file (solution_output.csv) must be identical to the sample_output.csv in the data directory.

NOTE: a 'format' spec was not provided to me ... instead, a sample output file was given with corresponding input data to check that my program would correctly format the data per the sample. Hence requirement (4)c.

Unit tests were added as a bonus, which are run in the build script prior to creating the Docker image.

When you run the build.sh script it will build the image, run the container & application, process the input data, and write/overwrite the 'solution_output.csv' file. Check the diff between 'solution_output.csv' and 'sample_output.csv' (there should be no diff...).

Feel free to manually run main.py (remember to pass the required args! see Dockerfile CMD) if you want to debug through the code and review my parsing logic, data formatting & subnet coalescing logic, or any of the common functions which include customized exception handling, bit manipulation, binary math, IPv4/Mask/CIDR conversions, and so on...


Why did I use Python's Alpine Linux image?
--> Because of requirement #2 (smallest possible image).
    Python's "Bullseye-slim" has better performance for building the image,
    but performance is not listed as a requirement whereas image size explicitly is.
    The size savings from Bullseye-slim to Alpine was about 80MB (roughly 60% decrease).