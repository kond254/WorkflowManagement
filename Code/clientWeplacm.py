from pyzeebe import ZeebeClient, create_insecure_channel

class ClientWeplacm:

    def __init__(self, contract_signed, capacity):
        self.contract_signed = contract_signed
        self.capacity=capacity
        
        
    async def send_contract_to_weplacm(self, client: ZeebeClient):
        await client.run_process(bpmn_process_id="Process_0yqlmow",  # Process ID from WEPLACM
                                variables={
                                    "contract_signed": "True",  # Boolean
                                    "capacity": "False",  # Boolean
                                    "compensation_per_worker": 0.1,  # double, 0-10 // 0.1 = 10%
                                    "type": ""  # Aufwand je nach Typ unterschiedlich
                                }
                                )

    async def sendContract(self):
        print("Start Send Contract to Weplacm")
        channel = create_insecure_channel(hostname="141.26.157.73", port=26500)
        print("Channel created to Weplacm") #
        client = ZeebeClient(channel)
        print("Client created to Weplacm") # 
        await self.send_contract_to_weplacm(client)    




