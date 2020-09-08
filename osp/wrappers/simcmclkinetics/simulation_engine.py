# Class that actually handles the technical aspects of setting up, submitting,
# and returning the generated output from an SRM driver job.
class SimulationEngine:

    # Constructor
    def __init__(self):
        self.executed = False
        print("Engine instantiated!")

    # Textual representation
    def __str__(self):
        return "Some Engine Connection"

    # Executes the simulation
    # Does this need a 'currentlyExecuting' variable to prevent multiple calls?
    def run(self):

        # TODO - Build the JSON string from the CUDS objects
        # TODO - Submit HTTP request to KineticsAgent
        # TODO - Store job ID returned by the KineticsAgent
        # TODO - Wait until the KineticsAgent finishes that job
        # TODO - Store output data from the KineticsAgent
        # TODO - Organise output data into CUDS objects???

        self.executed = True

    def update_c2h2_massfrac(self, uid, value):
        """"""
        print("Update inlet mixture %s. Setting C2H2 mass fraction to %s"
              % (uid, value))

    def update_c6h6_massfrac(self, uid, value):
        """"""
        print("Update inlet mixture %s. Setting C6H6 mass fraction to %s"
              % (uid, value))

    def update_n2_massfrac(self, uid, value):
        """"""
        print("Update inlet mixture %s. Setting N2 mass fraction to %s"
              % (uid, value))

    def update_m_flow(self, uid, value):
        """"""
        print("Update inlet mixture %s. Setting mass flowrate to %s"
              % (uid, value))

    # heterog mixture updates
    def update_temperature(self, uid, value):
        """"""
        print("Update phase heterogeneous reactive mixture %s. Setting temperature to %s"
              % (uid, value))

    def update_pressure(self, uid, value):
        """"""
        print("Update phase heterogeneous reactive mixture %s. Setting pressure to %s"
              % (uid, value))

    def update_part_num_dens(self, uid, value):
        """"""
        print("Update phase heterogeneous reactive mixture %s. Setting particle number density to %s"
              % (uid, value))

    def update_mean_part_size(self, uid, value):
        """"""
        print("Update phase heterogeneous reactive mixture %s. Setting mean particle size to %s"
              % (uid, value))

    def update_part_vol_frac(self, uid, value):
        """"""
        print("Update phase heterogeneous reactive mixture %s. Setting particle volume fraction to %s"
              % (uid, value))

    # cb reactor updates
    def update_length(self, uid, value):
        """"""
        print("Update cb reactor property %s. Setting reactor length to %s"
              % (uid, value))

    def update_area(self, uid, value):
        """"""
        print("Update cb reactor property %s. Setting reactor cross sectional area to %s"
              % (uid, value))
