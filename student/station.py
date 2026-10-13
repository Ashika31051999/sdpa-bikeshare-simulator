class Station:
    def __init__(self, station_id, name, capacity, current_bikes):
        if capacity < 0 or current_bikes < 0 or current_bikes > capacity:
            raise ValueError("Invalid capacity or bike constraints configuration.")
        self.id = str(station_id)
        self.name = str(name)
        self.capacity = int(capacity)
        self.bikes = int(current_bikes)

    def free_docks(self):
        return self.capacity - self.bikes

    def copy(self):
        return Station(self.id, self.name, self.capacity, self.bikes)
