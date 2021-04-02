from datetime import datetime
import CollectData

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


"""
Efficiency write data from IOT sensor - write changed temperature every minute
"""
import atexit
import platform
from datetime import timedelta

#import psutil as psutil
import rx
from rx import operators as ops

from influxdb_client import InfluxDBClient, WriteApi, WriteOptions

node = "ns=2;s=Demo.Dynamic.Scalar.Double"
ServerName = 'opc.tcp://localhost:48010'
NodeObject = CollectData.SensorData('opc', ServerName, node)


# You can generate a Token from the "Tokens Tab" in the UI
def ConnnectDatabase():
    token = "C3Guf2T-IQ4uDxvFK74Yjm5v5uNtxaP_py4FUr4Q48aDjOxSJh-eCBbSz2HGBo1BvNeJfbw6lUz1dPQHWlLysw=="

    client = InfluxDBClient(url="http://8.140.157.208:8086", token=token)
    return client


def WriteData(client):
    org = "IWM"
    bucket = "django_cms"
    write_api = client.write_api(write_options=SYNCHRONOUS)
    Value = NodeObject.getData()

    data = "double,host=opc used_percent={}".format(Value)
    write_api.write(bucket, org, data)

def WriteDataPoint(client: InfluxDBClient):
    org = "IWM"
    bucket = "django_cms"
    Value = NodeObject.getData()
    point = Point("mem").tag("host", "host1").field("used_percent", Value).time(datetime.utcnow(), WritePrecision.NS)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket, org, point)



def Query(client: InfluxDBClient):
    org = "IWM"
    bucket = "django_cms"
    query = f'from(bucket: \\"{bucket}\\") |> range(start: -1h)'
    tables = client.query_api().query(query, org=org)
    return tables


def line_protocol(temperature):
    """Create a InfluxDB line protocol with structure:

        iot_sensor,hostname=mine_sensor_12,type=temperature value=68

    :param temperature: the sensor temperature
    :return: Line protocol to write into InfluxDB
    """

    import socket
    return 'iot_sensor,hostname=opc,type=temperature value={}'.format(NodeObject.getData())

def on_exit(db_client: InfluxDBClient, write_api: WriteApi):
    """Close clients after terminate a script.

    :param db_client: InfluxDB client
    :param write_api: WriteApi
    :return: nothing
    """
    write_api.close()
    db_client.close()


"""
Read temperature every minute; distinct_until_changed - produce only if temperature change
"""
data = rx\
    .interval(period=timedelta(seconds=2))\
    .pipe(ops.map(lambda t: NodeObject.getData()),
          ops.distinct_until_changed(),
          ops.map(lambda temperature: line_protocol(temperature)))

token = "C3Guf2T-IQ4uDxvFK74Yjm5v5uNtxaP_py4FUr4Q48aDjOxSJh-eCBbSz2HGBo1BvNeJfbw6lUz1dPQHWlLysw=="

#client = InfluxDBClient(url="http://8.140.157.208:8086", token=token)
_db_client = InfluxDBClient(url="http://8.140.157.208:8086", token=token, org="IWM", debug=True)

"""
Create client that writes data into InfluxDB
"""
_write_api = _db_client.write_api(write_options=WriteOptions(batch_size=1))
_write_api.write(bucket="django_cms", record=data)


"""
Call after terminate a script
"""
atexit.register(on_exit, _db_client, _write_api)

input()

#if __name__ == "__main__":
    #pass
    #client = ConnnectDatabase()
    #WriteData(client)


