from . import create_app
import os
import logging
import logging.config

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    handlers=[logging.FileHandler(os.path.join(THIS_DIR,"mock_agent.log"),'w'),
                              logging.StreamHandler()])
logging.getLogger("werkzeug").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

app = create_app()
