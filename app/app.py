from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import serial

# import serial.tools.list_ports

# ports = serial.tools.list_ports.comports()
# for port in ports:
#     print(port)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SliderValue(BaseModel):
    value: int

try:
    ser = serial.Serial(port="COM3", baudrate=9600, timeout=1) 
except Exception as e:
    print(f"Error opening serial port: {e}")
    ser = None

@app.post("/send-slider")
async def send_slider_value(slider: SliderValue):

    if not (0 <= slider.value <= 255):
        raise HTTPException(status_code=400, detail="Slider value must be between 0 and 255")

    if ser is None or not ser.is_open:
        raise HTTPException(status_code=500, detail="UART connection not established")

    try:
        ser.write(bytes([slider.value])) 
        return {"status": "success", "message": f"Sent {slider.value} to STM32"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send data via UART: {e}")

@app.get("/")

def root():
    return {"message": "FastAPI server for STM32 UART communication is running."}

