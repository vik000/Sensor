# Pipeline 
This project is built of 2 parts, set into 2 different directories.
- AA_Gen: This simulates the sensor data flowing in. It is in the form of a websocket.
- BB_Reader: This is a more complex project. It consists of a client file that constantly reads from the websocket. It uses a worker class that is initialised through a thread. Each worker carries the data and prepares it for Db Storage. 

The first simulates a Sensor giving readings and sending them over a websocket.
The second is a data processing pipeline.

## Getting Started
This project is built on python 3.7. For all cases, when using python or pip, you may read python3 or pip3. 
This project requires to have Redis installed in your machine. Make sure you install it first. If you have a mac, you may do so using homebrew:
`brew install redis`
Once you have cloned the project, install the dependencies as usual
`pip install -r requirements.txt` 

### Running the project:
0. Make sure you have Redis running. You may start it by running `redis-server`
1. Make sure you are in the right environment, normally `source venv/bin/activate` if you are on a mac.

***The generator and the reader have to be run independently:***
1. Get inside the 01_Gen folder and execute the program:
`python server.py`
2. Now get inside the 02_Reader folder and run:
`python client.py`

Once it's running you will see the connection established in the console running the server, and the data stored in the client console. A logging file should have appeared under the name: logs.log (no sweating with name choosing). 

Finally, you may check the DB for files.
Open a new console and enter
`redis-cli`
now enter
`keys *`
a list of uuids should appear.
Copy one (without the "")
Now enter:
`hget uuid time_of_measurement`, uuid being the copied value.
You should get the time the measurement was taken.

This is a list of the fields you can access instead of time_of_measurement:
- id
- type
- time_of_measurement
- temperature_f
- temperature_c

## Running the tests
`python -m pytest launch_tests.py`

