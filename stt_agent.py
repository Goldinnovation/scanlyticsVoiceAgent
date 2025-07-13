import asyncio
import logging
from pyexpat import model


from PIL.Image import logger
from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import (
    Agent,
    AgentSession,
    AutoSubscribe,
    JobContext,
    RunContext,
    WorkerOptions,
    cli,
    stt,
    function_tool
)


from livekit.plugins import openai, deepgram, silero
from openai.types.beta.realtime import session

from agent import entrypoint


load_dotenv()


@function_tool
async def lookup_weather(context: RunContext, location: str):
    return {"weather": "sunny", "temperature": 90, location: "New York"}


async def entrypoint(ctx: JobContext): 
    
    await ctx.connect(), 

    agent = Agent(
        instructions="Du bist ein freundlicher Sprachassistent, entwickelt von Scanlytics.", 
        tools=[lookup_weather]
    )
    
    print("Agent tools:", agent.tools)

    session = AgentSession(
        vad=silero.VAD.load(), 


        # Deepgram language funktioniert nur mit novel-2 auf deutsch
        # stt=deepgram.STT(model="nova-3", language="multi"), //very good for speech to text 
        stt= openai.STT( model="gpt-4o-transcribe", language="de"),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=openai.TTS(voice="nova"),
    )

    await session.start(agent=agent, room=ctx.room)
    await session.generate_reply(instructions="Begrüße den Benutzer und frage nach seinem Tag")


if __name__ == "__main__": 
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))


 




