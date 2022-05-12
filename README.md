<img align="right" src="cmcl_logo.png" alt="CMCL Logo">

# SimCMCLKinetics
SimPhoNy wrapper for the CMCL's "*k*inetics & SRM Engine Suite" software.

## Requirements
- docker
- docker-compose

## Build instructions
In order to create the kinetics osp wrapper docker image run:
```bash
./docker_install.sh
```

## Execution
To run the kinetics wrapper, use the following commands:

```bash
 ./run_container.sh [command] [options]
 #  where:
 #  command - choose between running tests and examples
 #            if not provided, defaults to tests
 #            * tests    - launches all tests using the MOCK kinetics
 #                         disregards any other options
 #            * examples - launches examples using the REAL kinetics
 #                         agent, accepts further options
 #            * bash     - opens container bash terminal
 #                         disregards any other options
 #  options - control which examples are run, if not defined all
 #            examples are run, possible values:
 #            * cb       - run all carbon black examples
 #            * cb momic - run carbon black momic example
 #            * cb stoch - run carbon black stochastic example
 #            * eat      - run all eat examples
 #            * eat twc  - run eat twc example
 #            * eat gpd  - run eat gpf example
 #
 # Some examples:
 # 1. run all the tests
./run_container.sh
 # 2. run all the tests
./run_container.sh tests
 # 3. run all the examples
 ./run_container.sh examples
 # 4. run all carbon black examples
./run_container.sh examples cb
 # 5. run carbon black momic example
./run_container.sh examples cb momic
 # 6. run all eat examples
./run_container.sh examples eat
```


Each example file has been created to generate the expected inputs (with sample values) for each of the four SimDOME use cases attributed to CMCL.

## Current Limitations
- The "calculation accuracy" setting listed in the initial deliverable plan is not yet implemented.
- CUDS objects are generated from a sample CMCL ontology and set using sample input values. This should be replaced with the CUDS objects (generated from the EMMO) passed from the Fraunhofer UI.
- Remote simulation results are currently translated to CUDS objects and written to file, this will need to be passed back to the Fraunhofer UI when such a framework exists.

## Workflow
When one of the example scripts is executed, the wrapper currently does the following:

- Input CUDS objects are created by the example script
- A new KineticsEngine instance is created (using either the CarbonBlackEngine or EATEngine concrete classes)
- Key parameters are identified to determine which simulation template should be used
- That engine instance is passed to a new KineticsSession as an argument
- Input CUDS objects are written to file for inspection
- Input CUDS objects are translated to JSON
- JSON is transmitted as a HTTP request to the remote KineticsAgent server
	- From this point on, the AgentBridge class continually contacts the KineticsAgent server to request the simulation status
- KineticsAgent applies JSON inputs to the relevant simulation template
- Final simulation files are sent to compute node for execution
	- Once complete, the KineticsAgent identifies the requested outputs from the simulation and will respond with them upon the next check from the AgentBridge
- JSON outputs are received from the remote KineticsAgent
- Results from JSON are parsed into new CUDS objects
- CUDS outputs are written to file for inspection

![Workflow overview](technical-overview.JPG)

## Contact
For questions, issues, or suggestions, please contact mdhillman<@>cmclinnovations.com