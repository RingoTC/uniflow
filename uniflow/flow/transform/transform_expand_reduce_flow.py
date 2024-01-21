"""Flow class."""
from typing import Any, Dict, Sequence, Mapping, Tuple, List

from uniflow.constants import TRANSFORM
from uniflow.flow.flow import Flow
from uniflow.node import Node
from uniflow.op.basic.copy_op import CopyOp
from uniflow.op.basic.expand_op import ExpandOp
from uniflow.op.basic.reduce_op import ReduceOp
from uniflow.op.prompt import PromptTemplate


def expand_fn(value_dicts: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Expand function."""
    # Concatenate all dictionaries into one
    all_values = {key: value for value_dict in value_dicts for key, value in value_dict.items()}

    n = len(all_values)
    half_n = n // 2

    expand_1 = {key: all_values[key] for i, key in enumerate(all_values) if i < half_n}
    expand_2 = {key: all_values[key] for i, key in enumerate(all_values) if i >= half_n}

    return expand_1, expand_2


def reduce_fn(expand_1, expand_2, unique_name):
    """Reduce function."""
    reduce_value_dict = {}

    for key_1, value_1 in expand_1["value_dict"].items():
        for key_2, value_2 in expand_2["value_dict"].items():
            new_key = f"{key_1} {key_2}"
            new_value = f"{value_1} {value_2}"
            reduce_value_dict[new_key] = new_value

    node = Node(name=unique_name, value_dict=reduce_value_dict, prev_nodes=[expand_1, expand_2])

    return [node]


class TransformExpandReduceFlow(Flow):
    """Expand and Reduce flow class.

    This is a demo flow expand and reduce the nodes.
    """

    TAG = TRANSFORM

    def __init__(
            self,
            prompt_template: PromptTemplate,
            model_config: Dict[str, Any],
    ) -> None:
        """Initialize ExpandReduceFlow class."""
        self._expand_op = ExpandOp(name="expand_op", expand_fn=expand_fn)
        self._reduce_op = ReduceOp(name="reduce_op", reduce_fn=reduce_fn)
        super().__init__()

    def run(self, nodes: Sequence[Node]) -> Sequence[Node]:
        """Run ExpandReduceFlow.

        Args:
            nodes (Sequence[Node]): Nodes to run.

        Returns:
            Sequence[Node]: Nodes after running.
        """

        expand_nodes = self._expand_op(nodes)
        reduce_nodes = self._reduce_op(expand_nodes)
        return reduce_nodes
