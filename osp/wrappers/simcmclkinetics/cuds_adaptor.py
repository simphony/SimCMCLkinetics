import requests
import json
import urllib.parse
import time


class CUDSAdaptor:
    """Class to handle translation bewteen CUDS and JSON objects.
    """

    @staticmethod
    def toJSON(root_cuds_object, simulation_template):
        """Translates the input CUDS object to a JSON object matching the 
        INPUT format of remote kinetics simulations.

        Arguments:
            root_cuds_object    -- Root of CUDS object representing inputs
            simulation_template -- Name (index?) of simulation template

        Returns:
            JSON data generated from CUDS
        """

        # TODO - If these input CUDS objects are generated from a CMCL Ontology that
        # covers all use cases (or the larger EMMO one in future), they may contain 
        # more data than we need to put in the input JSON string. May need to consider
        # this and only translate required objects here.

        # TODO - Implementation
        return None


    @staticmethod
    def toCUDS(jsonData, root_cuds_object):
        """Given JSON data representing the outputs of a remote simulation, this
        will populate the input CUDS objects with that output data.

        Arguments:
            jsonData         -- JSON data representing outputs
            root_cuds_object -- Root of CUDS object representing inputs
        """

        # TODO - Implementation