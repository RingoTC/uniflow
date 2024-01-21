import unittest

from uniflow.node import Node
from uniflow.op.basic.expand_op import ExpandOp


class TestExpandOp(unittest.TestCase):
    def test_call(self):
        # Test with one input node
        input_node = Node(name="input_node", value_dict={"example_key": "example_value"})
        expand_fn = lambda value_dict: (value_dict["example_key"][:2], value_dict["example_key"][2:])
        op = ExpandOp(name="expand_op", expand_fn=expand_fn)
        output_nodes = op([input_node])

        self.assertEqual(
            input_node.flatten(),
            [
                {
                    "is_end": False,
                    "name": "input_node",
                    "next_nodes": ["expand_op_1", "expand_op_2"],
                    "prev_nodes": [],
                    "value_dict": {"example_key": "example_value"},
                },
                {
                    "is_end": False,
                    "name": "expand_op_1",
                    "next_nodes": [],
                    "prev_nodes": ["input_node"],
                    "value_dict": {"expand_1": "ex", "expand_2": "ample_value"},
                },
                {
                    "is_end": False,
                    "name": "expand_op_2",
                    "next_nodes": [],
                    "prev_nodes": ["input_node"],
                    "value_dict": {"expand_1": "example_value", "expand_2": ""},
                },
            ],
        )


if __name__ == "__main__":
    unittest.main()
