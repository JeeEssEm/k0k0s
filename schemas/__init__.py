from .users import *
from .auth import *
from .categories import *
from .items import *
from .orders import *
from .cart import *

CategoryItems.model_rebuild()  # noqa
Item.model_rebuild()  # noqa
Cart.model_rebuild()  # noqa
Order.model_rebuild()  # noqa
