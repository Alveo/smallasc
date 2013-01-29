# Unfortunately this is required because some of the manage.py scripts
# look for these imports such as syncdb
from baseapp.modelspackage.animals import Animal
from baseapp.modelspackage.colours import Colour