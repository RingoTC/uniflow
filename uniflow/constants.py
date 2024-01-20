"""Flow constants."""

ROOT_NAME = "root"
OUTPUT_NAME = "output"

# Flow Types
EXTRACT = "extract"
TRANSFORM = "transform"
RATER = "rater"

# I don't think the ExpandReduceFlow should be registered as a flow type,
# it should be registered in uniform/flow/transform/__init__.py
# just like CopyOp does.
