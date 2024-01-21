import unittest

from uniflow.node import Node
from uniflow.op.basic.reduce_op import ReduceOp


class TestReduceOp(unittest.TestCase):
    def test_call(self):
        # Test with two input nodes (expand_1 and expand_2)
        input_node_1 = Node(name="expand_op_1", value_dict={"key_1": "value_1"})
        input_node_2 = Node(name="expand_op_2", value_dict={"key_2": "value_2"})

        reduce_fn = lambda expand_1_value_dict, expand_2_value_dict: {"reduced_key": f"{expand_1_value_dict['key_1']}_{expand_2_value_dict['key_2']}"}

        op = ReduceOp(name="reduce_op", reduce_fn=reduce_fn)
        output_nodes = op([input_node_1, input_node_2])

        self.assertEqual(
            input_node_1.flatten() + input_node_2.flatten(),
            [
                {
                    "is_end": False,
                    "name": "expand_op_1",
                    "next_nodes": ["reduce_op_3"],
                    "prev_nodes": [],
                    "value_dict": {"key_1": "value_1"},
                },
                {
                    "is_end": False,
                    "name": "expand_op_2",
                    "next_nodes": ["reduce_op_3"],
                    "prev_nodes": [],
                    "value_dict": {"key_2": "value_2"},
                },
                {
                    "is_end": False,
                    "name": "reduce_op_3",
                    "next_nodes": [],
                    "prev_nodes": ["expand_op_1", "expand_op_2"],
                    "value_dict": {"reduced_key": "value_1_value_2"},
                },
            ],
            )


if __name__ == "__main__":
    unittest.main()
