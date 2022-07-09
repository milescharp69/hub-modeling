from Port import Port
from VehicleClass import VehicleClass
import numpy as np
import quantities as pq
import pandas as pd
import collections
import timeit

# Global Variables
OPERATION_HOURS = pq.Quantity(24, 'hour')
NOTIONAL_HOURS = pq.Quantity([15, 9], 'hour')


class Session:
    def __init__(self, hub, current_time):
        self.start_time = current_time

        self.vehicle = np.random.choice(hub.vehicle_classes, 1, p=hub.vehicle_mix)[0]
        port_weight = hub.port_weights(self.vehicle)
        self.port_weight = port_weight

        if np.sum(port_weight) != 1:
            self.status = False
        else:
            self.status = True
            self.port_used = np.random.choice(hub.hub_ports, 1, p=hub.port_weights(self.vehicle))[0]

            # Remove the port from the list of ports in the hub
            hub.ports_used.append(hub.hub_ports.pop(hub.hub_ports.index(self.port_used)))
            #TODO: Enable Charging Profile

            # Charging Profile

            # Enable Charging Profile
            # self.charge_profile = np.random.choice([.60, .80], 1, p=[.5, .5])[0]

            # Calculation
            # Base = .10-60 = .5 or .10-.80 =.7

            # self.consumption = float(((self.vehicle.monthly_consumption()).rescale('(kW * hour) / week') * (
            #             self.charge_profile - 0.2) * pq.week).rescale('kW * hour').magnitude)

            self.consumption = float((self.vehicle.consumption()).magnitude)

            #Adjust power/ charge_time depending of the charging profile

            self.power = self.port_used.Port_kW.magnitude

            self.charge_time = float(pq.Quantity(self.consumption / self.power, 'hour').rescale('second').magnitude)

            # Rounded time
            self.port_used.open_date = pd.Timestamp(current_time.timestamp() + self.charge_time, unit='s').ceil(
                freq='5T')
            self.end_time = self.port_used.open_date
            self.port_used.time_usage[self.vehicle.className] += abs(self.end_time - self.start_time)
            # Disable port
            self.port_used.status = False

