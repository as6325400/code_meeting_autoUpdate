import requests
import time
import os
import dotenv

dotenv.load_dotenv()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded"
}

def login():
  login_url = "https://vjudge.net/user/login"

  payload = {
      "username": os.getenv("USERNAME"),  
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
  return status_data

login()
status_data = get_data()
print(status_data)