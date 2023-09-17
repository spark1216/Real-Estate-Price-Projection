from flask import Flask, request, jsonify
import util
app=Flask(__name__)
@app.route('http://127.0.0.1:5000/get_estimated_price',methods=['POST'])
def get_estimated_price():
    bed=int(request.form['bed'])
    bath=int(request.form['bath'])
    acre_lot = int(request.form['acre_lot'])
    housesize=int(request.form['house_size'])
    zipcode=int(request.form['zip_code'])
    estimated_price=util.get_estimated_price(bed, bath, acre_lot, housesize, zipcode)
    response=jsonify({'estimated_price': estimated_price})
    response.headers.add("Access-Control-Allow-Origin","*")
    return response
if __name__ == "__main__":
    util.load_saved_artifacts()
    print("Starting Python Flask Server for Home Price Prediction...")
    app.run()
