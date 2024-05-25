from fastapi import Request


async def get_ip(request: Request):
    ip = request.client.host

    return ip