module_path = r'D:\PCCS\01_Dmine\Scripts'
if module_path not in sys.path:
    sys.path.append(module_path)

from classes.Meta import Meta
from classes.test import test

ElMetadato = Meta

dir(ElMetadato)

ElMetadato.__class__
ElMetadato.__delattr__
ElMetadato.__dict__
ElMetadato.__dir__
ElMetadato.__doc__
ElMetadato.__eq__
ElMetadato.__format__
ElMetadato.__ge__
ElMetadato.__getattribute__
ElMetadato.__gt__
ElMetadato.__hash__
ElMetadato.__init__
ElMetadato.__init_subclass__
ElMetadato.__le__
ElMetadato.__lt__
ElMetadato.__module__
ElMetadato.__ne__
ElMetadato.__new__
ElMetadato.__reduce__
ElMetadato.__reduce_ex__
ElMetadato.__repr__
ElMetadato.__setattr__
ElMetadato.__sizeof__
ElMetadato.__str__
ElMetadato.__subclasshook__
ElMetadato.__weakref__
ElMetadato.fillmeta
ElMetadato.metafromds

import json

thejson = open(r'D:\testjson.json')
thejson = json.load(thejson)