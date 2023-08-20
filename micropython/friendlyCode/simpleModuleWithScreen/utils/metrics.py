class Metrics:
    def __init__(self):
        pass
    
    @staticmethod
    def get_average(iterator: iter) -> float:
        """
            Returns the average of the iterator
        """
        return sum(iterator) / len(iterator)

    @staticmethod
    def get_variance(iterator: iter) -> float:
        """
            Returns the variance of the iterator
        """
        average = Metrics.get_average(iterator)
        return sum((x - average)**2 for x in iterator) / len(iterator)