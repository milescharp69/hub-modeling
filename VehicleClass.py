import quantities as pq
import numpy as np
import pandas as pd
from Port import Port

class VehicleClass:
    def __init__(self, veh_class):
        if veh_class == 0:
            self.mi_kWH = pq.Quantity(3.181, 'miles / (kW * hour)')
            self.mi_year = pq.Quantity(15638, 'miles / year')
            self.className = 'Class 1-2'
            self.max_charge_speed = pq.Quantity(150, 'kW')
        elif veh_class == 1:
            self.mi_kWH = pq.Quantity(1.245, 'miles / (kW * hour)')
            self.mi_year = pq.Quantity(16200, 'miles / year')
            self.className = 'Class 3-6'
            self.max_charge_speed = pq.Quantity(350, 'kW')
        else:
            self.mi_kWH = pq.Quantity(0.41, 'miles / (kW * hour)')
            self.mi_year = pq.Quantity(48750, 'miles / year')
            self.className = 'Class 7-8'
            self.max_charge_speed = pq.Quantity(1000, 'kW')


class car(VehicleClass):
    def __init__(self, battery_capacity, vehicle_class):
        super().__init__(vehicle_class)
        self.battery_capacity = battery_capacity  # Energy Capacity in kWH
        self.battery = np.random.uniform(0.1, 0.3) * self.battery_capacity  # Set initial state of charge

    def charging_rate(self, battery_capacity, max_capacity, charge_rate_exp):
        soc = battery_capacity / max_capacity
        if soc < 0.2:
            return charge_rate_exp[0]
        elif soc < 0.4:
            return charge_rate_exp[int(0.2 * len(charge_rate_exp))]
        elif soc < 0.6:
            return charge_rate_exp[int(0.4 * len(charge_rate_exp))]
        elif soc < 0.8:
            return charge_rate_exp[int(0.6 * len(charge_rate_exp))]
        else:
            return charge_rate_exp[int(0.8 * len(charge_rate_exp))]

    def charging_time(self, initial_percentage, target_percentage, port):
        # Limit charging speed
        max_charging_speed = self.max_charge_speed.magnitude
        if port.Port_kW.magnitude < self.max_charge_speed.magnitude:
            max_charging_speed = port.Port_kW.magnitude

        charge_rate_exp = max_charging_speed * np.exp(-3 * self.battery.magnitude)
        delta_capacity = self.battery_capacity / charge_rate_exp.size
        initial_capacity = initial_percentage * self.battery_capacity / 100
        target_capacity = target_percentage * self.battery_capacity / 100
        battery_capacity_range = np.arange(initial_capacity, target_capacity, delta_capacity)

        charge_rates = [self.charging_rate(bat, self.battery_capacity.magnitude, charge_rate_exp) for bat in
                        battery_capacity_range]
        time_needed = [delta_capacity / rate for rate in charge_rates]

        return sum(time_needed)

    def charge_session(self, session_start_time, port_used):
        """
        Create a DataFrame representing the charging session.
        :param session_start_time: Timestamp object
        :param port_used: Port object
        :return: DataFrame with time, charging speed, and battery state columns
        """
        initial_percentage = self.battery / self.battery_capacity
        target_percentage = np.random.uniform(0.4, 0.85)

        charge_time_minutes = self.charge_time(initial_percentage, target_percentage, port_used)
        session_end_time = session_start_time + pd.to_timedelta(charge_time_minutes, unit='minutes')
        time_range = pd.date_range(start=session_start_time, end=session_end_time, freq='1T')

        battery_capacity_range = np.linspace(self.battery, target_percentage * self.battery_capacity, len(time_range))
        charging_speed = [self.charging_rate(cap, port_used) for cap in battery_capacity_range]

        battery_state = [self.battery + pq.Quantity(cumulative_charge, 'kW * hour') for cumulative_charge in
                         np.cumsum(charging_speed) * 1 / 60]

        session_df = pd.DataFrame(
            {'time': time_range, 'charging_speed': charging_speed, 'battery_state': battery_state})

        return session_df
