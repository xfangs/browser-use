import os
import asyncio
import json
import sys
import threading
import logging
import contextlib
import websockets
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from dotenv import load_dotenv
from browser_use import Agent, BrowserSession
from browser_use.llm import ChatOllama
import uvicorn

# 设置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

# 创建FastAPI应用
app = FastAPI(title="Browser-Use Multi-Agent HTTP API", version="1.0.0")

# WebSocket客户端集合（全局WebSocket）
websocket_clients = set()
websocket_loop = None  # 全局事件循环引用

# 请求模型
class AgentRequest(BaseModel):
    cdp_url: str = "http://127.0.0.1:9222"
    model: str = "qwen2.5:7b"
    host: str = "http://127.0.0.1:11434"
    task: str
    max_steps: int = 20
    headless: bool = False
    verbose: bool = True

# 响应模型
class AgentResponse(BaseModel):
    success: bool
    message: str
    result: Any = None
    error: str = None

# 安全的调试输出
def debug(msg):
    sys.__stdout__.write(f"{msg}\n")
    sys.__stdout__.flush()
    logger.debug(msg)

# WebSocket客户端处理器（全局WebSocket，支持订阅agent_id）
async def websocket_handler(websocket):
    subscribed_agent_id = None
    websocket_clients.add(websocket)
    debug(f"[WS] 客户端已连接，当前连接数: {len(websocket_clients)}")
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                if data.get("type") == "subscribe":
                    subscribed_agent_id = data.get("agent_id")
                    debug(f"[WS] 客户端订阅 Agent: {subscribed_agent_id}")
            except json.JSONDecodeError:
                debug("[WS] 无效的订阅消息")
    except Exception as e:
        debug(f"[WS] 接收消息异常: {e}")
    finally:
        websocket_clients.remove(websocket)
        debug(f"[WS] 客户端断开连接，剩余连接数: {len(websocket_clients)}")

# WebSocket服务主循环
async def websocket_server():
    global websocket_loop
    websocket_loop = asyncio.get_running_loop()
    debug("[WS] 启动 WebSocket 服务：ws://0.0.0.0:7789")
    async with websockets.serve(websocket_handler, "0.0.0.0", 7789, ping_interval=None):
        await asyncio.Future()

def start_websocket_server():
    asyncio.run(websocket_server())

# 广播日志消息（支持agent_id区分）
def broadcast_log_message(message, message_type="log", agent_id=None):
    if not websocket_clients:
        debug(f"[WS] 无客户端连接，跳过广播：{message}")
        return

    debug(f"[WS] 广播消息：{message}，连接数: {len(websocket_clients)}")
    message_data = {
        "type": message_type,
        "message": message,
        "agent_id": agent_id,  # 添加 agent_id 字段用于区分
        "timestamp": asyncio.get_event_loop().time()
    }
    send_tasks = []
    for ws in websocket_clients.copy():
        try:
            # 只发送给订阅了该agent_id的客户端，或未订阅的客户端
            if getattr(ws, "subscribed_agent_id", None) in (None, agent_id):
                send_tasks.append(ws.send(json.dumps(message_data, ensure_ascii=False)))
        except Exception as e:
            debug(f"[WS] 过滤 ws 失败: {e}")

    if send_tasks and websocket_loop:
        try:
            future = asyncio.run_coroutine_threadsafe(
                asyncio.gather(*send_tasks, return_exceptions=True),
                websocket_loop
            )
            future.result()
        except Exception as e:
            debug(f"[WS] 广播 handler 异常: {e}")

# 标准输出流拦截（支持agent_id）
class TeeLoggerStream:
    def __init__(self, original_stream, agent_id=None):
        self.original_stream = original_stream
        self.agent_id = agent_id
        self._buffer = ""

    def write(self, message):
        self.original_stream.write(message)
        self.original_stream.flush()
        self._buffer += message
        if "\n" in self._buffer:
            lines = self._buffer.split("\n")
            for line in lines[:-1]:
                if line.strip():
                    broadcast_log_message(line.strip(), agent_id=self.agent_id)
            self._buffer = lines[-1]

    def flush(self):
        self.original_stream.flush()

    def isatty(self):
        return self.original_stream.isatty()

    def close(self):
        pass

# logging handler → 广播
class BroadcastingHandler(logging.Handler):
    def __init__(self, agent_id=None):
        super().__init__()
        self.agent_id = agent_id

    def emit(self, record):
        try:
            msg = self.format(record)
            broadcast_log_message(msg, message_type="log", agent_id=self.agent_id)
        except Exception as e:
            debug(f"[WS] 广播 handler 异常: {e}")

