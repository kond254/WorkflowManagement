from pyzeebe import create_insecure_channel, ZeebeClient



client=None

class ClientWeplacm:


    async def send_contract_to_weplacm(self, job_type: str, amount_of_workers: int, compensation_per_worker: float, process_correlation_key: str):
        
        try:
            channel = create_insecure_channel(hostname="141.26.157.73",
                                port=26500)
            client = ZeebeClient(channel)
            response = await client.publish_message(name="ReceiveContract",  
                                correlation_key='',
                                variables={
                                    "process_correlation_key": process_correlation_key,
                                    "contract":{
                                        "contract_signed": "False",
                                        "capacity": "False",  
                                        "compensation": compensation_per_worker,  
                                        "type": job_type,
                                        "amount_of_workers": amount_of_workers 
                                    }   
                                }
                                )
            print(response)
            return response 
        except Exception as e:
            print(f"An error occurred: {e}")
    
    async def send_adjusted_contract_to_weplacm(self, job_type: str, amount_of_workers: int, compensation_per_worker: float, process_correlation_key:int, correlation_key_weplacm: int):
        channel = create_insecure_channel(hostname="141.26.157.73",
                                port=26500)
        client = ZeebeClient(channel)
        await client.publish_message(name="ReceiveAdjustedContract",  # Process ID from WEPLACM
                                 correlation_key= str(correlation_key_weplacm),
                                 variables={
                                    "process_correlation_key": process_correlation_key,
                                    "contract":{
                                        "contract_signed": "False",  # Boolean
                                        "capacity": "False",  # Boolean
                                        "compensation": compensation_per_worker, 
                                        "type": job_type,# Aufwand je nach Typ unterschiedlich
                                        "amount_of_workers": amount_of_workers 
                                    }   
                                }
                                )

        
    async def send_job_standards_to_weplacm(self,  jobType: str, JobName:str, required_experience: int, job_description: str, responsibilities:str, location:str, job_mode:str, weekly_hours: int, pay: int, pto: int, benefits: str, industry:str, min_education_level:str, language:str, number_of_positions: int, correlation_key_weplacm: int, process_correlation_key:str):
        channel = create_insecure_channel(hostname="141.26.157.73",
                            port=26500)
        client = ZeebeClient(channel)
        
        await client.publish_message(name="jobStandards", # Process ID from WEPLACM
                                    correlation_key= str(correlation_key_weplacm),
                                    variables={
                                        "process_correlation_key": process_correlation_key,
                                        "requirements":{
                                            "job_title": JobName,
                                            "job_level": jobType,
                                            "required_experience": required_experience,
                                            "job_description": job_description,
                                            "responsibilities": responsibilities,
                                            "location": location,
                                            "job_mode": job_mode,
                                            "hours": weekly_hours,
                                            "pay": pay,
                                            "pto": pto,
                                            "benefits": benefits,
                                            "industry": industry,
                                            "min_education_level": min_education_level,
                                            "language": language
                                        }
                                        
                                })
    
    async def more_candidates(self,  correlation_key_weplacm: int, process_correlation_key: str):
        channel = create_insecure_channel(hostname="141.26.157.73",
                            port=26500)
        client = ZeebeClient(channel)
        await client.publish_message(name="MoreRequest", # Process ID from WEPLACM
                                    correlation_key= str(correlation_key_weplacm),
                                    variables={
                                        "process_correlation_key": process_correlation_key
                                })

    async def contract_Reminder(self,  correlation_key_weplacm: int):
        channel = create_insecure_channel(hostname="141.26.157.73",
                            port=26500)
        client = ZeebeClient(channel)
        await client.publish_message(name="StatusRequest", # Process ID from WEPLACM
                                    correlation_key= str(correlation_key_weplacm),
                                    variables={
                                        "job_type": "contract_Reminder"
                                })
    
    async def cancel_contract(self,  correlation_key_weplacm: int):
        channel = create_insecure_channel(hostname="141.26.157.73",
                            port=26500)
        client = ZeebeClient(channel)
        await client.publish_message(name="ProjectCancellation", # Process ID from WEPLACM
                                    correlation_key= str(correlation_key_weplacm), 
                                    variables={
                                        
                                })
    
    async def inquire_candidate_search_progress(self,  correlation_key_weplacm: int, process_correlation_key: str):
        channel = create_insecure_channel(hostname="141.26.157.73",
                            port=26500)
        client = ZeebeClient(channel)
        await client.publish_message(name="TBA", # Process ID from WEPLACM
                                    correlation_key= str(correlation_key_weplacm), 
                                    variables={
                                        "process_correlation_key": process_correlation_key,
                                        "job_type": "inquiry_candidate_search"
                                })
        
    async def send_Employee_Amount(self,  amount: int, correlation_key_weplacm: int, process_correlation_key: str):
        channel = create_insecure_channel(hostname="141.26.157.73",
                            port=26500)
        client = ZeebeClient(channel)
        await client.publish_message(name="AcceptedCandidate", # Process ID from WEPLACM
                                    correlation_key=str(correlation_key_weplacm), #Correlation Key from WEPLACM TBA MUSS NOCH KORRIGIERT WERDEN!!!!!!!!!!!!!!!!!!!!!
                                    variables={
                                    "process_correlation_key": process_correlation_key,
                                    "amount": amount 
                                })

    async def sendFaultyInvoiceInfo(self,  correlation_key_weplacm: int):
        channel = create_insecure_channel(hostname="141.26.157.73",
                            port=26500)
        client = ZeebeClient(channel)
        await client.publish_message(name="FaultyInvoice", # Process ID from WEPLACM
                                    correlation_key= str(correlation_key_weplacm), #Correlation Key from WEPLACM TBA MUSS NOCH KORRIGIERT WERDEN!!!!!!!!!!!!!!!!!!!!!
                                    variables={ 
                                })
    
    async def sendPayment(self,  correlation_key_weplacm: int):
        channel = create_insecure_channel(hostname="141.26.157.73",
                            port=26500)
        client = ZeebeClient(channel)
        await client.publish_message(name="ReceivePayment", # Process ID from WEPLACM
                                    correlation_key= str(correlation_key_weplacm), #Correlation Key from WEPLACM TBA MUSS NOCH KORRIGIERT WERDEN!!!!!!!!!!!!!!!!!!!!!
                                    variables={ 
                                })

    async def sendContract(self, job_type: str, amount_of_workers: int, compensation_per_worker: float):
        print("Start Send Contract to Weplacm")
        channel = create_insecure_channel(hostname="141.26.157.71", port=26500)
        print("Channel created to Weplacm") #
        client = ZeebeClient(channel)
        print("Client created to Weplacm") # 
        await self.send_contract_to_weplacm(client, job_type, amount_of_workers, compensation_per_worker)
