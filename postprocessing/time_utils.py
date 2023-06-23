import pytz
import logging
import calendar
import datetime as Date
from datetime import timedelta
from .OffsetHelper import GrainUnitExtractionhindi, \
    GrainUnitExtractiontelugu, \
        GrainUnitExtractionmalayalam, \
            GrainUnitExtractiontamil, \
                GrainUnitExtractionkannada, \
                    GrainUnitExtractionmarathi, \
                        GrainUnitExtractionbengali, \
                            GrainUnitExtractionenglish, \
                                GrainUnitExtractionpunjabi, \
                                    GrainUnitExtractiongujrati


class DateHelper:
    
    def __init__(self, offset=None, grain=None):
        self.offset = offset
        self.grain = grain
        
    def validate_offset(self):
        if self.grain == "Day":
            if self.offset[0] <= 31 and self.offset[0]>=1:
                return True
            else:
                return False
    
    @staticmethod
    def convert_datetime_to_string(date):
        logging.info(f"Convert datetime to string: {date}")
        datestring = date.strftime("%d/%m/%Y")
        logging.info(f'Datestring: {datestring}')
        return datestring
    
    def validate_dates(self, day, month, year):
        return day.replace(day = calendar.monthrange(year, month)[1], month = month, year = year)
    
    def update(self, time_to_update):
        if self.grain == "Day":
            try:
                return time_to_update + timedelta(days=self.offset[0])
            except ValueError as err:
                day = time_to_update.day + self.offset[0]
                month = time_to_update.month 
                year = time_to_update.year
                return self.validate_dates(time_to_update, month, year)
        elif self.grain == "Date":
            date = time_to_update.day
            month = time_to_update.month
            year = time_to_update.year
            month_extracted = 0
            if len(self.offset) == 3:
                if self.offset[2] != -1:
                    year = self.offset[2]
            if len(self.offset) >= 2:
                if self.offset[1] != -1:
                    month = self.offset[1]
                    month_extracted = 1
            if self.offset[0] != -1 and self.offset[0] != "last_day":
                date = self.offset[0]
            elif self.offset[0] == -1:
                date = 1
            elif self.offset[0] == "last_day":
                date = calendar.monthrange(year, month)[1]
            if month_extracted == 1 and month == time_to_update.month and self.offset[0] in [-1,"last_day"]:
                date = calendar.monthrange(year, month)[1]
            if date < time_to_update.day and month == time_to_update.month and month_extracted == 0:
                if month + 1 > 12:
                    month = 1
                    year += 1
                else: 
                    month = month + 1
            elif date == time_to_update.day:
                date = time_to_update.day
            try:
                response = time_to_update.replace(day = date, month = month, year = year)
            except ValueError as err:
                response = self.validate_dates(time_to_update, month, year)
            if response < time_to_update:
                return response.replace(year = year + 1)
            else:
                return response
            # if len(self.offset) > 1:
            #     try:
            #         # return time_to_update.replace(day=self.offset[0], month = self.offset[1]) 
            #         try:
            #             year = self.offset[2]
            #             response = time_to_update.replace(day=self.offset[0], month = self.offset[1], year = year) 
            #             return response
            #         except Exception as ex:
            #             year = time_to_update.year
            #         if self.offset[0] == -1:
            #             self.offset[0] = 1
            #         response = time_to_update.replace(day=self.offset[0], month = self.offset[1], year = year) 
            #         year = time_to_update.year
            #         if response < time_to_update:
            #             return response.replace(year = year + 1)
            #         else:
            #             return response
            #     except ValueError as err:
            #         day = self.offset[0]
            #         month = self.offset[1]
            #         year = time_to_update.year
            #         return self.validate_dates(day, month, year)
            # elif date > self.offset[0]:
            #     current_month = time_to_update.month
            #     year = time_to_update.year
            #     try:
            #         if current_month + 1 > 12:
            #             current_month = 1
            #             year += 1
            #         else: 
            #             current_month = current_month + 1
            #         response = time_to_update.replace(day=self.offset[0], month = current_month, year = year) 
            #         if response < time_to_update:
            #             return response.replace(year = year + 1)
            #         else:
            #             return response
            #     except ValueError as err:
            #         day = self.offset[0]
            #         month = current_month + 1
            #         year = time_to_update.year
            #         return self.validate_dates(day, month, year)
            # elif date == self.offset:
            #     return time_to_update
            # else:
            #     try:
            #         return time_to_update.replace(day=self.offset[0]) 
            #     except ValueError as err:
            #         day = self.offset[0]
            #         month = time_to_update.month 
            #         year = time_to_update.year
            #         return self.validate_dates(day, month, year)
        elif self.grain == "Month":
            date = time_to_update
            month = date.month + self.offset[0]
            year = time_to_update.year
            if month > 12:
                month = month - 12
                year = year + 1
            if len(self.offset)>1:
                if self.offset[1] == "first_day":
                    return date.replace(day = 1, month = month, year = year)
                else:
                    try:
                        return date.replace(day = self.offset[1], month = month, year = year)
                    except Exception as ex:
                        return date.replace(day = calendar.monthrange(date.year, month)[1], month = month, year = year)
            else:
                return date.replace(day = calendar.monthrange(date.year, month)[1], month = month, year = year)
        elif self.grain == "Week":
            date = time_to_update
            current_week = date.isoweekday()
            if current_week >= self.offset[0]:         # TODO issue
                day_diff = 7*self.offset[1] - (current_week - self.offset[0])
            else:
                day_diff = self.offset[0] - current_week
            return date + timedelta(days=day_diff)

        elif self.grain == "Hour":
            return time_to_update

        elif self.grain == "Quarter":
            return time_to_update

    @staticmethod
    def filter_dates(dates_list):
        valid_list = []
        for dates in dates_list:
            if dates[0] != 'No pattern found' and dates[0] != "Invalid date":
                valid_list.append(dates)

        m = -1000000000
        response = []

        for dates in valid_list:
            if dates[1] > m:
                m = dates[1]
                response = [dates[0]]
            elif dates[1] == m:
                m = dates[1]
                response.append(dates[0])

        if len(response) == 0:
            return None, -1
        return min(response), m