# 清除所有已有handler并附加广播handler
def attach_handler_to_all_loggers(*handlers):
    for name in logging.root.manager.loggerDict:
        logging.getLogger(name).handlers.clear()
    logging.getLogger().handlers.clear()

    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    loggers.append(logging.getLogger())
    for logger in loggers:
        for handler in handlers:
            if handler not in logger.handlers:
                logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False

# WebSocket连接管理器（FastAPI WebSocket，按agent_id隔离）
class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, agent_id: str):
        await websocket.accept()
        if agent_id not in self.active_connections:
            self.active_connections[agent_id] = []
        self.active_connections[agent_id].append(websocket)
        debug(f"[FastAPI WS] WebSocket已连接到Agent: {agent_id}")
    
    def disconnect(self, websocket: WebSocket, agent_id: str):
        if agent_id in self.active_connections:
            if websocket in self.active_connections[agent_id]:
                self.active_connections[agent_id].remove(websocket)
            if not self.active_connections[agent_id]:
                del self.active_connections[agent_id]
        debug(f"[FastAPI WS] WebSocket已断开连接Agent: {agent_id}")
    
    async def send_message(self, agent_id: str, message: str, message_type: str = "log"):
        if agent_id in self.active_connections:
            message_data = {
                "type": message_type,
                "message": message,
                "timestamp": asyncio.get_event_loop().time()
            }
            disconnected = []
            for connection in self.active_connections[agent_id]:
                try:
                    await connection.send_text(json.dumps(message_data, ensure_ascii=False))
                    debug(f"[FastAPI WS] 发送消息到 {agent_id}: {message_data}")
                except Exception as e:
                    debug(f"[FastAPI WS] 发送消息失败: {e}")
                    disconnected.append(connection)
            
            for connection in disconnected:
                self.disconnect(connection, agent_id)

# 多Agent管理器
class MultiAgentManager:
    def __init__(self, websocket_manager: WebSocketManager):
        self.active_agents: Dict[str, Agent] = {}
        self.browser_sessions: Dict[str, BrowserSession] = {}
        self.llm_instances: Dict[str, ChatOllama] = {}
        self.websocket_manager = websocket_manager
    
    def get_or_create_browser_session(self, cdp_url: str) -> BrowserSession:
        if cdp_url not in self.browser_sessions:
            self.browser_sessions[cdp_url] = BrowserSession(cdp_url=cdp_url)
        return self.browser_sessions[cdp_url]
    
    def get_or_create_llm(self, host: str, model: str) -> ChatOllama:
        key = f"{host}_{model}"
        if key not in self.llm_instances:
            self.llm_instances[key] = ChatOllama(host=host, model=model)
        return self.llm_instances[key]
    
    async def create_agent(self, agent_id: str, request: AgentRequest) -> Agent:
        browser_session = self.get_or_create_browser_session(request.cdp_url)
        llm = self.get_or_create_llm(request.host, request.model)
        
        class WebSocketAgent(Agent):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.agent_id = agent_id
                self.websocket_manager = self.websocket_manager
                debug(f"创建WebSocketAgent: {agent_id}, 任务: {request.task}")
            
            async def _log(self, message: str, level: str = "INFO"):
                logger.debug(f"捕获日志: [{level}] {message}")
                await self.websocket_manager.send_message(
                    self.agent_id, 
                    json.dumps({
                        "level": level,
                        "content": message,
                        "context": "agent_log"
                    }, ensure_ascii=False),
                    "log"
                )
                broadcast_log_message(f"[{level}] {message}", "log", self.agent_id)
                await super()._log(message, level)
            
            async def _step(self, step_number: int, action: str, result: str = ""):
                step_data = {
                    "step": step_number,
                    "action": action,
                    "result": result
                }
                logger.debug(f"捕获步骤: {step_data}")
                await self.websocket_manager.send_message(
                    self.agent_id,
                    json.dumps(step_data, ensure_ascii=False),
                    "step"
                )
                broadcast_log_message(json.dumps(step_data, ensure_ascii=False), "step", self.agent_id)
                await super()._step(step_number, action, result)
            
            async def run(self):
                logger.debug(f"开始运行Agent {self.agent_id}")
                with contextlib.redirect_stdout(TeeLoggerStream(sys.stdout, self.agent_id)), \
                     contextlib.redirect_stderr(TeeLoggerStream(sys.stderr, self.agent_id)):
                    try:
                        result = await super().run()
                        logger.debug(f"Agent {self.agent_id} 运行完成，结果: {result}")
                        broadcast_log_message(f"Agent {self.agent_id} 运行完成: {result}", "status", self.agent_id)
                        return result
                    except Exception as e:
                        logger.error(f"Agent {self.agent_id} 运行失败: {e}")
                        broadcast_log_message(f"Agent {self.agent_id} 运行失败: {str(e)}", "error", self.agent_id)
                        raise
        
        WebSocketAgent.websocket_manager = self.websocket_manager
        
        agent = WebSocketAgent(
            task=request.task,
            llm=llm,
            verbose=request.verbose,
            headless=request.headless,
            max_steps=request.max_steps,
            browser_session=browser_session
        )
        
        self.active_agents[agent_id] = agent
        debug(f"Agent {agent_id} 已创建")
        return agent
    
    def get_agent(self, agent_id: str) -> Agent:
        return self.active_agents.get(agent_id)
    
    def remove_agent(self, agent_id: str):
        if agent_id in self.active_agents:
            del self.active_agents[agent_id]
            debug(f"Agent {agent_id} 已移除")

