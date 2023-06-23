from calendar import SATURDAY, month, week
import re


class GrainUnitExtractionhindi:
    
    def extractIntPos(self, text, i):
        try:
            text = " ".join(text[0]).strip()
            temp = re.findall(r'\d+', text)
            temp = list(map(int, temp))
            return temp[i]
        except Exception as ex:
            return -1

    def extractInt(self, text):
        text = " ".join(text[0]).strip()
        temp = re.findall(r'\d+', text)
        if len(temp) == 0:
            return -1
        temp = list(map(int, temp))
        return temp[0]

    def extractMonth(self, text):
        text = " ".join(text[0])
        january = re.search(r'जनवरी|january', text)
        if january != None and january.group() == "":
            return 1
        febuary = re.search(r'फरवरी|फेब्रुअरी|फेब्रुवारी|february', text)
        if febuary != None and febuary.group() != "":
            return 2
        march = re.search(r'मार्च|march', text)
        if march != None and march.group() != "":
            return 3
        april = re.search(r'अप्रैल|april', text)
        if april != None and april.group != "":
            return 4
        may = re.search(r'मई|may', text)
        if may != None and may.group() != "":
            return 5
        june = re.search(r'जून|june', text)
        if june != None and june.group() != "":
            return 6
        july = re.search(r'जुलाई|july', text)
        if july != None and july.group() != "":
            return 7
        august = re.search(r'अगस्त|august', text)
        if august != None and august.group() != "":
            return 8
        september = re.search(r'सितम्बर|सितम्बर|सितंबर|सप्टेंबर|सेप्टेम्बर|सेप्तेम्बर|सेप्टैंबर|september', text)
        if september != None and september.group() != "":
            return 9
        october = re.search(r'अक्टूबरी|अक्टूबर|october', text)
        if october != None and october.group() != "":
            return 10
        november = re.search(r'नवंबर|november', text)
        if november != None and november.group() != "":
            return 11
        december = re.search(r'दिसंबर|december', text)
        if december != None and december.group() != "":
            return 12
        return ""

    def extractWeekday(self, text):
        text = " ".join(text[0])
        monday = re.search(r'सोमवार|मंडे|monday', text)
        if monday != None and monday.group() != "":
            return 1
        tuesday = re.search(r'मंगलवार|ट्यूसडे|tuesday', text)
        if tuesday != None and tuesday.group() != "":
            return 2
        webnesday = re.search(r'बुधवार|वेनसडे|वेडनेसडे|wednesday', text)
        if webnesday != None and webnesday.group() != "":
            return 3
        thursday = re.search(r'गुरुवार|थर्सडे|thursday', text)
        if thursday != None and thursday.group() != "":
            return 4
        friday = re.search(r'शुक्रवार|फ्राइडे|friday', text)
        if friday != None and friday.group() != "":
            return 5
        saturday = re.search(r'शनिवार|सैटरडे|सेटरडे|saturday', text)
        if saturday != None and saturday.group() != "":
            return 6
        sunday = re.search(r'रविवार|संडे|sunday', text)
        if sunday != None and sunday.group() != "":
            return 7
        return ""

    def extractMeridiam(self, text):
        # text = " ".join(text[0])
        a = re.search(r'ऍम|पीऍम|पीएम|ऐम|am|pm|a.m.|p.m.', text)
        if a == None or a.group() == "":
            return ""
        meridiam = a.group()
        if meridiam == "ऍम" or meridiam == "ऐम" or meridiam == "am" or meridiam == "a.m.":
            return 1
        elif meridiam == "पीऍम" or meridiam == "पीएम" or meridiam == "pm" or meridiam == "p.m.":
            return 2
        else:
            return -1

    def extractDaytime(self, text):
        # text = " ".join(text[0])
        text = text[0]
        a = re.search(r'शाम|इवनिंग|रात|नाईट|सुबह|मॉर्निंग|आफ्टरनून|दोपहर|तुरंत|सेकंड|अभी|night|tonight|morning|afternoon|evening', text)
        if a == None or a.group() == "":
            return ""
        day_time = a.group()
        if day_time == "शाम" or day_time == "इवनिंग" or day_time == "evening":
            return 18
        elif day_time == "रात" or day_time == "नाईट" or day_time == "night" or day_time == "tonight":
            return 20
        elif day_time == "सुबह" or day_time == "मॉर्निंग" or day_time == "morning":
            return 10
        elif day_time == "आफ्टरनून" or day_time == "दोपहर" or day_time == "afternoon":
            return 12
        elif day_time == "तुरंत" or day_time == "सेकंड" or day_time == "अभी":
            return -1
        else:
            return ""

    def extractTimeModule(self, text):
        text = " ".join(text[0])
        before = re.search(r'पहले|before', text)
        if before != None and before.group() != "":
            return -1
        after = re.search(r'बाद|later', text)
        if after != None and after.group() != "":
            return 1
        return ""

    def extractDueDate(self, text):
        # text = " ".join(text[0])
        due_date = re.search(r'ड्यू डेट|ड्यूटी|देय डेट|due date', text)
        if due_date != None and due_date.group() != "":
            return "due_date"
        return ""

class GrainUnitExtractionmarathi:
    
    def extractIntPos(self, text, i):
        try:
            text = " ".join(text[0]).strip()
            temp = re.findall(r'\d+', text)
            temp = list(map(int, temp))
            return temp[i]
        except Exception as ex:
            return -1

    def extractInt(self, text):
        text = " ".join(text[0]).strip()
        temp = re.findall(r'\d+', text)
        if len(temp) == 0:
            return -1
        temp = list(map(int, temp))
        return temp[0]

    def extractMonth(self, text):
        text = " ".join(text[0])
        a = re.search(r'जनवरी|जानेवारी|january|फरवरी|फेब्रुअरी|february|मार्च|march|अप्रैल|एप्रिल|april|मई|मे|may|जून|june|जुलाय|जुलाई|july|अगस्त|ऑगस्ट|august|सितम्बर|सितंबर|सेप्टेंबर|सप्टेंबर|सेप्टेम्बर|सेप्तेम्बर|सेप्टैंबर|september|अक्टूबर|ऑक्टोबर|october|नवंबर|नोव्हेंबर|november|दिसंबर|डिसेंबर|december', text)
        if a == None or a.group() == "":
            return ""
        month_group = a.group()
        if month_group == "जनवरी" or month_group == 'जानेवारी' or month_group == 'january':
            return 1
        elif month_group == "फरवरी" or month_group == "फेब्रुअरी" or month_group == 'february':
            return 2
        elif month_group == "मार्च" or month_group == 'march':
            return 3
        elif month_group == "अप्रैल" or month_group == 'एप्रिल' or month_group == 'april':
            return 4
        elif month_group == "मई" or month_group == 'मे' or month_group == 'may':
            return 5
        elif month_group == "जून" or month_group == 'june':
            return 6
        elif month_group == "जुलाई" or month_group == 'जुलाय' or month_group == 'july':
            return 7
        elif month_group == "अगस्त" or month_group == 'ऑगस्ट' or month_group == 'august':
            return 8
        elif month_group == "सितम्बर" or month_group == "सितंबर" or month_group == "सप्टेंबर" \
                                    or month_group == 'सेप्टेंबर' or month_group == "सेप्टेम्बर" \
                                    or month_group == "सेप्तेम्बर" or month_group == "सेप्टैंबर" \
                                    or month_group == 'september':
            return 9
        elif month_group == "अक्टूबर" or month_group == "ऑक्टोबर" or month_group == 'october':
            return 10
        elif month_group == "नवंबर" or month_group == 'नोव्हेंबर' or month_group == 'november':
            return 11
        elif month_group == "दिसंबर" or month_group == 'डिसेंबर' or month_group == 'december':
            return 12
        else:
            return ""

    def extractWeekday(self, text):
        text = " ".join(text[0])
        a = re.search(r'सोमवार|सोमवारी|मंडे|monday|मंगळवार|मंगळवारी|ट्यूसडे|tuesday|बुधवार|बुधवारी|वेडनेसडे|wednesday|गुरुवार|गुरुवारी|थर्सडे|thursday|शुक्रवार|शुक्रवारी|फ्राइडे|friday|शनिवार|शनिवारी|सैटरडे|saturday|रविवार|रविवारी|संडे|sunday', text)
        if a == None or a.group() == "":
            return ""
        week_group = a.group()
        if week_group == "सोमवार" or week_group == 'सोमवारी' or week_group == "मंडे" or week_group == 'monday':
            return 1
        elif week_group == "मंगळवार" or week_group == 'मंगळवारी' or week_group == "ट्यूसडे" or week_group == 'tuesday':
            return 2
        elif week_group == "बुधवार" or week_group == 'बुधवारी' or week_group == "वेडनेसडे" or week_group == 'wednesday':
            return 3
        elif week_group == "गुरुवार" or week_group == 'गुरुवारी' or week_group == "थर्सडे" or week_group == 'thursday':
            return 4
        elif week_group == "शुक्रवार" or week_group == 'शुक्रवारी' or week_group == "फ्राइडे" or week_group == 'friday':
            return 5
        elif week_group == "शनिवार" or week_group == 'शनिवारी' or week_group == "सैटरडे" or week_group == 'saturday':
            return 6
        elif week_group == "रविवार" or week_group == 'रविवारी' or week_group == "संडे" or week_group == 'sunday':
            return 7
        else:
            return ""

    def extractMeridiam(self, text):
        # text = " ".join(text[0])
        a = re.search(r'ऍम|पीऍम|पीएम|ऐम', text)
        if a == None or a.group() == "":
            return ""
        meridiam = a.group()
        if meridiam == "ऍम" or meridiam == "ऐम":
            return 1
        elif meridiam == "पीऍम" or meridiam == "पीएम":
            return 2
        else:
            return -1

    def extractDaytime(self, text):
        # text = " ".join(text[0])
        text = text[0]
        a = re.search(r'संध्याकाळ|संध्याकाळी|संध्याकाळपर्यंत|इवनिंग|रात्र|रात्री|रात्रीपर्यंत|नाईट|सकाळ|सकाळी|मॉर्निंग|दुपार|दुपारी|आफ्टरनून|ताबडतोब|तुरंत|आता|लगेच', text)
        if a == None or a.group() == "":
            return ""
        day_time = a.group()
        if day_time == "संध्याकाळ" or day_time == "संध्याकाळी" or day_time == 'संध्याकाळपर्यंत' or day_time == 'इवनिंग':
            return 18
        elif day_time == "रात्र" or day_time == "रात्री" or day_time == 'रात्रीपर्यंत' or day_time == 'नाईट':
            return 20
        elif day_time == "सकाळ" or day_time == "सकाळी" or day_time == 'मॉर्निंग':
            return 10
        elif day_time == "दुपार" or day_time == "दुपारी" or day_time == 'आफ्टरनून':
            return 12
        elif day_time == "ताबडतोब" or day_time == "तुरंत" or day_time == "आता" or day_time == 'लगेच':
            return -1
        else:
            return ""

    def extractTimeModule(self, text):
        text = " ".join(text[0])
        before = re.search(r'आधी|च्या आधी|च्याधी|पहले|च्या पहले|च्याप्ले|च्यापले|अगोदर|च्या अगोदर|च्यागोदर|आगोदर', text)
        if before != None and before.group() != "":
            return -1
        after = re.search(r'नंतर|च्या नंतर', text)
        if after != None and after.group() != "":
            return 1
        return ""

    def extractDueDate(self, text):
        # text = " ".join(text[0])
        due_date = re.search(r'देय तारीख|देतारीख|देया तारीख|ड्यू डेट', text)
        if due_date != None and due_date.group() != "":
            return "due_date"
        return ""

