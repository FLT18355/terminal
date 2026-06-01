import asyncio
import websockets
import json
import uuid
import sys
import time
import os
import random

#配置文件
#音乐路径
music_path = "/storage/emulated/0/系统文件勿删/data/python/音乐播放器整合一/"
#权限
music_op = [ "StarAwA10001", "FLT18355" ]

#初始化
#暗色
R = "\033[31m" #红
G = "\033[32m" #绿
Y = "\033[33m" #黄
B = "\033[34m" #蓝
M = "\033[35m" #紫
C = "\033[36m" #青
W = "\033[37m" #灰

#亮色
BR = "\033[91m" #红
BG = "\033[92m" #绿
BY = "\033[93m" #黄
BB = "\033[94m" #蓝
BM = "\033[95m" #紫
BC = "\033[96m" #青
BW = "\033[97m" #白

#重置
X = "\033[0m"

ws = None
test = False
music_running = False
music_preparename = None
music_preparelist = None

def is_ws_open(connection):
    """检查 WebSocket 连接是否处于打开状态（兼容新版 websockets）"""
    if connection is None:
        return False
    # 新版 websockets 使用 state 属性
    if hasattr(connection, 'state'):
        return connection.state == websockets.protocol.State.OPEN
    # 旧版兼容
    if hasattr(connection, 'closed'):
        return not connection.closed
    return False

async def ainput():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, sys.stdin.readline)

async def runc(command):
    global ws
    global test
    
    if not is_ws_open(ws):
        return
    send_command={
        "body": {
		    "origin": {
			    "type": "player"
		    },
		    "commandLine": command,
		    "version": 17039360
	    },
	    "header": {
		    "requestId": str(uuid.uuid4()),
		    "messagePurpose": "commandRequest",
		    "version": 1,
		    "messageType": "commandRequest"
	    }
    }
    try:
        await ws.send(json.dumps(send_command))
    except Exception as e:
        if test:
            print(f"{BR}Error {W}>> {BW}发包: {e}{X}")

async def sub(event):
    global ws
    global test
    
    if not is_ws_open(ws):
        return
    send_subscribe={
	    "body": {
		    "eventName": event
	    },
	    "header": {
	    	"requestId": str(uuid.uuid4()),
	    	"messagePurpose": "subscribe",
		    "version": 1,
		    "messageType": "commandRequest"
	    }
    }
    try:
        await ws.send(json.dumps(send_subscribe))
    except Exception as e:
        if test:
            print(f"{BR}Error {W}>> {BW}发包: {e}{X}")

async def music_run(music_name, music_list):
    if not music_name or not music_list:
        print(f"{BR}System {W}>> {BW}音乐列表为空 {X}")
        return
    
    global music_running
    if music_running:
        print(f"{BR}System {W}>> {BW}已有音乐播放 {X}")
        return
    
    print(f"{BB}System {W}>> {BW}正在播放 {BY}{music_name} {X}")
    await runc(f"/me §f正在播放 §e{music_name}")
    music_running = True
    
    start_time = asyncio.get_event_loop().time()
    
    for music_time, music_timbre, music_pitch, music_volume in music_list:
        if not music_running:
            print(f"{BB}System {W}>> {BW}音乐进程已关闭 {X}")
            await runc("/me §f音乐进程已关闭")
            return
        
        wait_time = music_time - asyncio.get_event_loop().time() + start_time
        
        if wait_time > 0:
            await asyncio.sleep(wait_time)
            
        command = f"/execute as @a at @s run playsound {music_timbre} @s ~ ~ ~ {music_pitch} {music_volume}"
        try:
            asyncio.create_task(runc(command))
        except Exception as e:
            if test:
                print(f"{BR}Error {W}>> {BW}播放: {e}{X}")
            print(f"{BB}System {W}>> {BW}未知错误 音乐进程关闭{X}")
            await runc("未知错误 音乐进程关闭")
            music_running = False
            return
        
    print(f"{BB}System {W}>> {BY}{music_name} {BW}已播放完毕{X}")
    await runc(f"/me §e{music_name} §f已播放完毕")
    music_running = False

