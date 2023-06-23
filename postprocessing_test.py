from postprocessing.main import postprocess_entities

if __name__=='__main__':
    text = "end of next 2 week"
    entities = ['L-ptp_date', 'L-ptp_date', 'U-ptp_date', 'U-ptp_date', 'U-ptp_date', 'U-ptp_date']
    print(postprocess_entities(text, entities, lang="english", current_date="29/01/2023 12:00:00"))

# import requests
# from tqdm import tqdm
# import pytz
# from datetime import datetime as Date
# import pandas as pd

# def strip_func(x):
#         return str(x).strip()
    
# def convert_date_time_format(date, current_format = "%Y-%m-%d %H:%M:%S", required_format = "%d/%m/%Y %H:%M:%S"):
#     try:
#         updated_date = Date.strptime(date, current_format)
#         return Date.strftime(updated_date, required_format)
#     except Exception as ex:
#         return None


# if __name__ == "__main__":

    # df = pd.read_csv("./../../TestingDataChatbot/kn-IN_call_logs_26thApril_6thMay.csv")
    # all_text = df["Text"].apply(strip_func)
    # date = df["Created At"].apply(convert_date_time_format)
    # lang = "kannada"
    # ner2, ner2_label_text, post_ner, post_ner_time, tags = [], [], [], [], []
    # for i, text in tqdm(enumerate(all_text)):
    #     try:
    #         entity_response = requests.post('http://52.151.242.140:80/api/v1/service/testing-ner/score',json={"data": text, "date": date[i], "lang":lang}).json()
    #     except Exception as ex:
    #         print(text + " ------ " + f"{i}" + " ------- " + str(ex.args))
    #     try:
    #         post_ner.append(str(entity_response["entities"][0]["value"]))
    #     except Exception as ex:
    #         post_ner.append("none")
    #     try:
    #         post_ner_time.append(str(entity_response["entities"][1]["value"]))
    #     except Exception as ex:
    #         post_ner_time.append("none")
    #     try:
    #         tags.append(str(entity_response["tags"]))
    #     except Exception as ex:
    #         tags.append("none")
            
    # df1 = pd.DataFrame()
    # df1["Text"] = all_text
    # df1["Reference_Date"] = date
    # df1["NER2.0 Date"] = post_ner
    # df1["NER2.0 Time"] = post_ner_time
    # df1["Tags"] = tags

    # df1.to_csv("./../" + lang.title() + "NER_Pred.csv", index = False)

# # import ast

# # if __name__ == "__main__":
# #     df = pd.read_csv('./../TestingDataChatbot/hi-IN_call_logs.csv')
# #     lang = "hindi"
# #     text = df["text"]
# #     date = df["created_at"].apply(convert_date_time_format)
# #     tags = df["Tags"]

# #     ner_date, ner_time = [], []
# #     for i in tqdm(range(len(df))):
# #         tags[i] = ast.literal_eval(tags[i])
# #         response = postprocess_entities(str(text[i]), tags[i], current_date=date[i], lang = lang)
# #         if len(response["date"]) == 0:
# #             ner_date.append("none")
# #         else:
# #             ner_date.append(response["date"][0])
# #         if len(response["time"]) == 0:
# #             ner_time.append("none")
# #         else:
# #             ner_time.append(response["time"][0])

# #     df1 = pd.DataFrame()
# #     df1["Text"] = text
# #     df1["Reference_Date"] = date
# #     df1["NER2.0 Date"] = ner_date
# #     df1["NER2.0 Time"] = ner_time
# #     df1["Tags"] = tags

# #     df1.to_csv(lang.title()+"NER_Pred.csv", index = False)