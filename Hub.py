import timeit

import numpy as np
import pandas as pd
import quantities as pq

from Port import Port
from VehicleClass import car

import streamlit as st

# Global Variables
OPERATION_HOURS = pq.Quantity(24, 'hour')
NOTIONAL_HOURS = pq.Quantity([15, 9], 'hour')

#TODO: Check units C:\Users\Miles\AppData\Local\Programs\Python\Python39\Lib\site-packages\quantities\units
#This might vary per device that is running the code actuall

class Session:
    def __init__(self, hub, current_time):
        self.start_time = current_time

        self.vehicle = np.random.choice(hub.vehicle_types, 1, p=hub.vehicle_mix)[0]



        port_weight = hub.port_weights(self.vehicle)
        self.port_weight = port_weight

        if np.sum(port_weight) != 1:
            # There is not a port available
            self.status = False
        else:
            self.status = True
            self.port_used = np.random.choice(hub.hub_ports, 1, p=hub.port_weights(self.vehicle))[0]
            # Remove the port from the list of ports in the hub and append it to the list that is currently in use
            hub.ports_used.append(hub.hub_ports.pop(hub.hub_ports.index(self.port_used)))

            #TODO: Make the consumption more realistic
            self.consumption = self.vehicle.charge().magnitude

            #TODO:Adjust power/ charge_time depending of the charging profile

            self.power = self.port_used.Port_kW.magnitude

            #Charge time is in seconds
            self.charge_time = float(pq.Quantity(self.consumption / self.power, 'hour').rescale('second').magnitude) + 360

            # Rounded time
            #TODO: Future improvement- Make sure there is a reasonable amount of time between the sessions
            self.port_used.open_date = pd.Timestamp(current_time.timestamp() + self.charge_time, unit='s').ceil(
                freq='5T')
            self.end_time = self.port_used.open_date

            self.port_used.time_usage[self.vehicle.className] += abs(self.end_time - self.start_time)

            blocks_used = np.ceil(self.charge_time / 300)

            test = round(hub.usage_factor[0] / blocks_used, 4)

            if 7 <= current_time.hour < 22:
                if np.random.choice([True, False], 1, p=[round(hub.usage_factor[0] / blocks_used, 4), round(1 - round(hub.usage_factor[0] / blocks_used, 4), 4)])[0]:
                    self.status = True
                else:
                    self.status = False
            else:
                if np.random.choice([True, False], 1, p=[round(hub.usage_factor[1] / blocks_used, 4), round(1 - round(hub.usage_factor[1] / blocks_used, 4), 4)])[0]:
                    self.status = True
                else:
                    self.status = False

            # Disable port
            self.port_used.status = False

