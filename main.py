import requests, csv, json, time

client_id = ''
client_secret = ''
base_url = 'https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc?coords={longitude},{latitude}&output=json'

headers = {
    'X-NCP-APIGW-API-KEY-ID': client_id, 
    'X-NCP-APIGW-API-KEY': client_secret
}

f = open('dummy.csv', 'r', encoding='utf-8')
csv_reader = csv.reader(f)
lines = []
for line in csv_reader: 
    if line[1] == '경도': 
        lines.append(line)
        continue
    if line[1] == '':
        continue

    longitude, latitude = line[1], line[2]
    print('longidute: {}, lantitude: {}'.format(longitude, latitude))

    count = 5
    response = None
    while(count > 0):
        try:
            response = requests.get(base_url.format(longitude=longitude, latitude=latitude), headers=headers)
            break
        except:
            print('connection error 발생')
            count -= 1
            time.sleep(3)
    if count == 0:
        break # 걍 저장

    if response.status_code != 200:
        raise Exception('스테이터스 코드 이상: ' + response.status_code)
    
    print('response status code: ' + str(response.status_code))
    
    response_json = json.loads(response.text)

    if response_json['status']['code'] != 0:
        raise Exception('응답 데이터 이상: \n'+ response_json)
    
    area1 = response_json['results'][0]['region']['area1']['name']
    area2 = response_json['results'][0]['region']['area2']['name']
    area3 = response_json['results'][0]['region']['area3']['name']
    line[3]= area1
    line[4]= area2
    line[5]= area1
    print('area1: {}, area2: {}, area3: {}'.format(area1, area2, area3))
    print('')

    lines.append(line)
f.close()

print('data save')
f = open('dummy_export.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(f)
writer.writerows(lines)

f.close