class GrainUnitExtractiontelugu:
    
    def extractIntPos(self, text, i):
        try:
            text = " ".join(text[0]).strip()
            temp = re.findall(r'\d+', text)
            temp = list(map(int, temp))
            return temp[i]
        except Exception as ex:
            return -1

    def extractInt(self, text):
        text = " ".join(text[0]).strip()
        temp = re.findall(r'\d+', text)
        if len(temp) == 0:
            return -1
        temp = list(map(int, temp))
        return temp[0]

    def extractMonth(self, text):
        text = " ".join(text[0]) 
        a = re.search(r'జాన్|మొదటి నెల|జనుఅరీ|జనవరి|january|ఫిబ్రవరి|ఫెబ్|రెండో నెల|రెండొ నెల|february|మార్చ్|మర్చి|మూడో నెల|మూడొ నెల|మార్చి|march|మార్|ఏప్రిల్|ఏప్రెల్|నాల్గో నెల|నాలుగో నెల|నాలుగొ నెల|నాల్గొ నెల|april|మే|ఐదో నెల|ఐదొ నెల|may|జూన్|ఆరో నెల|ఆరొ నెల|june|జులై|ఏడో నెల|july|ఎడొ నెల|ఆగష్టు|అగస్ట్|ఆగస్ట్|ఎనిమిదో నెల|august|ఎనిమిదొ నెల|ఆగస్టు|అగష్టు|సెప్టెంబర్|తొమ్మిదో నెల|తొమ్మిదొ నెల|september|అక్టోబర్|అక్టోబరు|పదో నెల|పదొ నెల|october|నవంబర్|పదకొండొ నెల|పదకొండో నెల|november|నవెంబర్|డిసెంబరు|డెక్|డిసెంబర్|పన్నెండో నెల|పన్నెండొ నెల|december', text)
        if a == None or a.group() == "":
            return ""
        month_group = a.group()
        if month_group == "జాన్" or month_group == "మొదటి నెల" or month_group == "జనుఅరీ" or month_group == "జనవరి" or month_group == "january":
            return 1
        elif month_group == "ఫిబ్రవరి" or month_group == "ఫెబ్" or month_group == "రెండో నెల" or month_group == "రెండొ నెల" or month_group == "february":
            return 2
        elif month_group == "మార్చ్" or month_group == "మార్" or month_group == "మర్చి" or month_group == "మూడో నెల" or month_group == "మూడొ నెల" or month_group == "మార్చి" or month_group == "march":
            return 3
        elif month_group == "ఏప్రిల్" or month_group == "ఏప్రెల్" or month_group == "నాల్గో నెల" or month_group == "నాలుగో నెల" or month_group == "నాలుగొ నెల" or month_group == "నాల్గొ నెల" or month_group == "april":
            return 4
        elif month_group == "మే" or month_group == "ఐదో నెల" or month_group == "ఐదొ నెల" or month_group == "may":
            return 5
        elif month_group == "జూన్" or month_group == "ఆరో నెల" or month_group == "ఆరొ నెల" or month_group == "june":
            return 6
        elif month_group == "జులై" or month_group == "ఏడో నెల" or month_group == "ఎడొ నెల" or month_group == "july":
            return 7
        elif month_group == "ఆగష్టు" or month_group == "అగస్ట్" or month_group == "ఆగస్ట్" or month_group == "ఎనిమిదో నెల" or month_group == "అగష్టు" or month_group == "ఎనిమిదొ నెల" or month_group == "ఆగస్టు" or month_group == "august":
            return 8
        elif month_group == "సెప్టెంబర్" or month_group == "తొమ్మిదో నెల" or month_group == "తొమ్మిదొ నెల" or month_group == "september":
            return 9
        elif month_group == "అక్టోబర్" or month_group == "అక్టోబరు" or month_group == "పదో నెల" or month_group == "పదొ నెల" or month_group == "october":
            return 10
        elif month_group == "నవంబర్" or month_group == "పదకొండొ నెల" or month_group == "నవెంబర్" or month_group == "పదకొండో నెల" or month_group == "november":
            return 11
        elif month_group == "డిసెంబరు" or month_group == "డిసెంబర్" or month_group == "డెక్" or month_group == "పన్నెండో నెల" or month_group =="పన్నెండొ నెల" or month_group == "december":
            return 12
        else:
            return ""

    def extractWeekday(self, text):
        text = " ".join(text[0])                                                                       
        a = re.search(r'సోమవారం|సోమారం|ఇందువాసరము|మండే|మంగళవారము|మంగళవారం|మంగళారం|అంగారకవారమ|జయవారము|ట్యూస్డే|బుధవారము|బుధారం|సౌమ్యవాసరము|బుధవారం|వెడ్నెస్డే|వెన్స్ డే|గురువారము|బృహస్పతి వారము|లక్ష్మివారము|గురు|గురువారం|బేస్తారం|బేస్తవారము|బెస్తవారం|తర్సడై|శుక్రవారము|శుక్రవారం|శుక్రారం|ఫ్రైడే|శనివారము|షెనారం|స్థిరవారము|మందవారము|సాటర్డే|శెనివారము|శెనివారం|శనివారం|ఆదివారము|భానువారము|రవివారము|అధిత్యవారము|తొలివారము|సండే|ఆదివారం|monday|tuesday|wednesday|thursday|friday|saturday|sunday', text)
        if a == None or a.group() == "":
            return ""
        week_group = a.group() 
        if week_group == "సోమవారం" or week_group == "సోమారం" or week_group == "ఇందువాసరము" or week_group == "మండే" or week_group == "monday":
            return 1  
        elif week_group == "మంగళవారం"  or week_group == "మంగళవారము" or week_group == "మంగళారం" or week_group == "అంగారకవారమ" or week_group == "జయవారము" or week_group == "ట్యూస్డే" or week_group == "tuesday":
            return 2 
        elif week_group == "బుధవారము" or week_group == "బుధారం" or week_group == "సౌమ్యవాసరము" or week_group == "బుధవారం" or week_group == "వెడ్నెస్డే" or week_group == "వెన్స్ డే" or week_group == "wednesday":
            return 3
        elif week_group == "గురువారము" or week_group == "బృహస్పతి వారము" or week_group == "లక్ష్మివారము" or week_group == "గురు" or week_group == "గురువారం" or week_group == "బేస్తారం" or week_group == "బేస్తవారము" or week_group == "బెస్తవారం" or week_group == "తర్సడై" or week_group == "thursday":
            return 4
        elif week_group == "శుక్రవారము" or week_group == "శుక్రవారం" or week_group == "శుక్రారం" or week_group == "ఫ్రైడే" or week_group == "friday":
            return 5
        elif week_group == "శనివారము" or week_group == "షెనారం" or week_group == "స్థిరవారము" or week_group == "సాటర్డే" or week_group == "మందవారము" or week_group == "శెనివారము" or week_group == "శెనివారం" or week_group == "శనివారం" or week_group == "saturday":
            return 6
        elif week_group == "ఆదివారము" or week_group == "భానువారము" or week_group == "రవివారము" or week_group == "అధిత్యవారము" or week_group == "తొలివారము" or week_group == "సండే" or week_group == "ఆదివారం" or week_group == "sunday":
            return 7
        else:
            return ""

    def extractMeridiam(self, text):
        # text = " ".join(text[0])
        a = re.search(r'ఏ ఎమ్|ఏఎమ్|పీ ఎమ్|పీఎమ్|a.m.|am|p.m.|pm', text)
        if a == None or a.group() == "":
            return ""
        meridiam = a.group()
        if meridiam == "ఏ ఎమ్" or meridiam == "ఏఎమ్" or meridiam == "a.m." or meridiam == "am":
            return 1
        elif meridiam == "పీ ఎమ్" or meridiam == "పీఎమ్" or meridiam == "pm" or meridiam == "p.m.":
            return 2
        else:
            return -1

    def extractDaytime(self, text):
        text = text[0]
        a = re.search(r'పొద్దున|ఉదయం|పొద్దున్నే|ఉదయాన్నే|ప్రొద్దున|మార్నింగ్|మధ్యాహ్నం|మద్యానం|ఆఫ్టర్ నూన్|పగటీలి|సాయంత్రం|ఆఫ్టేర్నూన్|ఈవెనింగ్|ఈవినింగ్|సాయంకాలం|రాత్రి|నైట్|చీకటి|వెంటనే|ఇప్పుడే|ఇప్పుడు|ఇమ్మీడియేటగా|తక్షణమే|క్షణం|క్షణమే|క్షణంలో', text)
        if a == None or a.group() == "":
            return ""
        day_time = a.group()
        if day_time == "సాయంత్రం" or day_time == "సాయంకాలం" or day_time == "ఈవినింగ్" or day_time == "ఈవెనింగ్":
            return 18
        elif day_time == "రాత్రి" or day_time == "నైట్" or day_time == "చీకటి":
            return 20
        elif day_time == "పొద్దున" or day_time == "ప్రొద్దున" or day_time == "మార్నింగ్" or day_time == "ఉదయాన్నే" or day_time == "ఉదయం" or day_time == "పొద్దున్నే":
            return 10
        elif day_time == "మధ్యాహ్నం" or day_time == "పగటీలి" or day_time == "ఆఫ్టేర్నూన్" or day_time == "మద్యానం" or day_time == "ఆఫ్టర్ నూన్":
            return 12
        elif day_time == "వెంటనే" or day_time == "ఇప్పుడే" or day_time == "ఇప్పుడు" or day_time == "ఇమ్మీడియేటగా" or day_time == "తక్షణమే" or day_time == "క్షణం" or day_time == "క్షణమే" or day_time == "క్షణంలో":
            return -1
        else:
            return ""

    def extractTimeModule(self, text):
        text = " ".join(text[0])
        before = re.search(r'ముందు|ముందర|ముంద|మనువు|ముందుగా|ముందుగానే|బెఫోర్|బిఫోర్', text)
        if before != None and before.group() != "":
            return -1
        after = re.search(r'తరువాత|తర్వాత|అనంతరం|తరవాత|ఆఫ్టర్|అఫ్ప్టర్|తరువత', text)
        if after != None and after.group() != "":
            return 1
        return ""

    def extractDueDate(self, text):
        # text = " ".join(text[0])
        due_date = re.search(r'గడువు తేది|గడువుతేది|గడవుతేది|గదవు తేది|గడవుతెది|గడవ తేది|యూ డేట్|డ్యూడేట్|బకాయితేది|బకాయతేది|బకయతేది|బకాయితేడి|బకయితేది|బాకయితేది|పేమెంట్ డేట్|డ్యూ తేది|బకాయి తారీకు|గడువు రోజు|పేమెంట్ తేది|డ్యూ తారీకు|గడువు తారీకు', text)
        if due_date != None and due_date.group() != "":
            return "due_date"
        return ""

