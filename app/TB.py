import numpy as np
import pandas as pd
import xgboost as xgb


class model():
    subset = [
        "AGE",
        "CO",
        "O3",
        "SO2",
        "NO",
        "NO2",
        "NOx",
        "PM2.5",
        "PM10",
        "SEX",
        "Pneumonia",
        "PeripheralVascularDisease",
        "Hyperlipidemia",
        "MyocardialInfraction",
        "Dementia",
        "CongestiveHeartFailure",
        "Cancer",
        "DiabetesMellitus",
        "ObstructiveLungDisease",
        "AcuteRenalFailure",
        "ChronicKidneyDisease",
        "CerebrovascularDiease",
        "HBV",
        "HCV"
    ]
    caution_count = 0
    model = xgb.Booster()

    def __init__(self):
        self.model.load_model('app/TB.json')

    def set_airfactor_color(self, aqi):
        if aqi["co"] > 15.4:
            case_co = 4
        elif 15.4 >= aqi["co"] > 12.4:
            case_co = 3
        elif 12.4 >= aqi["co"] > 6.4:
            case_co = 2
        elif 9.4 >= aqi["co"] > 4.4:
            case_co = 1
        else:
            case_co = 0

        if aqi["o3"] > 105:
            case_o3 = 4
        elif 105 >= aqi["o3"] > 85:
            case_o3 = 3
        elif 85 >= aqi["o3"] > 70:
            case_o3 = 2
        elif 70 >= aqi["o3"] > 54:
            case_o3 = 1
        else:
            case_o3 = 0

        if aqi["so2"] > 304:
            case_so2 = 4
        elif 304 >= aqi["so2"] > 185:
            case_so2 = 3
        elif 185 >= aqi["so2"] > 75:
            case_so2 = 2
        elif 75 >= aqi["so2"] > 35:
            case_so2 = 1
        else:
            case_so2 = 0

        if aqi["no"] > 649:
            case_no = 4
        elif 649 >= aqi["no"] > 360:
            case_no = 3
        elif 360 >= aqi["no"] > 100:
            case_no = 2
        elif 100 >= aqi["no"] > 53:
            case_no = 1
        else:
            case_no = 0

        if aqi["no2"] > 649:
            case_no2 = 4
        elif 649 >= aqi["no2"] > 360:
            case_no2 = 3
        elif 360 >= aqi["no2"] > 100:
            case_no2 = 2
        elif 100 >= aqi["no2"] > 53:
            case_no2 = 1
        else:
            case_no2 = 0

        if aqi["nox"] > 649:
            case_nox = 4
        elif 649 >= aqi["nox"] > 360:
            case_nox = 3
        elif 360 >= aqi["nox"] > 100:
            case_nox = 2
        elif 100 >= aqi["nox"] > 53:
            case_nox = 1
        else:
            case_nox = 0

        if aqi["pm2.5"] > 150.4:
            case_pm25 = 4
        elif 150.4 >= aqi["pm2.5"] > 54.4:
            case_pm25 = 3
        elif 54.4 >= aqi["pm2.5"] > 35.4:
            case_pm25 = 2
        elif 35.4 >= aqi["pm2.5"] > 15.4:
            case_pm25 = 1
        else:
            case_pm25 = 0

        if aqi["pm10"] > 354:
            case_pm10 = 4
        elif 354 >= aqi["pm10"] > 254:
            case_pm10 = 3
        elif 254 >= aqi["pm10"] > 125:
            case_pm10 = 2
        elif 125 >= aqi["pm10"] > 54:
            case_pm10 = 1
        else:
            case_pm10 = 0

        self.caution_count = sum([case_co, case_no, case_no2, case_nox,case_so2, case_o3, case_pm10, case_pm25])

    def predict(self, data):
        self.set_airfactor_color(data.air_data)
        row = {
            "HBV": data.dis_list[0],
            "HCV": data.dis_list[1],
            "Cancer": data.dis_list[2],
            "Dementia": data.dis_list[3],
            "Hyperlipidemia": data.dis_list[4],
            "DiabetesMellitus": data.dis_list[5],
            "MyocardialInfraction": data.dis_list[6],
            "ChronicKidneyDisease": data.dis_list[7],
            "CerebrovascularDiease": data.dis_list[8],
            "CongestiveHeartFailure": data.dis_list[9],
            "PeripheralVascularDisease": data.dis_list[10],
            "Pneumonia": data.dis_list[11],
            "ObstructiveLungDisease": data.dis_list[12],
            "AcuteRenalFailure": data.dis_list[13],
            "AGE": int(data.age),
            "ID": data.id,
            "ADDR": data.address,
            "PM2.5": data.air_data["pm2.5"],
            "CO": data.air_data["co"],
            "PM10": data.air_data["pm10"],
            "O3": data.air_data["o3"],
            "SO2": data.air_data["so2"],
            "NO": data.air_data["no"],
            "NOx": data.air_data["nox"],
            "NO2": data.air_data["no2"],
            "SEX": data.sex
        }
        df = pd.DataFrame(row, index=[0])
        df = df[self.subset]
        df = df.astype(float)
        df = df[['SEX', 'Pneumonia', 'PeripheralVascularDisease', 'Hyperlipidemia', 'MyocardialInfraction', 'Dementia', 'CongestiveHeartFailure', 'Cancer', 'DiabetesMellitus', 'ObstructiveLungDisease', 'AcuteRenalFailure', 'ChronicKidneyDisease', 'CerebrovascularDiease', 'HBV', 'HCV', 'CO', 'O3', 'SO2', 'NO', 'NO2', 'NOx', 'PM2.5', 'PM10', 'AGE']]
        df = xgb.DMatrix(df)
        res = self.model.predict(df)
        prediction_output = self.two_class_encoding(res)
        cof = prediction_output[0][0]
        cof = 1 - cof
        cof *= 100
        cof = round(cof, 3)
        if cof > 100:
            cof = 100
        if cof < 0:
            cof = 0.0
        cof = round(cof, 3)
        if cof >= 60:
            if self.caution_count == 0:
                cof -= 30
            elif self.caution_count == 1:
                cof -= 20
            elif self.caution_count == 2:
                cof -= 10
        return cof
	 
    def two_class_encoding(self,flat_prediction):
        if len(np.shape(flat_prediction)) == 2:
            return flat_prediction
        else:
            # class 1 probability
            class_one_prob = 1.0 / (1.0 + np.exp(-flat_prediction))
            class_one_prob = np.reshape(class_one_prob, [-1, 1])
            # class 0 probability
            class_zero_prob = 1 - class_one_prob
            class_zero_prob = np.reshape(class_zero_prob, [-1, 1])
            # concatenate the probabilities to get the final prediction
            sigmoid_two_class_pred = np.concatenate((class_zero_prob, class_one_prob), axis=1)

            return sigmoid_two_class_pred
