import re
from .. import utils
from calendar import month
from ..time_utils import DateHelper, TimeHelper, DateHelperRefactor
from ..OffsetHelper import GrainUnitExtractionhindi,    \
                            GrainUnitExtractionbengali,  \
                            GrainUnitExtractionkannada, \
                            GrainUnitExtractionmalayalam, \
                            GrainUnitExtractionmarathi, \
                            GrainUnitExtractiontamil, \
                            GrainUnitExtractiontelugu, \
                            GrainUnitExtractionenglish
# from .rules_pattern import get_pattern_date, get_pattern_time
from .rules_pattern import Pattern


class RulesRefactored:

    def DateFinder(self, text, due_date, date, lang = "hindi", festival_bool = False):
        pattern = Pattern()
        dates = []
        patterns_dict = pattern.get_pattern_date(lang)
        for sequence in patterns_dict.values():
            pattern, offset_sequence, grain = sequence[0], sequence[1], sequence[2]
            pattern_text = re.findall(pattern, text)
            if len(pattern_text) == 0:
                dates.append(("No pattern found", 0))
                continue
            match_length = utils.get_match_length(pattern_text, lang)
            dateHelper = DateHelperRefactor(grain)
            dateHelper.update_offset(pattern_text, offset_sequence, lang)
            updatedDate, date_diff = dateHelper.update(date)
            if due_date == "due_date" or (date_diff!="none" and date_diff < 0 and festival_bool == False):
                dates.append((date_diff, match_length))
            else:
                dates.append((updatedDate, match_length))
        return dates

    def TimeFinder(self, text, date, lang = "hindi"):
        pattern = Pattern()
        dates = []
        patterns_dict = pattern.get_pattern_time(lang)
        for sequence in patterns_dict.values():
            pattern, offset_sequence, grain = sequence[0], sequence[1], sequence[2]
            pattern_text = re.findall(pattern, text)
            if len(pattern_text) == 0:
                dates.append("No pattern found")
                continue
            timeHelper = TimeHelper(grain)
            timeHelper.update_offset(pattern_text, offset_sequence, lang)
            dates.append(timeHelper.update(date))
        return dates
