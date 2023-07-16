# coalescer
Make sure you have `Docker` installed. Then you can simply clone this repository and run the `./build.sh` script in your Linux terminal. This program does not have a Windows or Mac version.

NOTE: This program has only been tested using Docker on Debian distros. Other container tools like Podman may experience issues, namely with 'Write' permissions for the output solution. Not all Linux distros have been tested, but Debian distros appear to work as intended.

______________________________________________________________________________________

This project had several requirements from the "customer":

    (1) Dockerfile must udpate packages, create a new user, and allow the app to be run by the new user.
    
    (2) Docker image must have minimal layers and be as small as possible.
    
    (3) Create a bash/sh script to build the image and run the container for:
    
            a) processing the input data.
            
            b) writing the solution output datafile.
            
    (4) Application must parse input data and process it as follows:
    
            a) combine subnets on each line into least amount of possible subnets.
            
            b) format invalid data & coalesced data accordingly.
            
            c) the output solution (`solution_output.csv`) must be identical to the `sample_output.csv` which can be found in the `test_files` directory.
            

__NOTE:__ A format spec was not provided to me. Instead, I was given the input CSV file and a sample output CSV file to validate that my program correctly formats the data per the sample; hence requirement (4)c.

Unit tests were added as a bonus, which are run in the build script prior to creating the App docker image.

When you run the `build.sh` script it will build the Test image and execute the unit tests inside the container. Then it will:
- build the App image
- run the App container with a mounted data volume (*coalescer/output* directory for persistent data from container's *app/data* directory)
- start the Coalescer app
- process the input data
- write/overwrite the `solution_output.csv` file.

Check the diff between `output/solution_output.csv` and `test_files/sample_output.csv` (there should be no diff...).

Feel free to manually run `main.py` _(remember to pass the required args! ...see the Dockerfile's `CMD`)_ if you want to debug the code and review my parsing logic, data formatting & subnet coalescing logic, or any of the common functions which include customized exception handling, bit manipulation, binary math, IPv4/Mask/CIDR conversions, and so on...

______________________________________________________________________________________

Why did I use Python's _Alpine_ Linux image? Because of requirement #2 (smallest possible image!)

Python's _Bullseye-slim_ has better performance for building the image,
but performance is not listed as a requirement and image size is.

The savings in size from _Bullseye-slim_ to _Alpine_ was about **80MB** (roughly 60% decrease in size).