class Hub:
    def __init__(self, hub_id, usage_factor, hub_ports, vehicle_mix, vehicle_classes) -> None:
        """
        Constructor to generate a hub object
        :param hub_id: string    Name for hub object
        :param usage_factor:
        :param hub_ports:
        :param vehicle_mix:
        :param vehicle_classes:
        """
        self.hub_id = hub_id
        self.usage_factor = usage_factor  # [7A-10P,10P-7A]
        self.hub_ports = hub_ports
        self.vehicle_mix = vehicle_mix
        self.vehicle_classes = vehicle_classes
        self.total_ports = len(self.hub_ports)

        #Types of Ports
        self.port_types = {}
        for port in self.hub_ports:
            if float(port.Port_kW.magnitude) not in self.port_types.keys():
                self.port_types[float(port.Port_kW.magnitude)] = 1
            else:
                self.port_types[float(port.Port_kW.magnitude)] += 1

        self.ports_used = []
        #TODO:compare and rewrite this do for port in the port list
        peak = 0
        for i in range(0, len(self.hub_ports)):
            peak += (self.hub_ports[i].Port_kW.rescale('kW')).magnitude * self.hub_ports[i].Port_Efficiency
        self.peak_load = pq.Quantity(peak, 'kW')

    def port_weights(self, vehicle):
        """

        :param vehicle:
        :return:
        """
        weights = []

        #TODO: Improve
        #Add co
        types_of_ports = [Port(pq.Quantity(1000, 'kW')), Port(pq.Quantity(350, 'kW')), Port(pq.Quantity(300, 'kW')),
                          Port(pq.Quantity(150, 'kW'))]

        # Shuffle Ports around to induce more variability

        np.random.shuffle(self.hub_ports)

        temp = True
        if vehicle.Veh_Class == 2:
            if 1000.0 in self.port_types.keys():
                # Class 7-8 will not use 150 ports
                for a in types_of_ports[0:2]:
                    if a.Port_kW in [self.hub_ports[n].Port_kW for n in range(len(self.hub_ports))]:
                        for port in self.hub_ports:
                            if port.Port_kW == a.Port_kW and temp:
                                weights.append(1)
                                temp = False
                            else:
                                weights.append(0)
                        return weights
            else:
                for a in types_of_ports:
                    if a.Port_kW in [self.hub_ports[n].Port_kW for n in range(len(self.hub_ports))]:
                        for port in self.hub_ports:
                            if port.Port_kW == a.Port_kW and temp:
                                weights.append(1)
                                temp = False
                            else:
                                weights.append(0)
                        return weights
            return None

        elif vehicle.Veh_Class == 1:
            for a in types_of_ports[1:]:
                if a.Port_kW in [self.hub_ports[n].Port_kW for n in range(len(self.hub_ports))]:
                    for port in self.hub_ports:
                        if port.Port_kW == a.Port_kW and temp:
                            weights.append(1)
                            temp = False
                        else:
                            weights.append(0)
                    return weights
            return None

        else:
            for a in types_of_ports[2:]:
                if a.Port_kW in [self.hub_ports[n].Port_kW for n in range(len(self.hub_ports))]:
                    for port in self.hub_ports:
                        if port.Port_kW == a.Port_kW and temp:
                            weights.append(1)
                            temp = False
                        else:
                            weights.append(0)
                    return weights
            return None

    def check_port_status(self, current_date):
        """
        Opens ports back up if the date is same as the given open_date
        :param current_date:
        """
        for port in self.ports_used:
            # TODO: Compare and fix this
            if current_date >= port.open_date:
                # Open the port back up
                port.status = True
                port.open_date = None
                self.hub_ports.append(self.ports_used.pop(self.ports_used.index(port)))

    def current_power(self):
        return np.sum([float(port.Port_kW.magnitude) for port in self.ports_used])


    def simulate_hub_data(self, end_date):
        """

        :param end_date:
        :return: Pandas DataFrame containing a list of vehicles using the hub at a given time
        """

        date_range = pd.date_range(start='1/1/2022', end=end_date, freq='5T')
        df = pd.DataFrame()
        df['Index'] = []
        df['Vehicle'] = []
        df['Sessions'] = []
        df['Consumption'] = []
        power_list = []
        previous_date = False
        for date in date_range:
            self.check_port_status(date)  # Refreshes Hub ports
            if (7 <= date.hour < 22) and date.minute % 30 == 0:
                for port in self.hub_ports:
                    if np.random.choice([True, False], 1, p=[self.usage_factor[0], 1 - self.usage_factor[0]])[0]:
                        sub_session = Session(self, date)
                        if sub_session.status:
                            df_temp = pd.DataFrame(
                                data={
                                    'Index': [date],
                                    'Vehicle': [sub_session.vehicle.className],
                                    'Sessions': [1],
                                    'Consumption': [sub_session.consumption]
                                }
                            )
                            df = pd.concat([df, df_temp], ignore_index=True)
            elif (date.hour < 7 or date.hour >= 22) and date.minute % 30 == 0:
                for port in self.hub_ports:
                    if np.random.choice([True, False], 1, p=[self.usage_factor[1], 1 - self.usage_factor[1]])[0]:
                        sub_session = Session(self, date)
                        if sub_session.status:
                            df_temp = pd.DataFrame(
                                data={
                                    'Index': [date],
                                    'Vehicle': [sub_session.vehicle.className],
                                    'Sessions': [1],
                                    'Consumption': [sub_session.consumption]
                                }
                            )
                            df = pd.concat([df, df_temp], ignore_index=True)
            power_list.append(self.current_power())

            if previous_date is not False:
                for port in self.hub_ports:
                    port.time_free += abs(date - previous_date)
            previous_date = date

        df_temp1 = df.set_index('Index').groupby('Vehicle')['Sessions'].resample('M').sum().reset_index()
        df_temp2 = (df.set_index('Index').groupby('Vehicle')['Consumption'].resample('M').sum() * 0.001).reset_index()
        df_power = pd.DataFrame({
            'Index': date_range,
            'Power': power_list
        })
        df_power = df_power.set_index('Index').resample('M').max().reset_index()

        #Port Usage %
        temp_ports = [Port(pq.Quantity(port_type, 'kW')) for port_type in self.port_types.keys()]
        for port_type in temp_ports:
            for port in self.hub_ports + self.ports_used:
                if port.Port_kW == port_type.Port_kW:
                    port_type + port
        port_data_df = pd.concat([port.usage_percent() for port in temp_ports],
                                 keys=[str(port_type) for port_type in self.port_types.keys()],
                                 names= ['Port Type'])
        port_data_df = port_data_df.reset_index().drop('level_1', axis=1).set_index('Port Type')
        return df_temp1.merge(df_temp2, on=["Index", "Vehicle"]), df_power, port_data_df

    def graphic_sim(self, end_date):
        date_range = pd.date_range(start='1/1/2022', end=end_date, freq='5T')
        df = pd.DataFrame()
        df["Date"] = date_range
        port_dict = {}
        for port in self.hub_ports:
            port_dict[port] = []

        df.set_index("Date")

        data_df = pd.DataFrame()
        data_df['Index'] = []
        data_df['Vehicle'] = []
        data_df['Sessions'] = []
        data_df['Consumption'] = []
        valid_sessions = []
        power_list = []
        previous_date = False
        for date in date_range:
            self.check_port_status(date)  # Refreshes Hub ports
            for port in self.hub_ports:
                if (7 <= date.hour < 22) and date.minute % 30 == 0:
                    if np.random.choice([True, False], 1, p=[self.usage_factor[0], 1 - self.usage_factor[0]])[0]:
                        sub_session = Session(self, date)
                        if sub_session.status:
                            valid_sessions.append(sub_session)
                            df_temp = pd.DataFrame(
                                data={
                                    'Index': [date],
                                    'Vehicle': [sub_session.vehicle.className],
                                    'Sessions': [1],
                                    'Consumption': [sub_session.consumption]
                                }
                            )
                            data_df = pd.concat([data_df, df_temp], ignore_index=True)

                elif (date.hour < 7 or date.hour >= 22) and date.minute % 30 == 0:
                    if np.random.choice([True, False], 1, p=[self.usage_factor[1], 1 - self.usage_factor[1]])[0]:
                        sub_session = Session(self, date)
                        if sub_session.status:
                            valid_sessions.append(sub_session)
                            df_temp = pd.DataFrame(
                                data={
                                    'Index': [date],
                                    'Vehicle': [sub_session.vehicle.className],
                                    'Sessions': [1],
                                    'Consumption': [sub_session.consumption]
                                }
                            )
                            data_df = pd.concat([data_df, df_temp], ignore_index=True)

            power_list.append(self.current_power())
            for port in self.hub_ports + self.ports_used:
                port_dict[port].append(port.status)

            if previous_date is not False:
                for port in self.hub_ports:
                    port.time_free += abs(date - previous_date)
            previous_date = date


        temp_df = pd.DataFrame().from_dict(port_dict)
        df = df.join(temp_df)

        df = df.style.applymap(lambda x: "background-color: red" if x is False else "background-color: white")
        #df.to_excel("output.xlsx")
        df_temp1 = data_df.set_index('Index').groupby('Vehicle')['Sessions'].resample('M').sum().reset_index()
        df_temp2 = (data_df.set_index('Index').groupby('Vehicle')['Consumption'].resample('M').sum() * 0.001).reset_index()

        df_power = pd.DataFrame({
            'Index' : date_range,
            'Power' : power_list
        })
        df_power = df_power.set_index('Index').resample('M').max().reset_index()

        with pd.ExcelWriter('output.xlsx') as writer:
            df.to_excel(writer, sheet_name='Graphic Schedule')
            df_temp1.merge(df_temp2, on=["Index", "Vehicle"]).to_excel(writer, sheet_name='Data')
            df_power.to_excel(writer, sheet_name='Power')
        #print(valid_sessions)


        return valid_sessions