async def music_load(music_file):
    global music_preparelist
    global music_preparename
    
    try:
        with open(music_file, "r", encoding="utf-8") as f:
            music_config = json.load(f)
        
        music_preparename = music_config["title"]
        music_preparelist = music_config["tracks"]
        
        return True
    except Exception as e:
        if test:
            print(f"{BR} {W}>> {BW}文件: {e}{X}")
        return False

async def music_fastrun(text):
    global music_running
    global music_preparelist
    global music_preparename
    global music_path
    
    if await music_load(music_path + text[11:].strip() + ".json"):
        print(f"{BB}System {W}>> {BW}音乐文件配置成功{X}")
    else:
        print(f"{BR}Error {W}>> {BW}音乐文件配置失败{X}")
        return
    
    if not is_ws_open(ws):
        print(f"{BB}System {W}>> {BW}服务器未连接{X}")
        return
        
    if music_running:
        print(f"{BB}System {W}>> {BW}已有音乐进程播放{X}")
        return
    else:
        await music_run(music_preparename, music_preparelist)

async def loop():
    while True:
        await asyncio.sleep(60)
        if is_ws_open(ws):
            try:
                await ws.send('{"type":"ping"}')
            except Exception as e:
                if test:
                    print(f"{BR}Error {W}>> {BW}保活: {e}{X}")

async def connect(websocket, path=None):
    global ws
    global test
    global music_running
    global music_preparelist
    global music_preparename
    global music_path
    
    if is_ws_open(ws):
        print(f"{BB}System {W}>> {BW}已有连接，拒绝新连接{X}")
        await websocket.close(1000, "已有连接存在")
        return

    ws = websocket
    print(f"{BB}System {W}>> {BW}服务器已连接{X}")
    
    asyncio.create_task(loop())
    
    await runc("/me §bStar §fMusic 已启动")
    
    await sub("PlayerMessage")
    
    try:
        async for message in ws:
            data = json.loads(message)
            purpose = data.get("header", {}).get("messagePurpose")
            if purpose == "event":
                if test:
                    print(f"{BY}Test {W}>> {BW}检测到服务包\n{W}{data}\n\n{X}")
                    
                event_name = data.get("header", {}).get("eventName")
                
                if event_name == "PlayerMessage":
                    message_type=data.get("body", {}).get("type")
                    message_text=data.get("body", {}).get("message")
                    message_sender=data.get("body", {}).get("sender")
                    
                    if message_type == "chat":
                        print(f"{W}<{BW}{message_sender}{W}> {BW}{message_text}{X}")
                        
                        if not message_text.startswith("!"):
                            continue
                            
                        if message_sender != "StarAwA10001" and message_sender not in music_op:
                            await runc(f'/tellraw {message_sender} {{"rawtext":[{{"text":"§cError §7>> §f您没有使用命令的权限！§r"}}]}}')
                            continue
                            
                        if message_text == "!music run":
                            if not is_ws_open(ws):
                                print(f"{BB}System {W}>> {BW}服务器未连接{X}")
                            elif music_running:
                                print(f"{BB}System {W}>> {BW}已有音乐进程播放{X}")
                            else:
                                asyncio.create_task(music_run(music_preparename, music_preparelist))
                            
                        elif message_text.startswith("!music run "):
                            asyncio.create_task(music_fastrun(message_text))
                            
                        elif message_text == "!music random":
                            json_files = [f for f in os.listdir(music_path) if f.endswith(".json")]
                            if json_files:
                                random_file = random.choice(json_files)
                                asyncio.create_task(music_fastrun(f"!music run {random_file[:-5]}"))
                                print(f"{BB}System {W}>> {BW}随机选取文件 {random_file}{X}")
                            else:
                                print(f"{BB}System {W}>> {BW}文件获取失败{X}")
                            
                        elif message_text == "!music stop":
                            if music_running:
                                print(f"{BB}System {W}>> {BW}等待音乐进程取消…{X}")
                                await runc("/me §f等待音乐端§e取消中…")
                                music_running = False
                            else:
                                print(f"{BB}System {W}>> {BW}当前不存在任何音乐进程{X}")
                                await runc("/me §f当前没有§e正在播放的音乐")
                            
                        else:
                            await runc(f'/tellraw {message_sender} {{"rawtext":[{{"text":"§cError §7>> §f命令库中没有该命令§r"}}]}}')
                            
                    elif message_type == "me":
                        print(f"{W}* {BW}{message_sender} {BW}{message_text}{X}")
                    
                    elif message_type == "say":
                        print(f"{BW}{message_text}{X}")
                    
            elif purpose == "commandResponse":
                status_message = data.get("body", {}).get("statusMessage")
                if status_message:
                    pass
                    #print(f"{BM}CR {W}>> {BW}{status_message}{X}")
    except Exception as e:
        if test:
            print(f"{BR}music_path {W}>> {BW}服务: {e}{X}")
    finally:
        ws = None

