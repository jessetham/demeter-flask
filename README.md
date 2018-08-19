# Sensor Vault

Flask backend to receive, store, and retrieve information from IOT sensors. Written in Python 3 and Flask.

## Contributing

### Setup the environment
Create a virtual environment to store all of the project requirements. Python 3 is tested and recommended.
```bash
# Create a venv
$ python3 -m venv sensorvault
$ source sensorvault/bin/activate
# Update pip to the latest version
(sensorvault)$ pip install --upgrade pip

# Change directories to the project directory
(sensorvault)$ cd <path-to-project>/sensorvault
# Download dependencies for PyPI using pip
(sensorvault)$ pip install -r requirements.txt
```

### Run unit tests
```bash
# In root directory of the project
(sensorvault)$ python -m unittest tests
```
