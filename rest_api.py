from flask import Flask, jsonify, request
import pandas as pd
import datetime

app = Flask(__name__)

def read_data():
    for chunk in pd.read_csv('weather.csv',chunksize=1000):
        yield chunk

@app.route('/forecasts', methods=['GET'])
def get_forecasts():
    # Get the parameters
    now = request.args.get('now')
    then = request.args.get('then')

    if now == None:
        return jsonify({'error':"Missing 'now' parameter"})
    
    if then == None:
        return jsonify({'error':"Missing 'then' parameter"})

    # Convert them to datetime
    try:
        now = datetime.datetime.fromisoformat(now)
    except Exception:
        return jsonify({'error':"Parameter 'now' is wrong formated.Please provide iso format"})
    
    try:
        then = datetime.datetime.fromisoformat(then)
    except Exception:
        return jsonify({'error':"Parameter 'then' is wrong formated.Please provide iso format"})

    results_now = []
    results_then = []

    for chunk in read_data():
        now_str = now.strftime("%Y-%m-%d %H:%M:%S%z")[:-2]
        then_str = then.strftime("%Y-%m-%d %H:%M:%S%z")[:-2]
        filtered_chunk_now = chunk.query("event_start == @now_str")
        filtered_chunk_then=chunk.query("event_start == @then_str")
        data_now = filtered_chunk_now.to_dict('records')
        data_then = filtered_chunk_then.to_dict('records')

        if data_now:
            for line in data_now:
                results_now.append(line)

        if data_then:
            for line in data_then:
                results_then.append(line)

    result=[]
    added_temp=False
    added_sunny=False
    added_wind_speed=False

    for now in data_now:
        for then in data_then:
            sensor_now = now['sensor']
            value_now = now['event_value']
            sensor_then=then['sensor']
            value_then=then['event_value']

            if sensor_now =='temperature' and sensor_then=='temperature' and value_now == value_then and added_temp == False:
                result.append(then)
                added_temp=True
            elif sensor_now == 'irradiance' and sensor_then=='irradiance' and value_now == value_then and added_sunny==False:
                result.append(then)
                added_sunny=True
            elif added_wind_speed == False:
                result.append(then)
                added_wind_speed=True
            

    if result:
         return jsonify({'data':result})
   
    # Convert to json and return
    return jsonify({'data':[]})

@app.route('/tomorrow', methods=['GET'])
def get_tomorrow():
    #values to return
    warm=False
    sunny=False
    windy = False

    #actual values
    temperature_all=0
    temperature_count=0
    sunny_all=0
    sunny_count=0
    windy_all=0
    windy_count=0

    #theresholds
    warm_threshold = 15
    sunny_threshold = 50
    windy_threshold = 2

    # Get the parameters
   
    now = request.args.get('now')
    
    if now == None:
        return jsonify({'error':"Missing 'now' parameter"})
    
    # Convert them to datetime
    try:
        now = datetime.datetime.fromisoformat(now)
    except Exception as e:
        return jsonify({'error':"Parameter 'now' is wrong formated.Please provide iso format"})

    tomorrow = now + datetime.timedelta(days=1)

    for chunk in read_data():
        tomorrow_str = tomorrow.strftime("%Y-%m-%d %H:%M:%S%z")[:-2]
        filtered_chunk = chunk.query("event_start == @tomorrow_str")
        data = filtered_chunk.to_dict('records')
        if data:
            for line in data:
                sensor = line['sensor']
                value = line['event_value']

                if sensor =='temperature':
                    temperature_all = temperature_all + value
                    temperature_count += 1
                elif sensor == 'irradiance':
                    sunny_all=sunny_all+value
                    sunny_count+=1
                else: #wind speed
                    windy_all = windy_all+value
                    windy_count+=1

    if temperature_all / temperature_count >= warm_threshold:
        warm=True
    if sunny_all/sunny_count >= sunny_threshold:
        sunny=True
    if windy_all/windy_count >= windy_threshold:
        windy=True 

    data={
        'warm':warm,
        'sunny':sunny,
        'windy':windy
    }
    # Convert to json and return
    return jsonify({'data':data}),200

if __name__ == '__main__':
    app.run(port=5000,debug=True)