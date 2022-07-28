from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS,ASYNCHRONOUS
from influxdb_client import InfluxDBClient, WriteApi, WriteOptions
import time

class Influxdb:
    def __init__(self):
        self.url = "http://8.140.157.208:8086"
        self.token = "vqB03SdNF2KDD5MEPSDnS3Tw2cy4BJUppr7BzmbAg_e8Kei8aEwIOuaaE2_of99uIWiVkCUm5aUnI_sefVSRIw=="
        self.org = "IWM"
        self.bucket = 'django-cms'

    # Connect to the database
    def ConnnectDatabase(self):
        try:
            self.client = InfluxDBClient(url=self.url, token=self.token,org=self.org)
            return True
        except Exception:
            print(Exception.args)
            return False

    def WriteDatapoint(self,measurement,protocol, Name, Value):
        org = "IWM"
        bucket='django_cms'
        _point1 = Point(measurement).tag("protocol", protocol).field(Name, Value).time(datetime.utcnow(), WritePrecision.MS)
        _write_api = self.client.write_api(write_options=SYNCHRONOUS)
        _write_api.write(bucket=bucket, org=org, record=_point1)
        print('Write Data success!')

    def WriteDataset(self,measurement,protocol,name,dataset):
        #org = "IWM"
        #bucket='django-cms'
        sequence = []
        for value in dataset:
            data = "{},protocol={} {}={}".format(measurement,protocol,name,value)
            sequence.append(data)
        #print(sequence)

        _write_api = self.client.write_api(write_options=WriteOptions(batch_size=1))
        #_write_api = self.client.write_api(write_options=ASYNCHRONOUS)
        _write_api.write(self.bucket, self.org, sequence)

        #print('Write Data completed!')

    def Query(self,measurement,protocol,name,start,end):
        query = 'from(bucket: "django-cms") |> range(start: {}m,stop: {}m)' \
                '|> filter(fn:(r) => r._measurement == \"{}\")' \
                '|> filter(fn: (r) => r.protocol == \"{}\")' \
                '|> filter(fn:(r) => r._field == \"{}\")'.format(start,end,measurement,protocol,name)
        result = self.client.query_api().query(query)
        #print(result)
        dataset = []
        for table in result:
            for row in table.records:
                dataset.append(row.get_value())
        return dataset


    def line_protocol(self,Protocol,VariableName,Value):
        """Create a InfluxDB line protocol with structure:

        iot_sensor,hostname=mine_sensor_12,type=temperature value=68
        :param temperature: the sensor temperature
        :return: Line protocol to write into InfluxDB
        """

        import socket
        return 'iot_sensor,host={},Name={} value={} value'.format(Protocol,VariableName,Value)

if __name__ == "__main__":
    _db_client=Influxdb()
    result = _db_client.ConnnectDatabase()
    print(result)
    #_db_client.WriteDatapoint('tem','opc','value',30)
    #_db_client.WriteDataset('tem', 'opc', 'value3', [1,2,3,4,6,7,8,9])
    #time.sleep(5)
    dataset = _db_client.Query('sensor','mqtt','numValue')
    print(dataset)

    url = "http://8.140.157.208:8086"
    token = "vqB03SdNF2KDD5MEPSDnS3Tw2cy4BJUppr7BzmbAg_e8Kei8aEwIOuaaE2_of99uIWiVkCUm5aUnI_sefVSRIw=="
    org = "IWM"
    bucket = 'django-cms'

'''
    client = InfluxDBClient(url=url, token=token, org=org)
    query = 'from(bucket: "django-cms") |> range(start: -5m)' \
            '|> filter(fn:(r) => r._measurement == \"{}\")' \
            '|> filter(fn: (r) => r.protocol == \"{}\")' \
            '|> filter(fn:(r) => r._field == \"{}\")'.format('sensor','mqtt','numValue')
    result = client.query_api().query(query)
    print(result)
    dataset = []
    for table in result:
        for row in table.records:
            dataset.append(row.get_value())
    print(dataset)
'''
