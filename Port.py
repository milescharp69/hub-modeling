class Port:
    def __init__(self, Port_kW, Port_Amount, Port_Efficiency=.975):
        self.Port_kW = Port_kW
        self.Port_Amount = Port_Amount
        self.Port_Efficiency = Port_Efficiency

    # Port Methods
    def show(self):
        print("Port kW:", self.Port_kW)
        print("Port Amount:", self.Port_Amount)

    def data(self):
        return [self.Port_kW, self.Port_Amount]
    def datatext(self):
        return "{}x{}".format(self.Port_Amount, self.Port_kW)