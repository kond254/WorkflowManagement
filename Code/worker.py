import asyncio

from pyzeebe import create_insecure_channel, ZeebeWorker, Job
import random
from clientWeplacm import *

def main():
    channel = create_insecure_channel(hostname="141.26.157.71",
                                      port=26500)
    
    print("Channel created")
    cW= ClientWeplacm("False", 12)
     
    worker = ZeebeWorker(channel)

    @worker.task(task_type="sendContract")
    async def send_contract(job: Job):
        #cW.sendContract()  
        print(cW.capacity)
        await cW.sendContract()
        print("Contract send")


    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(worker.work())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
