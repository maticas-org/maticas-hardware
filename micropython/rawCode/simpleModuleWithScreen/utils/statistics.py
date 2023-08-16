class Statistics:
    def __init__(self, max_measurements=100, minutes_between_measurements=1):
        self.measurements = []
        self.max_measurements = max_measurements
        self.minutes_between_measurements = minutes_between_measurements

    def add_measurement(self, measurement):
        if len(self.measurements) >= self.max_measurements:
            self.measurements.pop(0)
        self.measurements.append(int(round(measurement)))# cast to save memory
    
    def _last_x_minutes_generator(self, minutes):
        now = len(self.measurements) - 1
        start_index = now - minutes + 1 if now >= minutes - 1 else 0
        
        for i in range(start_index, now + 1):
            yield self.measurements[i]
    
    def get_average(self):
        if not self.measurements:
            return -1
        return sum(self.measurements)/len(self.measurements)
    
    def get_last_measurement(self):
        if not self.measurements:
            return -1
        return self.measurements[-1]
    
    def get_average_of_last_x_hours(self, hours):
        minutes = int(hours * 60)

        if not self.measurements:
            return -1
        
        last_x_minutes_data = self._last_x_minutes_generator(minutes)
        return sum(last_x_minutes_data) / minutes