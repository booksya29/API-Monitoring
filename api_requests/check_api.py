import aiohttp
from schemes import ApiResponse_scheme
async def check_api(data:dict):
    method = data["send_method"]
    body = data['body']
    url = data["url"]
    async with aiohttp.ClientSession() as session:
        async with session.request(method=method, url=url, json=body, ssl=False) as response:
            status_code = response.status
            answer = await response.text()
    
    api_response = ApiResponse_scheme(request_id=data["id"], status_code=status_code, answer=answer)
    api_response()
    return api_response

async def build_check_list(data:list[dict]):
    return [check_api(api_data) for api_data in data]
