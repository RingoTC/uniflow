import sys

sys.path.append(".")
sys.path.append("..")
sys.path.append("../..")

from uniflow.flow.client import TransformClient
from uniflow.flow.config import TransformCopyConfig
from uniflow.flow.config import TransformExpandReduceConfig
from uniflow.flow.flow_factory import FlowFactory
from uniflow.viz import Viz

client = TransformClient(TransformExpandReduceConfig())
input = [{"1": "2", "3": "4", "5": "6", "7": "8"}]
# expand: {"1": "2", "3": "4"} and {"5": "6", "7": "8"}
# output should be {"1 5": "2 6", "3 7": "4 8"}
output = client.run(input)

print(output)