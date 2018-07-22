# demeter-flask

Backend component of Demeter. Written in Python 3 and Flask.

## Contributing

### Setup the environment
Create a virtual environment to store all of the project requirements. Python 3 is tested and recommended.
```bash
# Create a venv
$ python3 -m venv demeter
$ source demeter/bin/activate
# Update pip to the latest version
(demeter)$ pip install --upgrade pip

# Change directories to the project directory
(demeter)$ cd <path-to-project>/demeter-flask
# Download dependencies for PyPI using pip
(demeter)$ pip install -r requirements.txt
```

### Run unit tests
```bash
# In root directory of the project
(demeter)$ python -m unittest tests
```