class GrainUnitExtractionmalayalam:
    
    def extractIntPos(self, text, i):
        try:
            text = " ".join(text[0]).strip()
            temp = re.findall(r'\d+', text)
            temp = list(map(int, temp))
            return temp[i]
        except Exception as ex:
            return -1

    def extractInt(self, text):
        text = " ".join(text[0]).strip()
        temp = re.findall(r'\d+', text)
        if len(temp) == 0:
            return -1
        temp = list(map(int, temp))
        return temp[0]

    def extractMonth(self, text):
        text = " ".join(text[0])   
        a = re.search(r'ജനവരി|ജാനുവരി|ജനുവരി|ഫെബ്രുവരി|ജനുവരിയിൽ|ഫെബ്രുവരിയിൽ|മാർച്ച്|മാർച്ചിൽ|ഏപ്രിൽ|ഏപ്രിലിൽ|മെയ്|മേയിൽ|ജൂൺ|ജൂണിൽ|ജൂലൈ|ജൂലായിൽ|ഓഗസ്റ്റ്|ആഗസ്റ്റ്|ആഗസ്റ്|ഓഗസ്റ്|ഓഗസ്റ്റിൽ|സെപ്റ്റംബർ|സെപ്റ്റംബര്|സെപ്തംബര്|സെപ്റ്റംബറിൽ|ഒക്ടോബർ|ഒക്‌ട്‌ബേർ|ഒക്ടോബറിൽ|നവംബർ|നവംബറിൽ|ഡിസംബർ|ഡിസംബറിൽ', text)
        if a == None or a.group() == "":
            return ""
        month_group = a.group()
        if month_group == "ജനുവരി" or month_group == "ജാനുവരി" or month_group == "ജനവരി" or month_group == "ജനുവരിയിൽ":
            return 1
        elif month_group == "ഫെബ്രുവരി" or month_group == "ഫെബ്രുവരിയിൽ":
            return 2
        elif month_group == "മാർച്ച്" or month_group == "മാർച്ചിൽ":
            return 3
        elif month_group == "ഏപ്രിൽ" or month_group == "ഏപ്രിലിൽ":
            return 4
        elif month_group == "മെയ്" or month_group == "മേയിൽ":
            return 5
        elif month_group == "ജൂൺ" or month_group == "ജൂണിൽ":
            return 6
        elif month_group == "ജൂലൈ" or month_group == "ജൂലായിൽ":
            return 7
        elif month_group == "ഓഗസ്റ്റ്" or month_group == "ആഗസ്റ്റ്" or month_group == "ആഗസ്റ്" or month_group == "ഓഗസ്റ്" or month_group == "ഓഗസ്റ്റിൽ":
            return 8
        elif month_group == "സെപ്റ്റംബർ" or month_group == "സെപ്റ്റംബര്" or month_group == "സെപ്തംബര്" or month_group == "സെപ്റ്റംബറിൽ":
            return 9
        elif month_group == "ഒക്ടോബർ" or month_group == "ഒക്‌ട്‌ബേർ" or month_group == "ഒക്ടോബറിൽ":
            return 10
        elif month_group == "നവംബർ" or month_group == "നവംബറിൽ":
            return 11
        elif month_group == "ഡിസംബർ" or month_group == "ഡിസംബറിൽ":
            return 12
        else:
            return ""

    def extractWeekday(self, text):
        text = " ".join(text[0])
        a = re.search(r'തിങ്കൾ|തിങ്കളാഴ്ച|മോണ്ടായ്|ചൊവ്വ|ചൊവ്വാഴ്ച|ടുസ്‌ഡേ|ബുധൻ|ബുധനാഴ്ച|വെഡ്നെസ്‌ഡേ|വ്യാഴം|വ്യാഴാഴ്ച|തുര്സ്ടായ്|വെള്ളി|വെള്ളിയാഴ്ച|ഫ്രൈഡേ|ശനി|ശനിയാഴ്ച|സടുർദായ്|ഞായർ|ഞായറാഴ്ച|സൺ‌ഡേ', text)
        if a == None or a.group() == "":
            return ""
        week_group = a.group()
        if week_group == "തിങ്കൾ" or week_group == "തിങ്കളാഴ്ച" or week_group == "മോണ്ടായ്":
            return 1
        elif week_group == "ചൊവ്വ" or week_group == "ചൊവ്വാഴ്ച" or week_group == "ടുസ്‌ഡേ":
            return 2
        elif week_group == "ബുധൻ" or week_group == "ബുധനാഴ്ച" or week_group == "വെഡ്നെസ്‌ഡേ":
            return 3
        elif week_group == "വ്യാഴം" or week_group == "വ്യാഴാഴ്ച" or week_group == "തുര്സ്ടായ്":
            return 4
        elif week_group == "വെള്ളി" or week_group == "വെള്ളിയാഴ്ച" or week_group == "ഫ്രൈഡേ":
            return 5
        elif week_group == "ശനി" or week_group == "ശനിയാഴ്ച" or week_group == "സടുർദായ്":
            return 6
        elif week_group == "ഞായർ" or week_group == "ഞായറാഴ്ച" or week_group == "സൺ‌ഡേ":
            return 7
        else:
            return ""

    def extractMeridiam(self, text):
        # text = " ".join(text[0])
        a = re.search(r'a.m.|am|p.m.|pm', text)
        if a == None or a.group() == "":
            return ""
        meridiam = a.group()
        if meridiam == "" or meridiam == "" or meridiam == "a.m." or meridiam == "am":
            return 1
        elif meridiam == "" or meridiam == "" or meridiam == "pm" or meridiam == "p.m.":
            return 2
        else:
            return -1

    def extractDaytime(self, text):
        text = text[0]
        a = re.search(r'രാത്രി|നൈറ്റ്|വൈകിട്ട്|വൈകുന്നേരം|സന്ധ്യ|എവെനിംഗ്|ഉച്ച|ഉച്ചക്ക്|ഉച്ചകഴിഞ്ഞ്|അഫ്റെർൂൺ|രാവിലെ|മോണിങ്|പുലർച്ചെ|പുലര്വേള|പുലർവേള|ഇപ്പോൾ|ഇപ്പോള്|നൗ|ഇപ്പം', text)
        if a == None or a.group() == "":
            return ""
        day_time = a.group()
        if day_time == "വൈകിട്ട്" or day_time == "വൈകുന്നേരം" or day_time == "സന്ധ്യ" or day_time == "എവെനിംഗ്" or day_time == "ഈവനിങ്":
            return 6
        elif day_time == "രാത്രി" or day_time == "നൈറ്റ്" or day_time == "നൈയ്യിറ്റ്":
            return 20
        elif day_time == "രാവിലെ" or day_time == "മോണിങ്" or day_time == "പുലർച്ചെ" or day_time == "പുലര്വേള" or day_time == "പുലർവേള":
            return 10
        elif day_time == "ഉച്ച" or day_time == "ഉച്ചക്ക്" or day_time == "ഉച്ചകഴിഞ്ഞ്" or day_time == "ആഫ്റ്റർനൂൺ" or day_time == "അഫ്റ്റർനൂൺ":
            return 12
        elif day_time == "സെക്കൻഡ്‌ " or day_time == "സെക്കന്ഡ്" or day_time == "സെക്കന്റ്" or day_time == "ഇപ്പോൾ" or day_time == "നൗ" or day_time == "ഉടനടി" or day_time == "തല്‍ക്ഷണം" or day_time == "പെട്ടെന്ന്" or day_time == "ഉടൻതന്നെ" or day_time == "ഇപ്പൊ" or day_time == "ഇപ്പം":
            return -1
        else:
            return ""

    def extractTimeModule(self, text):
        text = " ".join(text[0])
        before = re.search(r'മുമ്പ്|ബിഫോർ|മുന്നേ|മുൻബ്|ബിഫോര്|ബിഫോറെ|ബിഫോരെ|മുന്ബ്|മുൻബി|മുമ്ബ്|മുന്ന|മൂന്നേ|മണ്ണേ|മുൻനേ', text)
        if before != None and before.group() != "":
            return -1
        after = re.search(r'ശേഷം|അതിനുശേഷം|ആഫ്റ്റർ|കഴിഞ്ഞേ|കഴിഞ്ഞ്|കഴിഞ്ഞിട്ട്|ശെഷം|ശേഷവും|ശേശം|ശേഷമെ|ശഷം|ശേഷവും|ആഫ്റ്റര്|ആഫ്‌റ്റർ|ആഫ്ടർ|ആഫ്റ്റെർ|ശേഷ|കഴിഞു|ക്കഴിഞ്ഞു|കഴിഞ്ഞ', text)
        if after != None and after.group() != "":
            return 1
        return ""

    def extractDueDate(self, text):
        # text = " ".join(text[0])
        due_date = re.search(r'ഡ്യൂ ഡേറ്റ്|ഡ്യൂ തീയതി|അവസാന ഡേറ്റ്|അവസാന തീയതി', text)
        if due_date != None and due_date.group() != "":
            return "due_date"
        return ""
    
