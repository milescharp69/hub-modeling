import numpy as np
import pandas as pd
import quantities as pq
from Port import Port
from VehicleClass import car


# Global Variables
OPERATION_HOURS = pq.Quantity(24, 'hour')
NOTIONAL_HOURS = pq.Quantity([15, 9], 'hour')

#TODO: Check units C:\Users\Miles\AppData\Local\Programs\Python\Python39\Lib\site-packages\quantities\units
#This might vary per device that is running the code actually

class Session:
    def __init__(self, hub, current_time):
        self.end_time = None
        self.charge_time = None
        self.power = None
        self.consumption = None
        self.start_time = current_time
        self.vehicle = np.random.choice(hub.vehicle_types, 1, p=hub.vehicle_mix)[0]
        self.port_weight = hub.port_weights(self.vehicle)

        # Initialize the session status
        self.status = False

        if self.is_port_available(hub):
            self.status = True
            self.assign_port(hub)
            self.set_consumption_and_charge_time(hub, current_time)
            self.set_end_time_and_update_port_usage(hub)

    def is_port_available(self, hub):
        return np.sum(self.port_weight) == 1

    def assign_port(self, hub):
        self.port_used = np.random.choice(hub.hub_ports, 1, p=self.port_weight)[0]
        hub.ports_used.append(hub.hub_ports.pop(hub.hub_ports.index(self.port_used)))

    def set_consumption_and_charge_time(self, hub, current_time):
        min_battery_percentage = 0.4
        max_battery_percentage = 0.85
        target_battery_percentage = np.random.uniform(min_battery_percentage, max_battery_percentage)

        #target_charge =  pq.Quantity(self.vehicle.battery_capacity * target_battery_percentage, 'kWh')
        target_charge = pq.Quantity(self.vehicle.battery_capacity * target_battery_percentage, 'kWh')
        required_charge = target_charge - self.vehicle.battery

        self.vehicle.battery += pq.Quantity(required_charge, 'kWh')
        self.consumption =  pq.Quantity(required_charge, 'kWh').magnitude

        charge_time_minutes = self.vehicle.charging_time(self.vehicle.battery / self.vehicle.battery_capacity, target_battery_percentage, self.port_used)

        self.power = self.port_used.Port_kW.magnitude

        self.charge_time = float(pq.Quantity(charge_time_minutes, 'hour').rescale('second').magnitude)

        self.port_used.open_date = pd.Timestamp(current_time.timestamp() + self.charge_time, unit='s').ceil(
            freq='5T')
        self.end_time = self.port_used.open_date

        self.port_used.time_usage[self.vehicle.className] += abs(self.end_time - self.start_time)

    def set_end_time_and_update_port_usage(self, hub):
        self.port_used.open_date = pd.Timestamp(self.start_time.timestamp() + self.charge_time, unit='s').ceil(
            freq='5T')
        self.end_time = self.port_used.open_date
        self.port_used.time_usage[self.vehicle.className] += abs(self.end_time - self.start_time)


