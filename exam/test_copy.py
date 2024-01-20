import sys

sys.path.append(".")
sys.path.append("..")
sys.path.append("../..")

from uniflow.flow.client import TransformClient
from uniflow.flow.config import TransformCopyConfig
from uniflow.flow.config import TransformExpandReduceConfig
from uniflow.flow.flow_factory import FlowFactory
from uniflow.viz import Viz

client = TransformClient(TransformCopyConfig())
input = [{"1": "2", "3": "4", "5": "6", "7": "8"}]
output = client.run(input)

print(output)