class GrainUnitExtractiontamil:
    
    def extractIntPos(self, text, i):
        try:
            text = " ".join(text[0]).strip()
            temp = re.findall(r'\d+', text)
            temp = list(map(int, temp))
            return temp[i]
        except Exception as ex:
            return -1

    def extractInt(self, text):
        text = " ".join(text[0]).strip()
        temp = re.findall(r'\d+', text)
        if len(temp) == 0:
            return -1
        temp = list(map(int, temp))
        return temp[0]

    def extractMonth(self, text):
        text = " ".join(text[0]) 
        a = re.search(r'ஜனவரி|சனவரி|ஜன|january|தை|பிப்ரவரி|february|பிப்|மாசி|மார்ச்|march|மார்|பங்குனி|ஏப்ரல்|april|சித்திரை|மே|வைகாசி|may|ஜூன்|ஆனி|june|ஜூல்|ஜூலை|july|ஆடி|ஆக்|ஆகஸ்ட்|august|ஆவணி|செப்|செப்டெம்பர்|september|புரட்டாசி|அக்ட்|அக்டோபர்|october|ஐப்பசி|நவ|நவம்பர்|november|கார்த்திகை|டிச|டிசம்பர்|மார்கழி|december', text)
        if a == None or a.group() == "":
            return ""
        month_group = a.group()
        if month_group == "ஜனவரி" or month_group == "ஜன" or month_group == "தை" or month_group == "january" or month_group == "சனவரி":
            return 1
        elif month_group == "பிப்ரவரி" or month_group == "பிப்" or month_group == "மாசி" or month_group == "february":
            return 2
        elif month_group == "மார்ச்" or month_group == "மார்" or month_group == "பங்குனி" or month_group == "march":
            return 3
        elif month_group == "ஏப்ரல்" or month_group == "சித்திரை" or month_group == "april":
            return 4
        elif month_group == "மே" or month_group == "வைகாசி" or month_group == "may":
            return 5
        elif month_group == "ஜூன்" or month_group == "ஆனி" or month_group == "june":
            return 6
        elif month_group == "ஜூல்" or month_group == "ஜூலை" or month_group == "ஆடி" or month_group == "july": 
            return 7
        elif month_group == "ஆக்" or month_group == "ஆகஸ்ட்" or month_group == "ஆவணி" or month_group == "august":
            return 8
        elif month_group == "செப்" or month_group == "புரட்டாசி" or month_group == "செப்டெம்பர்" or month_group == "september":
            return 9
        elif month_group == "அக்ட்" or month_group == "அக்டோபர்" or month_group == "ஐப்பசி" or month_group == "october":
            return 10
        elif month_group == "நவ" or month_group == "கார்த்திகை" or month_group == "நவம்பர்" or month_group == "november":
            return 11
        elif month_group == "டிச" or month_group == "மார்கழி" or month_group == "டிசம்பர்" or month_group == "december":
            return 12
        else:
            return ""

    def extractWeekday(self, text):
        text = " ".join(text[0])    
        a = re.search(r'திங்கள்கிழமை|திங்கள்|திங்ககிழமை|திங்கக்கிழமை|திங்கட்கிழமை|திங்கட்கிழமை|மன்டே|மண்டே|செவ்வாய்க்கிழமை|செவ்வாய்கிழமை|செவ்வாய்|செவ்வாக்கிழமை|ட்யூஸ்டே|புதன்கிழமை|புதன்|புதன்கிழமை|புதங்கிழமை|வெட்னஸ்டே|வியாழக்கிழமை|வியாழன்கிழமை|வியாழன்|தர்ஸ்டே|வெள்ளிக்கிழமை|வெள்ளிகிழமை|வெள்ளி|ஃப்ரைடே|சனிக்கிழமை|இப்பொழுது|சனிகிழமை|சனி|சாடர்டே|சாட்டர்டே|ஞாயிற்றுக்கிழமை|ஞாயிறுகிழமை|ஞாயிறு|ஞாயித்துக்கிழமை|சண்டே|சன்டே', text)
        if a == None or a.group() == "":
            return ""
        week_group = a.group()
        if week_group == "திங்கள்கிழமை" or week_group == "திங்கள்" or week_group == "திங்கக்கிழமை" or week_group == "திங்கட்கிழமை" or week_group == "மன்டே" or week_group == "மண்டே" or week_group == "திங்ககிழமை" or week_group == "திங்கட்கிழமை":
            return 1
        elif week_group == "செவ்வாய்க்கிழமை" or week_group == "ட்யூஸ்டே" or week_group == "செவ்வாக்கிழமை" or week_group == "செவ்வாய்" or week_group == "செவ்வாய்கிழமை":
            return 2
        elif week_group == "புதன்கிழமை" or week_group == "வெட்னஸ்டே" or week_group == "புதங்கிழமை" or week_group == "புதன்" or week_group == "புதன்கிழமை":
            return 3
        elif week_group == "வியாழக்கிழமை" or week_group == "வியாழன்கிழமை" or week_group == "வியாழன்" or week_group == "தர்ஸ்டே":
            return 4
        elif week_group == "வெள்ளிக்கிழமை" or week_group == "வெள்ளிகிழமை" or week_group == "வெள்ளி" or week_group == "ஃப்ரைடே":
            return 5
        elif week_group == "சனிக்கிழமை" or week_group == "சனிகிழமை" or week_group == "சனி" or week_group == "சாடர்டே" or week_group == "சாட்டர்டே":
            return 6
        elif week_group == "ஞாயிற்றுக்கிழமை" or week_group == "இப்பொழுது" or week_group == "ஞாயிறுகிழமை" or week_group == "ஞாயிறு" or week_group == "ஞாயித்துக்கிழமை" or week_group == "சண்டே" or week_group == "சன்டே":
            return 7
        else:
            return ""

    def extractMeridiam(self, text):
        # text = " ".join(text[0])
        a = re.search(r'a.m.|am|p.m.|pm', text)
        if a == None or a.group() == "":
            return ""
        meridiam = a.group()
        if meridiam == "" or meridiam == "" or meridiam == "a.m." or meridiam == "am":
            return 1
        elif meridiam == "" or meridiam == "" or meridiam == "pm" or meridiam == "p.m.":
            return 2
        else:
            return -1
 
    def extractDaytime(self, text):
        # text = " ".join(text[0])
        text = text[0]
        a = re.search(r'ஈவினிங்|மாலை|ஈவ்னிங்|சாயிந்திரம்|சாயுங்காலம்|நைட்|நைட்டு|இரவு|ராத்திரி|மார்னிங்|காலை|காலைல|மதியம்|மத்தியானம்|ஆஃப்டர் நூன்|நூன்|ஆஃப்டர்நூன்|உடனடியாக|இப்போது|இப்போ|இப்ப|உடனே|இப்பவே|ரைட்நவ்|நவ்|இப்போதே|இப்பவே|இப்போதே|இப்பவே|உடனடியாக|இப்போ|இப்ப|உடனே|இப்பவே|ரைட்நவ்|நவ்', text)
        if a == None or a.group() == "":
            return ""
        day_time = a.group()
        if day_time == "ஈவினிங்" or day_time == "மாலை" or day_time == "சாயிந்திரம்" or day_time == "சாயுங்காலம்" or day_time == "ஈவ்னிங்":
            return 6
        elif day_time == "நைட்" or day_time == "ராத்திரி" or day_time == "இரவு" or day_time == "நைட்டு":
            return 20
        elif day_time == "மார்னிங்" or day_time == "காலைல" or day_time == "காலை":
            return 10
        elif day_time == "மதியம்" or day_time == "மத்தியானம்" or day_time == "நூன்" or day_time == "ஆஃப்டர் நூன்" or day_time == "ஆஃப்டர்நூன்":
            return 12
        elif day_time == "உடனடியாக" or day_time == "இப்போது" or day_time == "இப்போ" or day_time == "இப்ப" or day_time == "உடனே" or day_time == "இப்பவே" or day_time == "ரைட்நவ்" or day_time == "நவ்" or day_time == "இப்போதே" or day_time == 'இப்பவே' \
             or day_time == "இப்போதே" or day_time == "இப்பவே" or day_time == "உடனடியாக" or day_time == "இப்போ" or day_time == "இப்ப" or day_time == "உடனே" or day_time == "இப்பவே" \
                 or day_time == "ரைட்நவ்" or day_time == "நவ்":
            return -1
        else:
            return ""

    def extractTimeModule(self, text):
        text = " ".join(text[0])
        before = re.search(r'முன்|முன்னாடி|முன்னால்|முன்ப|முன்பு|முன்னாடி|முன்னாடியே|முன்னர்', text)
        if before != None and before.group() != "":
            return -1
        after = re.search(r'பிறகு|பின்|பின்னர்|பின்னால்|பின்பு|பின்னாடி|பின்னால்|பின்னாடியே|பின்னர்', text)
        if after != None and after.group() != "":
            return 1
        return ""

    def extractDueDate(self, text):
        # text = " ".join(text[0])
        due_date = re.search(r'நிலுவைத் தேதி|நிலுவை தேதி|நிலுவை தேதி|நிலுவை|நிலுவை தேதி|டியூ தேதி|டியூ  டேட்|நிலுவை டேட்|நிலுவைத் தேதி|நிலுவைத் தேதி', text)
        if due_date != None and due_date.group() != "":
            return "due_date"
        return ""

