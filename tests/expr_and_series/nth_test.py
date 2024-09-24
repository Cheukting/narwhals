from __future__ import annotations

import polars as pl
import pytest

import narwhals.stable.v1 as nw
from narwhals.utils import parse_version
from tests.utils import Constructor
from tests.utils import compare_dicts

data = {"a": [1, 3, 2], "b": [4, 4, 6], "z": [7.1, 8, 9]}


@pytest.mark.parametrize(
    ("idx", "expected"),
    [
        (0, {"a": [1, 3, 2]}),
        ([0, 1], {"a": [1, 3, 2], "b": [4, 4, 6]}),
        ([0, 2], {"a": [1, 3, 2], "z": [7.1, 8, 9]}),
    ],
)
def test_nth_not_polars(
    not_polars_constructor: Constructor,
    idx: int | list[int],
    expected: dict[str, list[int]],
) -> None:
    df = nw.from_native(not_polars_constructor(data))
    result = df.select(nw.nth(idx))
    compare_dicts(result, expected)


@pytest.mark.xfail(
    parse_version(pl.__version__) < parse_version("0.20.26"),
    reason="nth not supported for Polars versions < 0.20.26",
)
@pytest.mark.parametrize(
    ("idx", "expected"),
    [
        (0, {"a": [1, 3, 2]}),
        ([0, 1], {"a": [1, 3, 2], "b": [4, 4, 6]}),
        ([0, 2], {"a": [1, 3, 2], "z": [7.1, 8, 9]}),
    ],
)
def test_nth_polars(
    polar_constructor: Constructor, idx: int | list[int], expected: dict[str, list[int]]
) -> None:
    df = nw.from_native(polar_constructor(data))
    result = df.select(nw.nth(idx))
    compare_dicts(result, expected)


@pytest.mark.skipif(
    parse_version(pl.__version__) >= parse_version("0.20.26"),
    reason="only riase error for Polars versions < 0.20.26",
)
def test_nth_not_supported() -> None:
    df = nw.from_native(pl.DataFrame(data))
    with pytest.raises(
        AttributeError, match="`nth` is only supported for Polars>=0.20.26."
    ):
        df.select(nw.nth(0))
