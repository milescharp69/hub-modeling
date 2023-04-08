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
        elif veh_class == 1:
            self.mi_kWH = pq.Quantity(1.245, 'miles / (kW * hour)')
            self.mi_year = pq.Quantity(16200, 'miles / year')
            self.className = 'Class 3-6'
        else:
            self.mi_kWH = pq.Quantity(0.41, 'miles / (kW * hour)')
            self.mi_year = pq.Quantity(48750, 'miles / year')
            self.className = 'Class 7-8'


class car(VehicleClass):
    def __init__(self, battery_capacity, vehicle_class):
        super().__init__(vehicle_class)
        self.battery_capacity = battery_capacity  # Energy Capacity
        self.battery = np.random.uniform(0.1, 0.3) * self.battery_capacity  # Set initial state of charge

    def charging_curve(self, port_power):
        """
        Synthesize charging curve for the car.
        :param port_power: Maximum power of the charging port
        :return: A function representing the charging curve
        """
        max_charging_speed = min(self.battery_capacity / 4, port_power)  # Limit the charging speed by port power

        def curve(t):
            if t < 0.5:
                return 2 * max_charging_speed * t
            elif 0.5 <= t < 1.5:
                return max_charging_speed
            else:
                return max_charging_speed * (2 - t)

        return curve

    def charge_time(self, port_used, target_battery_percentage):
        """
        Calculate the charge time in minutes considering the charging curve.
        :param port_used: Port object
        :param target_battery_percentage: Target state of charge as a percentage of battery capacity
        :return: Charge time in minutes
        """
        curve = self.charging_curve(port_used.Port_kW.magnitude)
        remaining_charge = self.battery_capacity * target_battery_percentage - self.battery
        time = 0
        total_charge = 0

        while total_charge < remaining_charge:
            total_charge += curve(time) * 1 / 60  # 1/60 hour per minute
            time += 1

        return time

    def charge_session(self, session_start_time, port_used, target_battery_percentage):
        """
        Create a DataFrame representing the charging session.
        :param session_start_time: Timestamp object
        :param port_used: Port object
        :param target_battery_percentage: Target state of charge as a percentage of battery capacity
        :return: DataFrame with time, charging speed, and battery state columns
        """
        charge_time_minutes = self.charge_time(port_used, target_battery_percentage)
        session_end_time = session_start_time + pd.to_timedelta(charge_time_minutes, unit='minutes')
        time_range = pd.date_range(start=session_start_time, end=session_end_time, freq='1T')

        curve = self.charging_curve(port_used.Port_kW.magnitude)
        charging_speed = [curve(t) for t in np.arange(0, charge_time_minutes / 60, 1 / 60)]

        battery_state = [self.battery + pq.Quantity(cumulative_charge, 'kW * hour') for cumulative_charge in
                         np.cumsum(charging_speed) * 1 / 60]

        session_df = pd.DataFrame(
            {'time': time_range, 'charging_speed': charging_speed, 'battery_state': battery_state})

        return session_df