class GrainUnitExtractionkannada:
    
    def extractIntPos(self, text, i):
        try:
            text = " ".join(text[0]).strip()
            temp = re.findall(r'\d+', text)
            temp = list(map(int, temp))
            return temp[i]
        except Exception as ex:
            return -1

    def extractInt(self, text):
        text = " ".join(text[0]).strip()
        temp = re.findall(r'\d+', text)
        if len(temp) == 0:
            return -1
        temp = list(map(int, temp))
        return temp[0]

    def extractMonth(self, text):
        text = " ".join(text[0])
        a = re.search(r'ಜನವರಿ|ಜ್ಯಾನ್ವರಿ|january|ಫೆಬ್ರವರಿ|ಫೆಬ್ರುವರಿ|february|ಮಾರ್ಚ್|march|ಏಪ್ರಿಲ್|april|ಮೇ|may|ಜೂನ್|ಜುನ್|june|ಜೂಲೈ|ಜುಲೈ|ಜುಲೈನಲ್ಲಿ|july|ಆಗಸ್ಟ್|ಅಗಸ್ಟ್|ಅಗಸ್ಟಿಗೆ|august|ಸೆಪ್ಟೆಂಬರ್|september|ಅಕ್ಟೋಬರ್|october|ನೋವೊಂಬೆರ್|ನವೆಂಬರ್|november|ಡಿಸೆಂಬರ್|december', text)
        if a == None or a.group() == "":
            return ""
        month_group = a.group()
        if month_group == "ಜನವರಿ" or month_group == "ಜ್ಯಾನ್ವರಿ" or month_group == "january":
            return 1
        elif month_group == "ಫೆಬ್ರವರಿ" or month_group == "ಫೆಬ್ರುವರಿ" or month_group == "february":
            return 2
        elif month_group == "ಮಾರ್ಚ್" or month_group == "march":
            return 3
        elif month_group == "ಏಪ್ರಿಲ್" or month_group == "april":
            return 4
        elif month_group == "ಮೇ" or month_group == "may":
            return 5
        elif month_group == "ಜೂನ್" or month_group == "june" or month_group == "ಜುನ್":
            return 6
        elif month_group == "ಜೂಲೈ" or month_group == "ಜುಲೈ" or month_group == "ಜುಲೈನಲ್ಲಿ" or month_group == "july":
            return 7
        elif month_group == "ಆಗಸ್ಟ್" or month_group == "ಅಗಸ್ಟ್" or month_group == "august" or month_group == "ಅಗಸ್ಟಿಗೆ":
            return 8
        elif month_group == "ಸೆಪ್ಟೆಂಬರ್" or month_group == "september":
            return 9
        elif month_group == "ಅಕ್ಟೋಬರ್" or month_group == "october":
            return 10
        elif month_group == "ನೋವೊಂಬೆರ್" or month_group == "ನವೆಂಬರ್" or month_group == "november":
            return 11
        elif month_group == "ಡಿಸೆಂಬರ್" or month_group == "december":
            return 12
        else:
            return ""

    def extractWeekday(self, text):
        text = " ".join(text[0])
        a = re.search(r'ಸೋಮವಾರ|ಸೋಮ್ವಾರ|ಮಂಡೇ|ಮಂಡೆ|ಮಂಡೆ|somawara|monday|somwara|ಮಂಗಳವಾರ|ಟ್ಯೂಸ್ಡೇ|mangalawara|tuesday|ಬುಧವಾರ|ವೆಡ್ನೆಸ್ಡೇ|ಬುದುವಾರ|budhawara|wednesday|buduwara|ಗುರುವಾರ|ಥರ್ಸ್ಡೇ|guruwara|thursday|ಶುಕ್ರವಾರ|ಫ್ರೈಡೇ|ಶುಕ್ರುವಾರ|ಫ್ರೈಡೆ|ಶುಕ್ರವಾರದೊಳಗೆ|shukrawara|friday|shukruwara|ಶನಿವಾರ|ಸಾಟರ್ಡೆ|shaniwara|saturday|ಭಾನುವಾರ|ಸಂಡೆ|ರವಿವಾರ|ಆದಿತ್ಯವಾರ|bhanuwara|sunday|ravivara|adityavara', text)
        if a == None or a.group() == "":
            return ""
        week_group = a.group()
        if week_group == "ಸೋಮವಾರ" or week_group == "ಸೋಮ್ವಾರ" or week_group == "ಮಂಡೇ" or week_group == "ಮಂಡೆ" or week_group == "ಮಂಡೆ" or week_group == "somawara" or week_group == "monday" or week_group == "somwara":
            return 1
        elif week_group == "ಮಂಗಳವಾರ" or week_group == "ಟ್ಯೂಸ್ಡೇ" or week_group == "mangalawara" or week_group == "tuesday":
            return 2
        elif week_group == "ಬುಧವಾರ" or week_group == "ವೆಡ್ನೆಸ್ಡೇ" or week_group == "ಬುದುವಾರ" or week_group == "budhawara" or week_group == "wednesday" or week_group == "buduwara":
            return 3
        elif week_group == "ಗುರುವಾರ" or week_group == "ಥರ್ಸ್ಡೇ" or week_group == "guruwara" or week_group == "thursday":
            return 4
        elif week_group == "ಶುಕ್ರವಾರ" or week_group == "ಫ್ರೈಡೇ" or week_group == "ಶುಕ್ರುವಾರ" or week_group == "ಫ್ರೈಡೆ" or week_group == "ಶುಕ್ರವಾರದೊಳಗೆ" or week_group == "shukrawara" or week_group == "friday" or week_group == "shukruwara":
            return 5
        elif week_group == "ಶನಿವಾರ" or week_group == "ಸಾಟರ್ಡೆ" or week_group == "shaniwara" or week_group == "saturday":
            return 6
        elif week_group == "ಭಾನುವಾರ" or week_group == "ಸಂಡೆ" or week_group == "ರವಿವಾರ" or week_group == "ಆದಿತ್ಯವಾರ" or week_group == "bhanuwara" or week_group == "sunday" or week_group == "ravivara" or week_group == "adityavara":
            return 7
        else:
            return ""

    def extractMeridiam(self, text):
        # text = " ".join(text[0])
        a = re.search(r'ऍम|पीऍम|पीएम|ऐम', text)
        if a == None or a.group() == "":
            return ""
        meridiam = a.group()
        if meridiam == "ऍम" or meridiam == "ऐम":
            return 1
        elif meridiam == "पीऍम" or meridiam == "पीएम":
            return 2
        else:
            return -1

    def extractDaytime(self, text):
        # text = " ".join(text[0])
        text = text[0]
        a = re.search(r'ಸಾಯಂಕಾಲ|ಸಂಜೆ|ಇವಿನಿಂಗ್|ಸಂಜೆಗೆ|ಸಂಜೆಯೊಳಗೆ|ಸಂಜೆಯ|ನೈಟ್|ರಾತ್ರಿ|ರಾತ್ರಿಗೆ|ರಾತ್ರಿನೇ|ರಾತ್ರಿಯೊಳಗೆ|ರಾತ್ರಿಯವರೆಗೆ|ಬೆಳೆಗೆ|ಮಾರ್ನಿಂಗ್|ಬೆಳಿಗೆ|ಬೆಳೆಗೇನೆ|ಬೆಳಿಗ್ಗೆ|ಬೆಳಿಗೆಯೊಳಗೆ|ಬೆಳಗ್ಗೆ|ಮಧ್ಯಾಹ್ನ|ಆಫ್ಟರ್ನೂನ್|ಆಫ್ಟರ್ ನೂನ್|ಮಧ್ಯಾಹ್ನದೊಳಗೆ|ಈಗ|ಇಗಾ|ಕೂಡಲೇ|ಕುಡ್ಲೆ|ಈವಾಗಲೇ|ಸೆಕೆಂಡ್|ಈಗಳೇ|ಇವಾಗ್ಲೇ|ಇವತ್ತು|ಇಂದು|ಟುಡೇ|ಇವತ್|ಇಂದೇ|ಇವತ್ತೆ|ಇವಾಗ|ಈಗಲೇ|ಇವಾಗ್ಲೆ|ಈಗಲೆ|ಇಂದಿಗೆ|ಇಮ್ಮಿಡಿಯೇಟಲಿ|ತಕ್ಷಣ|ತಕ್ಷಣವೇ|ಇಂದಿನ|ಇವತ್ತಿನ|ಇವತ್ತೇ|ಈ|ಇವಾಗಲೇ|ಟುಡೇ|ಇವತ್ತ|ಟುಡೆ|ಇವಾಗೆ|ಈಗ್ಲೇ|ಇಂದಿಗಾಗಲೇ|ಇಂದಿನೊಳಗೆ', text)
        if a == None or a.group() == "":
            return ""
        day_time = a.group()
        if day_time == "ಸಾಯಂಕಾಲ" or day_time == "ಸಂಜೆ" or day_time == "ಇವಿನಿಂಗ್" or day_time == "ಸಂಜೆಗೆ" or day_time == "ಸಂಜೆಯೊಳಗೆ" or day_time == "ಸಂಜೆಯ":
            return 6
        elif day_time == "ನೈಟ್" or day_time == "ರಾತ್ರಿ" or day_time == "ರಾತ್ರಿಗೆ" or day_time == "ರಾತ್ರಿನೇ" or day_time == "ರಾತ್ರಿಯೊಳಗೆ" or day_time == "ರಾತ್ರಿಯವರೆಗೆ":
            return 20
        elif day_time == "ಬೆಳೆಗೆ" or day_time == "ಬೆಳೆಗೇನೆ" or day_time == "ಬೆಳಿಗೆಯೊಳಗೆ" or day_time == "ಬೆಳಿಗೆ" or day_time == "ರಾತ್ರಿನೇ" or day_time == "ಮಾರ್ನಿಂಗ್" or day_time == "ಬೆಳಗ್ಗೆ" or day_time == "ಬೆಳಿಗ್ಗೆ":
            return 10
        elif day_time == "ಮಧ್ಯಾಹ್ನ" or day_time == "ಆಫ್ಟರ್ ನೂನ್" or day_time == "ಆಫ್ಟರ್ನೂನ್" or day_time == "ಮಧ್ಯಾಹ್ನದೊಳಗೆ":
            return 12
        elif day_time == "ಈಗ" or day_time == "ಇವತ್ತ" or day_time == "ಟುಡೆ" or day_time == "ಇವಾಗೆ" or day_time == "ಟುಡೇ" or day_time == "ಇವಾಗಲೇ" or day_time == "ಈ" or day_time == "ಇವತ್ತೇ" or day_time == "ಇವತ್ತಿನ" \
                                        or day_time == "ಇಗಾ" or day_time == "ಕೂಡಲೇ" or day_time == "ಕುಡ್ಲೆ" or day_time == "ಈವಾಗಲೇ" or day_time == "ಸೆಕೆಂಡ್" \
                                            or day_time == "ಈಗಳೇ" or day_time == "ಇವಾಗ್ಲೇ" or day_time == "ಇವತ್ತು" or day_time == "ಇಂದು" or day_time == "ಟುಡೇ" \
                                                or day_time == "ಇವತ್" or day_time == "ಇಂದೇ" or day_time == "ಇವತ್ತೆ" or day_time == "ಇವಾಗ" or day_time == "ಈಗಲೇ" \
                                                     or day_time == "ಇವಾಗ್ಲೆ" or day_time == "ಈಗಲೆ" or day_time == "ಇಂದಿಗೆ" or day_time == "ಇಮ್ಮಿಡಿಯೇಟಲಿ" or day_time == "ತಕ್ಷಣ" \
                                                         or day_time == "ತಕ್ಷಣವೇ" or day_time == "ಇಂದಿನ" or day_time == "ಈಗ್ಲೇ" or day_time == "ಇಂದಿಗಾಗಲೇ" or day_time == "ಇಂದಿನೊಳಗೆ":
            return -1
        else:
            return ""

    def extractTimeModule(self, text):
        text = " ".join(text[0])
        before = re.search(r'ಮುಂಚೆ|ಮುಂಚೆನೇ|ಮೊದಲು|ಮುಂಚಿತವಾಗಿ|ಬಿಫೋರ್', text)
        if before != None and before.group() != "":
            return -1
        after = re.search(r'ಆಮೇಲೆ|ನಂತರ|ಆದಮೇಲೆ|ಆಫ್ಟರ್', text)
        if after != None and after.group() != "":
            return 1
        return ""

    def extractDueDate(self, text):
        # text = " ".join(text[0])
        due_date = re.search(r'ಡ್ಯೂಡೇಟ್|ಡ್ಯೂ ಡೇಟ್|ಡ್ಯೂಟಿ|ಡ್ಯು ಡೇಟ್|ಡ್ಯೂಡೇಟ್|ಡ್ಯುಡೇಟ್|ಪೇಮೆಂಟ್ ಡೇಟ್|ಕೊನೆಯ ದಿನಾಂಕ|ಲಾಸ್ಟ ಡೇಟ್|ಪೇಮೆಂಟ್ ದಿನಾಂಕ|ಲಾಸ್ಟ ತಾರೀಖ್|ಡ್ಯೂ ಡೆಟ್|ಡ್ಯು ಡೆಟ್', text)
        if due_date != None and due_date.group() != "":
            return "due_date"
        return ""

