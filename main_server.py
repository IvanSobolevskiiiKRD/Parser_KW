from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import base64
import requests
import Text as Text
import request as rq
import json
from Token import TOKEN

app = FastAPI()

class NewOrder_Data(BaseModel):
    url_order: str
    description: str
    name_oder: str
    price_customer: str

class Get_Data_Order(BaseModel):
    url_order: str
    description: str
    description_ai:str
    name_oder: str
    price_customer: str
    price_ai: str
    lead_time_ai: str

@app.post("/new_order")
async def parse_images(request: NewOrder_Data):
    url_order = request.url_order
    description = request.description
    name_oder = request.name_oder
    price = request.price_customer

    description = base64.b64decode(description)
    description = description.decode('utf-8')

    url = 'https://lokatekonet.beget.app/webhook/ff8aa89e-dd2d-4ec9-8e1b-ce1d4c39137f'
    data_to_send = {'url_order': url_order, 'description': description, 'name_oder': name_oder, 'price': price}
    response = requests.post(url, json=data_to_send)

    otvet = response.json()
    description = otvet["description"]
    description_ai = otvet["description_ai"]
    name_oder = otvet["name_oder"]
    price_customer = otvet["price_customer"]
    price_ai = otvet["price_ai"]
    lead_time_ai = otvet["lead_time_ai"]
    url_order = otvet["url_order"]

    description_ai = base64.b64decode(description_ai)
    description_ai = description_ai.decode('utf-8')

    description = base64.b64decode(description)
    description = description.decode('utf-8')

    await rq.create_order(name_oder,url_order, description, description_ai, price_customer, price_ai, lead_time_ai)
    data_order = await rq.get_data_one_order_by_url(url_order)
    data_order = data_order.__dict__
    reply_markup = {"inline_keyboard": []}
    
    workers = await rq.get_data_all_user()

    for worker in workers:
        button = [{"text": f"{worker.name} - {worker.otklikow}", "url": f"http://t.me/qwooorkbot?start=setworker_{worker.id}_{data_order["id"]}"}]
        reply_markup['inline_keyboard'].append(button)

    chat_id = '816427281'
    text = Text.new_order.format(name_oder, description_ai, price_customer, price_ai, lead_time_ai)
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML', 'reply_markup': json.dumps(reply_markup)}
    response = requests.post(url, params=params)

    return True

    

if __name__ == "__main__":
    uvicorn.run("main_server:app", host="127.0.0.1", port=8000, reload=True)