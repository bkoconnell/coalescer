##########################
# ----- TEST STAGE ----- #
##########################
# Base image
FROM python:3.10.9-alpine3.16 as test
WORKDIR /test
COPY . .
# Install dependencies
RUN pip3 install -r requirements.txt
# Execute unit tests
ENTRYPOINT [ "./unit_test.py" ]

#########################
# ----- APP STAGE ----- #
#########################
# Base image
FROM python:3.10.9-alpine3.16 as app
ARG APP_HOME=/app
ARG user=testuser
WORKDIR ${APP_HOME}
# Get latest packages and add new "testuser" account
RUN apk update && apk upgrade \
 && addgroup -S ${user} && adduser -S ${user} -G ${user}
# Switch to "testuser", copy files, and change workdir ownership
ENV USER=${user}
COPY --chown=${user} . .
# Set default executable with command line args (input & output filepaths)
ENTRYPOINT [ "./main.py" ]
CMD [ "test_files/input_data.csv", "data/solution_output.csv" ]