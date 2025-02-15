import logging
import sys

import pandas as pd

from hamilton import base, driver
from hamilton.io.materialization import to

logging.basicConfig(stream=sys.stdout)
initial_columns = {  # load from actuals or wherever -- this is our initial data we use as input.
    # Note: these values don't have to be all series, they could be a scalar.
    "signups": pd.Series([1, 10, 50, 100, 200, 400]),
    "spend": pd.Series([10, 10, 20, 40, 40, 50]),
}
# we need to tell hamilton where to load function definitions from
# programmatic code to load modules:
# module_name = "my_functions"
# my_functions = importlib.import_module(module_name)
# or import module(s) directly:

import my_functions

df_builder = base.PandasDataFrameResult()

dr = driver.Driver({}, my_functions)  # can pass in multiple modules
# we need to specify what we want in the final dataframe. These can be string names, or function references.
output_columns = [
    "spend",
    "signups",
    "avg_3wk_spend",  # could just pass "avg_3wk_spend" here
    "spend_per_signup",  # could just pass "spend_per_signup" here
    "spend_zero_mean_unit_variance",  # could just pass "spend_zero_mean_unit_variance" here
]

materializers = [
    # materialize the dataframe to a pickle file
    to.pickle(
        dependencies=output_columns,
        id="df_to_pickle",
        path="./df.pkl",
        combine=df_builder,
    ),
]
# Visualize what is happening
dr.visualize_materialization(
    *materializers,
    additional_vars=output_columns,
    output_file_path="./dag",
    render_kwargs={},
    inputs=initial_columns,
)
# Materialize a result, i.e. execute the DAG!
materialization_results, additional_outputs = dr.materialize(
    *materializers,
    additional_vars=[
        "df_to_pickle_build_result"
    ],  # because combine is used, we can get that result here.
    inputs=initial_columns,
)
print(materialization_results)
print(additional_outputs["df_to_pickle_build_result"])
