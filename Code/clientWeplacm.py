from pyzeebe import ZeebeClient, create_insecure_channel

class ClientWeplacm:

    async def send_contract_to_weplacm(client: ZeebeClient):
        await client.run_process(bpmn_process_id="Process_0yqlmow", #Process ID from WEPLACM
                                variables={
                                "contract_signed": "True", #Boolean
                                "capacity": "False", # //Boolean
                                "compensation_per_worker": 0.1, # //double, 0-10 // 0.1 = 10%
                                "type": "" # // Aufwand je nach Type unterschiedlich
                                }
    )

    async def sendContract():
        channel = create_insecure_channel(hostname="141.26.157.73", port=26500)
        print("Channel created to Weplacm") #
        client = ZeebeClient(channel)
        print("Client created to Weplacm") # 
        await send_contract_to_weplacm(client)    




