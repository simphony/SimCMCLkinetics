<img align="right" src="docs/static/cmcl_logo.png" alt="CMCL Logo">

# SimCMCLKinetics
SimPhoNy wrapper for the CMCL's "*k*inetics & SRM Engine Suite" software.

## Installation

<!---installation-start-9ed7307d-->

To set up the wrapper, clone the repository and then install the Python package
and the CMCL ontology.

```shell
git clone https://github.com/simphony/SimCMCLkinetics.git
pip install ./SimCMCLkinetics
pico install ./SimCMCLkinetics/cmcl.ontology.yml
```

### Docker

Alternatively, it is possible to execute the wrapper in a Docker container.
`docker` and `docker-compose` are required. To create the 
kinetics osp wrapper docker image run:

```bash
./docker_install.sh
```

<!---installation-end-9ed7307d-->

## Usage


A script `examples_runner.py` that can be used to run examples of all use cases
is provided in the `examples` folder. 

<!---examples-runner-start-c7140d1f-->

```bash
python examples/examples_runner.py [options]
# where:
#  options - control which examples are run, if not defined all
#            examples are run, possible values:
#            * cb       - run all carbon black examples
#            * cb momic - run carbon black momic example
#            * cb stoch - run carbon black stochastic example
#            * eat      - run all eat examples
#            * eat twc  - run eat twc example
#            * eat gpd  - run eat gpf example
```

<!---examples-runner-end-c7140d1f-->

Each example has been created to generate the expected inputs (with sample
values) for each of the three SimDOME use cases attributed to CMCL.

If you prefer to use Docker to run the kinetics wrapper, use the following
commands instead:

<!---examples-runner-docker-start-bc6ec07e-->

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
 #            examples are run, possible values: see options for 
 #            `examples_runner.py`
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

<!---examples-runner-docker-end-bc6ec07e-->

## Documentation

More extensive documentation can be found at
[simcmclkinetics.readthedocs.io](https://simcmclkinetics.readthedocs.io).

## Contact
For questions, issues, or suggestions, please contact mdhillman<@>cmclinnovations.com
