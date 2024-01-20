"""Expand operation."""
import copy
from typing import Any, Mapping, Sequence, List

from uniflow.node import Node
from uniflow.op.op import Op
from typing import Callable


class ExpandOp(Op):
    """Expand operation class."""

    def __init__(self, name: str, expand_fn: Callable):
        """Initialize expand operation.

        Args:
            expand_fn (Callable[[Mapping[str, Any]], Mapping[str, Any]]): Expand function.
        """
        super().__init__(name="expand")
        self.expand_fn = expand_fn

    def _transform(self, value_dict: Mapping[str, Any]) -> Mapping[str, Any]:
        """Transform value dict.

        Args:
            value_dict (Mapping[str, Any]): Input value dict.

        Returns:
            Mapping[str, Any]: Output value dict.
        """
        expand_1, expand_2 = self.expand_fn(value_dict)
        return {"expand_1": expand_1, "expand_2": expand_2}

    def __call__(self, nodes: Sequence[Node]) -> List[Node]:
        """Call expand operation.

        Args:
            nodes (Sequence[Node]): Input nodes.

        Returns:
            expand_1 contains the first half of the value_dict
            expand_2 contains the second half of the value_dict
        """

        node = nodes[0]
        value_dict = self._transform(node.value_dict)
        output_nodes = [
            Node(name=self.unique_name(), value_dict=value_dict['expand_1'], prev_nodes=[node]),
            Node(name=self.unique_name(), value_dict=value_dict['expand_2'], prev_nodes=[node]),
        ]

        return output_nodes
