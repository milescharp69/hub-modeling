import pandas as pd
import quantities as pq

class Port:
    def __init__(self, Port_kW, Port_Efficiency=.975):
        self.Port_kW = Port_kW
        self.Port_Efficiency = Port_Efficiency

        self.status = True  # Port not being used
        self.open_date = None

        #TODO: Improve this Dont give the keys :/ bad code >:C
        self.time_usage = {
            "Class 1-2": pd.Timedelta(days=0),
            "Class 3-6": pd.Timedelta(days=0),
            "Class 7-8": pd.Timedelta(days=0)
        }

        self.time_free = pd.Timedelta(days=0)

    def __add__(self, other_port):
        """
        Add ports together combines the self.time_usage dictionary and the self.time_free
        :param other_port:
        :return:
        """
        #TODO add an assert if the port are not the same
        for key in self.time_usage.keys():
            self.time_usage[key] += other_port.time_usage[key]

        self.time_free += other_port.time_free

    def usage_percent(self):
        #Do we really need the time_free though prob not
        #TODO: add time_free later to double check this stuff works
        #TODO: Improve this vectorize it
        total_time = self.time_free
        for vehicle in self.time_usage.keys():
            total_time += self.time_usage[vehicle]

        port_percent_dict = {}
        for vehicle in self.time_usage.keys():
            port_percent_dict[vehicle] = self.time_usage[vehicle] / total_time
        return pd.DataFrame([port_percent_dict])

    def datatext(self):
        return self.Port_kW


# test1 = Port(pq.Quantity(150, 'kW'))
# print(test1.Port_kW)
# test2 = Port(pq.Quantity(150, 'kW'))
# test2.time_usage["Class 1-2"] += pd.Timedelta(days=1)
#
# test1 + test2
# print(test1.time_usage)

#Should I find the time_usage for a port ca



