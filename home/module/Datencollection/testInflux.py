from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "django_cms"

client = InfluxDBClient(url="http://8.140.157.208:8086", token="C3Guf2T-IQ4uDxvFK74Yjm5v5uNtxaP_py4FUr4Q48aDjOxSJh-eCBbSz2HGBo1BvNeJfbw6lUz1dPQHWlLysw==", org="IWM")

write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

p = Point("my_measurement").tag("location", "Prague").field("temperature", 28)

write_api.write(bucket=bucket, record=p)

## using Table structure
tables = query_api.query('from(bucket:"django_cms") |> range(start: -30m)')
print(tables)
for table in tables:
    print(table)
    for row in table.records:
        pass
        print (row.values)


## using csv library
csv_result = query_api.query_csv('from(bucket:"django_cms") |> range(start: -10m)')
val_count = 0
for row in csv_result:
    for cell in row:
        val_count += 1