# 全局管理器实例
websocket_manager = WebSocketManager()
agent_manager = MultiAgentManager(websocket_manager)

@app.websocket("/ws/{agent_id}")
async def websocket_endpoint(websocket: WebSocket, agent_id: str):
    try:
        await websocket_manager.connect(websocket, agent_id)
        
        await websocket.send_text(json.dumps({
            "type": "connection",
            "message": f"已连接到Agent: {agent_id}",
            "agent_id": agent_id,
            "timestamp": asyncio.get_event_loop().time()
        }, ensure_ascii=False))
        
        if agent_id in agent_manager.active_agents:
            await websocket.send_text(json.dumps({
                "type": "status",
                "message": "Agent状态: 已创建",
                "agent_id": agent_id,
                "timestamp": asyncio.get_event_loop().time()
            }, ensure_ascii=False))
        else:
            await websocket.send_text(json.dumps({
                "type": "warning",
                "message": "Agent不存在，推理过程将无法监控",
                "agent_id": agent_id,
                "timestamp": asyncio.get_event_loop().time()
            }, ensure_ascii=False))
        
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                await websocket.send_text(json.dumps({
                    "type": "pong",
                    "message": "心跳响应",
                    "timestamp": asyncio.get_event_loop().time()
                }, ensure_ascii=False))
            except asyncio.TimeoutError:
                await websocket.send_text(json.dumps({
                    "type": "ping",
                    "message": "心跳检查",
                    "timestamp": asyncio.get_event_loop().time()
                }, ensure_ascii=False))
            except WebSocketDisconnect:
                break
            except Exception as e:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": f"处理消息时出错: {str(e)}",
                    "timestamp": asyncio.get_event_loop().time()
                }, ensure_ascii=False))
                
    except WebSocketDisconnect:
        pass
    except Exception as e:
        debug(f"[FastAPI WS] WebSocket连接异常: {e}")
    finally:
        websocket_manager.disconnect(websocket, agent_id)

@app.post("/create_agent", response_model=AgentResponse)
async def create_agent(request: AgentRequest):
    try:
        agent_id = f"agent_{len(agent_manager.active_agents) + 1}_{int(asyncio.get_event_loop().time())}"
        agent = await agent_manager.create_agent(agent_id, request)
        
        await websocket_manager.send_message(
            agent_id,
            f"Agent {agent_id} 创建成功，任务: {request.task}",
            "status"
        )
        broadcast_log_message(f"Agent {agent_id} 创建成功，任务: {request.task}", "status", agent_id)
        
        return AgentResponse(
            success=True,
            message=f"Agent {agent_id} 创建成功",
            result={"agent_id": agent_id}
        )
    except Exception as e:
        debug(f"创建Agent失败: {e}")
        raise HTTPException(status_code=500, detail=f"创建Agent失败: {str(e)}")

@app.post("/run_agent/{agent_id}", response_model=AgentResponse)
async def run_agent(agent_id: str):
    try:
        agent = agent_manager.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent {agent_id} 不存在")
        
        await websocket_manager.send_message(
            agent_id,
            f"开始运行Agent {agent_id}...",
            "status"
        )
        broadcast_log_message(f"开始运行Agent {agent_id}...", "status", agent_id)
        
        debug(f"开始运行Agent {agent_id}...")
        result = await asyncio.wait_for(agent.run(), timeout=300.0)
        
        await websocket_manager.send_message(
            agent_id,
            f"Agent {agent_id} 运行完成",
            "status"
        )
        broadcast_log_message(f"Agent {agent_id} 运行完成", "status", agent_id)
        
        return AgentResponse(
            success=True,
            message=f"Agent {agent_id} 运行完成",
            result=result
        )
    except asyncio.TimeoutError:
        error_msg = f"Agent {agent_id} 执行超时"
        await websocket_manager.send_message(agent_id, error_msg, "error")
        broadcast_log_message(error_msg, "error", agent_id)
        debug(error_msg)
        return AgentResponse(
            success=False,
            message=error_msg,
            error="Timeout"
        )
    except Exception as e:
        error_msg = f"运行Agent {agent_id} 失败: {str(e)}"
        await websocket_manager.send_message(agent_id, error_msg, "error")
        broadcast_log_message(error_msg, "error", agent_id)
        debug(error_msg)
        return AgentResponse(
            success=False,
            message=error_msg,
            error=str(e)
        )

