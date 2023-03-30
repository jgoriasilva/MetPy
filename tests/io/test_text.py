# Copyright (c) 2021 MetPy Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
"""Test text handling functions."""
from datetime import datetime

import numpy as np
import shapely.geometry as sgeom

from metpy.cbook import get_test_data
from metpy.io import parse_wpc_surface_bulletin


def test_parse_wpc_surface_bulletin():
    """Test parser reading a WPC coded surface bulletin into a dataframe."""
    # Get rows 17 and 47 from dataframe representing parsed text file
    # Row 17 is a pressure center and row 47 is front
    input_file = get_test_data('WPC_sfc_fronts_20210628_1800.txt')
    df = parse_wpc_surface_bulletin(input_file)
    assert len(df) == 89
    assert len(df[df.feature == 'HIGH']) == 16
    assert len(df[df.feature == 'LOW']) == 24
    assert len(df[df.feature == 'TROF']) == 22

    assert df.feature[17] == 'LOW'
    assert df.strength[17] == 1002.0
    assert df.geometry[17] == sgeom.Point([-114.5, 34.4])

    assert df.feature[47] == 'STNRY'
    assert np.isnan(df.strength[47])
    assert df.geometry[47] == sgeom.LineString([[-100.5, 32.4], [-101.0, 31.9],
                                                [-101.9, 31.5], [-102.9, 31.2]])

    assert all(df.valid == datetime(2021, 6, 28, 18, 0, 0))