def test():
    Class_A = VehicleClass(0, pq.Quantity(3.181, 'miles / (kW * hour)'), pq.Quantity(15638, 'miles / year'),
                           "Class 1-2")
    Class_B = VehicleClass(1, pq.Quantity(1.245, 'miles / (kW * hour)'), pq.Quantity(16200, 'miles / year'),
                           'Class 3-6')
    Class_C = VehicleClass(2, pq.Quantity(0.41, 'miles / (kW * hour)'), pq.Quantity(48750, 'miles / year'), 'Class 7-8')

    Hub_Name = "Urban Multimodal"
    Hub_Notional_Loading = [0.7, 0.5]
    Hub_Ports = [Port(pq.Quantity(150, 'kW')) for i in range(8)] + [Port(pq.Quantity(300, 'kW')) for i in range(2)]
    Hub_Vehicle_Mix = [0.35, 0.5, 0.15]

    Vehicle_Classes = [Class_A, Class_B, Class_C]

    hub = Hub(Hub_Name, Hub_Notional_Loading, Hub_Ports, Hub_Vehicle_Mix, Vehicle_Classes)

    return hub.simulate_hub_data('1/30/2022')



starttime = timeit.default_timer()
print("The start time is :", starttime)
data_set = []
power_set = []
portdata_set = []
for runs in range(10):
    data, power, portdata = test()
    data_set.append(data)
    power_set.append(power)
    portdata_set.append(portdata)

print("The time difference is :", timeit.default_timer() - starttime)

pd.set_option('display.max_columns', 100)  # or 1000
pd.set_option('display.max_rows', 100)  # or 1000
pd.set_option('display.max_colwidth', 199)  # or 199

# print((pd.concat(data_set).set_index('Index').groupby('Vehicle')['Sessions'].describe()).T)
# print("------------------")
# print((pd.concat(data_set).set_index('Index').groupby('Vehicle')['Consumption'].describe()).T)
# print("------------------")
# print((pd.concat(power_set).set_index('Index').describe()).T)
# print(pd.concat(portdata_set).groupby(['Port Type']).describe().T)

with pd.ExcelWriter('output.xlsx') as writer:
    (pd.concat(data_set).set_index('Index').groupby('Vehicle')['Sessions'].describe()).T.to_excel(writer, sheet_name='Sessions')
    (pd.concat(data_set).set_index('Index').groupby('Vehicle')['Consumption'].describe()).T.to_excel(writer, sheet_name='Consumption')
    (pd.concat(power_set).set_index('Index').describe()).T.to_excel(writer, sheet_name='Power')
    pd.concat(portdata_set).groupby(['Port Type']).describe().T.to_excel(writer, sheet_name='Port Usage')

