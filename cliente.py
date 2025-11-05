import sys
import asyncio
import json
import time
import aiohttp
import hashlib
import requests

blockchain_local = []

def criar_bloco(index, previous_hash, data):
    timestamp = int(time.time() * 1000)
    raw = f"{index}{previous_hash}{timestamp}{data}"
    block_hash = hashlib.sha256(raw.encode()).hexdigest()
    return {
        "index": index,
        "previous_hash": previous_hash,
        "timestamp": timestamp,
        "data": data,
        "hash": block_hash
    }

def validar_bloco(novo, anterior):
    if novo["previous_hash"] != anterior["hash"]:
        return False
    recalculado = hashlib.sha256(f'{novo["index"]}{novo["previous_hash"]}{novo["timestamp"]}{novo["data"]}'.encode()).hexdigest()
    return recalculado == novo["hash"]

# Gera o mesmo bloco gênese fixo para todos os nós
def gerar_genesis():
    raw = "00Bloco gênese"
    return {
        "index": 0,
        "previous_hash": "0",
        "timestamp": 0,
        "data": "Bloco gênese",
        "hash": hashlib.sha256(raw.encode()).hexdigest()
    }

GENESIS_BLOCK = gerar_genesis()

async def listen_and_send(node_name, server_url):
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(f"{server_url}/ws") as ws:
            print(f"[{node_name}] Conectado ao servidor!")

            # Inicia blockchain com bloco gênese fixo
            if not blockchain_local:
                blockchain_local.append(GENESIS_BLOCK)
                print(f"[{node_name}] Bloco gênese criado.")

            # Recebe blocos da rede
            async def receive_blocks():
                async for msg in ws:
                    bloco = json.loads(msg.data)
                    # Ignora blocos duplicados
                    if any(b["hash"] == bloco["hash"] for b in blockchain_local):
                        continue
                    # Valida o bloco recebido
                    if validar_bloco(bloco, blockchain_local[-1]):
                        blockchain_local.append(bloco)
                        latency = (time.time() * 1000) - bloco["timestamp"]
                        print(f"\n[{node_name}] Bloco {bloco['index']} adicionado! Latência: {latency:.2f}ms\nDados: {bloco['data']}")
                        print(f"[{node_name}] Digite dados do bloco: ", end="", flush=True)
                    else:
                        print(f"[{node_name}] Bloco inválido ignorado.")

            # Envia blocos criados pelo usuário (em thread separada)
            async def send_blocks():
                while True:
                    message = await asyncio.to_thread(input, f"[{node_name}] Digite dados do bloco: ")
                    novo_bloco = criar_bloco(len(blockchain_local), blockchain_local[-1]["hash"], message)
                    try:
                        requests.post(f"{server_url}/publish", json=novo_bloco)
                        print(f"[{node_name}] Bloco enviado para rede!")
                    except Exception as e:
                        print(f"Erro ao enviar bloco: {e}")

            await asyncio.gather(receive_blocks(), send_blocks())

if __name__ == "__main__":
    node_name = sys.argv[1]
    server_url = sys.argv[2]
    asyncio.run(listen_and_send(node_name, server_url))
