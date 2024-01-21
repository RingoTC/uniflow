"""Reduce operation."""
import copy
from typing import Any, Mapping, Sequence

from typing import Callable, Mapping, Any, Sequence
from uniflow.node import Node
from uniflow.op.op import Op


class ReduceOp(Op):
    """Reduce operation class."""

    def __init__(self, name: str, reduce_fn):
        """
        Initialize ReduceOp.

        Args:
            reduce_fn (Callable[[Mapping[str, Any], Mapping[str, Any]], Mapping[str, Any]]):
                Function to merge value_dicts of expand_1 and expand_2.
        """
        super().__init__(name="reduce")
        self.reduce_fn = reduce_fn

    def _transform(self, expand_1_value_dict: Mapping[str, Any], expand_2_value_dict: Mapping[str, Any]) -> Mapping[
        str, Any]:
        """Transform value dict.

        Args:
            reduce_value_dict (Mapping[str, Any]): Input value dict.

        Returns:
            Mapping[str, Any]: Output value dict.
        """
        # Combine key-value pairs from expand_1 and expand_2 with concatenation
        reduce_value_dict = {}

        for key_1, value_1 in expand_1_value_dict.items():
            for key_2, value_2 in expand_2_value_dict.items():
                new_key = f"{key_1} {key_2}"
                new_value = f"{value_1} {value_2}"
                reduce_value_dict[new_key] = new_value

        return reduce_value_dict

    def __call__(self, nodes: Sequence[Node]) -> Sequence[Node]:
        """
        Call reduce operation.

        Args:
            nodes (Sequence[Node]): Input nodes (expand_1 and expand_2).

        Returns:
            Sequence[Node]: Output nodes (reduce_1).
        """

        output_nodes = [
            Node(name=self.unique_name(), value_dict=self._transform(nodes[0].value_dict, nodes[1].value_dict),
                 prev_nodes=nodes)
        ]
        return output_nodes
