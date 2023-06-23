from cmath import nan
import pytz
import logging
from datetime import datetime as Date
from .time_utils import DateHelper, TimeHelper
from .utils import TextToInt, get_ner_prediction_text_new
from .rules.rules import RulesRefactored
from .event_list import EventExtraction
from .OffsetHelper import GrainUnitExtractionhindi,    \
                            GrainUnitExtractionbengali,  \
                            GrainUnitExtractionkannada, \
                            GrainUnitExtractionmalayalam, \
                            GrainUnitExtractionmarathi, \
                            GrainUnitExtractiontamil, \
                            GrainUnitExtractiontelugu, \
                            GrainUnitExtractionenglish, \
                            GrainUnitExtractiongujrati, \
                            GrainUnitExtractionpunjabi
                            # GrainUnitExtractionOriya

def postprocess_entities(utterance, labels, current_date=None, lang = 'hindi'):
    ner_out = get_ner_prediction_text_new(utterance.lower(), labels)
    logging.info(f'NER out: {ner_out}') 

    if current_date == None or current_date == nan:
        current_date = Date.now(pytz.timezone('Asia/Kolkata'))
    else:
        current_date = Date.strptime(current_date, '%d/%m/%Y %H:%M:%S')
        current_date = current_date.replace(tzinfo = pytz.timezone('Asia/Kolkata'))
    
    festival_bool = False
    
    for text in ner_out[0]:
        text = " " + text + " "
        eventExtraction = EventExtraction()
        date_festival = eventExtraction.extract_festivals(text, current_date, lang)
        if date_festival == -1:
            continue
        current_date = Date.strptime(date_festival, '%d/%m/%Y')
        current_date = current_date.replace(tzinfo = pytz.timezone('Asia/Kolkata'))
        festival_bool = True

    logging.info(f'Current date: {current_date}')
    post_ner = []
    temp = []
    current_max = -1
    for text in ner_out[0]:
        text = " " + text + " "   # Adding spaces to help convert_hindi_text_to_int function to work properly
        textToInt = TextToInt()  
        text = eval(f'textToInt.convert_{lang}_text_to_int(text)')
        logging.info(f'Convert {lang} to int: {text}')
        # dates = run_rules(text, current_date, lang)
        rulesRefactored = RulesRefactored()
        grainUnitExtraction = eval(f'GrainUnitExtraction{lang}()')
        due_date = grainUnitExtraction.extractDueDate(text)
        dates = rulesRefactored.DateFinder(text, due_date, current_date, lang, festival_bool)
        logging.info(f'Dates: {dates}')
        filtered_date, max_length = DateHelper.filter_dates(dates)
        if current_max < max_length:
            current_max = max_length
        else:
            continue
        logging.info(f'Filtered Dates: {filtered_date}')
        # print(date)
        if filtered_date == None:
            temp.append("none")
        else:
            temp.append(filtered_date)
        # print(temp)
    new_temp = []
    logging.info(f'Temp Dates: {temp}')
    for pred in temp:
        if pred != "none":
            new_temp.append(pred)
    # print(new_temp)
    logging.info(f'New Temp Dates: {new_temp}')
    if len(ner_out[1]) == 0 and len(new_temp) != 0:
        # logging.info(f'Final date value: {DateHelper.convert_datetime_to_string(min(new_temp))}')
        try:
            post_ner.append(DateHelper.convert_datetime_to_string(min(new_temp)))
            return {"date": post_ner, "time": []}
        except Exception as ex:
            if len(new_temp) == 0 and due_date == "due_date":
                return {"date": ["due_date"], "time": []}
            if min(new_temp) < 0:
                return {"date": ["due_date" + str(min(new_temp))], "time": []}
            else:
                return {"date": ["due_date+"+str(min(new_temp))], "time": []}
    if len(new_temp) != 0:
        date = min(new_temp)
        only_date = min(new_temp)
    else:
        date = current_date
        only_date = "none"
    temp = []
    for text in ner_out[1]:
        text = " " + text + " "   # Adding spaces to help convert_hindi_text_to_int function to work properly
        textToInt = TextToInt()  
        text = eval(f'textToInt.convert_{lang}_text_to_int(text)')
        # dates = run_rules_time(text, date, lang)
        rulesRefactored = RulesRefactored()
        dates = rulesRefactored.TimeFinder(text, date, lang)
        filtered_date = TimeHelper.filter_times(dates)
        if filtered_date == None:
            temp.append("none")
        else:
            temp.append(filtered_date)

    new_temp = []
    for pred in temp:
        if pred != "none":
            new_temp.append(pred)
    # print(new_temp)
    if len(new_temp) != 0:
        time = min(new_temp)
        time = TimeHelper.validate_time(time, text, lang = lang)
        post_ner.append(TimeHelper.convert_datetime_to_string(time))
        date = []
        try:
            date.append(DateHelper.convert_datetime_to_string(min(new_temp)))
            return {"date": date, "time": post_ner}
        except Exception as ex:
            if len(new_temp) == 0 and due_date == "due_date":
                return {"date": ["due_date"], "time": []}
            if min(new_temp) < 0:
                return {"date": ["due_date" + str(min(new_temp))], "time": post_ner}
            else:
                return {"date": ["due_date+"+str(min(new_temp))], "time": post_ner}
        # date.append(DateHelper.convert_datetime_to_string(min(new_temp)))
        # return {"date": date, "time": post_ner}
    else:
        try:
            date = []
            try:
                date.append(DateHelper.convert_datetime_to_string(only_date))
                return {"date": date, "time": []}
            except Exception as ex:
                if len(new_temp) == 0 and due_date == "due_date":
                    return {"date": ["due_date"], "time": []}
                if min(new_temp) < 0:
                    return {"date": ["due_date" + str(only_date)], "time": []}
                else:
                    return {"date": ["due_date+"+str(only_date)], "time": []}
        except:
            return {"date": [], "time": []}


if __name__=='__main__':
    text = "10 दिन के बाद में"
    entities = ["B-date", 'I-date', 'I-date', 'L-date']
    print(postprocess_entities(text, entities))