class GrainUnitExtractionbengali:
    
    def extractIntPos(self, text, i):
        try:
            text = " ".join(text[0]).strip()
            temp = re.findall(r'\d+', text)
            temp = list(map(int, temp))
            return temp[i]
        except Exception as ex:
            return -1

    def extractInt(self, text):
        text = " ".join(text[0]).strip()
        temp = re.findall(r'\d+', text)
        if len(temp) == 0:
            return -1
        temp = list(map(int, temp))
        return temp[0]

    def extractMonth(self, text):
        text = " ".join(text[0])
        january = re.search(r'জানুয়ারি|জানুয়ারী|জানুয়ারির|জানুয়ারীর|january', text)
        if january != None and january.group() == "":
            return 1
        febuary = re.search(r'ফেব্রুয়ারী|ফেবরারী|ফেব্রুয়ারীর|ফেবরারীর|february', text)
        if febuary != None and febuary.group() != "":
            return 2
        march = re.search(r'মার্চ|মার্চে|মার্চের|march', text)
        if march != None and march.group() != "":
            return 3
        april = re.search(r'এপ্রিল|এপ্রিলে|এপ্রিলের|april', text)
        if april != None and april.group != "":
            return 4
        may = re.search(r'মে|মের|may', text)
        if may != None and may.group() != "":
            return 5
        june = re.search(r'জুন|জুনে|জুনের|june', text)
        if june != None and june.group() != "":
            return 6
        july = re.search(r'জুলাই|জুলাইএ|জুলাইএর|july', text)
        if july != None and july.group() != "":
            return 7
        august = re.search(r'আগস্ট|অগাষ্ট|অগাস্টে|আগস্টে|অগাস্টের|আগস্টের|august', text)
        if august != None and august.group() != "":
            return 8
        september = re.search(r'সেপ্টেম্বর|সেপটেমবার|সেপ্টেম্বার|সেপ্টেম্বরের|সেপটেমবারের|সেপ্টেম্বারের|september', text)
        if september != None and september.group() != "":
            return 9
        october = re.search(r'অক্টোবর|ওকটোবার|অক্টোবার|অক্টোবরের|ওকটোবারের|অক্টোবারের|october', text)
        if october != None and october.group() != "":
            return 10
        november = re.search(r'নভেম্বর|ণবেম্বর|নভেম্বার|নভেম্বরের|ণবেম্বরের|নভেম্বারের|november', text)
        if november != None and november.group() != "":
            return 11
        december = re.search(r'ডিসেম্বর|ডিসেম্বার|ডিসেম্বরের|ডিসেম্বারের|december', text)
        if december != None and december.group() != "":
            return 12
        return ""

    def extractWeekday(self, text):
        text = ' '.join(text[0])
        a = re.search(r'রবিবার|রোববার|সানডে|সোমবার|মানডে|মন্ডে|মঙ্গলবার|টুয়েসডে|টিউসডে|বুধবার|ওয়েডনেসডে|বৃহস্পতিবার|থার্সডে|শুক্রবার|ফ্রাইডে|শনিবার|স্যাটারডে|সোমবারে|সমবার|সোম বার|মান্ডে|মঙ্গলবারে|মঙ্গল বার |মঙ্গোলবার|ট্য়ূসডে|টিউস ডে|বুধবারে|বূধবার|বূধ বার|ওয়েডনেস ডে|বৃহস্পতিবারে |বেশপতিবার|বৃহস্পতি বার|থার্স ডে|শুক্রবারে|শুক্কুরবার|শুক্র বার|জুম্মাবার|ফ্রাই ডে|শনিবারে|শনি বার|সোনিবার|শনীবার|শাটার ডে|শাটারডে|স্যাটার ডে|সাটার ডে|সাটারডে|রবিবারে|রোবিবার|monday|tuesday|wednesday|thursday|friday|saturday|sunday', text)
        if a == None or a.group() == "":
            return ""
        week_group = a.group()
        if week_group == "সোমবার" or week_group == "monday" or week_group == "মানডে" or week_group == "মান্ডে" or week_group == "মন্ডে" or week_group == "সোম বার" or week_group == "সমবার" or week_group == "সোমবারে":
            return 1
        elif week_group == "মঙ্গলবার" or week_group == "মঙ্গলবারে" or week_group == "মঙ্গল বার" or week_group == "মঙ্গোলবার" or week_group == "ট্য়ূসডে" or week_group == "টুয়েসডে" or week_group == "টিউস ডে" or week_group == "টিউসডে" or week_group == "tuesday":
            return 2
        elif week_group == "বুধবার" or week_group == "বুধবারে" or week_group == "বূধবার" or week_group == "ওয়েডনেসডে" or week_group == "বূধ বার" or week_group == "ওয়েডনেস ডে" or week_group == "wednesday":
            return 3
        elif week_group == "বৃহস্পতিবার" or week_group == "বৃহস্পতিবারে" or week_group == "বেশপতিবার" or week_group == "বৃহস্পতি বার" or week_group == "থার্সডে" or week_group == "থার্স ডে" or week_group == "thursday":
            return 4
        elif week_group == "শুক্রবার" or week_group == "শুক্রবারে" or week_group == "শুক্কুরবার" or week_group == "শুক্র বার" or week_group == "জুম্মাবার" or week_group == "ফ্রাইডে" or week_group == "ফ্রাই ডে" or week_group == "friday":
            return 5
        elif week_group == "শনিবার" or week_group == "শনিবারে" or week_group == "শনি বার" or week_group == "সোনিবার" or week_group == "শনীবার" or week_group == "স্যাটারডে" or week_group == "স্যাটার ডে" or week_group == "saturday":
            return 6
        elif week_group == "রবিবার" or week_group == "রবিবারে" or week_group == "রোবিবার" or week_group == "রোববার" or week_group == "সানডে" or week_group == "sunday":
            return 7
        else:
            return ""

    def extractMeridiam(self, text):
        # text = " ".join(text[0])
        a = re.search(r'ऍम|पीऍम|पीएम|ऐम', text)
        if a == None or a.group() == "":
            return ""
        meridiam = a.group()
        if meridiam == "ऍम" or meridiam == "ऐम":
            return 1
        elif meridiam == "पीऍम" or meridiam == "पीएम":
            return 2
        else:
            return -1

    def extractDaytime(self, text):
        # text = " ".join(text[0])
        text = text[0]
        a = re.search(r'জলদি|এক্ষুনি|ইক্ষুণী|ইক্ষুনি|আখনী|এখনই|সেকেন্ড|এক্ষুণি|একটু পর|একটুপর|একটু পরে|একটু খুনী পর|কিছুক্ষণের মধ্যে|কিছুক্ষণ পর|কিছুক্ষণ পরে|কয়েকঘন্টার মধ্যে|কয়েক ঘন্টার মধ্যে|এক্ষুণি|এক্ষুণী|একখুনী|এক্ষুনী|এক্ষুনি|এখনই|একখুনি|এখুনি|আখনই|আখনী', text)
        if a == None or a.group() == "":
            return ""
        day_time = a.group()
        # Evening
        if day_time == "সন্ধে" or day_time == "সন্ধ্যে" or day_time == "সন্ধ্যা" or day_time == "সন্ধা" or day_time == "ইভনিং" or day_time == "এভিনিং" or day_time == "ইভিনিং":
            return 18
        # Night
        elif day_time == "রাত" or day_time == "রাত্রি" or day_time == "রাতে" or day_time == "রাতেরবেলা":
            return 20
        # Morning
        elif day_time == "সকাল" or day_time == "মর্নিং" or day_time == "মর্নিংয়ে":
            return 10
        # Afternoon
        elif day_time == "বিকেল" or day_time == "বিকেলে" or day_time == "বিকালে" or day_time == 'বিকাল' or day_time == 'দুপুর' or day_time == 'দুপুরে' or day_time == 'দুপুরবেলা':
            return 12
        # Immediately
        elif day_time == "জলদি" or day_time == "এক্ষুনি" or day_time == "ইক্ষুণী" or day_time == "ইক্ষুনি" or day_time == "আখনী" or day_time == "এখনই" or day_time == "সেকেন্ড" or day_time == "এক্ষুণি":
            return -1
        else:
            return ""

    def extractTimeModule(self, text):
        text = " ".join(text[0])
        before = re.search(r'আগে|আগের|পূর্বে|পুর্বে|পুরবে|বিফোর|before', text)
        if before != None and before.group() != "":
            return -1
        after = re.search(r'পরে|পর|বাদে|বাদ|আফ্টার|after', text)
        if after != None and after.group() != "":
            return 1
        return ""

    def extractDueDate(self, text):
        # text = " ".join(text[0])
        due_date = re.search(r'ডিউ ডেট|ডিউডেট|ডিউটি|ডিউটির|ডিউটিটা|ডিউডেটটা|ডিউ ডেটটা|ডিউটিএর|ডিউডেটের|ডিউডেট টা|ডিউ ডেটের|ডিউটি টা|ডিউটিটি|ডিউটি টি', text)
        if due_date != None and due_date.group() != "":
            return "due_date"
        return ""

