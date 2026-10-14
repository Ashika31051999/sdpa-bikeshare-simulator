# SDPA Formative Coursework - Bike-Share Simulator

This is a text-based Python simulation of a small city bike-sharing scheme with three stations (Temple Meads, Harbourside, and Clifton). It runs day-by-day in the terminal, processing van moves, repairs, and daily commuter trips.

## Project Files
* `main.py` - The main file that runs the text menus and asks for user input.
* `student/rules.py` - Functions for parsing integers, converting pence to pounds, and calculating trip stats.
* `student/station.py` - The Station class that tracks bike counts and capacities.
* `student/bikeshare.py` - The BikeShare class that manages the daily simulation steps and finances.

## How to Run the Program
To start the simulator, run this command in your terminal:
python main.py

## How to Run the Tests
To run all the public and student unit tests together, use:
python -m unittest discover -s tests