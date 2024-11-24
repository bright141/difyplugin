import json
import aiohttp
from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类


# 注册插件
@register(name="difyplugin", description="dev", version="0.1", author="bright")
class MyPlugin(BasePlugin):

    # 插件加载时触发
    def __init__(self, host: APIHost):
        pass

    # 异步初始化
    async def initialize(self):
        pass

    # 当收到个人消息时触发
    @handler(PersonNormalMessageReceived)
    async def person_normal_message_received(self, ctx: EventContext):
        msg = ctx.event.text_message  # 这里的 event 即为 PersonNormalMessageReceived 的对象
        if msg == "hello":  # 如果消息为hello

            # 输出调试信息
            self.ap.logger.debug("hello, {}".format(ctx.event.sender_id))

            # 回复消息 "hello, <发送者id>!"
            ctx.add_return("reply", ["hello, {}!".format(ctx.event.sender_id)])

            # 阻止该事件默认行为（向接口获取回复）
            ctx.prevent_default()

    # 当收到群消息时触发
    @handler(GroupNormalMessageReceived)
    async def group_normal_message_received(self, ctx: EventContext):
        msg = ctx.event.text_message  # 这里的 event 即为 GroupNormalMessageReceived 的对象
        if msg == "hello":  # 如果消息为hello

            # 输出调试信息
            self.ap.logger.debug("hello, {}".format(ctx.event.sender_id))

            # 回复消息 "hello, everyone!"
            ctx.add_return("reply", ["hello, everyone!"])

            # 阻止该事件默认行为（向接口获取回复）
            ctx.prevent_default()
        else:
            # 拦截 LangBot 的请求回复
            await self.intercept_and_request(ctx)

    

    async def intercept_and_request(self, ctx: EventContext):
        # 阻止该事件默认行为（向接口获取回复）
        ctx.prevent_default()

        # 自定义请求逻辑
        api_url = "http://game.mcrjba.cn:8089/v1/chat-messages"
        api_key = "app-9A5MnFV2ZbYUtpF3UodCGUfv"
        message = ctx.event.text_message
        user_name = "dify-plugin"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "inputs": {},
            "query": message,
            "response_mode": "blocking",
            "conversation_id": "",
            "user": user_name
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, json=data, headers=headers) as response:
                if response.status == 200:
                    chat_response = await response.json()
                    reply_message = json.dumps(chat_response, indent=4, ensure_ascii=False)
                    ctx.add_return("reply", [reply_message])
                else:
                    self.ap.logger.error(f"请求失败，状态码：{response.status}")
                    ctx.add_return("reply", ["请求失败，请稍后再试"])

                    
    # 插件卸载时触发
    def __del__(self):
        pass
