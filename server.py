import asyncio
import json
from aiohttp import web, WSMsgType
 
clients = set()
 
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
 
    clients.add(ws)
    print("Cliente conectado")
 
    async for msg in ws:
        if msg.type == WSMsgType.ERROR:
            print("Erro no WebSocket:", ws.exception())
 
    clients.remove(ws)
    print("Cliente desconectado")
    return ws
 
async def publish_block(request):
    try:
        block = await request.json()
        print(f"Publicando bloco {block['index']} para {len(clients)} clientes")
        for ws in clients:
            await ws.send_str(json.dumps(block))
        return web.Response(text="Bloco publicado com sucesso")
    except Exception as e:
        return web.Response(text=f"Erro: {e}", status=500)
 
app = web.Application()
app.router.add_post('/publish', publish_block)
app.router.add_get('/ws', websocket_handler)
 
if __name__ == "__main__":
    web.run_app(app, port=8080)
 