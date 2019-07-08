# The ordering is important, don't move these around
from tests.models import (  # noqa
    CategoryModelCase,
    SensorModelCase,
    ReadingModelCase,
    UserModelCase,
)
from tests.api import (  # noqa
    CategoriesAPICase,
    SensorsAPICase,
    TokensAPICase,
    ReadingsAPICase,
    UsersAPICase,
)
