import pickle
import numpy as np
import pgeocode
__model=None
__st=None
__scaler_bed=None
__scaler_bath=None
__scaler_acre_lot=None
__scaler_latitude=None
__scaler_longitude=None
__scaler_house_size=None
__scaler_price=None

def get_state(zipcode):
    try:
        zipcode = int(zipcode)
    except ValueError:
        return None

    if 35000 <= zipcode <= 36999:
        st = 'AL'
    elif 99500 <= zipcode <= 99999:
        st = 'AK'
    elif 85000 <= zipcode <= 86999:
        st = 'AZ'
    elif 71600 <= zipcode <= 72999:
        st = 'AR'
    elif 90000 <= zipcode <= 96699:
        st = 'CA'
    elif 80000 <= zipcode <= 81999:
        st = 'CO'
    elif (6000 <= zipcode <= 6389) or (6391 <= zipcode <= 6999):
        st = 'CT'
    elif 19700 <= zipcode <= 19999:
        st = 'DE'
    elif 32000 <= zipcode <= 34999:
        st = 'FL'
    elif (30000 <= zipcode <= 31999) or (39800 <= zipcode <= 39999):
        st = 'GA'
    elif 96700 <= zipcode <= 96999:
        st = 'HI'
    elif 83200 <= zipcode <= 83999 and zipcode != 83414:
        st = 'ID'
    elif 60000 <= zipcode <= 62999:
        st = 'IL'
    elif 46000 <= zipcode <= 47999:
        st = 'IN'
    elif 50000 <= zipcode <= 52999:
        st = 'IA'
    elif 66000 <= zipcode <= 67999:
        st = 'KS'
    elif 40000 <= zipcode <= 42999:
        st = 'KY'
    elif 70000 <= zipcode <= 71599:
        st = 'LA'
    elif 3900 <= zipcode <= 4999:
        st = 'ME'
    elif 20600 <= zipcode <= 21999:
        st = 'MD'
    elif (1000 <= zipcode <= 2799) or (zipcode == '5501') or (zipcode == '5544'):
        st = 'MA'
    elif 48000 <= zipcode <= 49999:
        st = 'MI'
    elif 55000 <= zipcode <= 56899:
        st = 'MN'
    elif 38600 <= zipcode <= 39999:
        st = 'MS'
    elif 63000 <= zipcode <= 65999:
        st = 'MO'
    elif 59000 <= zipcode <= 59999:
        st = 'MT'
    elif 27000 <= zipcode <= 28999:
        st = 'NC'
    elif 58000 <= zipcode <= 58999:
        st = 'ND'
    elif 68000 <= zipcode <= 69999:
        st = 'NE'
    elif 88900 <= zipcode <= 89999:
        st = 'NV'
    elif 3000 <= zipcode <= 3899:
        st = 'NH'
    elif 7000 <= zipcode <= 8999:
        st = 'NJ'
    elif 87000 <= zipcode <= 88499:
        st = 'NM'
    elif (10000 <= zipcode <= 14999) or (zipcode == 6390) or (zipcode == 501) or (zipcode == 544):
        st = 'NY'
    elif 43000 <= zipcode <= 45999:
        st = 'OH'
    elif (73000 <= zipcode <= 73199) or (73400 <= zipcode <= 74999):
        st = 'OK'
    elif 97000 <= zipcode <= 97999:
        st = 'OR'
    elif 15000 <= zipcode <= 19699:
        st = 'PA'
    elif 300 <= zipcode <= 999:
        st = 'PR'
    elif 2800 <= zipcode <= 2999:
        st = 'RI'
    elif 29000 <= zipcode <= 29999:
        st = 'SC'
    elif 57000 <= zipcode <= 57999:
        st = 'SD'
    elif 37000 <= zipcode <= 38599:
        st = 'TN'
    elif (75000 <= zipcode <= 79999) or (73301 <= zipcode <= 73399) or (88500 <= zipcode <= 88599):
        st = 'TX'
    elif 84000 <= zipcode <= 84999:
        st = 'UT'
    elif 5000 <= zipcode <= 5999:
        st = 'VT'
    elif (20100 <= zipcode <= 20199) or (22000 <= zipcode <= 24699) or (zipcode == 20598):
        st = 'VA'
    elif (20000 <= zipcode <= 20099) or (20200 <= zipcode <= 20599) or (56900 <= zipcode <= 56999):
        st = 'DC'
    elif 98000 <= zipcode <= 99499:
        st = 'WA'
    elif 24700 <= zipcode <= 26999:
        st = 'WV'
    elif 53000 <= zipcode <= 54999:
        st = 'WI'
    elif (82000 <= zipcode <= 83199) or (zipcode == 83414):
        st = 'WY'
    else:
        st=None

    global __st
    __st=st
    return st


