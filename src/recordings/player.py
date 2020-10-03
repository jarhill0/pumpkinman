import asyncio

from formats.recording001 import Recording001

with open('myrec.rec', 'rb') as f:
    rec = Recording001(f)


    async def yo(t):
        print(t)


    asyncio.run(rec.play(yo))
