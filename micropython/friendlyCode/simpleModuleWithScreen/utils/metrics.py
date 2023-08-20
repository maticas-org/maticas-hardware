class Metrics:
    def __init__(self):
        pass
    
    @staticmethod
    def get_average(iterator: iter) -> float:
        """
            Returns the average of the iterator
        """
        n = 0
        for x in iterator:
            n += 1
        return sum(iterator) / n

    @staticmethod
    def get_variance(iterator: iter) -> float:
        """
            Returns the variance of the iterator
        """
        n = 0
        for x in iterator:
            n += 1
        average = Metrics.get_average(iterator)
        return sum((x - average)**2 for x in iterator) / n