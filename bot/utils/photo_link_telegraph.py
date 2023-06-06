import io

from aiohttp import ClientSession


async def upload_photo(bytes_photo: io.BytesIO):
    session = ClientSession()
    url = 'https://telegra.ph/upload'
    f = io.BytesIO(bytes_photo.read())
    resp = await session.post(url, data={'key': f})
    response = await resp.json()
    await session.close()
    return 'https://telegra.ph' + response[0]['src']
