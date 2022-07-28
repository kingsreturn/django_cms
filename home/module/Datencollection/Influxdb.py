from datetime import datetime
#import CollectData
import random
import time,sched
from rx.scheduler import ThreadPoolScheduler

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import schedule
import pandas
#from .opc import Opc
import _thread
import json

import atexit
import platform
from datetime import timedelta

#import psutil as psutil
import rx
from rx import operators as ops

from influxdb_client import InfluxDBClient, WriteApi, WriteOptions

class Influxdb:
    def __init__(self):
        self.url= "http://8.140.157.208:8086"
        self.token="mPOJrMM1ZhVx0J_gUVCuNiu7H0qYtg5Dhp-RnXcZ0MvNY_UZ_Vv_pbB_l8Mq_TJBjYrQVxu-iOuwaYARIh1s8A=="
        self.org="IWM"
        #self.client=InfluxDBClient()

    # You can generate a Token from the "Tokens Tab" in the UI
    def ConnnectDatabase(self):
        try:
            self.client = InfluxDBClient(url=self.url, token=self.token,org=self.org)
            return True
        except Exception:
            print(Exception.args)
            return False

    def WriteDataPoint(self,bucket,Measurement,Tag,Value,time):
        org = "IWM"
        Value=random.randint(1,100)
        bucket='django-cms'
        #_point1 = Point(Measurement).tag("Quality", Tag).field("temperature", Value).time(datetime.utcnow(), WritePrecision.MS)
        _write_api = self.client.write_api(write_options=WriteOptions(batch_size=1))
        #_write_api = self.client.write_api(write_options=SYNCHRONOUS)
        #_write_api.write(bucket=bucket, record=line_protocol('opc', Measurement, Value))
        _write_api.write(bucket, org, line_protocol('opc', Measurement, Value))
        print('Write Data success!')

    def WriteData(self,Protocol,VariableName,Value,time):

        data = rx \
            .interval(period=timedelta(seconds=5)) \
            .pipe(ops.map(lambda t: random.randint(0,100)),
                  ops.distinct_until_changed(),
                  ops.map(lambda Value: line_protocol(Protocol,VariableName,Value)))


        _write_api = self.client.write_api(write_options=WriteOptions(batch_size=1))
        _write_api.write(bucket="opc", record=data)

        print('Write Data completed!')

    def ConstantWriteData(self,Protocol,VariableName,Value):

        data = rx \
            .interval(period=timedelta(seconds=5)) \
            .pipe(ops.map(lambda t: random.randint(0,100)),
                  ops.distinct_until_changed(),
                  ops.map(lambda Value: line_protocol(Protocol,VariableName,Value)))

        _write_api = self.client.write_api(write_options=WriteOptions(batch_size=1))
        _write_api.write(bucket="opc", record=data)

        print('Write Data completed!')
        atexit.register(on_exit, _db_client.client, _write_api)

        input()

    def Query(self,org,bucket):
        org = "IWM"
        #bucket = "django_cms"
        query = 'from(bucket: \\"{bucket}\\") |> range(start: -30m)'
        tables = self.client.query_api().query(query)
        for table in tables:
            print(table)
            for row in table.records:
                pass
                print(row.values)
        return tables


def line_protocol(Protocol,VariableName,Value):
        """Create a InfluxDB line protocol with structure:

        iot_sensor,hostname=mine_sensor_12,type=temperature value=68

        :param temperature: the sensor temperature
        :return: Line protocol to write into InfluxDB
        """

        import socket
        return 'iot_sensor,host={},Name={} value={} value'.format(Protocol,VariableName,Value)

def on_exit(db_client: InfluxDBClient, write_api: WriteApi):
    """Close clients after terminate a script.

    :param db_client: InfluxDB client
    :param write_api: WriteApi
    :return: nothing
    """
    write_api.close()
    db_client.close()



if __name__ == "__main__":
    """
    Read temperature every minute; distinct_until_changed - produce only if temperature change
    """

    data = rx.interval(period=timedelta(seconds=5)) \
        .pipe(ops.map(lambda t: random.randint(0,100)),
              ops.distinct_until_changed(),
              ops.map(lambda temperature: line_protocol('mqtt','temprature',temperature)))


    token = "C3Guf2T-IQ4uDxvFK74Yjm5v5uNtxaP_py4FUr4Q48aDjOxSJh-eCBbSz2HGBo1BvNeJfbw6lUz1dPQHWlLysw=="

    _db_client=Influxdb()
    _db_client.ConnnectDatabase()

    bucket = "django_cms"
    url = "http://8.140.157.208:8086"
    org = "IWM"

    # You can generate a Token from the "Tokens Tab" in the UI


    _db_client = InfluxDBClient(url=url, token=token, org=org)

    query_api = _db_client.query_api()

    ## using Table structure

    tables = query_api.query('from(bucket:"opc") |> range(start: -15m)')

    for table in tables:
        print(table)
        for row in table.records:
            print(row.values)



    # using Dataframe
    #data_frame = pandas.DataFrame()
    data_frame = query_api.query_data_frame('from(bucket:"opc") '
                                            '|> range(start: -12m) '
                                            '|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value") '
                                            '|> keep(columns: ["location", "Beschleunigung"])')
    print(data_frame)

    #print(table)
    #_db_client.WriteData('opc','temperature','gut',35)
    #opc=Opc('','','Weg')
    #value=opc.GetData().value
    #schedule.clear()
    #schedule.every(5).seconds.do(_db_client.ConstantWriteData('opc', 'Weg', random.randint(0,100)))
    #_db_client.ConstantWriteData('opc', 'Beschleunigung', 3)
    #_db_client.Query('','opc')
    '''
    n=0
    while True:
        _db_client.ConstantWriteData('opc', 'Weg', 3)
        n+=1
        print('Signal is read {} times!'.format(n))
        time.sleep(5)
        '''
    #_point1 = Point("my_measurement").tag("location", "Prague").field("temperature", random.randint(0,100))
    #print(_point1)
    #_write_api = _db_client.client.write_api(write_options=WriteOptions(batch_size=1))
    #_write_api.write(bucket="django_cms", record=data)
    #_write_api.write(bucket="django_cms", record=_point1)

    # client = InfluxDBClient(url="http://8.140.157.208:8086", token=token)
    #_db_client = InfluxDBClient(url="http://8.140.157.208:8086", token=token, org="IWM", debug=True)

    """
    Create client that writes data into InfluxDB
    """
    #_write_api = _db_client.write_api(write_options=WriteOptions(batch_size=1))
    #_write_api.write(bucket="django_cms", record=data)

    """
    Call after terminate a script
    """
    #atexit.register(on_exit, _db_client.client, _write_api)

    #input()
    #pass
    #client = ConnnectDatabase()
    #WriteData(client)