class Hub:

    def __init__(self, hub_id, usage_factor, hub_ports, vehicle_mix) -> None:
        self.hub_id = hub_id
        self.usage_factor = usage_factor  # [7A-10P,10P-7A]
        self.hub_ports = hub_ports
        self.vehicle_mix = vehicle_mix
        self.vehicle_types = [car(pq.Quantity(85, 'kWh'), 0), car(pq.Quantity(225, 'kWh'), 1),
                              car(pq.Quantity(525, 'kWh'), 2)]
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


        self.slots = 0



    def vehicles_serviced(self):

        def charge_time(vehicle, port_used):
            return float((((vehicle.mi_year * (1/vehicle.mi_kWH)).rescale('(kW * hour) / month')  / port_used.Port_kW) * pq.month).rescale("minute").magnitude)

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
                        serviced_vehicles[vehicle_num] = int(total_minutes_1000kW / charge_time(self.vehicle_types[vehicle_num], Port(pq.Quantity(1000, 'kW')) ))

                    elif total_time_needed_for_allocation > total_time_port[2]:
                        serviced_vehicles[vehicle_num] = int(total_time_port[2] / charge_time(self.vehicle_types[vehicle_num], Port(pq.Quantity(1000, 'kW')) ))
                        total_time_needed_for_allocation -= total_time_port[2]
                        total_time_port[2] = 0

                        if total_time_needed_for_allocation < total_time_port[1]:
                            total_minutes_350kW = total_time_needed_for_allocation
                            total_time_port[1] -= total_time_needed_for_allocation
                            serviced_vehicles[vehicle_num] = int(total_minutes_350kW / charge_time(self.vehicle_types[vehicle_num], Port(pq.Quantity(350, 'kW')) ))
                        else:
                            serviced_vehicles[vehicle_num] = int(total_time_port[1] / charge_time(self.vehicle_types[vehicle_num], Port(pq.Quantity(350, 'kW')) ))
                            total_time_port[1] = 0
                    else:
                        serviced_vehicles[vehicle_num] = int(total_time_port[2]/ charge_time(self.vehicle_types[vehicle_num], Port(pq.Quantity(1000, 'kW')) ))
                        total_time_port[2] = 0

                elif vehicle_num == 1:
                    #only use 350kW and 150kW
                    #from how many 350kW are left
                    if total_time_needed_for_allocation < total_time_port[1]:
                        total_minutes_350kW = total_time_needed_for_allocation
                        serviced_vehicles[vehicle_num] += int(total_minutes_350kW / charge_time(self.vehicle_types[vehicle_num], Port(pq.Quantity(350, 'kW')) ))
                        total_time_port[1] -= total_minutes_350kW
                        break
                    elif total_time_needed_for_allocation > total_time_port[1]:
                        serviced_vehicles[vehicle_num] += int(total_time_port[1] / charge_time(self.vehicle_types[vehicle_num], Port(pq.Quantity(350, 'kW')) ))
                        total_time_needed_for_allocation  -= total_time_port[1]
                        total_time_port[1] = 0

                        if total_time_needed_for_allocation < total_time_port[0]:
                            total_minutes_150kW  = total_time_needed_for_allocation
                            serviced_vehicles[vehicle_num] += int(total_minutes_150kW / charge_time(self.vehicle_types[vehicle_num], Port(pq.Quantity(150, 'kW')) ))
                            total_time_port[0] -= total_minutes_150kW
                        else:
                            serviced_vehicles[vehicle_num] += int(total_time_port[0] / charge_time(self.vehicle_types[vehicle_num], Port(pq.Quantity(150, 'kW')) ))
                            total_time_port[0] = 0
                    else:
                        serviced_vehicles[vehicle_num] += int(total_time_port[1] / charge_time(self.vehicle_types[vehicle_num], Port(pq.Quantity(350, 'kW')) ))
                        total_time_port[1] = 0

                else:
                    #only use 150kW maybe also have it use 350kW ports
                    if total_time_needed_for_allocation < total_minutes_150kW:
                        total_minutes_150kW = total_time_needed_for_allocation
                        total_time_port[0] -= total_time_needed_for_allocation
                        serviced_vehicles[vehicle_num] += int(total_minutes_150kW / charge_time(self.vehicle_types[vehicle_num], Port(pq.Quantity(150, 'kW')) ))
                    else:
                        serviced_vehicles[vehicle_num] += int(total_minutes_150kW / charge_time(self.vehicle_types[vehicle_num], Port(pq.Quantity(150, 'kW')) ))
                        total_time_port[0] = 0
        elif 1000.0 not in self.port_types.keys()  and 300.0 not in self.port_types.keys(): #only has 150 kW ports

            for vehicle_num in range(len(self.vehicle_types)):
                total_minutes = (30 * self.usage_factor[0] + 18 * self.usage_factor[1]) * 30 * 30 * self.total_ports  \
                                * self.vehicle_mix[vehicle_num]
                serviced_vehicles[vehicle_num] += (int(total_minutes / charge_time(self.vehicle_types[vehicle_num], Port(pq.Quantity(150, 'kW')) )))
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
                        serviced_vehicles[vehicle_num] += (int(total_minutes_300kW /charge_time(self.vehicle_types[vehicle_num], Port(pq.Quantity(300, 'kW')) )))
                    else:
                        serviced_vehicles[vehicle_num] += (int(total_time_port[1] / charge_time(self.vehicle_types[vehicle_num], Port(pq.Quantity(300, 'kW')) )))
                        total_time_port[1] = 0

                elif vehicle_num == 1:
                    if total_time_needed_for_allocation < total_time_port[1]:
                        total_minutes_300kW = total_time_needed_for_allocation
                        total_time_port[1] -= total_minutes_300kW
                        serviced_vehicles[vehicle_num] += (int(total_minutes_300kW / charge_time(self.vehicle_types[vehicle_num], Port(pq.Quantity(300, 'kW')) )))
                    elif total_time_needed_for_allocation > total_time_port[1]:
                        serviced_vehicles[vehicle_num] += (int(total_time_port[1] / charge_time(self.vehicle_types[vehicle_num], Port(pq.Quantity(300, 'kW')) )))

                        total_time_needed_for_allocation -= total_time_port[1]
                        total_time_port[1] = 0

                        if total_time_needed_for_allocation < total_time_port[0]:
                            total_minutes_150kW = total_time_needed_for_allocation
                            total_time_port[0] -= total_minutes_150kW
                            serviced_vehicles[vehicle_num] += (
                                int(total_minutes_150kW / charge_time(self.vehicle_types[vehicle_num], Port(pq.Quantity(150, 'kW')) )))
                        else:
                            serviced_vehicles[vehicle_num] += (
                                int(total_time_port[0] / charge_time(self.vehicle_types[vehicle_num], Port(pq.Quantity(150, 'kW')) )))
                            total_time_port[0] = 0
                    else:
                        serviced_vehicles[vehicle_num] += (int(total_time_port[1] / charge_time(self.vehicle_types[vehicle_num], Port(pq.Quantity(300, 'kW')) )))
                        total_time_port[1] = 0
                else:
                    if total_time_needed_for_allocation < total_time_port[0]:
                        total_minutes_150kW = total_time_needed_for_allocation
                        total_time_port[0] -= total_minutes_150kW
                        serviced_vehicles[vehicle_num] += (int(total_minutes_150kW / charge_time(self.vehicle_types[vehicle_num], Port(pq.Quantity(150, 'kW')) )))
                    else:
                        serviced_vehicles[vehicle_num] += (int(total_time_port[0] / charge_time(self.vehicle_types[vehicle_num], Port(pq.Quantity(150, 'kW')) )))
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

    def graphic_sim(self, end_date):
        """
        Simulates the charging hub's behavior over a given date range and collects various statistics, such as
        power consumption, sessions, and port status. It also updates the hub_ports and ports_used lists based
        on the current simulation date.

        :param end_date: The end date of the simulation
        :return: DataFrames with simulation results (df, df_temp1, df_temp2, df_power)
        """
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
        slot_switch = [1,1] #did it switch periods 1

        for date in date_range:
            self.check_port_status(date)  # Refreshes Hub ports
            # Determine if the current time is within the specified charging hours
            if 7 <= date.hour < 22:
                slot_switch[1] = 0
            else:
                slot_switch[1] = 1
            # Check if the charging hour period has changed
            if slot_switch[0] != slot_switch[1]:
                # Reset the number of possible slots
                if slot_switch[0] == 1:
                    self.slots = 108
                else:
                    self.slots = 180
                slot_switch[0] = slot_switch[1]

            # Create a new session every 30 minutes
            if date.minute % 30 == 0:
                sub_session = Session(self, date)
                if sub_session.status:
                    sessioncount = sub_session.consumption / (sub_session.vehicle.mi_year / sub_session.vehicle.mi_kWH).rescale('kW * hour / month').magnitude
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

            # Update port time_free attribute
            if previous_date is not False:
                for port in self.hub_ports:
                    port.time_free += abs(date - previous_date)
            previous_date = date

        # Create DataFrame with port status
        col_names = [col.id for col in port_dict.keys()]
        temp_df = pd.DataFrame().from_dict(port_dict)
        temp_df.columns = col_names
        df = df.join(temp_df)

        # Aggregate session data and consumption data by month
        df_temp1 = data_df.set_index('Index').groupby('Vehicle')['Sessions'].resample('M').sum().reset_index()
        df_temp2 = (data_df.set_index('Index').groupby('Vehicle')['Consumption'].resample('M').sum() * 0.001).reset_index()

        #Round up the number of sessions to the nearest whole number
        df_temp1["Sessions"] = df_temp1["Sessions"].apply(np.ceil)

        df_power = pd.DataFrame({
            'Index' : date_range,
            'Power' : power_list
        })

        # Calculate maximum power used per mont
        df_power = df_power.set_index('Index').resample('M').max().reset_index()

        return df, df_temp1, df_temp2, df_power