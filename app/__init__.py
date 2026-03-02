import json
from logger import init_logging
from app.constants import GRAPH_INFO_PATH

perf_logger = init_logging()
#load the json that holds the count for the edges
graph_info = json.load(open(GRAPH_INFO_PATH))