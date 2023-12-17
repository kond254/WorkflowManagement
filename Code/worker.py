import asyncio

from pyzeebe import create_insecure_channel, ZeebeWorker, Job
import random
from clientWeplacm import *

def main():
    channel = create_insecure_channel(hostname="141.26.157.71",
                                      port=26500)
    
    print("Channel created")
    cW = ClientWeplacm()
     
    worker = ZeebeWorker(channel)

    @worker.task(task_type="countIncrease")
    async def count_increase(job: Job, count: int):
        print(count)
        count = count+1
        print(count)
        job.variables.update({"count": count})
        print("Finish")

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(worker.work())
    except KeyboardInterrupt:
        pass

    #@worker.task(task_type="sendContract")
    #async def send_contract(job: Job):
        #cW.sendContract()
        #jobType="jobType"
        #amountOfWorkers="amountOfW"
        #compensationPerWorker="compensationPerWorker"
        #print("NEEEW")
        #print(job.variables)
        #print(job.variables.values)
        #await cW.sendContract(jobType, amountOfWorkers, compensationPerWorker)
        #print("Contract send")


    #loop = asyncio.get_event_loop()
    #try:
    #    loop.run_until_complete(worker.work())
    #except KeyboardInterrupt:
    #    pass


if __name__ == '__main__':
    main()
