# -*- coding: utf-8 -*-
from fastapi import FastAPI, APIRouter
from fastapi import Depends
from dependency import http_response, has_access
from models import ResponseModel, RequestModel, get_all_data, insert_data
import uvicorn
import pendulum
import os, logging
logging.basicConfig(filename='execution.log', format="%(asctime)s;%(levelname)s;%(message)s", level=logging.INFO)  
router = APIRouter(prefix='/iot/gateway/v1', tags=['APIs'])

@router.get('/sensor/data', dependencies=[Depends(has_access)])
async def get_response_data(limit: int=10, offset: int=0):
    results = get_all_data(limit, offset)
    return {'results': results}

@router.post("/sensor/store", response_model=ResponseModel, dependencies=[Depends(has_access)])
async def store_sensor_data(request_obj: RequestModel):
	try:
		request_at = pendulum.now(tz='UTC')
		payload = {'created_at': request_at}
		payload.update(request_obj.dict())
		result = insert_data(payload)
		return http_response(message="Request received", data=result)
	except Exception as ex:
		logging.info(ex)
		return http_response(message="Request failed", code=500, error=str(ex))

app = FastAPI(title='Sensor Data API', docs_url=None, redoc_url=None)
app.include_router(router)

if __name__ =='__main__':
	uvicorn.run(app, host='0.0.0.0', port=8000)