class Hub:

    def __init__(self, hub_id, usage_factor, hub_ports, vehicle_mix) -> None:
        self.hub_id = hub_id
        self.usage_factor = usage_factor  # [7A-10P,10P-7A]
        self.hub_ports = hub_ports
        self.vehicle_mix = vehicle_mix
        self.vehicle_types = [car(pq.Quantity(85, 'kW'), 0), car(pq.Quantity(225, 'kW'), 1),
                              car(pq.Quantity(525, 'kW'), 2)]
        self.total_ports = len(self.hub_ports)

        #Types of Ports
        self.port_types = {}
        for port in self.hub_ports:
            if float(port.Port_kW.magnitude) not in self.port_types.keys():
                self.port_types[float(port.Port_kW.magnitude)] = 1
            else:
                self.port_types[float(port.Port_kW.magnitude)] += 1

            port.id = str(int(port.Port_kW.magnitude)) + 'kWxx00' + str(self.port_types[float(port.Port_kW.magnitude)])
        self.ports_used = []

        #TODO:Rewrite the peak load

        # peak = 0
        # for i in range(0, len(self.hub_ports)):
        #     peak += (self.hub_ports[i].Port_kW.rescale('kW')).magnitude * self.hub_ports[i].Port_Efficiency
        # self.peak_load = pq.Quantity(peak, 'kW')

    def vehicles_serviced(self):
        # 30 sessions between 7am -10 pm
        # 18 sessions between 10 pm -7am
         # session per port per month
        #Rural it would just be the total number of session * hub.vehicle_mix / vehicle_charge_time
        serviced_vehicles = [0, 0, 0]

        if 1000.0 in self.port_types.keys():
            #Class C will use only 1000 kW


            total_time = (30 * self.usage_factor[0] + 18 * self.usage_factor[0]) * 30 * 30 * self.total_ports
            total_minutes_1000kW = (30 * self.usage_factor[0] + 18 * self.usage_factor[0]) * 30 * 30 * self.port_types[
                1000.0]
            total_minutes_350kW = (30 * self.usage_factor[0] + 18 * self.usage_factor[0]) * 30 * 30 * self.port_types[
                350.0]
            total_minutes_150kW = (30 * self.usage_factor[0] + 18 * self.usage_factor[0]) * 30 * 30 * self.port_types[
                150.0]
            total_time_port = [total_minutes_150kW, total_minutes_350kW, total_minutes_1000kW]
            for vehicle_num in [2,1,0]:
                total_time_needed_for_allocation = (30 * self.usage_factor[0] + 18 * self.usage_factor[0]) * 30 * 30 * self.total_ports * self.vehicle_mix[vehicle_num]

                percentage_of_allocation_needed = self.vehicle_mix[vehicle_num]

                if percentage_of_allocation_needed == 0:
                    break

                if vehicle_num == 2:
                    #Will only use 350kW and 1000kW ports
                    if total_time_needed_for_allocation < total_time_port[2]:
                        total_minutes_1000kW = total_time_needed_for_allocation
                        total_time_port[2] -= total_time_needed_for_allocation
                        serviced_vehicles[vehicle_num] = int(total_minutes_1000kW / self.vehicle_types[
                            vehicle_num].charge_time(Port(pq.Quantity(1000, 'kW'))))

                    elif total_time_needed_for_allocation > total_time_port[2]:
                        serviced_vehicles[vehicle_num] = int(total_time_port[2] / self.vehicle_types[
                            vehicle_num].charge_time(Port(pq.Quantity(1000, 'kW'))))
                        total_time_needed_for_allocation -= total_time_port[2]
                        total_time_port[2] = 0

                        if total_time_needed_for_allocation < total_time_port[1]:
                            total_minutes_350kW = total_time_needed_for_allocation
                            total_time_port[1] -= total_time_needed_for_allocation
                            serviced_vehicles[vehicle_num] = int(total_minutes_350kW / self.vehicle_types[
                                vehicle_num].charge_time(Port(pq.Quantity(350, 'kW'))))
                        else:
                            serviced_vehicles[vehicle_num] = int(total_time_port[1] / self.vehicle_types[
                                vehicle_num].charge_time(Port(pq.Quantity(350, 'kW'))))
                            total_time_port[1] = 0
                    else:
                        serviced_vehicles[vehicle_num] = int(total_time_port[2]/ self.vehicle_types[
                            vehicle_num].charge_time(Port(pq.Quantity(1000, 'kW'))))
                        total_time_port[2] = 0

                elif vehicle_num == 1:
                    #only use 350kW and 150kW
                    #from how many 350kW are left
                    if total_time_needed_for_allocation < total_time_port[1]:
                        total_minutes_350kW = total_time_needed_for_allocation
                        serviced_vehicles[vehicle_num] += int(total_minutes_350kW / self.vehicle_types[
                            vehicle_num].charge_time(Port(pq.Quantity(350, 'kW'))))
                        total_time_port[1] -= total_minutes_350kW
                        break
                    elif total_time_needed_for_allocation > total_time_port[1]:
                        serviced_vehicles[vehicle_num] += int(total_time_port[1] / self.vehicle_types[
                            vehicle_num].charge_time(Port(pq.Quantity(350, 'kW'))))
                        total_time_needed_for_allocation  -= total_time_port[1]
                        total_time_port[1] = 0

                        if total_time_needed_for_allocation < total_time_port[0]:
                            total_minutes_150kW  = total_time_needed_for_allocation
                            serviced_vehicles[vehicle_num] += int(total_minutes_150kW / self.vehicle_types[
                                vehicle_num].charge_time(Port(pq.Quantity(150, 'kW'))))
                            total_time_port[0] -= total_minutes_150kW
                        else:
                            serviced_vehicles[vehicle_num] += int(total_time_port[0] / self.vehicle_types[
                                vehicle_num].charge_time(Port(pq.Quantity(150, 'kW'))))
                            total_time_port[0] = 0
                    else:
                        serviced_vehicles[vehicle_num] += int(total_time_port[1] / self.vehicle_types[
                            vehicle_num].charge_time(Port(pq.Quantity(350, 'kW'))))
                        total_time_port[1] = 0

                else:
                    #only use 150kW maybe also have it use 350kW ports
                    if total_time_needed_for_allocation < total_minutes_150kW:
                        total_minutes_150kW = total_time_needed_for_allocation
                        total_time_port[0] -= total_time_needed_for_allocation
                        serviced_vehicles[vehicle_num] += int(total_minutes_150kW / self.vehicle_types[
                            vehicle_num].charge_time(Port(pq.Quantity(150, 'kW'))))
                    else:
                        serviced_vehicles[vehicle_num] += int(total_minutes_150kW / self.vehicle_types[
                            vehicle_num].charge_time(Port(pq.Quantity(150, 'kW'))))
                        total_time_port[0] = 0
        elif 1000.0 not in self.port_types.keys()  and 300.0 not in self.port_types.keys(): #only has 150 kW ports

            for vehicle_num in range(len(self.vehicle_types)):
                total_minutes = (30 * self.usage_factor[0] + 18 * self.usage_factor[1]) * 30 * 30 * self.total_ports  \
                                * self.vehicle_mix[vehicle_num]
                serviced_vehicles[vehicle_num] += (int(total_minutes /self.vehicle_types[vehicle_num].charge_time(Port(pq.Quantity(150, 'kW')))))
        else:
            serviced_vehicles = [0, 0, 0]
            total_time = (30 * self.usage_factor[0] + 18 * self.usage_factor[0]) * 30 * 30 * self.total_ports
            total_minutes_300kW = (30 * self.usage_factor[0] + 18 * self.usage_factor[0]) * 30 * 30 * self.port_types[
                300.0]
            total_minutes_150kW = (30 * self.usage_factor[0] + 18 * self.usage_factor[0]) * 30 * 30 * self.port_types[
                150.0]
            total_time_port = [total_minutes_150kW, total_minutes_300kW]
            #Has only 300kW and 150kW
            #Class C will use only 300 kW
            #Class B will use the rest of the 300 kW sessions that are open
            for vehicle_num in [2, 1, 0]:
                total_time_needed_for_allocation = (30 * self.usage_factor[0] + 18 * self.usage_factor[
                    0]) * 30 * 30 * self.total_ports * self.vehicle_mix[vehicle_num]
                if vehicle_num == 2:
                    #Will only us 300 kW port
                    if total_time_needed_for_allocation < total_time_port[1]:
                        total_minutes_300kW = total_time_needed_for_allocation
                        total_time_port[1] -= total_minutes_300kW
                        serviced_vehicles[vehicle_num] += (int(total_minutes_300kW / self.vehicle_types[vehicle_num].charge_time(
                            Port(pq.Quantity(300, 'kW')))))
                    else:
                        serviced_vehicles[vehicle_num] += (int(total_time_port[1] / self.vehicle_types[vehicle_num].charge_time(
                            Port(pq.Quantity(300, 'kW')))))
                        total_time_port[1] = 0

                elif vehicle_num == 1:
                    if total_time_needed_for_allocation < total_time_port[1]:
                        total_minutes_300kW = total_time_needed_for_allocation
                        total_time_port[1] -= total_minutes_300kW
                        serviced_vehicles[vehicle_num] += (int(total_minutes_300kW / self.vehicle_types[vehicle_num].charge_time(
                            Port(pq.Quantity(300, 'kW')))))
                    elif total_time_needed_for_allocation > total_time_port[1]:
                        serviced_vehicles[vehicle_num] += (int(total_time_port[1] / self.vehicle_types[vehicle_num].charge_time(
                            Port(pq.Quantity(300, 'kW')))))

                        total_time_needed_for_allocation -= total_time_port[1]
                        total_time_port[1] = 0

                        if total_time_needed_for_allocation < total_time_port[0]:
                            total_minutes_150kW = total_time_needed_for_allocation
                            total_time_port[0] -= total_minutes_150kW
                            serviced_vehicles[vehicle_num] += (
                                int(total_minutes_150kW / self.vehicle_types[vehicle_num].charge_time(
                                    Port(pq.Quantity(150, 'kW')))))
                        else:
                            serviced_vehicles[vehicle_num] += (
                                int(total_time_port[0] / self.vehicle_types[vehicle_num].charge_time(
                                    Port(pq.Quantity(150, 'kW')))))
                            total_time_port[0] = 0
                    else:
                        serviced_vehicles[vehicle_num] += (int(total_time_port[1] / self.vehicle_types[vehicle_num].charge_time(
                            Port(pq.Quantity(300, 'kW')))))
                        total_time_port[1] = 0
                else:
                    if total_time_needed_for_allocation < total_time_port[0]:
                        total_minutes_150kW = total_time_needed_for_allocation
                        total_time_port[0] -= total_minutes_150kW
                        serviced_vehicles[vehicle_num] += (int(total_minutes_150kW / self.vehicle_types[vehicle_num].charge_time(
                            Port(pq.Quantity(150, 'kW')))))
                    else:
                        serviced_vehicles[vehicle_num] += (int(total_time_port[0] / self.vehicle_types[vehicle_num].charge_time(
                            Port(pq.Quantity(150, 'kW')))))
                        total_time_port[0] = 0
        return serviced_vehicles

    def port_weights(self, vehicle):
        """

        :param vehicle:
        :return:
        """
        weights = []

        #TODO: Improve logic
        #Add co
        types_of_ports = [Port(pq.Quantity(1000, 'kW')), Port(pq.Quantity(350, 'kW')), Port(pq.Quantity(300, 'kW')),
                          Port(pq.Quantity(150, 'kW'))]

        # Shuffle Ports around to induce more variability

        np.random.shuffle(self.hub_ports)

        temp = True
        if vehicle.className ==  'Class 7-8':
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

        elif vehicle.className ==  'Class 3-6':
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

        #TODO: Perhaps instead of making a temp dataframe everytime just append the data to list and then make a data frame at the end

        for date in date_range:
            self.check_port_status(date)  # Refreshes Hub ports
            if (7 <= date.hour < 22) and date.minute % 15 == 0:
                for port in self.hub_ports:
                    if np.random.choice([True, False], 1, p=[self.usage_factor[0], 1 - self.usage_factor[0]])[0]:
                        sub_session = Session(self, date)
                        if sub_session.status:
                            if sub_session.vehicle.className == 'Class 7-8':
                                sessioncount = 1/7
                            else:
                                sessioncount = 0.5
                            df_temp = pd.DataFrame(
                                data={
                                    'Index': [date],
                                    'Vehicle': [sub_session.vehicle.className],
                                    'Sessions': [sessioncount],
                                    'Consumption': [sub_session.consumption]
                                }
                            )
                            df = pd.concat([df, df_temp], ignore_index=True)
            elif (date.hour < 7 or date.hour >= 22) and date.minute % 15 == 0:
                for port in self.hub_ports:
                    if np.random.choice([True, False], 1, p=[self.usage_factor[1], 1 - self.usage_factor[1]])[0]:
                        sub_session = Session(self, date)
                        if sub_session.status:
                            if sub_session.vehicle.className == 'Class 7-8':
                                sessioncount = 1/7
                            else:
                                sessioncount = 0.5
                            df_temp = pd.DataFrame(
                                data={
                                    'Index': [date],
                                    'Vehicle': [sub_session.vehicle.className],
                                    'Sessions': [sessioncount],
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
            if date.minute % 30 == 0:
                sub_session = Session(self, date)
                if sub_session.status:
                    if sub_session.vehicle.className == 'Class 7-8':
                        sessioncount = (1 / 7) * (1 / 4)
                    else:
                        sessioncount = (0.5) * (1 / 4)
                    df_temp = pd.DataFrame(
                        data={
                            'Index': [date],
                            'Vehicle': [sub_session.vehicle.className],
                            'Sessions': [sessioncount],
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
        col_names = [col.id for col in port_dict.keys()]
        temp_df = pd.DataFrame().from_dict(port_dict)
        temp_df.columns = col_names
        df = df.join(temp_df)

        df_temp1 = data_df.set_index('Index').groupby('Vehicle')['Sessions'].resample('M').sum().reset_index()
        df_temp2 = (data_df.set_index('Index').groupby('Vehicle')['Consumption'].resample('M').sum() * 0.001).reset_index()

        df_power = pd.DataFrame({
            'Index' : date_range,
            'Power' : power_list
        })
        df_power = df_power.set_index('Index').resample('M').max().reset_index()

        return df, df_temp1, df_temp2, df_power

Hub_Name = "Rural"
Hub_Notional_Loading = [1, 1]
Hub_Ports = [Port(pq.Quantity(150, 'kW')) for i in range(2)]
Hub_Vehicle_Mix = [0.4, 0.5, 0.1]

hub = Hub(Hub_Name, Hub_Notional_Loading, Hub_Ports, Hub_Vehicle_Mix)

df, df1, df2, df3 = hub.graphic_sim('1/30/2022')


df.drop(range(0,264), inplace=True)
df.drop(df.columns[2], axis=1, inplace=True)
df = df.set_index(pd.DatetimeIndex(df['Date']))
df.drop(df.columns[0], axis=1, inplace=True)


df_during227 = [] #108

df_during722 = [] #180

count = 0

start_val = 0
end_val = 108
adder = 180

while count < 20:
    if adder == 180:
        tempdf = df.iloc[start_val:end_val]
        df_during227.append(tempdf)
        start_val = end_val
        end_val += adder
        adder = 108
        count += 1
        continue

    if adder == 108:
        tempdf = df.iloc[start_val:end_val]
        df_during722.append(tempdf)
        start_val = end_val
        end_val += adder
        adder = 180
    count += 1


loadingpercent_227 = []
loadingpercent_722 = []

for df in df_during227:
    try:
        true_count, false_count = df.value_counts().tolist()
    except:
        print(df.value_counts())

    loadingpercent_227.append(false_count/ (true_count + false_count))

for df in df_during722:
    try:
        true_count, false_count = df.value_counts().tolist()
    except:
        print(df.value_counts())
    loadingpercent_722.append(false_count/ (true_count + false_count))

print('g')