def get_estimated_price(bed, bath, acre_lot, housesize, zipcode):
    nomi = pgeocode.Nominatim('us')
    query = nomi.query_postal_code(str(zipcode))
    if not query.empty:
        latitude = query['latitude']
        longitude = query['longitude']
    if get_state(zipcode) == 'ME':
        ME = np.array(1)
        MA = np.array(0)
        NJ = np.array(0)
        NY = np.array(0)
    elif get_state(zipcode) == 'MA':
        MA = np.array(1)
        NJ = np.array(0)
        NY = np.array(0)
        ME = np.array(0)
    elif get_state(zipcode) == 'NJ':
        MA = np.array(0)
        NJ = np.array(1)
        NY = np.array(0)
        ME = np.array(0)
    elif get_state(zipcode) == 'NY':
        MA = np.array(0)
        NJ = np.array(0)
        NY = np.array(1)
        ME = np.array(0)
    else:
        MA = np.array(0)
        NJ = np.array(0)
        NY = np.array(0)
        ME = np.array(0)
    bed = __scaler_bed.transform(np.array(bed).reshape(-1, 1))
    bath = __scaler_bath.transform(np.array(bath).reshape(-1, 1))
    acre_lot = __scaler_acre_lot.transform(np.array(acre_lot ** 0.02).reshape(-1, 1))
    latitude = __scaler_latitude.transform(np.array(latitude).reshape(-1, 1))
    longitude = __scaler_longitude.transform(np.array(longitude).reshape(-1, 1))
    house_size = __scaler_house_size.transform(np.array(np.log(housesize)).reshape(-1, 1))
    features = [bed, bath, acre_lot, latitude, longitude, house_size, ME, MA, NJ, NY]
    features = np.concatenate([arr.flatten() for arr in features])
    features_2d = np.array(features).reshape(1, -1)
    pred = __model.predict(features_2d)
    pred = __scaler_price.inverse_transform(pred.reshape(-1, 1))
    price = np.exp(pred)
    return np.round(price,2)[0][0]

def load_saved_artifacts():
    global __model
    global __scaler_bed
    global __scaler_bath
    global __scaler_acre_lot
    global __scaler_latitude
    global __scaler_longitude
    global __scaler_house_size
    global __scaler_price
    with open("./artifacts/US_house_prices_model.pickle","rb") as f:
        saved_artifacts1=pickle.load(f)
        __model=saved_artifacts1
    with open("./artifacts/US_house_prices_model_scaler.pickle", "rb") as f:
        saved_artifacts=pickle.load(f)
        __scaler_bed = saved_artifacts['scaler_bed']
        __scaler_bath = saved_artifacts['scaler_bath']
        __scaler_acre_lot = saved_artifacts['scaler_acre_lot']
        __scaler_latitude = saved_artifacts['scaler_latitude']
        __scaler_longitude = saved_artifacts['scaler_longitude']
        __scaler_house_size = saved_artifacts['scaler_house_size']
        __scaler_price=saved_artifacts['scaler_price']
    print("loading saved artifacts... done")
if __name__ == "__main__":
    load_saved_artifacts()