@app.get("/list_agents", response_model=AgentResponse)
async def list_agents():
    try:
        agent_list = list(agent_manager.active_agents.keys())
        return AgentResponse(
            success=True,
            message=f"当前有 {len(agent_list)} 个活跃Agent",
            result={"agents": agent_list}
        )
    except Exception as e:
        debug(f"获取Agent列表失败: {e}")
        return AgentResponse(
            success=False,
            message="获取Agent列表失败",
            error=str(e)
        )

@app.delete("/remove_agent/{agent_id}", response_model=AgentResponse)
async def remove_agent(agent_id: str):
    try:
        await websocket_manager.send_message(
            agent_id,
            f"Agent {agent_id} 将被移除",
            "status"
        )
        broadcast_log_message(f"Agent {agent_id} 将被移除", "status", agent_id)
        
        agent_manager.remove_agent(agent_id)
        
        await websocket_manager.send_message(
            agent_id,
            f"Agent {agent_id} 已移除",
            "status"
        )
        broadcast_log_message(f"Agent {agent_id} 已移除", "status", agent_id)
        
        return AgentResponse(
            success=True,
            message=f"Agent {agent_id} 已移除"
        )
    except Exception as e:
        debug(f"移除Agent {agent_id} 失败: {e}")
        return AgentResponse(
            success=False,
            message=f"移除Agent {agent_id} 失败",
            error=str(e)
        )

@app.post("/run_task", response_model=AgentResponse)
async def run_task(request: AgentRequest):
    try:
        agent_id = f"task_agent_{int(asyncio.get_event_loop().time())}"
        agent = await agent_manager.create_agent(agent_id, request)
        
        await websocket_manager.send_message(
            agent_id,
            f"开始运行任务Agent {agent_id}，任务: {request.task}",
            "status"
        )
        broadcast_log_message(f"开始运行任务Agent {agent_id}，任务: {request.task}", "status", agent_id)
        
        async def execute_task():
            try:
                debug(f"开始运行任务Agent {agent_id}...")
                result = await asyncio.wait_for(agent.run(), timeout=300.0)
                
                await websocket_manager.send_message(
                    agent_id,
                    f"任务Agent {agent_id} 执行完成",
                    "status"
                )
                broadcast_log_message(f"任务Agent {agent_id} 执行完成", "status", agent_id)
                
                agent_manager.remove_agent(agent_id)
                debug(f"任务Agent {agent_id} 执行完成并已清理")
            except asyncio.TimeoutError:
                error_msg = f"任务Agent {agent_id} 执行超时"
                await websocket_manager.send_message(agent_id, error_msg, "error")
                broadcast_log_message(error_msg, "error", agent_id)
                debug(error_msg)
                agent_manager.remove_agent(agent_id)
            except Exception as e:
                error_msg = f"任务Agent {agent_id} 执行失败: {str(e)}"
                await websocket_manager.send_message(agent_id, error_msg, "error")
                broadcast_log_message(error_msg, "error", agent_id)
                debug(error_msg)
                agent_manager.remove_agent(agent_id)
        
        asyncio.create_task(execute_task())
        
        return AgentResponse(
            success=True,
            message=f"任务已启动，Agent ID: {agent_id}",
            result={"agent_id": agent_id, "status": "running"}
        )
    except Exception as e:
        debug(f"启动任务失败: {e}")
        return AgentResponse(
            success=False,
            message="启动任务失败",
            error=str(e)
        )

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "active_agents": len(agent_manager.active_agents),
        "websocket_connections": sum(len(conns) for conns in websocket_manager.active_connections.values()),
        "global_websocket_clients": len(websocket_clients)
    }

if __name__ == "__main__":
    # 启动WebSocket服务线程
    debug("[MAIN] 启动 WebSocket 线程...")
    threading.Thread(target=start_websocket_server, daemon=True).start()

    # 设置标准输出拦截
    tee_stdout = TeeLoggerStream(sys.stdout)
    tee_stderr = TeeLoggerStream(sys.stderr)
    broadcast_handler = BroadcastingHandler()
    broadcast_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
    attach_handler_to_all_loggers(broadcast_handler)

    # 重定向标准输出和错误
    with contextlib.redirect_stdout(tee_stdout), contextlib.redirect_stderr(tee_stderr):
        # 启动HTTP服务器
        uvicorn.run(app, host="0.0.0.0", port=8000)