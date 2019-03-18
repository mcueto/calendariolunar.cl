"""
lunarphases app utils.

----------------------
Code copied from: https://gist.github.com/miklb/ed145757971096565723
the position & phase methods are copied from the link above, and are created
by Sean B. Palmer, from inamidst.com

To the copied code, i have added translations using gettext to display it
correctly on different languages.
"""
import datetime
from astral import Astral
from dateutil.relativedelta import relativedelta
from django.utils.translation import gettext as _


def get_lunar_phasecode_from_day(day):
    phase_code = ''

    if day == 0:
        phase_code = 'new_moon'

    elif day >= 1 and day < 7:
        phase_code = 'waxing_crescent'

    elif day == 7:
        phase_code = 'first_quarter'

    elif day >= 8 and day < 14:
        phase_code = 'waxing_gibbous'

    elif day == 14:
        phase_code = 'full_moon'

    elif day >= 15 and day < 21:
        phase_code = 'waning_gibbous'

    elif day == 21:
        phase_code = 'last_quarter'

    elif day >= 22 and day <= 27:
        phase_code = 'waning_crescent'

    else:
        pass

    return phase_code


def get_lunar_phasename_from_code(code):
    phasenames = {
        'new_moon': _('New Moon'),
        'waxing_crescent': _('Waxing Crescent'),
        'first_quarter': _('First Quarter'),
        'waxing_gibbous': _('Waxing Gibbous'),
        'full_moon': _('Full Moon'),
        'waning_gibbous': _('Waning Gibbous'),
        'last_quarter': _('Last Quarter'),
        'waning_crescent': _('Waning Crescent'),
    }

    return phasenames[code]


def get_lunar_phase_data(reference_datetime=None):
    if reference_datetime is None:
        reference_datetime = datetime.datetime.now()

    astral = Astral()
    moon_phase_day = astral.moon_phase(
        date=reference_datetime
    )

    phase_code = get_lunar_phasecode_from_day(moon_phase_day)
    phase_name = get_lunar_phasename_from_code(phase_code)

    lunar_phase_data = {
        'datetime': reference_datetime,
        'code': phase_code,
        'name': phase_name,
        'moon_phase_day': moon_phase_day
    }

    return lunar_phase_data


def get_lunar_phase_tips(lunar_phase):

    PLANT_HARVERST_FLOWER_AND_FRUITS = {
        'title': _('Sow and harvest plants with flowers or fruits'),
        'message': _('It is advisable to plant and harvest those plants that we grow in order to take advantage of their flowers or fruits.')
    }

    PLANT_HARVERST_ROOTS_AND_LEAVES = {
        'title': _('Sow and harvest root or leaf plants'),
        'message': _('It is advisable to plant and harvest those plants that we grow in order to take advantage of their roots and leaves.')
    }

    HARVEST_FLOWER_AND_FRUITS = {
        'title': _('Harvest fruits or flowers'),
        'message': _('Today the moon is at its maximum power and all the sap is concentrated in the upper part of the plants, therefore it is a good day to harvest flowers or fruits that are ripe.')
    }

    HARVEST_ROOTS_AND_LEAVES = {
        'title': _('Harvest roots or leaves'),
        'message': _('Today all the sap is concentrated in the lower part of the plants, therefore it is a good day to harvest root and leaf plants.')
    }

    DONT_PRUNE = {
        'title': _('DO NOT perform pruning'),
        'message': _('It is not a good day to prune your plants, because it could suppose an unnecessary stress to them.'),
    }

    CAN_PRUNE = {
        'title': _('You can prune your plants'),
        'message': _('If you prune your plants today, they will respond better to pruning and cause less stress.'),
    }

    CAN_MAKE_CUTTINGS = {
        'title': _('You can make cuttings'),
        'message': _('If you make a cutting today, it will have more energy and therefore it will be more likely to root and generate a new plant.')
    }

    tips = {
        'new_moon': [
            HARVEST_ROOTS_AND_LEAVES,
        ],
        'waxing_crescent': [
            PLANT_HARVERST_FLOWER_AND_FRUITS,
            DONT_PRUNE,
        ],
        'first_quarter': [
            PLANT_HARVERST_FLOWER_AND_FRUITS,
            DONT_PRUNE,
        ],
        'waxing_gibbous': [
            PLANT_HARVERST_FLOWER_AND_FRUITS,
            DONT_PRUNE,
        ],
        'full_moon': [
            HARVEST_FLOWER_AND_FRUITS,
            CAN_MAKE_CUTTINGS,
        ],
        'waning_gibbous': [
            PLANT_HARVERST_ROOTS_AND_LEAVES,
        ],
        'last_quarter': [
            PLANT_HARVERST_ROOTS_AND_LEAVES,
            CAN_PRUNE,
        ],
        'waning_crescent': [
            PLANT_HARVERST_ROOTS_AND_LEAVES,
            CAN_PRUNE,
        ],
    }

    return tips[lunar_phase.code]


def get_following_moon_phase_day_delta(current_moon_phase_day):
    following_moon_phase_day_delta = 0

    if current_moon_phase_day % 7 == 0:
        following_moon_phase_day_delta = 1
    else:
        following_moon_phase_day_delta = 7 - (current_moon_phase_day % 7)

    return following_moon_phase_day_delta


def get_following_lunar_phases(reference_datetime=None,
                               following_phases_count=4):
    following_lunar_phases = []

    if reference_datetime is None:
        reference_datetime = datetime.datetime.now()

    # for following_phases_counter in range(0, following_phases_count):
    for following_phases_counter in range(0, following_phases_count):
        appended = False

        # While the following lunar phase is not appended
        while appended is False:
            current_lunar_phase = get_lunar_phase_data(reference_datetime)

            following_moon_phase_day_delta = get_following_moon_phase_day_delta(
                current_lunar_phase.get('moon_phase_day')
            )

            # Updates reference_datetime to the following lunar phase datetime
            reference_datetime = reference_datetime + relativedelta(
                days=following_moon_phase_day_delta
            )

            # Get following lunar phase
            following_lunar_phase = get_lunar_phase_data(reference_datetime)

            # If there are items on following_lunar_phases
            if len(following_lunar_phases) > 0:
                # If the current lunar phase is not the last
                # following_lunar_phases get_lunar_phasecode_from_day item, append it to the array
                if following_lunar_phases[-1].get('code') is not following_lunar_phase.get('code'):
                    following_lunar_phases.append(following_lunar_phase)
                    appended = True

            # If following_lunar_phases is empty
            else:
                following_lunar_phases.append(following_lunar_phase)
                appended = True

    return following_lunar_phases
