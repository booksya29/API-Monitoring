import aiohttp
from schemes import ApiResponse_scheme
async def check_api(data:dict, bot):
    user_id = data["creator_id"]
    method = data["send_method"]
    body = data['body']
    url = data["url"]
    async with aiohttp.ClientSession() as session:
        async with session.request(method=method, url=url, json=body, ssl=False) as response:
            status_code = response.status
            answer = await response.text()
    if status_code < 200 or status_code >= 300:
        await bot.send_message(chat_id=user_id, text=f"API {url} повернуло код {status_code}.")
    api_response = ApiResponse_scheme(request_id=data["id"], status_code=status_code, answer=answer)
    return api_response

async def build_check_list(data:list[dict], bot):
    return [check_api(api_data, bot) for api_data in data]
