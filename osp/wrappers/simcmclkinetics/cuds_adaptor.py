# Import CUDS objects generated from CMCL ontology
# pylint: disable=no-name-in-module
from osp.core.namespaces import CMCL

# Import CUDS searching from OSP Core
import osp.core.utils.simple_search as search
import requests
import json
import urllib.parse
import time
import osp.wrappers.simcmclkinetics.agent_cases as ac

TRANS_FUNC_KEY = 'transFunc'
TRANS_FUNC_ARGS_KEY = 'transArgs'
TRANS_FUNC_INP_DEPS_KEY = 'transInpDeps'
TRANS_FUNC_OUT_DEPS_KEY = 'transOutDeps'
CUDS_BIND = 'cudsEntity'

class CUDSAdaptor:
    """Class to handle translation between CUDS and JSON objects.
    """

    @staticmethod
    def toJSON(root_cuds_object, simulation_template):
        """Translates the input CUDS object to a JSON object matching the
        INPUT format of remote kinetics simulations.

        Arguments:
            root_cuds_object    -- Root of CUDS object representing inputs
            simulation_template -- Object that provides a mapping between
                                   semantic ontological description and its
                                   syntactic descirption that engine understands

        Returns:
            jsonData            -- JSON data generated from CUDS
            synEntityToCUDSmap  -- Dictionary which stores a mapping between concrete
                                   cuds object instances and their syntactic representation
                                   (keys) that engine understands. This is used to map back
                                   engine outputs to cuds.
        """
        # NOTE - This translation relies heavily on the structure of the CUDS data,
        # which is defined by the ontology. If the ontology changes, it is likely
        # that this translation will need updating too. The translation is defined
        # in the agent_cases module.

        jsonData = {}
        synEntityToCUDSmap = {}

        jsonData["Case"]    = simulation_template.template
        jsonData["Inputs"]  = {}
        jsonData["Outputs"] = []

        # Find and register all input quantities (input)
        for inpSemSynMap in simulation_template.inputs:
            CUDSAdaptor.registerInput(root_cuds_object, jsonData["Inputs"], inpSemSynMap)

        # Find and register all output quantities (outputs) and construct synEntityToCUDSmap dictionary
        for outSemSynMap in simulation_template.outputs:
            CUDSAdaptor.registerOutput(root_cuds_object, jsonData["Outputs"], jsonData["Inputs"], outSemSynMap, synEntityToCUDSmap)

        return jsonData, synEntityToCUDSmap

    @staticmethod
    def registerInput(root_cuds_object, json_inp_dict, inpSemSynMap):
        """Registers the passed quantity as an input within the input JSON dict.

        Arguments:
            root_cuds_object    -- Root of CUDS object representing inputs
            json_inp_dict       -- JSON dictionary that would store a given input syntactic representation
            inpSemSynMap        -- object providing semantic-syntactic mapping for a given input
        """

        # Use the semEntity type associated with a given input from inpSemSynMap object to find the concrete cuds instance
        # that represents this input
        if inpSemSynMap.transFunc is not None:
            inputValue, inputUnit = CUDSAdaptor.getTransformedInput(root_cuds_object, inpSemSynMap, json_inp_dict)
        else:
            inputCUDS = search.find_cuds_objects_by_oclass(inpSemSynMap.semEntity, root_cuds_object, rel=None)
            if not inputCUDS:
                return

            inputCUDS = inputCUDS[0]

            # Store input cuds value and unit. the engine only accepts the string values, hence the conversion
            inputUnit = inputCUDS.unit

            # NOTE in order to support two possible values in ontological entities (float and string) there
            # are two "VALUE" cuds entities introduced: "VALUE" and "VALUE_STRING". These are further attached
            # to appropriate cuds entities as attribtues. In order to check if a given cuds has either former
            # or latter attribtue all its attributes names are put into a list below and are inspected.
            # NOTE this code will likely change in the future once a proper vector datatype support is added
            # to the simphony core
            inputCUDSattributeNames = [str(attr_name).lower() for attr_name in inputCUDS.get_attributes().keys()]
            if any('value_string' in attr_name for attr_name in inputCUDSattributeNames):
                # this cuds value is stored via "value_string" attribute
                inputValue = str(inputCUDS.value_string)
            else:
                inputValue = str(inputCUDS.value)

        # Not a valid input parameter, do not register
        if (inputValue == None) or (type(inputValue) is list and len(inputValue) == 0):
            return
        if inputValue == "":
            return

        # Register the input
        # Get the syntactic description of this input value and unit keys that the engine will understand
        inputSynValueKey = inpSemSynMap.synValueEntity
        inputSynUnitKey = inpSemSynMap.synUnitEntity

        json_inp_dict[inputSynValueKey] = inputValue
        # update the unit key only once
        if inputSynUnitKey is not None and inputSynUnitKey not in json_inp_dict:
            json_inp_dict[inputSynUnitKey] = inputUnit

    @staticmethod
    def getTransformedInput(root_cuds_object, inpSemSynMap, json_inp_dict):
        """Transforms the value of a given input by
           applying the transform function associated wits this input
           in the inp_dict_loc dictionary.

        Arguments:
            root_cuds_object    -- Root of CUDS object representing inputs
            inpSemSynMap        -- object providing semantic-syntactic mapping for a given input
            json_inp_dict       -- JSON dictionary that would store a given input

        Returns:
            transf_value    -- value after the transform operation
            transf_unit     -- unit after the transform operation
        """

        # get the transform function handle
        transf_func = inpSemSynMap.transFunc

        # assess all oclasses and their corresponding cuds instances needed
        # for the transformation

        transf_args_values = []
        for semEntity in inpSemSynMap.semEntity:
            inputCuds = search.find_cuds_objects_by_oclass(semEntity, root_cuds_object, rel=None)
            if not inputCuds:
                return

            inputCuds = inputCuds[0]

            # lookup the function arguments values and create the arguments array to be passed
            # to the function
            inputCUDSattributeNames = [str(attr_name).lower() for attr_name in inputCuds.get_attributes().keys()]
            if any('value_string' in attr_name for attr_name in inputCUDSattributeNames):
                # this cuds value is stored via "value_string" attribute
                transf_args_values.append(inputCuds.value_string)
            else:
                transf_args_values.append(inputCuds.value)

        # if defined, add extra arguments coming from transform function dependency on input values
        if inpSemSynMap.transFuncInpDep is not None:
            for inputDependencyKey in inpSemSynMap.transFuncInpDep:
                transf_args_values.append(json_inp_dict[inputDependencyKey])

        # call the transform function
        transf_value, transf_unit = transf_func(*transf_args_values)
        return transf_value, transf_unit


    @staticmethod
    def registerOutput(root_cuds_object, json_out_list, json_inp_dict, outSemSynMap, synEntityToCUDSmap):
        """Registers the passed quantity as an output within the input list.

        Arguments:
            root_cuds_object    -- Root of CUDS object representing inputs
            json_out_list       -- JSON list that would store a given output
            json_inp_dict       -- JSON inputs dictionary - used for special transformations
            outSemSynMap        -- object providing semantic-syntactic mapping for a given output
            synEntityToCUDSmap  -- Dictionary which stores a mapping between syntacitc (key) output
                                   representation that engine understands and the concrete CUDS
                                   instance that the it is associated with
        """

        # Use the oclass name/type associated with a given input from inp_dict_loc dictionary to find the concrete cuds instance
        # that represents this input
        outputCUDS = search.find_cuds_objects_by_oclass(outSemSynMap.semEntity, root_cuds_object, rel=None)
        if not outputCUDS:
            return

        outputCUDS = outputCUDS[0]
        # Get syntactic output keys
        synValueEntities = outSemSynMap.synValueEntity

        # Register the outputs
        json_out_list.extend(synValueEntities)

        # Update synEntityToCUDSmap
        CUDSAdaptor.updateOutputsCudsMap(outputCUDS, outSemSynMap, json_inp_dict, synEntityToCUDSmap)

    @staticmethod
    def updateOutputsCudsMap(out_cuds, outSemSynMap, json_inp_dict, synEntityToCUDSmap):
        """Given a concerete CUDS instance, dictionary 'out_dict_loc' holding metadata
            for the egine output associated with this CUDS class entity, add an entry to
            the synEntityToCUDSmap dictionary which binds the concrete CUDS instance with
            the engine output.

        Arguments:
            out_cuds            -- CUDS object assosiated with a given engine output
            outSemSynMap        -- object providing semantic-syntactic mapping for a given output
            json_inp_dict       -- JSON inputs dictionary - used for special transformations
            synEntityToCUDSmap  -- Dictionary which stores a mapping between syntacitc (key) output
                                   representation that engine understands and the concrete CUDS
                                   instance that the it is associated with
        """

        # update the synEntityToCUDSmap dictionary
        synValueEntities = outSemSynMap.synValueEntity

        synEntityToCUDS = {}
        synEntityToCUDS[CUDS_BIND] = out_cuds
        inputDependenciesValues = []
        if outSemSynMap.transFunc is not None:
            synEntityToCUDS[TRANS_FUNC_KEY] = outSemSynMap.transFunc
            synEntityToCUDS[TRANS_FUNC_ARGS_KEY] = synValueEntities

            if outSemSynMap.transFuncInpDep is not None:
                for inputDependencyKey in outSemSynMap.transFuncInpDep:
                    inputDependenciesValues.append(json_inp_dict[inputDependencyKey])
                synEntityToCUDS[TRANS_FUNC_INP_DEPS_KEY] = inputDependenciesValues

        # assign all mapping info under the first syntactic key
        synEntityToCUDSmap[synValueEntities[0]] = synEntityToCUDS

    @staticmethod
    def toCUDS(jsonData, synEntityToCUDSmap):
        """Given JSON data representing the outputs of a remote simulation and
        synEntityToCUDSmap dictionary which provides a mapping between concrete cuds
        instances and the corresponding engine outputs the method updates
        appropriate cuds values and units with the simulation data.

        Arguments:
            jsonData           -- JSON data representing outputs
            synEntityToCUDSmap -- Dictionary which stores a mapping between syntacitc (key) output
                                  representation that engine understands and the concrete CUDS
                                  instance that the it is associated with
        """

        # For each output in the returned JSON
        for key, value_unit in jsonData.items():
            # lookup which cuds instance a given output, identified by its key, belongs to
            if key in synEntityToCUDSmap:
                outputCUDS = synEntityToCUDSmap[key][CUDS_BIND]

                if TRANS_FUNC_KEY in synEntityToCUDSmap[key]:
                    value, unit = CUDSAdaptor.getTransformedResult(synEntityToCUDSmap, key, jsonData)
                else:
                    unit = value_unit['unit']
                    value = value_unit['value']

                    # NOTE remote simulation always returns an output as a list
                    # if the list is of length one, this is a single output
                    # so the list is dropped
                    # NOTE in case of the list output, it is currently converted
                    # to string as a work around to the fact that the current
                    # SimPhoNy implementation does not support vectors datatypes
                    # whose length is determined at runtime.
                    if len(value) == 1:
                        value = value[0]
                    else:
                        value = ','.join(str(e) for e in value)

                # assign values back to cuds
                # ------------------------------
                # unit assignment
                outputCUDS.unit = unit

                # value assignment
                # NOTE in order to support two possible values in ontological entities (float and string) there
                # are two "VALUE" cuds entities introduced: "VALUE" and "VALUE_STRING". These are further attached
                # to appropriate cuds entities as attribtues. In order to check if a given cuds has either former
                # or latter attribtue all its attributes names are put into a list below and are inspected.
                # NOTE this code will likely change in the future once a proper vector datatype support is added
                # to the simphony core
                outputCUDSattributeNames = [str(attr_name).lower() for attr_name in outputCUDS.get_attributes().keys()]
                if any('value_string' in attr_name for attr_name in outputCUDSattributeNames):
                    # this cuds value is stored via "value_string" attribute
                    outputCUDS.value_string = str(value)
                else:
                    # this cuds value is stored via "value" attribute
                    # NOTE at the moment all "value" attribtues are of type float
                    # NOTE It is not clear how to access datatype property of a given instance of cuds object
                    # so, a simple instance check is used instead.
                    outputCUDS.value = float(value)

    @staticmethod
    def getTransformedResult(synEntityToCUDSmap, output_key, jsonData):
        """Transforms the value of a given engine result by
           applying the transform function associated wits this result
           in the synEntityToCUDSmap dictionary.

        Arguments:
            synEntityToCUDSmap -- Dictionary which stores a mapping between syntacitc (key) output
                                  representation that engine understands and the concrete CUDS
                                  instance that the it is associated with
            output_key         -- key of the output to be transformed
            jsonData           -- JSON data generated from CUDS

        Returns:
            transf_value       -- value after the transform operation
            transf_unit        -- unit after the transform operation
        """

        # get the transform function handle and its main arguments names
        transf_func = synEntityToCUDSmap[output_key][TRANS_FUNC_KEY]
        transf_args_keys = synEntityToCUDSmap[output_key][TRANS_FUNC_ARGS_KEY]

        # lookup the function arguments values and create the arguments array to be passed
        # to the function
        transf_args_values = []
        for args_key in transf_args_keys:
            transf_args_values.append(jsonData[args_key]['value'])

        # if defined, add extra arguments coming from tranform function dependency on input values
        if TRANS_FUNC_INP_DEPS_KEY in synEntityToCUDSmap[output_key]:
            for inputDependenciesValue in synEntityToCUDSmap[output_key][TRANS_FUNC_INP_DEPS_KEY]:
                transf_args_values.append(inputDependenciesValue)

        # call the transform function
        transf_value, transf_unit = transf_func(*transf_args_values)
        return transf_value, transf_unit
