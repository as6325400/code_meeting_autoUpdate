import requests
import time
import os
import dotenv
import pygsheets

dotenv.load_dotenv()

contestNum_ID = os.getenv("CONTESTNUM_ID")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded"
}

def login():
  login_url = "https://vjudge.net/user/login"

  payload = {
      "userName": os.getenv("USERNAME"),  
      "password": os.getenv("PASSWORD")  
  }

  session = requests.Session()

  login_response = session.post(login_url, data=payload, headers=headers)
  if login_response.status_code == 200:
      print("login success")
  else:
      print(f"login fail: {login_response.status_code}")
      print("response：", login_response.text)
      exit()


def get_data():
  session = requests.Session()
  data_url = "https://vjudge.net/status/data"

  params = {
      "draw": 2,
      "start": 0,  
      "length": 20,
      "un": "",
      "num": "-",
      "res": 1,
      "language": "",
      "inContest": "true",
      "contestId": os.getenv("CONTEST_ID"),
      "_": int(time.time() * 1000)
  }

  status_data = []

  count = 0;
  while True:
      count += 1
      response = session.get(data_url, headers=headers, params=params)
      
      if response.status_code != 200:
          print(f"GET error: {response.status_code}")
          print("response：", response.text)
          break

      try:
          data = response.json()
          records = data.get("data", []) 
          status_data.extend(records)
          if len(records) < 20:
              break
          params["start"] += 20

      except Exception as e:
          print("error:", e)
          print("error response：", response.text)
          break

  print(f"共發送了 {count} 次 GET 請求")
  print(f"共取得 {len(status_data)} 筆資料")
  # print(status_data)
  d = dict()
  for i in status_data:
    if i["userName"] not in d:
      d[i["userName"]] = {contestNum_ID[0]: -1, contestNum_ID[1]: -1, contestNum_ID[2]: -1, contestNum_ID[3]: -1}
  for i in status_data:
    if i["userName"] in d:
      try:
        if i["contestNum"] in d[i["userName"]]:
          if d[i["userName"]][i["contestNum"]] == -1:
            d[i["userName"]][i["contestNum"]] = i["runtime"]
          else:
            d[i["userName"]][i["contestNum"]] = min(d[i["userName"]][i["contestNum"]], i["runtime"])
      except:
        pass
          
  return d

# login()
# status_data = get_data()
# print(status_data)

gc = pygsheets.authorize(service_file='token.json')
spreadsheet = gc.open_by_url(os.getenv("SHEET_URL"))
worksheet = spreadsheet.worksheet_by_title('工作表1')
namerow = worksheet.get_row(2, include_tailing_empty=False)[1:]
status_data = get_data()
inform = []
for name in namerow:
  if name not in status_data:
    status_data[name] = {contestNum_ID[0]: -1, contestNum_ID[1]: -1, contestNum_ID[2]: -1, contestNum_ID[3]: -1}
for id in contestNum_ID:
  temp = []
  for name in namerow:
    temp.append(status_data[name][id])
  inform.append(temp)
worksheet.update_values('B7:U10', inform)
print('update finis ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))