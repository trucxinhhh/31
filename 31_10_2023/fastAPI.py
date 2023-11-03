from fastapi import FastAPI, Form, Request, HTTPException, status, Response, Depends, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pymongo
import io
from fastapi.security import APIKeyHeader
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import base64
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")

trang_thai = " "

# Định nghĩa tài khoản và mật khẩu
username = "truc"
password = "1234"


myclient = pymongo.MongoClient("mongodb+srv://delihoe6:d6c42IAyIGcejoVg@cluster0.axvvvwk.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["mydatabase"]
mycol = mydb["Master"]
mycol1 = mydb["IotGateWay"]
mycol2 = mydb["IotNode"]
cottatcadulieu=mydb["all_data"]




API_KEY = "lBJGSf9VWp9g5ok"
api_key_header = APIKeyHeader(name="X-API-Key")


def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")



class Master(BaseModel):
    id: int
    led1_status: int
    led2_status: int
    temp: float
    humi: float
    timestamp: str


class st(BaseModel):
    status: str

class IotGateWay(BaseModel):
    id: int
    lamp: int
    siren: int
    timestamp: str


class IotNode(BaseModel):
    id: int
    vibration: int
    relay: int
    Light_Sensor: float
    Distance_Sensor: float
    timestamp: str


class AllData(BaseModel):
    id: int
    led1_status: int
    led2_status: int
    temp: float
    humi: float
    lamp: int
    siren: int
    vibration: int
    relay: int
    Light_Sensor: float
    Distance_Sensor: float
    timestamp: str

class SingleData(BaseModel):
    id: int
    data: float
    timestamp: str
app.mount("/static", StaticFiles(directory="D:/HOC/HKI_N4/IOT/Buoi_12_13/31_10_2023/templates"), name="static")
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("login3.html", {"request": request})


@app.get("/login")
async def login(request: Request, username_form: str = Form(...), password_form: str = Form(...)):
    if username_form == username and password_form == password:
        response = RedirectResponse("/welcome")
        return response
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")


@app.get("/welcome", response_class=HTMLResponse)
async def welcome(request: Request):
    return templates.TemplateResponse("new.html", {"request": request})


@app.get("/interface", response_class=HTMLResponse)
async def interface(request: Request):
    return templates.TemplateResponse("Interface.html", {"request": request})


@app.get("/graph", response_class=HTMLResponse)
async def get_graph():
    global trang_thai
    data_sensor = list(cottatcadulieu.find({}, {"_id": 0}).sort("timestamp", pymongo.DESCENDING).limit(10))
    df = pd.DataFrame(data_sensor)

    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    last_data = df.tail(1)
    print(last_data)
    formatted_time = last_data['timestamp'].iloc[0].strftime("%I:%M %p %m/%d/%Y")

    fig, axs = plt.subplots(5, 2, figsize=(15, 12))
    fig.suptitle('BIỂU ĐỒ THỂ HIỆN GIÁ TRỊ')

    for i, column, color, title in zip(range(10), ['temp', 'humi', 'lamp', 'siren', 'vibration', 'relay', 'Light_Sensor', 'Distance_Sensor', 'led2_status', 'led1_status'], ['blue', 'green', 'red', 'orange', 'blue', 'green', 'red', 'orange', 'blue', 'green'], ['Nhiệt độ', 'Độ ẩm', 'Lamp', 'Siren', 'Vibration', 'Relay', 'Light Sensor', 'Distance Sensor', 'LED2', 'LED1']):
        axs[i // 2, i % 2].plot(df['timestamp'], df[column], color=color, label=title)
        axs[i // 2, i % 2].set_title(f'Biểu đồ {title}')
        axs[i // 2, i % 2].legend()
        axs[i // 2, i % 2].set_xlabel('Thời gian')
        axs[i // 2, i % 2].set_ylabel('Giá trị')

    for i in range(2):
        for j in range(2):
            axs[i, j].legend(loc='upper right')

    fig.suptitle('BIỂU ĐỒ THỂ HIỆN GIÁ TRỊ')

    buffer = BytesIO()
    plt.tight_layout()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    plt.close(fig)

    
    html_content = f"""
    <html>
    <head>
        <title>Biểu đồ Matplotlib</title>
        
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f8f8f8;
            }}
            h1 {{
                color: #333;
                text-align: center;
            }}
            h2 {{
                color: #555;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                max-width: 800px;
                margin: 20px auto;
                background-color: #fff;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            }}
            table, th, td {{
                border: 1px solid #ddd;
            }}
            th, td {{
                padding: 12px;
                text-align: center;
            }}
            th {{
                background-color: #f5f5f5;
            }}
            tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
            tr:hover {{
                background-color: #e0e0e0;
            }}
            img {{
                max-width: 100%;
                display: block;
                margin: 20px auto;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            }}
        </style>
    </head>
    <body>
        <h1 id="stt">Trạng thái hiện tại: {trang_thai}</h1>
        <h2>Dữ liệu cuối cùng gửi lên:</h2>
        <table>
            <tr>
                <th>LED 1</th>
                <th>LED 2</th>
                <th>Nhiệt độ</th>
                <th>Độ ẩm</th>
                <th>Lamp</th>
                <th>Siren</th>
                <th>Vibration </th>
                <th>Relay</th>
                <th>Light Sensor </th>
                <th>Distance Sensor</th>
                <th>Thời gian</th>
            </tr>
            <tr>
                <td>{last_data['led1_status'].values[0]}</td>
                <td>{last_data['led2_status'].values[0]}</td>
                <td>{last_data['temp'].values[0]}</td>
                <td>{last_data['humi'].values[0]}</td>
                <td>{last_data['lamp'].values[0]}</td>
                <td>{last_data['siren'].values[0]}</td>
                <td>{last_data['vibration'].values[0]}</td>
                <td>{last_data['relay'].values[0]}</td>
                <td>{last_data['Light_Sensor'].values[0]}</td>
                <td>{last_data['Distance_Sensor'].values[0]}</td>
                <td>{formatted_time}</td>
            </tr>
        </table>
        <img src='data:image/png;base64,{image_base64}'>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/get_master_data")
async def get_master_data():
    latest_data = mycol.find_one(sort=[("timestamp", pymongo.DESCENDING)])
    print(latest_data)
    if latest_data:
        return {
            "id": latest_data["id"],
            "led1_status": latest_data["led1_status"],
            "led2_status": latest_data["led2_status"],
            "temp": latest_data["temp"],
            "humi": latest_data["humi"],
            "timestamp": latest_data["timestamp"]
        }
    return {"message": "Không có dữ liệu Master."}


@app.get("/get_gateway_data")
async def get_gateway_data():
    latest_data = mycol1.find_one(sort=[("timestamp", pymongo.DESCENDING)])
    if latest_data:
        return {
            "id": latest_data["id"],
            "lamp": latest_data["lamp"],
            "siren": latest_data["siren"],
            "timestamp": latest_data["timestamp"]
        }
    return {"message": "Không có dữ liệu Gateway."}


@app.get("/get_node_data")
async def get_node_data():
    latest_data = mycol2.find_one(sort=[("timestamp", pymongo.DESCENDING)])
    if latest_data:
        return {
            "id": latest_data["id"],
            "vibration": latest_data["vibration"],
            "relay": latest_data["relay"],
            "Light_Sensor": latest_data["Light_Sensor"],
            "Distance_Sensor": latest_data["Distance_Sensor"],
            "timestamp": latest_data["timestamp"]
        }
    return {"message": "Không có dữ liệu Node."}


@app.get("/get_all_data")
async def get_all_data():
    latest_data = cottatcadulieu.find_one(sort=[("timestamp", pymongo.DESCENDING)])
    if latest_data:
        return  {
            "id" : latest_data['id'],
            "led1_status": latest_data['led1_status'],
            "led2_status": latest_data['led2_status'],
            "temp": latest_data['temp'],
            "humi": latest_data['humi'],
            "lamp": latest_data['lamp'],
            "siren": latest_data['siren'],
            "vibration": latest_data['vibration'],
            "relay": latest_data['relay'],
            "Light_Sensor": latest_data['Light_Sensor'],
            "Distance_Sensor": latest_data['Distance_Sensor'],
            "timestamp": latest_data['timestamp']
    }
    return {"message": "Không có dữ liệu ."}


@app.post("/update_master_data")
async def update_master_data(item: Master,api_key: str = Depends(get_api_key)):
    master_data = {
        "id": item.id,
        "led1_status": item.led1_status,
        "led2_status": item.led2_status,
        "temp": item.temp,
        "humi": item.humi,
        "timestamp": item.timestamp
    }
    mycol.insert_one(master_data)
    return JSONResponse(content={"message": "Dữ liệu Master đã được cập nhật"})


@app.post("/update_gateway_data")
async def update_gateway_data(item: IotGateWay,api_key: str = Depends(get_api_key)):
    gateway_data = {
        "id": item.id,
        "lamp": item.lamp,
        "siren": item.siren,
        "timestamp": item.timestamp
    }
    mycol1.insert_one(gateway_data)
    return JSONResponse(content={"message": "Dữ liệu Gateway đã được cập nhật"})


@app.post("/update_node_data")
async def update_node_data(item: IotNode,api_key: str = Depends(get_api_key)):
    node_data = {
        "id": item.id,
        "vibration": item.vibration,
        "relay": item.relay,
        "Light_Sensor": item.Light_Sensor,
        "Distance_Sensor": item.Distance_Sensor,
        "timestamp": item.timestamp
    }
    mycol2.insert_one(node_data)
    return JSONResponse(content={"message": "Dữ liệu Node đã được cập nhật"})


@app.post("/update_all_data")
async def update_data_post(item: AllData,api_key: str = Depends(get_api_key)):
    BT = {
        "id" : item.id,
        "led1_status": item.led1_status,
        "led2_status": item.led2_status,
        "temp": item.temp,
        "humi": item.humi,
        "lamp": item.lamp,
        "siren": item.siren,
        "vibration": item.vibration,
        "relay": item.relay,
        "Light_Sensor": item.Light_Sensor,
        "Distance_Sensor": item.Distance_Sensor,
        "timestamp": item.timestamp
    }
    cottatcadulieu.insert_one(BT)
    return { "message": "Dữ liệu đã được cập nhật"}



@app.post("/post_status")
async def post_status(data :st):
    global trang_thai
    trang_thai =data.status
    return {"get status ok": trang_thai}

