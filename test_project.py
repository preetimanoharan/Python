import pandas as pd
import pytest
import matplotcheck.base as mpc
from unittest.mock import patch

from Python_project.project import get_input, subsetter, final

ildata=pd.read_csv('ildata.csv')

@pytest.mark.parametrize("mock_inputs, expected_exception",[
    (["Bacon", "4"], ValueError),  # Test case 1
    (["Macon", "3"], ValueError),  # Test case 2
    (["Bacon", "3"], ValueError),  # Test case 3
    (["Macon", "4"], None),  # Test case 4
    ])
def test_get_input(mock_inputs, expected_exception):
    with patch('builtins.input', side_effect=mock_inputs):
        if expected_exception is not None:
            with pytest.raises(ValueError):
                get_input()
        else:
            get_input()  # No exception expected

def test_subsetter():
    subset=subsetter("cook","4")
    assert all(value == "Cook County, IL" for value in subset["region_name"])
    assert all(value != "Macon County, IL" for value in subset["region_name"])
    assert all(value == "4 weeks" for value in subset["duration"])
    assert all(value != "12 weeks" for value in subset["duration"])
    assert all(value != "cook" for value in subset["region_name"])
    assert all(value != "1" for value in subset["duration"])
    assert len(subsetter("bacon","4")) == 0
    assert len(subsetter("macon","3")) == 0

def test_final_correct_input():
    axes=final("cook","4")
    plotcheck=mpc.PlotTester(axes)
    plotcheck.assert_plot_type("scatter")
    plotcheck.assert_title_contains(["Cook County, IL"])
    plotcheck.assert_axis_label_contains(axis="x", strings_expected=["period_time"])

def test_final_incorrect_input():
    with pytest.raises(ValueError):
        final("bacon","4")
    with pytest.raises(ValueError):
        final("bacon","3")
    with pytest.raises(ValueError):
        final("macon","3")
