#!/usr/bin/env python3
"""
Minecraft 基岩版 WebSocket 命令服务器
用法: python3 bedrock_cmd_server.py &
在 Minecraft 基岩版中执行: /connect localhost:8765
然后在终端输入命令（如 fastfetch），输出会显示在游戏聊天栏
"""

import asyncio
import websockets
import subprocess
import json
import uuid
import sys
import signal

HOST = "localhost"
PORT = 8765

connected_clients = set()


def create_request_id():
    """生成唯一的请求 ID"""
    return str(uuid.uuid4())


def create_subscribe_packet(event_name: str, request_id: str = None):
    """创建订阅事件的请求包"""
    if request_id is None:
        request_id = create_request_id()
    return {
        "body": {"eventName": event_name},
        "header": {
            "requestId": request_id,
            "messagePurpose": "subscribe",
            "version": 1,
            "messageType": "commandRequest"
        }
    }


def create_command_packet(command: str, request_id: str = None):
    """创建命令执行的请求包"""
    if request_id is None:
        request_id = create_request_id()
    return {
        "body": {
            "origin": {"type": "player"},
            "commandLine": command,
            "version": 1
        },
        "header": {
            "requestId": request_id,
            "messagePurpose": "commandRequest",
            "version": 1,
            "messageType": "commandRequest"
        }
    }


def create_unsubscribe_packet(event_name: str, request_id: str = None):
    """创建取消订阅的请求包"""
    if request_id is None:
        request_id = create_request_id()
    return {
        "body": {"eventName": event_name},
        "header": {
            "requestId": request_id,
            "messagePurpose": "unsubscribe",
            "version": 1,
            "messageType": "commandRequest"
        }
    }


async def execute_shell_command(command: str) -> str:
    """执行 Shell 命令并返回输出"""
    if not command or command.strip() == "":
        return ""

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            executable="/bin/bash"
        )

        output = ""
        if result.stdout:
            output += result.stdout
        if result.stderr:
            output += f"\n[STDERR]\n{result.stderr}"
        if not output:
            output = f"命令执行完成 (退出码: {result.returncode})"

        # Minecraft 聊天栏有长度限制，截断过长输出
        if len(output) > 50000:
            output = output[:50000] + "\n... (输出被截断)"

        return output.strip()
    except subprocess.TimeoutError:
        return "错误: 命令执行超时 (30秒)"
    except Exception as e:
        return f"错误: {e}"


async def handle_bedrock_client(websocket):
    """处理基岩版客户端连接"""
    connected_clients.add(websocket)
    print(f"✅ 基岩版客户端已连接 (当前连接数: {len(connected_clients)})")

    try:
        # 基岩版连接后需要先订阅 PlayerMessage 事件才能收到聊天消息
        subscribe_packet = create_subscribe_packet("PlayerMessage")
        await websocket.send(json.dumps(subscribe_packet))
        print("📡 已订阅 PlayerMessage 事件")

        async for message in websocket:
            try:
                data = json.loads(message)
                purpose = data.get("header", {}).get("messagePurpose")

                # 处理事件包（来自客户端的消息）
                if purpose == "event":
                    event_name = data.get("body", {}).get("eventName")
                    if event_name == "PlayerMessage":
                        props = data.get("body", {}).get("properties", {})
                        msg_type = props.get("MessageType")
                        if msg_type == "chat":
                            sender = props.get("Sender", "Unknown")
                            msg_text = props.get("Message", "")
                            print(f"💬 [{sender}] {msg_text}")

                            # 检查是否是命令（以 ! 开头）
                            if msg_text.startswith("!"):
                                cmd = msg_text[1:].strip()
                                print(f"🚀 执行命令: {cmd}")
                                result = await execute_shell_command(cmd)

                                # 通过命令将结果显示在聊天栏
                                if result:
                                    # 分行发送（避免消息过长被截断）
                                    for line in result.split('\n')[:10]:
                                        if line.strip():
                                            send_cmd = f'say §a[系统] §f{line}'
                                            await websocket.send(json.dumps(create_command_packet(send_cmd)))
                                            await asyncio.sleep(0.1)

                # 处理命令响应包
                elif purpose == "commandResponse":
                    status = data.get("body", {}).get("statusCode", -1)
                    status_msg = data.get("body", {}).get("statusMessage", "")
                    if status == 0 and status_msg:
                        pass  # 命令执行成功，静默处理

            except json.JSONDecodeError:
                print(f"⚠️ 收到非 JSON 消息: {message[:100]}")
            except Exception as e:
                print(f"⚠️ 处理消息时出错: {e}")

    except websockets.exceptions.ConnectionClosed:
        print("❌ 基岩版客户端断开连接")
    finally:
        connected_clients.discard(websocket)


async def terminal_input():
    """在终端读取用户输入，发送命令到 Minecraft"""
    loop = asyncio.get_event_loop()

    print("\n终端模式已启动，输入命令将发送到 Minecraft")
    print("特殊命令: /exit - 退出服务器, /clients - 查看连接数\n")

    while True:
        try:
            user_input = await loop.run_in_executor(None, lambda: input("> "))

            if not user_input or user_input.strip() == "":
                continue

            if user_input == "/exit":
                print("正在关闭服务器...")
                break
            elif user_input == "/clients":
                print(f"当前连接客户端数: {len(connected_clients)}")
                continue

            print(f"🚀 执行: {user_input}")
            result = await execute_shell_command(user_input)

            # 发送结果到所有连接的 Minecraft 客户端
            if connected_clients and result:
                for client in connected_clients:
                    try:
                        for line in result.split('\n')[:10]:
                            if line.strip():
                                send_cmd = f'say §a[终端] §f{line}'
                                await client.send(json.dumps(create_command_packet(send_cmd)))
                                await asyncio.sleep(0.05)
                    except Exception as e:
                        print(f"发送失败: {e}")
            elif not connected_clients:
                print("⚠️ 没有客户端连接，结果仅显示在终端")
                print(result)

        except EOFError:
            print("\n输入结束")
            break
        except KeyboardInterrupt:
            print("\n中断信号")
            break


async def main():
    # 启动 WebSocket 服务器
    server = await websockets.serve(
        handle_bedrock_client,
        HOST,
        PORT,
        max_size=10 ** 6
    )

    print(f"""
╔══════════════════════════════════════════════════════════════════╗
║     Minecraft 基岩版 WebSocket 命令服务器                        ║
╠══════════════════════════════════════════════════════════════════╣
║  服务器地址: ws://{HOST}:{PORT}                                    ║
║                                                                  ║
║  在 Minecraft 基岩版中执行:                                       ║
║    /connect {HOST}:{PORT}                                        ║
║                                                                  ║
║  在游戏中发送 !命令 来执行 (例如: !fastfetch)                      ║
║  或在终端直接输入命令，输出会发送到游戏聊天栏                       ║
║                                                                  ║
║  前提: 需要在游戏设置中开启「启用作弊」                           ║
╚══════════════════════════════════════════════════════════════════╝
    """)

    await asyncio.gather(
        server.wait_closed(),
        terminal_input()
    )


def signal_handler(signum, frame):
    print("\n正在关闭服务器...")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n服务器已停止")
        sys.exit(0)