async def main():
    server = await websockets.serve(connect, "0.0.0.0", 8887)
    print(f"{BB}System {W}>> {BW}服务器已启动{X}")
    global ws
    global test
    global music_running
    global music_preparelist
    global music_preparename
    global music_path
    
    try:
        while True:
            cmd = await ainput()
            cmd = cmd.strip()
            
            if not cmd:
                continue
            
            if cmd == "/stop":
                print(f"{BB}System {W}>> {BW}正在停止服务器...{X}")
                
                if is_ws_open(ws):
                    await runc("/me §bStar §fMusic 正断开连接")
                    try:
                        await runc("/closewebsocket")
                    except:
                        pass
                    ws = None
                    await asyncio.sleep(0.1)
                
                server.close()
                try:
                    await asyncio.wait_for(server.wait_closed(), timeout=5)
                    print(f"{BB}System {W}>> {BW}程序已退出{X}")
                    break
                except asyncio.TimeoutError:
                    print(f"{BB}System {W}>> {BW}关闭超时，强制终止程序{X}")
                    break
            elif cmd == "/status":
                if is_ws_open(ws):
                    print(f"{BB}System {W}>> {BW}状态: 已连接{X}")
                else:
                    print(f"{BB}System {W}>> {BW}状态: 未连接{X}")
                print(f"{BB}System {W}>> {BW}调试模式: {test}{X}")
            elif cmd == "/test True":
                test = True
                print(f"{BB}System {W}>> {BW}调试模式已启用{X}")
            elif cmd == "/test False":
                test = False
                print(f"{BB}System {W}>> {BW}调试模式已禁用{X}")
            elif cmd.startswith("/music load "):
                if await music_load(music_path + cmd[12:].strip() + ".json"):
                    print(f"{BB}System {W}>> {BW}音乐文件配置成功{X}")
                else:
                    print(f"{BR}System {W}>> {BW}音乐文件配置失败{X}")
            elif cmd == "/music run":
                if not is_ws_open(ws):
                    print(f"{BB}System {W}>> {BW}服务器未连接{X}")
                elif music_running:
                    print(f"{BB}System {W}>> {BW}已有音乐进程播放{X}")
                else:
                    asyncio.create_task(music_run(music_preparename, music_preparelist))
            
            elif cmd.startswith("/music run "):
                asyncio.create_task(music_fastrun(cmd))
                
            elif cmd == "/music stop":
                print(f"{BB}System {W}>> {BW}音乐命令判断中…{X}")
                if music_running:
                    print(f"{BB}System {W}>> {BW}等待音乐进程取消…{X}")
                    music_running = False
                else:
                    print(f"{BB}System {W}>> {BW}当前不存在任何音乐进程{X}")
            
            elif cmd[0] == "/":
                await runc(cmd)
            else:
                await runc(f"/me {cmd}")
        
    except KeyboardInterrupt:
        if is_ws_open(ws):
            await runc("/me §bStar §fMusic 正在断开连接")
            try:
                await ws.close(1000)
            except:
                pass
            ws = None
            await asyncio.sleep(0.1)
        
        server.close()
        try:
            await asyncio.wait_for(server.wait_closed(), timeout=5)
        except asyncio.TimeoutError:
            pass
    
    finally:
        ws = None
        sys.exit(0)

asyncio.run(main())