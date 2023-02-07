# Base image
FROM python:3.10.9-alpine3.16

# Set some default args for app home & user account
ARG APP_HOME=/app
ARG user=testuser

# Set the working directory
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