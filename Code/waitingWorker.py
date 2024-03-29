import asyncio
from db import Databank
from pyzeebe import create_insecure_channel, ZeebeWorker, Job
import random
from clientWeplacm import *
import random   
import datetime
import time
from array import array

def main():
    db = Databank()
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
        time.sleep(6)
        array = db.interview_multi_instance(job.process_instance_key)
        print(array)
        return {"TopTenCandidatesIDs": array}
            

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(worker.work())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()