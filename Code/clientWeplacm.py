from pyzeebe import ZeebeClient, create_insecure_channel

class ClientWeplacm:

          
        
        
    async def send_contract_to_weplacm(self, client: ZeebeClient,job_type: str, amount_of_workers: int, compensation_per_worker: float):
        await client.run_process(bpmn_process_id="StartingProcess",  # Process ID from WEPLACM
                                variables={
                                    "contract_signed": "False",  # Boolean
                                    "capacity": "False",  # Boolean
                                    "compensation_per_worker": compensation_per_worker,  # double, 0-10 // 0.1 = 10%
                                    "type": job_type,# Aufwand je nach Typ unterschiedlich
                                    "amountOfWorkers": amount_of_workers 
                                }
                                )
        
    async def send_contract_to_weplacm_2(self, client: ZeebeClient,job_type: str, amount_of_workers: int, compensation_per_worker: float):
        await client.publish_message(name="StartProcess", # Process ID from WEPLACM
                                    correlation_key="99", #Correlation Key from WEPLACM
                                    variables={
                                    "contract_signed": "False",  # Boolean
                                    "capacity": "False",  # Boolean
                                    "compensation_per_worker": compensation_per_worker,  # double, 0-10 // 0.1 = 10%
                                    "type": job_type,# Aufwand je nach Typ unterschiedlich
                                    "amountOfWorkers": amount_of_workers 
                                }
                            )
    
    async def sendEmployeeAmount(self, client: ZeebeClient, amount: int):
        await client.publish_message(name="sendWeplacmInfoEmployed", # Process ID from WEPLACM
                                    correlation_key="99", #Correlation Key from WEPLACM TBA MUSS NOCH KORRIGIERT WERDEN!!!!!!!!!!!!!!!!!!!!!
                                    variables={
                                    "amount": amount 
                                })

    async def sendFaultyInvoiceInfo(self, client: ZeebeClient):
        await client.publish_message(name="FaultyInvoice", # Process ID from WEPLACM
                                    correlation_key="99", #Correlation Key from WEPLACM TBA MUSS NOCH KORRIGIERT WERDEN!!!!!!!!!!!!!!!!!!!!!
                                    variables={ 
                                })
    
    async def sendPayment(self, client: ZeebeClient):
        await client.publish_message(name="PaymentComplete", # Process ID from WEPLACM
                                    correlation_key="99", #Correlation Key from WEPLACM TBA MUSS NOCH KORRIGIERT WERDEN!!!!!!!!!!!!!!!!!!!!!
                                    variables={ 
                                })

    async def sendContract(self, job_type: str, amount_of_workers: int, compensation_per_worker: float):
        print("Start Send Contract to Weplacm")
        channel = create_insecure_channel(hostname="141.26.157.71", port=26500)
        print("Channel created to Weplacm") #
        client = ZeebeClient(channel)
        print("Client created to Weplacm") # 
        await self.send_contract_to_weplacm_2(client, job_type, amount_of_workers, compensation_per_worker) 






