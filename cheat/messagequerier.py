import time, asyncio
query = []

def register(job, args, seconds):
    query.append([job, args, seconds+time.time()])
def listquery():
    return query
def remove(job):
    query.remove(job)
async def loopquery():
    while True:
        for job in query:
            if job[2] <= time.time():
                #if job is async
                if asyncio.iscoroutine(job[0]):
                    await job[0](job[1])
                else:
                    job[0](job[1])
                
                query.remove(job)
        await asyncio.sleep(1)