class GrainUnitExtractionpunjabi:
    
    def extractIntPos(self, text, i):
        try:
            text = " ".join(text[0]).strip()
            temp = re.findall(r'\d+', text)
            temp = list(map(int, temp))
            return temp[i]
        except Exception as ex:
            return -1

    def extractInt(self, text):
        text = " ".join(text[0]).strip()
        temp = re.findall(r'\d+', text)
        if len(temp) == 0:
            return -1
        temp = list(map(int, temp))
        return temp[0]

    def extractMonth(self, text):
        text = " ".join(text[0])
        january = re.search(r'ਜਨਵਰੀ|ਜਾਨਵਰੀ|ਜਾਨੇਵਰੀ|january', text)
        if january != None and january.group() == "":
            return 1
        febuary = re.search(r'ਫਰਵਰੀ|ਫੇਬਰੂਅਰੀ|ਫੇਬਰੂਵਰੀ|february', text)
        if febuary != None and febuary.group() != "":
            return 2
        march = re.search(r'ਮਾਰਚ|march', text)
        if march != None and march.group() != "":
            return 3
        april = re.search(r'ਅਪ੍ਰੈਲ|ਏਪ੍ਰਲ|april', text)
        if april != None and april.group != "":
            return 4
        may = re.search(r'ਮਈ|ਮੇ|may', text)
        if may != None and may.group() != "":
            return 5
        june = re.search(r'ਜੂਨ|june', text)
        if june != None and june.group() != "":
            return 6
        july = re.search(r'ਜੁਲਾਈ|ਜਲਾਈ|july', text)
        if july != None and july.group() != "":
            return 7
        august = re.search(r'ਅਗਸਤ|ਔਗਸਟ|ਔਗਸਤ|august', text)
        if august != None and august.group() != "":
            return 8
        september = re.search(r'ਸਤੰਬਰ|ਸੀਤੰਬਰ|ਸੇਤੰਬਰ|ਸਪਤੰਬਰ|ਸਪਟੰਬਰ|ਸਪਟੈਂਬਰ|september', text)
        if september != None and september.group() != "":
            return 9
        october = re.search(r'ਅਕਤੂਬਰ|ਅਕਟੂਬਰ|october', text)
        if october != None and october.group() != "":
            return 10
        november = re.search(r'ਨਵੰਬਰ|ਨਵੰਬਹ|ਨੌਵੰਬਰ|november', text)
        if november != None and november.group() != "":
            return 11
        december = re.search(r'ਦਸੰਬਰ|ਦੀਸੰਬਰ|december', text)
        if december != None and december.group() != "":
            return 12
        return ""

    def extractWeekday(self, text):
        text = " ".join(text[0])
        monday = re.search(r'ਸੋਮਵਾਰ|ਮੰਡੇ', text)
        if monday != None and monday.group() != "":
            return 1
        tuesday = re.search(r'ਮੰਗਲਵਾਰ|ਟਯੂਸਡੇ|ਟਯੂਜ਼ਡੇ', text)
        if tuesday != None and tuesday.group() != "":
            return 2
        webnesday = re.search(r'ਬੁਧਵਾਰ|ਬੁੱਧਵਾਰ|ਵੇਡਨਸਡੇ|ਵੇਡਨਜ਼ਡੇ|ਵੇਨਜ਼ਡੇ|ਵੇਨਸਡੇ', text)
        if webnesday != None and webnesday.group() != "":
            return 3
        thursday = re.search(r'ਗੁਰਵਾਰ|ਗੁਰੁਵਾਰ|ਵੀਰਵਾਰ|ਥਰਸਡੇ', text)
        if thursday != None and thursday.group() != "":
            return 4
        friday = re.search(r'ਸ਼ੁੱਕਰਵਾਰ|ਫਰਾਈਡੇ', text)
        if friday != None and friday.group() != "":
            return 5
        saturday = re.search(r'ਸ਼ਨੀਵਾਰ|ਸ਼ਨੀਚਰਵਾਰ', text)
        if saturday != None and saturday.group() != "":
            return 6
        sunday = re.search(r'ਐਤਵਾਰ|ਸੰਡੇ|ਰਵੀਵਾਰ', text)
        if sunday != None and sunday.group() != "":
            return 7
        return ""

    def extractMeridiam(self, text):
        # text = " ".join(text[0])
        a = re.search(r'ऍम|पीऍम|पीएम|ऐम', text)
        if a == None or a.group() == "":
            return ""
        meridiam = a.group()
        if meridiam == "ऍम" or meridiam == "ऐम":
            return 1
        elif meridiam == "पीऍम" or meridiam == "पीएम":
            return 2
        else:
            return -1

    def extractDaytime(self, text):
        # text = " ".join(text[0])
        text = text[0]
        evening = re.search(r"ਸ਼ਾਮ|ਸਾਂਝ|ਸੰਧਿਆ|ਆਥਣ|ਈਵ੍ਨਿਂਗ", text)
        if evening != None and evening.group() != "":
            return 18
        night = re.search(r"ਰਾਤ|ਨਿਸ਼ਾ|ਰਾਤਰੀ|ਨਾਈਟ", text)
        if night != None and night.group() != "":
            return 20
        morning = re.search(r"ਸਵੇਰੇ|ਸਵੇਰ|ਭੋਰ|ਉਸ਼ਾ|ਪਰਭਾਤ|ਫਜਰ|ਫ਼ਜਰ|ਮੌਰ੍ਨਿਂਗ", text)
        if morning != None and morning.group() != "":
            return 20
        afternoon = re.search(r"ਆਫਟਰਨੂੂਨ|ਦੁਪਹਿਰ|ਦੁਪੈੈਰ|ਦੁਪੈੈਰੇੇ", text)
        if afternoon != None and afternoon.group() != "":
            return 20
        now = re.search(r"ਤੁਰੰਤ|ਫੌਰਨ|ਤਤਕਾਲ|ਛੇਤੀ|ਕਾਹਲੀ", text)
        if now != None and now.group() != "":
            return 20
        else:
            return ""

    def extractTimeModule(self, text):
        text = " ".join(text[0])
        before = re.search(r'ਅੱਗੇ|ਪਹਿਲਾਂ|ਪਹਿਲੇ|ਅਗੇਤਰ|ਅਗੇਤਾ|ਸ਼ੁਰੂ|ਤੋਂ ਪਹਿਲਾਂ|ਇਸ ਤੋਂ ਪਹਿਲਾਂ|ਸ਼ੁਰੂਆਤੀ|ਦੇ ਅੱਗੇ|ਤੋਂ ਅੱਗੇ|ਮੋਹਰੀ|ਪਹਿਲਾਂ|ਸਾਹਮਣੇ|ਅਗੇਤੀ', text)
        if before != None and before.group() != "":
            return -1
        after = re.search(r'ਪਿਛਲੇ|ਬਾਅਦ|ਬਾਅਦ ਵਿੱਚ|ਹੇਠ|ਇਸ ਤੋਂ ਬਾਅਦ|ਪਿਛੇਤਾ|ਪਿਛੇਤਰ|ਪਿਛੇਤ|ਆਖਰੀ|ਮਗਰ|ਮਗਰਲੇ|ਮਗਾਰਲਾ|ਪਿਛਲਾ|ਪਿਛਲੇ', text)
        if after != None and after.group() != "":
            return 1
        return ""

    def extractDueDate(self, text):
        # text = " ".join(text[0])
        due_date = re.search(r'ਡਿਊ ਡੇਟ|ਡਿਊਟੀ|ਅਦਾਇਗੀ ਤਾਰੀਖ|ਅਦਾਇਗੀ ਮਿਤੀ|ਬਕਾਇਆ ਦੇਣ ਦੀ ਮਿਤੀ|ਬਕਾਇਆ ਦੇਣ ਦੀ ਤਾਰੀਖ|ਡੁਏ ਡਾਟੇ|ਨਿਰਧਾਰਤ ਮਿਤੀ|ਨਿਰਧਾਰਤ ਤਾਰੀਖ|ਬਕਾਇਆ ਮਿਤੀ|ਬਕਾਇਆ ਤਾਰੀਖ|ਭਰਨ ਦੀ ਮਿਤੀ|ਭਰਨ ਦੀ ਤਾਰੀਖ|ਆਦੀਇਗੀ ਤਰੀਕ|ਨਿਰਧਾਰਤ ਮਿਟੀ|ਬਾਕੀ ਮਿਤੀ|ਅਦਿਇਗੀ ਮਿਟੀ|ਅਦਿਇਗੀ ਤਾਰਿਕ਼|ਨਿਰ੍ਧਾਰਿਤ ਮਿਤੀ|ਨਿਰਧਾਰਿਤ ਤਾਰੀਕ|ਭੁਗਤਾਨ ਦੀ ਮਿਤੀ|ਭੁਗਤਾਨ ਦੀ ਤਾਰੀਕ|ਭੁਗਤਾਨ ਦੀ ਤਾਰੀਖ|ਭੁਗਤਣ ਮਿਟੀ|ਭੁਗਤਮਿਤੀ', text)
        if due_date != None and due_date.group() != "":
            return "due_date"
        return ""

