import json
from importlib import resources
from opendrift.models.openoil import OpenOil

def test_set_oil_type_json():
    o = OpenOil(loglevel=50)

    d = json.loads(resources.read_text('opendrift.models.openoil.adios.extra_oils', 'AD03128.json'))

    o.set_oiltype_by_json(d)
    assert o.oiltype.name == 'VEGA CONDENSATE 2015'
    print(o.oiltype)

def test_set_oil_type_file():
    o = OpenOil(loglevel=50)

    with resources.path('opendrift.models.openoil.adios.extra_oils', 'AD03128.json') as f:
        o.set_oiltype_from_file(f)

    assert o.oiltype.name == 'VEGA CONDENSATE 2015'
    print(o.oiltype)

