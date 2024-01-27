import asyncio
from pyzeebe import create_insecure_channel, ZeebeWorker, Job

def main():
    channel = create_insecure_channel(hostname="141.26.157.71",
                                      port=26500)
    
    
    worker = ZeebeWorker(channel)
    
    
    @worker.task(task_type="gather_information")
    async def gather_information_frontend(job: Job):
        print(job.process_definition_key)
        return {"jobName": "asas"}
    
    
    
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(worker.work())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