class GrainUnitExtractionenglish:
    
    def extractIntPos(self, text, i):
        try:
            text = " ".join(text[0]).strip()
            temp = re.findall(r'\d+', text)
            temp = list(map(int, temp))
            return temp[i]
        except Exception as ex:
            return -1

    def extractInt(self, text):
        text = " ".join(text[0]).strip()
        temp = re.findall(r'\d+', text)
        if len(temp) == 0:
            return -1
        temp = list(map(int, temp))
        return temp[0]

    def extractMonth(self, text):
        text = " ".join(text[0])
        january = re.search(r'january', text)
        if january != None and january.group() == "":
            return 1
        febuary = re.search(r'february', text)
        if febuary != None and febuary.group() != "":
            return 2
        march = re.search(r'march', text)
        if march != None and march.group() != "":
            return 3
        april = re.search(r'april', text)
        if april != None and april.group != "":
            return 4
        may = re.search(r'may', text)
        if may != None and may.group() != "":
            return 5
        june = re.search(r'june', text)
        if june != None and june.group() != "":
            return 6
        july = re.search(r'july', text)
        if july != None and july.group() != "":
            return 7
        august = re.search(r'august', text)
        if august != None and august.group() != "":
            return 8
        september = re.search(r'september', text)
        if september != None and september.group() != "":
            return 9
        october = re.search(r'october', text)
        if october != None and october.group() != "":
            return 10
        november = re.search(r'november', text)
        if november != None and november.group() != "":
            return 11
        december = re.search(r'december', text)
        if december != None and december.group() != "":
            return 12
        return ""

    def extractWeekday(self, text):
        text = " ".join(text[0])
        monday = re.search(r'monday|somwar|somvar', text)
        if monday != None and monday.group() != "":
            return 1
        tuesday = re.search(r'tuesday|mangalwar|mangalvar', text)
        if tuesday != None and tuesday.group() != "":
            return 2
        webnesday = re.search(r'wednesday|budhwar|budhvar', text)
        if webnesday != None and webnesday.group() != "":
            return 3
        thursday = re.search(r'thursday|guruwar|guruvar', text)
        if thursday != None and thursday.group() != "":
            return 4
        friday = re.search(r'friday|shukravar|shukarwar|shukarvar|shukrawar', text)
        if friday != None and friday.group() != "":
            return 5
        saturday = re.search(r'saturday|shaniwar|shanivar', text)
        if saturday != None and saturday.group() != "":
            return 6
        sunday = re.search(r'sunday|raviwar|ravivar', text)
        if sunday != None and sunday.group() != "":
            return 7
        return ""

    def extractMeridiam(self, text):
        # text = text
        a = re.search(r'am|pm|a.m.|p.m.', text)
        if a == None or a.group() == "":
            return ""
        meridiam = a.group()
        if meridiam == "am" or meridiam == "a.m.":
            return 1
        elif meridiam == "pm" or meridiam == "p.m.":
            return 2
        else:
            return -1

    def extractDaytime(self, text):
        # text = " ".join(text[0])
        text = text[0]
        evening = re.search(r"evening|shaam", text)
        if evening != None and evening.group() != "":
            return 18
        night = re.search(r"night|raat|tonight", text)
        if night != None and night.group() != "":
            return 20
        morning = re.search(r"morning|subah", text)
        if morning != None and morning.group() != "":
            return 10
        afternoon = re.search(r"afternoon|noon|din", text)
        if afternoon != None and afternoon.group() != "":
            return 12
        now = re.search(r"second|right away|right now", text)
        if now != None and now.group() != "":
            return -1
        else:
            return ""

    def extractTimeModule(self, text):
        text = " ".join(text[0])
        before = re.search(r'before', text)
        if before != None and before.group() != "":
            return -1
        after = re.search(r'after|later', text)
        if after != None and after.group() != "":
            return 1
        return ""

    def extractDueDate(self, text):
        # text = " ".join(text[0])
        due_date = re.search(r'due date', text)
        if due_date != None and due_date.group() != "":
            return "due_date"
        return ""



class GrainUnitExtractiongujrati:
    
    def extractIntPos(self, text, i):
        try:
            text = " ".join(text[0]).strip()
            temp = re.findall(r'\d+', text)
            temp = list(map(int, temp))
            return temp[i]
        except Exception as ex:
            return -1

    def extractInt(self, text):
        text = " ".join(text[0]).strip()
        temp = re.findall(r'\d+', text)
        if len(temp) == 0:
            return -1
        temp = list(map(int, temp))
        return temp[0]

    def extractMonth(self, text):
        text = " ".join(text[0])
        january = re.search(r'જાન્યુઆરી|જાન્યુવારી|january', text)
        if january != None and january.group() == "":
            return 1
        febuary = re.search(r'ફેબ્રુઆરી|ફેબ્રુવારી|february', text)
        if febuary != None and febuary.group() != "":
            return 2
        march = re.search(r'માર્ચ|માર્ચે|march', text)
        if march != None and march.group() != "":
            return 3
        april = re.search(r'એપ્રિલ|એપ્રિલે|april', text)
        if april != None and april.group != "":
            return 4
        may = re.search(r'મેય|may', text)
        if may != None and may.group() != "":
            return 5
        june = re.search(r'જુન|જુને|june', text)
        if june != None and june.group() != "":
            return 6
        july = re.search(r'જુલાઈ|જુલાય|july', text)
        if july != None and july.group() != "":
            return 7
        august = re.search(r'ઓગસ્ટ|ઓગસ્ટે|august', text)
        if august != None and august.group() != "":
            return 8
        september = re.search(r'સપ્ટેમ્બર|સપ્ટેંબર|સપ્ટેમ્બરે|સપ્ટેંબર|સપ્ટેંબરે|september', text)
        if september != None and september.group() != "":
            return 9
        october = re.search(r'ઓક્ટોબર|ઓક્ટોમ્બર|ઓક્ટોબરે|october', text)
        if october != None and october.group() != "":
            return 10
        november = re.search(r'નવંબર|નવેમ્બર|નવેંબર|નવેમ્બરે|november', text)
        if november != None and november.group() != "":
            return 11
        december = re.search(r'ડીસેમ્બર|ડીસેમ્બરે|december', text)
        if december != None and december.group() != "":
            return 12
        return ""

    def extractWeekday(self, text):
        text = " ".join(text[0])
        monday = re.search(r'સોમવાર|મંડે|સોમવારે', text)
        if monday != None and monday.group() != "":
            return 1
        tuesday = re.search(r'મંગળવાર|ટ્યુસડે|ટ્યુઝડે|મંગલવાર|મંગળવારે', text)
        if tuesday != None and tuesday.group() != "":
            return 2
        webnesday = re.search(r'બુધવાર|વેડનસડે|વેનસડે|બુધવારે', text)
        if webnesday != None and webnesday.group() != "":
            return 3
        thursday = re.search(r'ગુરુવાર|થર્સડે|ગુરુવારે', text)
        if thursday != None and thursday.group() != "":
            return 4
        friday = re.search(r'શુક્રવાર|ફ્રાઇડે|ફ્રાયડે|શુક્રવારે', text)
        if friday != None and friday.group() != "":
            return 5
        saturday = re.search(r'શનિવાર|સેટરડે|શનિવારે', text)
        if saturday != None and saturday.group() != "":
            return 6
        sunday = re.search(r'રવિવાર|સંડે|સનડે|રવિવારે', text)
        if sunday != None and sunday.group() != "":
            return 7
        return ""

    def extractMeridiam(self, text):
        # text = " ".join(text[0])
        a = re.search(r'am|pm|a.m.|p.m.', text)
        if a == None or a.group() == "":
            return ""
        meridiam = a.group()
        if meridiam == "am" or meridiam == "a.m.":
            return 1
        elif meridiam == "pm" or meridiam == "p.m.":
            return 2
        else:
            return -1

    def extractDaytime(self, text):
        # text = " ".join(text[0])
        text = text[0]
        evening = re.search(r"સાંજ|સાંજે|ઇવનિંગ", text)
        if evening != None and evening.group() != "":
            return 18
        night = re.search(r"રાત|રાત્રે|નાઈટ", text)
        if night != None and night.group() != "":
            return 20
        morning = re.search(r"સવાર|મોર્નિંગ", text)
        if morning != None and morning.group() != "":
            return 10
        afternoon = re.search(r"આફ્ટરનૂન|બપોર", text)
        if afternoon != None and afternoon.group() != "":
            return 12
        now = re.search(r"તરત|હમણાં|અત્યારે", text)
        if now != None and now.group() != "":
            return -1
        else:
            return ""

    def extractTimeModule(self, text):
        text = " ".join(text[0])
        before = re.search(r'પહેલા|પેહલા|પેલા', text)
        if before != None and before.group() != "":
            return -1
        after = re.search(r'પછી', text)
        if after != None and after.group() != "":
            return 1
        return ""

    def extractDueDate(self, text):
        # text = " ".join(text[0])
        due_date = re.search(r'due date|ડ્યુડેટ|છેલ્લી તારીખ|આખર તારીખ|ડ્યુટી', text)
        if due_date != None and due_date.group() != "":
            return "due_date"
        return ""
