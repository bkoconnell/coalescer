# Base image for running unit tests
FROM python:3.10.9-alpine3.16 as test
WORKDIR /test
COPY . .
RUN pip3 install -r requirements.txt
ENTRYPOINT [ "./unit_test.py" ]

# Base image for Coalescer app
FROM python:3.10.9-alpine3.16 as app
ARG APP_HOME=/app
ARG user=testuser
WORKDIR ${APP_HOME}
# Get latest packages and add new "test" user account
RUN apk update && apk upgrade \
 && addgroup -S ${user} && adduser -S ${user} -G ${user}
# Switch to "testuser" account and change directory owner
ENV USER=${user}
COPY --chown=${user} . .
# Set default executable with command line args (input file & output file paths)
ENTRYPOINT [ "./main.py" ]
CMD [ "./data/input_data.csv", "./data/solution_output.csv" ]