class DateHelperRefactor:

    def __init__(self, grain=None, offset=None):
        self.offset = offset
        self.grain = grain
        
    def validate_offset(self):
        if self.grain == "Day":
            if self.offset[0] <= 31 and self.offset[0]>=1:
                return True
            else:
                return False
    
    @staticmethod
    def convert_datetime_to_string(date):
        logging.info(f"Convert datetime to string: {date}")
        datestring = date.strftime("%d/%m/%Y")
        logging.info(f'Datestring: {datestring}')
        return datestring
    
    def validate_dates(self, day, month, year):
        return day.replace(day = calendar.monthrange(year, month)[1], month = month, year = year)
    
    def update(self, time_to_update):
        if self.grain == "Day":
            try:
                if "mod" in self.offset:
                    mod = self.offset["mod"]
                else:
                    mod = 1
                if "int" in self.offset:
                    if type(self.offset["int"]) == int:
                        return time_to_update + timedelta(days=self.offset["int"]*mod), self.offset["int"]*mod
                if "future_mod" in self.offset:
                    if type(self.offset["future_mod"]) == int:
                        return time_to_update + timedelta(days = self.offset["future_mod"]*mod), self.offset["future_mod"]*mod
            except ValueError as err:
                month = time_to_update.month 
                year = time_to_update.year
                return self.validate_dates(time_to_update, month, year), self.offset["int"]*mod
        elif self.grain == "Date":
            date = time_to_update.day
            month = time_to_update.month
            year = time_to_update.year
            if "year" in self.offset:
                if type(self.offset["year"]) == int:
                    year = self.offset["year"]
            if "month" in self.offset:
                if type(self.offset["month"]) == int:
                    month = self.offset["month"]
            if "int" in self.offset:
                if type(self.offset["int"]) == int:
                    date = self.offset["int"]
            elif "int" not in self.offset:
                if "end" in self.offset and self.offset["end"] == 1:
                    date = calendar.monthrange(year, month)[1]
                else:
                    date = 1
            if "int" not in self.offset and month == time_to_update.month:
                date = calendar.monthrange(year, month)[1]
            if date < time_to_update.day and month == time_to_update.month and "month" not in self.offset:
                if month + 1 > 12:
                    month = 1
                    year += 1
                else: 
                    month = month + 1
            elif date == time_to_update.day:
                date = time_to_update.day
            try:
                response = time_to_update.replace(day = date, month = month, year = year)
            except ValueError as err:
                response = self.validate_dates(time_to_update, month, year)
            if response < time_to_update:
                return response.replace(year = year + 1), "none"
            else:
                return response, "none"
        elif self.grain == "Month":
            date = time_to_update
            month = date.month
            if "mod" in self.offset:
                mod = self.offset["mod"]
            else:
                mod = 1
            if "future_mod" in self.offset:
                if type(self.offset["future_mod"]) == int:
                    month = date.month + self.offset["future_mod"]*mod
            if "future_mod" not in self.offset and "int" in self.offset:
                if type(self.offset["int"]) == int:
                    month = date.month + self.offset["int"]*mod
            year = time_to_update.year
            if month > 12:
                year = year + (month)//12
                if month%12 != 0:
                    month = month%12
                else:
                    month = 12
            try:
                if "int" in self.offset and "future_mod" in self.offset:
                    if type(self.offset["int"]) == int:                
                        day = self.offset["int"]
                else:
                    if "end" in self.offset:
                        day = calendar.monthrange(date.year, month)[1]
                    else:
                        day = 1
                return date.replace(day = day, month = month, year = year), "none"
            except Exception as ex:
                return date.replace(day = calendar.monthrange(date.year, month)[1], month = month, year = year), "none"
        elif self.grain == "Week":
            date = time_to_update
            current_week = date.isoweekday()
            if "mod" in self.offset:
                mod = self.offset["mod"]
            else:
                mod = 1
            if "end" in self.offset:
                if current_week == 7:
                    if "int" in self.offset:
                        day_diff = 7*(self.offset["int"]+1)*mod
                    if "future_mod" in self.offset:
                        day_diff = 7*self.offset["future_mod"]*mod
                else:
                    if "int" in self.offset:
                        day_diff = 7*(self.offset["int"]+1)*mod - current_week
                    if "future_mod" in self.offset:
                        day_diff = 7*self.offset["future_mod"]*mod - current_week
            if "weekday" not in self.offset and "end" not in self.offset:
                if "int" in self.offset:
                    day_diff = 7*self.offset["int"]*mod
                if "future_mod" in self.offset:
                    day_diff = 7*self.offset["future_mod"]*mod
            elif "weekday" in self.offset and "end" not in self.offset:
                if current_week >= self.offset["weekday"]: 
                    if "future_mod" in self.offset:         
                        day_diff = 7*self.offset["future_mod"] - (current_week - self.offset["weekday"])
                    if "int" in self.offset:
                        day_diff = 7*self.offset["int"] - (current_week - self.offset["weekday"])
                else:
                    day_diff = self.offset["weekday"] - current_week
            return date + timedelta(days=day_diff), day_diff
        elif self.grain == "Year":
            if "future_mod" in self.offset:
                if type(self.offset["future_mod"]) == int:
                    day_to_increase = 365*self.offset["future_mod"]
            if "int" in self.offset:
                if type(self.offset["int"]) == int:
                    day_to_increase = 365*int(self.offset["int"])
            return time_to_update + timedelta(days = day_to_increase), day_to_increase
        elif self.grain == "MonthWeek":  # ["future_mod1"->for month, "int", "weekday", "mod"]
            date = time_to_update
            month = date.month
            if "mod" in self.offset:
                mod = self.offset["mod"]
            else:
                mod = 1
            if "future_mod" in self.offset:
                if type(self.offset["future_mod"]) == int:
                    month = date.month + self.offset["future_mod"]
            year = time_to_update.year
            if month > 12:
                year = year + (month)//12
                if month%12 != 0:
                    month = month%12
                else:
                    month = 12
            try:
                day = 1
                date = date.replace(day = day, month = month, year = year)
                current_week = date.isoweekday()
                if current_week >= self.offset["weekday"]: 
                    if "int" in self.offset:
                        day_diff = 7*self.offset["int"] - (current_week - self.offset["weekday"])
                    else:
                        day_diff = 7 - (current_week - self.offset["weekday"])
                else:
                    day_diff = self.offset["weekday"] - current_week
                return date + timedelta(days=day_diff), "none"
            except Exception as ex:
                return date.replace(day = 1, month = month, year = year), "none"

    def update_offset(self, text, sequence_list, lang):
        try:
            offset = {}
            if "int" in sequence_list:
                grainUnitExtraction = eval(f'GrainUnitExtraction{lang}()')
                int_extracted = grainUnitExtraction.extractInt(text)
                if int_extracted != -1:
                    offset["int"] = int_extracted  
            if "month" in sequence_list:
                grainUnitExtraction = eval(f'GrainUnitExtraction{lang}()')
                month_extracted = grainUnitExtraction.extractMonth(text)
                if month_extracted != "":
                    offset["month"] = month_extracted  
            if "weekday" in sequence_list:
                grainUnitExtraction = eval(f'GrainUnitExtraction{lang}()')
                weekday_extracted = grainUnitExtraction.extractWeekday(text)
                if weekday_extracted != "":
                    offset["weekday"] = weekday_extracted
            if "future_mod0" in sequence_list:
                grainUnitExtraction = eval(f'GrainUnitExtraction{lang}()')
                future_mod = grainUnitExtraction.extractInt(["future_mod0"])
                if future_mod != -1:
                    offset["future_mod"] = future_mod
            if "future_mod1" in sequence_list:
                grainUnitExtraction = eval(f'GrainUnitExtraction{lang}()')
                future_mod = grainUnitExtraction.extractInt(["future_mod1"])
                if future_mod != -1:
                    offset["future_mod"] = future_mod
            if "future_mod2" in sequence_list:
                grainUnitExtraction = eval(f'GrainUnitExtraction{lang}()')
                future_mod = grainUnitExtraction.extractInt(["future_mod2"])
                if future_mod != -1:
                    offset["future_mod"] = future_mod
            if "mod" in sequence_list:
                grainUnitExtraction = eval(f'GrainUnitExtraction{lang}()')
                mod = grainUnitExtraction.extractTimeModule(text)
                if mod != "":
                    offset["mod"] = mod
            if "end" in sequence_list:
                offset["end"] = 1
            self.offset = offset
            return offset 
        except Exception as ex:
            return -1

    @staticmethod
    def filter_dates(dates_list):
        valid_list = []
        for dates in dates_list:
            if dates[0] != 'No pattern found' and dates[0] != "Invalid date":
                valid_list.append(dates)

        m = -1
        response = []

        for dates in valid_list:
            if dates[1] > m:
                m = dates[1]
                response = [dates[0]]
            elif dates[1] == m:
                m = dates[1]
                response.append(dates[0])

        if len(response) == 0:
            return None
        return min(response)


