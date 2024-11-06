import numpy as np
import pytest

from pandas import DataFrame
import pandas._testing as tm
from pandas.core.groupby.base import (
    reduction_kernels,
    transformation_kernels,
)


@pytest.fixture(params=[True, False])
def sort(request):
    return request.param


@pytest.fixture(params=[True, False])
def as_index(request):
    return request.param


@pytest.fixture(params=[True, False])
def dropna(request):
    return request.param


@pytest.fixture(params=[True, False])
def observed(request):
    return request.param


@pytest.fixture
def mframe(multiindex_dataframe_random_data):
    return multiindex_dataframe_random_data


@pytest.fixture
def df():
    return DataFrame(
        {
            "A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"],
            "B": ["one", "one", "two", "three", "two", "two", "one", "three"],
            "C": np.random.randn(8),
            "D": np.random.randn(8),
        }
    )


@pytest.fixture
def ts():
    return tm.makeTimeSeries()


@pytest.fixture
def tsd():
    return tm.getTimeSeriesData()


@pytest.fixture
def tsframe(tsd):
    return DataFrame(tsd)


@pytest.fixture
def df_mixed_floats():
    return DataFrame(
        {
            "A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"],
            "B": ["one", "one", "two", "three", "two", "two", "one", "three"],
            "C": np.random.randn(8),
            "D": np.array(np.random.randn(8), dtype="float32"),
        }
    )


@pytest.fixture
def three_group():
    return DataFrame(
        {
            "A": [
                "foo",
                "foo",
                "foo",
                "foo",
                "bar",
                "bar",
                "bar",
                "bar",
                "foo",
                "foo",
                "foo",
            ],
            "B": [
                "one",
                "one",
                "one",
                "two",
                "one",
                "one",
                "one",
                "two",
                "two",
                "two",
                "one",
            ],
            "C": [
                "dull",
                "dull",
                "shiny",
                "dull",
                "dull",
                "shiny",
                "shiny",
                "dull",
                "shiny",
                "shiny",
                "shiny",
            ],
            "D": np.random.randn(11),
            "E": np.random.randn(11),
            "F": np.random.randn(11),
        }
    )


@pytest.fixture()
def slice_test_df():
    data = [
        [0, "a", "a0_at_0"],
        [1, "b", "b0_at_1"],
        [2, "a", "a1_at_2"],
        [3, "b", "b1_at_3"],
        [4, "c", "c0_at_4"],
        [5, "a", "a2_at_5"],
        [6, "a", "a3_at_6"],
        [7, "a", "a4_at_7"],
    ]
    df = DataFrame(data, columns=["Index", "Group", "Value"])
    return df.set_index("Index")


@pytest.fixture()
def slice_test_grouped(slice_test_df):
    return slice_test_df.groupby("Group", as_index=False)


@pytest.fixture(params=sorted(reduction_kernels))
def reduction_func(request):
    """
    yields the string names of all groupby reduction functions, one at a time.
    """
    return request.param


@pytest.fixture(params=sorted(transformation_kernels))
def transformation_func(request):
    """yields the string names of all groupby transformation functions."""
    return request.param


@pytest.fixture(params=sorted(reduction_kernels) + sorted(transformation_kernels))
def groupby_func(request):
    """yields both aggregation and transformation functions."""
    return request.param


@pytest.fixture(params=[True, False])
def parallel(request):
    """parallel keyword argument for numba.jit"""
    return request.param


# Can parameterize nogil & nopython over True | False, but limiting per
# https://github.com/pandas-dev/pandas/pull/41971#issuecomment-860607472


@pytest.fixture(params=[False])
def nogil(request):
    """nogil keyword argument for numba.jit"""
    return request.param


@pytest.fixture(params=[True])
def nopython(request):
    """nopython keyword argument for numba.jit"""
    return request.param


@pytest.fixture(
    params=[
        ("mean", {}),
        ("var", {"ddof": 1}),
        ("var", {"ddof": 0}),
        ("std", {"ddof": 1}),
        ("std", {"ddof": 0}),
        ("sum", {}),
        ("min", {}),
        ("max", {}),
    ],
    ids=["mean", "var_1", "var_0", "std_1", "std_0", "sum", "min", "max"],
)
def numba_supported_reductions(request):
    """reductions supported with engine='numba'"""
    return request.param
