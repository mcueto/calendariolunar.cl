"""lunarphases."""
import datetime
from .utils import (
    get_lunar_phase_data,
)


class LunarPhase:
    """
    LunarPhase class.

    The LunarPhase class allows to easily instantiate *n* lunar phases given a
    datetime, if none is provided, the used datetime will be
    datetime.datetime.now()
    """

    def __init__(self, reference_datetime=None, fix_at_noon=True):
        """
        Initialize the current Lunar Phase instance.

        When datetime is None, datetime.datetime.now() will be used.
        """
        if reference_datetime is None:
            reference_datetime = datetime.datetime.now()

        if fix_at_noon:
            reference_datetime = reference_datetime.replace(
                hour=12,
                minute=0,
                second=0
            )

        lunar_phase_data = get_lunar_phase_data(
            reference_datetime
        )

        print(lunar_phase_data)

        self.datetime = lunar_phase_data.get('datetime')
        self.code = lunar_phase_data.get('code')
        self.name = lunar_phase_data.get('name')
        self.moon_phase_day = lunar_phase_data.get('moon_phase_day')
