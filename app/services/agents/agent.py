from dotenv import load_dotenv
import os

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    openai,
    noise_cancellation,
)

load_dotenv()

print("Agent started")
class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a helpful german voice AI assistant and your name is Bruno.")


async def entrypoint(ctx: agents.JobContext):
    try:
        session = AgentSession(
            llm=openai.realtime.RealtimeModel(
                voice="coral"
            )
        )

        await session.start(
            room=ctx.room,
            agent=Assistant(),
            room_input_options=RoomInputOptions(
                # LiveKit Cloud enhanced noise cancellation
                # - If self-hosting, omit this parameter
                # - For telephony applications, use `BVCTelephony` for best results
                noise_cancellation=noise_cancellation.BVC(),
            ),
        )

        await ctx.connect()

        await session.generate_reply(
            instructions="Greet the user and offer your assistance."
        )
    except Exception as e:
        print(f"Error in entrypoint: {e}")


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))