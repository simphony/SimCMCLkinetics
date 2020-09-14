# Import CUDS objects generated from CMCL ontology
# pylint: disable=no-name-in-module
from osp.core import CMCL

# Import CUDS searching from OSP Core
import osp.core.utils.simple_search as search

import requests
import json
import urllib.parse
import time


class CUDSAdaptor:
    """Class to handle translation between CUDS and JSON objects.
    """

    @staticmethod
    def toJSON(simulation_template, root_cuds_object):
        """Translates the input CUDS object to a JSON object matching the 
        INPUT format of remote kinetics simulations.

        Arguments:
            root_cuds_object    -- Root of CUDS object representing inputs
            simulation_template -- Name (index?) of simulation template

        Returns:
            JSON data generated from CUDS
        """
        # NOTE - This translation relies heavily on the structure of the CUDS data,
        # which is defined by the ontology. If the ontology changes, it is likely
        # that this translation will need updating too.

        # NOTE - This translation works by writing all OUTPUT_QUANTITY instances,
        # and any PHYSICAL_QUANTITY instance that has a value to JSON. As this 
        # wrapper code has no knowledge of what inputs are supported within the
        # JSON request, it may result in outputting additional JSON parameters if
        # they're present in the CUDS data. Without prior knowledge of the expected 
        # JSON inputs (or some "mark-for-input" flag within the ontology), then
        # I can see no way to prevent this.
    
        # NOTE - When parameters are translated from CUDS to JSON, their CUDS oclass 
        # name is used for the JSON string. This means that if the names in the 
        # ontology do not match the names expected in the JSON, there will be errors.
        # Short of writing a massive, hard-coded CUDS-to-JSON name mapper, I can see
        # no other solution here.

        jsonData = {}

        # Find and register all physical quantities (inputs)
        inputsDict = {}
        physicals = search.find_cuds_objects_by_oclass(CMCL.PHYSICAL_QUANTITY, root_cuds_object, rel=None)
        
        for physical in physicals:
            CUDSAdaptor.registerInput(inputsDict, physical)

        # Find and register all output quantities (outputs)
        outputsList = []
        outputs = search.find_cuds_objects_by_oclass(CMCL.OUTPUT_QUANTITY, root_cuds_object, rel=None)
        
        for output in outputs:
            CUDSAdaptor.registerOutput(outputsList, output)

        jsonData["Case"]    = simulation_template
        jsonData["Inputs"]  = inputsDict
        jsonData["Outputs"] = outputsList
 
        print(json.dumps(jsonData))        
        return jsonData


    @staticmethod
    def registerInput(dict, quantity):
        """Registered the passed quantity as an input within the input JSON dict.

        Arguments:
            dict     -- JSON dictionary
            quantity -- physical quantity
        """
        value = quantity.value
        unit = quantity.unit

        # Not a valid input parameter, do not register
        if (value == None) or (type(value) is list and len(value) == 0):
            return
        if value == "[]":
            return

        # Is the quantity part of a gas mixture AND has a dimensionless unit (if so, special handling)
        inletgas = search.find_cuds_objects_by_oclass(
                CMCL.INLET_GAS,
                quantity,
                rel=CMCL.IS_QUANTITATIVE_PROPERTY)  

        special_case = (unit == "-") and (inletgas is not None and len(inletgas) == 1)

        if not special_case:
            # Regular quantity
            name = "$INP_" + quantity.oclass.name
            unit = quantity.unit

            dict[name + "_VALUE"] = value
            dict[name + "_UNIT"] = unit

        else:
            # NOTE - This special handling is done if the quantity is a mass or mole
            # fraction. Currently, the only way to identify this is to check if the
            # quantity is part of the inlet gas mixture. In future, the ontology
            # should ideally group these into a "MIXTURE_FRACTION_QUANTITY" class.
            name = "$INP_MIX_COMP_" + quantity.oclass.name
            value = quantity.value

            dict[name] = value

            # Register the mixture unit too
            mixtureunit = inletgas[0].unit
            dict["$INP_MIX_COMP_UNIT"] = mixtureunit
            

    @staticmethod
    def registerOutput(outputs, quantity):
        """Registered the passed quantity as an output within the input list.

        Arguments:
            outputs  -- list of output names
            quantity -- output quantity
        """
        name = quantity.oclass.name
        outputs.append("$" + name)
            
 
    @staticmethod
    def toCUDS(jsonData, root_cuds_object):
        """Given JSON data representing the outputs of a remote simulation, this
        will populate the input CUDS objects with that output data.

        Arguments:
            jsonData           -- JSON data representing outputs
            root_cuds_object   -- Root CUDS object
        """
        # NOTE - Again, this works by assuming the CUDS oclass and JSON names 
        # match (i.e. a CUDS object with an oclass name matching the JSON string
        # is searched for); mismatches will cause errors.

        # For each output in the returned JSON
        for output_key in jsonData:
            name = output_key[1:]
            unit = jsonData[output_key]["unit"]
            value = jsonData[output_key]["value"]

            # Find the corresponding CUDS output (by oclass name)
            cuds_output = CUDSAdaptor.nameMatch(root_cuds_object, name)

            # Store returned unit and value
            if cuds_output is not None:
                print("Settings values for %s" % (name))
                cuds_output.unit = unit
                cuds_output.value = str(value).strip("[]")
            else:
                print("COULD NOT FIND OUTPUT %s" % (name))


    @staticmethod
    def nameMatch(root_cuds_object, name):
        """Searches for the first object in the inputs CUDS data
        that has a matching oclass name.

        Arguments:
            root_cuds_objects -- CUDS search space
            name              -- target oclass name
        """
        outputs = search.find_cuds_objects_by_oclass(CMCL.OUTPUT_QUANTITY, root_cuds_object, rel=None)
       
        for sub in outputs:
            if sub.oclass.name == name:
                return sub
    
        return None