class TimeHelper:
    
    def __init__(self, grain, offset = None):
        self.offset = offset
        self.grain = grain
    
    @staticmethod
    def convert_datetime_to_string(date):
        return date.strftime("%H:%M")
    
    @staticmethod
    def validate_time(date, text, lang="hindi"):
        hour = date.hour
        grainUnitExtraction = eval(f'GrainUnitExtraction{lang}()')
        meridiam = grainUnitExtraction.extractMeridiam(text)
        time = grainUnitExtraction.extractDaytime([text])
        if (time in [12, 18, 20] or meridiam == 2) and hour != time and hour < 12:
            hour += 12
            if hour >= 24:
                hour = 23
        date = date.replace(hour = hour)
        return date

    
    def validate_dates(self, day, month, year):
        return day.replace(day = calendar.monthrange(year, month)[1], month = month, year = year)
    
    def update(self, time_to_update):
        response = time_to_update
        if self.grain == "relative_time":
            if "hour" in self.offset and self.offset["hour"] != -1:
                try:
                    response = response + timedelta(hours = self.offset["hour"])
                except Exception as ex:
                    pass
            return response
        elif self.grain == "relative_minute":
            if "minute" in self.offset and self.offset["minute"] != -1:
                try:
                    response = response + timedelta(minutes = self.offset["minute"])
                except Exception as ex:
                    pass
            return response
        elif self.grain == "exact_time":
            if self.offset["meridiam"] != -1:
                response =  response
            if "minute" in self.offset and self.offset["minute"]!=-1:
                try:
                   response = response.replace(minute = self.offset["minute"])
                except Exception as ex:
                    pass
            else:
                response = response.replace(minute = 0)
            if "hour" in self.offset and self.offset["hour"] != -1:
                try:
                    response = response.replace(hour = self.offset["hour"])
                    # response = response.replace(minute = 0)
                except Exception as ex:
                    pass
            return response
        elif self.grain == "exact_minute":
            try:
                return response + timedelta(minutes = self.offset["minute"])
            except Exception as ex:
                pass
        elif self.grain == "daytime":
            try:
                if self.offset["daytime"] == -1:
                    return response
                return response.replace(hour = self.offset["daytime"], minute = 0)
            except Exception as ex:
                pass

    @staticmethod
    def filter_times(dates_list):
        valid_list = []
        for dates in dates_list:
            if dates != 'No pattern found' and dates != "Invalid date":
                valid_list.append(dates)
        if len(valid_list) == 0:
            return None
        return min(valid_list)

    def update_offset(self, text, sequence_list, lang):
        try:
            offset = {}
            if "hour" in sequence_list:
                # idx = sequence_list.index("exact_time")
                grainUnitExtraction = eval(f'GrainUnitExtraction{lang}()')
                hour = grainUnitExtraction.extractInt(text)
                if hour == -1:
                    offset["hour"] = 1
                else:
                    offset["hour"] = hour
            if "meridiam" in sequence_list:
                # idx = sequence_list.index("meridiam")
                grainUnitExtraction = eval(f'GrainUnitExtraction{lang}()')
                text = " ".join(text[0])
                offset["meridiam"] = grainUnitExtraction.extractMeridiam(text)
            if "minute" in sequence_list:
                # idx = sequence_list.index("exact_minute")
                grainUnitExtraction = eval(f'GrainUnitExtraction{lang}()')
                offset["minute"] = grainUnitExtraction.extractIntPos(text, 0)
            if "hour" in sequence_list and "minute" in sequence_list:
                grainUnitExtraction = eval(f'GrainUnitExtraction{lang}()')
                offset["minute"] = grainUnitExtraction.extractIntPos(text, 1)
            if "daytime" in sequence_list:
                grainUnitExtraction = eval(f'GrainUnitExtraction{lang}()')
                offset["daytime"] = grainUnitExtraction.extractDaytime(text)
            self.offset = offset
            return offset 
        except Exception as ex:
            return -1
        