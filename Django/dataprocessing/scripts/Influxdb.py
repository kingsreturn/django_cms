from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import InfluxDBClient, WriteApi, WriteOptions

class Influxdb:
    def __init__(self):
        self.url= "http://8.140.157.208:8086"
        self.token="vqB03SdNF2KDD5MEPSDnS3Tw2cy4BJUppr7BzmbAg_e8Kei8aEwIOuaaE2_of99uIWiVkCUm5aUnI_sefVSRIw=="
        self.org="IWM"

    # Connect to the database
    def ConnnectDatabase(self):
        try:
            self.client = InfluxDBClient(url=self.url, token=self.token,org=self.org)
            return True
        except Exception:
            print(Exception.args)
            return False

    # write Data point to Database
    def WriteDatapoint(self,measurement,protocol,Name,Value):
        org = "IWM"
        bucket='django_cms'
        _point1 = Point(measurement).tag("protocol", protocol).field(Name, Value).time(datetime.utcnow(), WritePrecision.MS)
        _write_api = self.client.write_api(write_options=SYNCHRONOUS)
        _write_api.write(bucket=bucket, org=org, record=_point1)
        print('Write Data success!')

    # write Data set to Database
    def WriteDataset(self,measurement,protocol,name,dataset):
        org = "IWM"
        bucket='django-cms'
        sequence = []
        for value in dataset:
            data = "{},protocol={} {}={}".format(measurement,protocol,name,value)
            sequence.append(data)
        #print(sequence)

        _write_api = self.client.write_api(write_options=WriteOptions(batch_size=1))
        #_write_api = self.client.write_api(write_options=SYNCHRONOUS)
        _write_api.write(bucket, org, sequence)

        #print('Write Data completed!')

    # Query data from Database
    def Query(self,measurement,protocol,name):
        org = "IWM"
        bucket = "django-cms"
        query = 'from(bucket: "django-cms") |> range(start: -10m)' \
                '|> filter(fn:(r) => r._measurement == \"{}\")' \
                '|> filter(fn: (r) => r.protocol == \"{}\")' \
                '|> filter(fn:(r) => r._field == \"{}\")'.format(measurement,protocol,name)
        result = self.client.query_api().query(query)
        dataset = []
        for table in result:
            for row in table.records:
                dataset.append(row.get_value())
                #print(row.get_field())
                print(row.get_value())
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
    #_db_client.WriteDatapoint('tem','opc','value','30')
    #_db_client.WriteDataset('tem', 'opc', 'value', [1,2,3,4,6,7,8,9])
    dataset = _db_client.Query('tem','opc','value')
    #print(dataset)
