from .abstractions.event         import *
from .abstractions.subscriber    import Subscriber
from .data_storage  import DataBase
from .api_client    import ApiClient

class DataManagementMicroService(Subscriber):

    def __init__(self,
                 config_file: str,
                 database_name: str = "data.jsonl"):

        self.last_measurement_event: EventList = None
        self.last_connection_event: Event      = None
        self.database: DataBase = DataBase(database_name)
        self.api_client: ApiClient = ApiClient(config_file)

        print("Initialized DataManagementMicroService.")

    #----------------- Subscriber interface -----------------#
    def update(self, event: Event):
        print('\nDataManagementMicroService got event: "{}"'.format(event))

        if isinstance(event, EventList):
            self.last_measurement_event = event
            self.main()
        elif isinstance(event, Event):
            self.last_connection_event = event
            self.main()
        else:
            raise TypeError('Cannot handle event {} of type {}'.format(event, type(event)))

    #----------------- Business logic -----------------#
    def main(self):
        print('DataManagementMicroService running business logic...')

        if (self.last_measurement_event == None) or (self.last_connection_event == None):
            return None

        if self.last_connection_event.status_code == OK_STATUS:
            print('DataManagementMicroService sending data to cloud...')
            self.send_stored_data()
            self.send_allocated_data()

        else:
            print('DataManagementMicroService storing data locally...')
            self.store_data()

    
    def send_stored_data(self,
                         threshold: int = 10):

        print('DataManagementMicroService sending stored data to cloud...')
        #check if there is data stored locally.
        
        #if there is, send it to the cloud and delete it from the local storage
        #if there isn't, do nothing
        succesfully_sent_data = []
        count = 0

        try:
            for data in self.database.read_file():
                
                if count < threshold:
                    self.api_client.send_data(data)
                    succesfully_sent_data.append(data)
                    count += 1
                else:
                    break

        #if it fails, raise exception
        except Exception as e:
            
            #if it managed to send some data, before failing to send the rest
            #delete the succesfully_sent_data from the local storage
            if count > 0:
                self.database.rewrite_file(remove_data = succesfully_sent_data)

            raise e
        
        #if it succeeds, delete the succesfully_sent_data from the local storage
        #so it doesn't get sent again
        else:
            if count > 0:
                self.database.rewrite_file(remove_data = succesfully_sent_data)

    def send_allocated_data(self):
        print('DataManagementMicroService sending allocated data to cloud...')
        if self.last_measurement_event == None:
            return None

        #try to send data to cloud
        #if it fails, store data locally

        succesfully_sent_data = []
        count = 0

        try:
            
            for measurement_event in self.last_measurement_event:
                self.api_client.send_data(measurement_event.data)
                succesfully_sent_data.append(measurement_event.data)
                count += 1

        #if it did not managed to send all the data, store the
        #remaining data locally
        except Exception as e:

            unsent_data = []

            for measurement_event in self.last_measurement_event:
                if measurement_event.data not in succesfully_sent_data:
                    unsent_data.append(measurement_event.data)

            #if it fails to store the data locally, raise exception
            try:
                for data in unsent_data:
                    self.database.write_file(data)
            except Exception as e:
                raise e
        
        #if it succeeds, delete the last_measurement_event, so it doesn't get stored or
        #sent again
        else:
            self.last_measurement_event = None

    def store_data(self):

        print('DataManagementMicroService storing data locally...')
        if self.last_measurement_event == None:
            return None
        
        #try to store data locally
        try:
            
            for measurement_event in self.last_measurement_event:
                self.database.write_file(measurement_event.data)
        
        #if it fails, raise exception
        except Exception as e:
            raise e

        #if it succeeds, delete the last_measurement_event, so it doesn't get stored again
        else:
            self.last_measurement_event = None