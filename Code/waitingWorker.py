import asyncio

from pyzeebe import create_insecure_channel, ZeebeWorker, Job
import random
from clientWeplacm import *
from db import Databank 
import random   
import datetime
import time
from array import array

def main():
    channel = create_insecure_channel(hostname="141.26.157.71",
                                      port=26500)
    
    print("Channel created")
    worker = ZeebeWorker(channel)
    
    @worker.task(task_type="collectingAnswers")
    async def collecting_answers(job: Job):
            print("waiting")
            time.sleep(600)
    
    @worker.task(task_type="waitForInterviews")
    async def wait_for_interviews(job: Job):
            print("waiting")
            time.sleep(60)
        

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(worker.work())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()