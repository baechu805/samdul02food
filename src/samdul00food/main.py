import os
from typing import Union
from fastapi import FastAPI
import time
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import pytz
from datetime import datetime

app = FastAPI()

origins = [
    "http://127.0.0.1:8899", # 로컬 개발 환경에서 클라이언트 URL
    "http://localhost", # CORS 설정을 통해 **로컬 클라이언트(웹 페이지)**에서 FastAPI 서버에 요청할 수 있도록 허용
    "http://localhost:8899",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 허용할 출처 (클라이언트 URL)
    allow_credentials=True,
    allow_methods=["*"],  # 허용할 HTTP 메서드 설정 (모든 메서드를 허용)
    allow_headers=["*"],  # 허용할 HTTP 헤더 설정 (모든 헤더를 허용)
)

def get_path():
    file_path = __file__ # 현재 파일경로
    dirpath = os.path.dirname(file_path) # 현재 파일 디렉토리 경로 반환
    print(dirpath)
    return dirpath

@app.get("/")
def read_root():
    return {"Hello": "n72"}

@app.get("/food")
def food(name: str):
    # 현재 시간을 한국 표준시(KST)로 변환
    tz_kst = pytz.timezone('Asia/Seoul')
    # 현재 시간을 구함
    t = datetime.now(tz_kst).strftime('%Y-%m-%d %H:%M:%S')  # 한국 시간을 가져옴
    # 음식 이름과 시간을 데이터프레임으로 저장
    df = pd.DataFrame([[t, name]], columns=['time', 'name'])

    # 파일을 저장할 디렉토리 경로 생성
    dir_path = get_path()
    data_dir = os.path.join(dir_path, 'data')
    
    # 디렉토리가 없으면 생성
    os.makedirs(data_dir, exist_ok=True)

    # 파일 경로 설정
    file_path = os.path.join(data_dir, 'food72.csv')

    # 데이터프레임을 CSV 파일로 저장 (append 모드로, 헤더는 처음에만 추가)
    df.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)

    response = {"food": name, "time": t}
    print(f"응답 데이터: {response}")  # 로그에 응답 출력
    print("================================================================")

    return response

