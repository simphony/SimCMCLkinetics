class SimulationEngine:
    """
    CMCL kinetics engine code.
    """

    def __init__(self):
        self.executed = False
        print("Engine instantiated!")

    def __str__(self):
        return "Some Engine Connection"

    def run(self):
        """Call the run command of the engine."""
        print("Now the engine is running")
        self.executed = True

    def add_gas_species(self, uid, name, conc):
        """"""
        print("Added gas-phase species %s with name %s and conc %s"
              % (uid, name, conc))

    def remove_gas_species(self, uid):
        """"""
        print("Removed gas-phase species %s"
              % (uid))

    def update_length(self, uid, length):
        """"""
        print("Update reactor %s. Setting length to %s"
              % (uid, length))

    def update_cross_sect_area(self, uid, cross_sect_area):
        """"""
        print("Update reactor %s. Setting cross sectional area to %s"
              % (uid, cross_sect_area))

    def update_temperature(self, uid, temperature):
        """"""
        print("Update reactor %s. Setting temperature to %s"
              % (uid, temperature))

    def update_pressure(self, uid, pressure):
        """"""
        print("Update reactor %s. Setting pressure to %s"
              % (uid, pressure))

    def update_gas_species_conc(self, uid, conc):
        """"""
        print("Updated gas-phase species %s. Setting concentration to %s"
              % (uid, conc))

    #def get_temperature(self, uid):
    #   
