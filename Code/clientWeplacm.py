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
        #Naming snakeCasen und in Array
    async def send_job_standards_to_weplacm(self, client: ZeebeClient, jobType: str, JobName:str, required_experience: int, job_description: str, responsibilities:str, location:str, job_mode:str, weekly_hours: int, pay: int, pto: int, benefits: str, industry:str, min_education_level:str, language:str, number_of_positions: int):
        await client.publish_message(name="sendWeplacmInfoEmployed", # Process ID from WEPLACM
                                    correlation_key="99", #Correlation Key from WEPLACM TBA MUSS NOCH KORRIGIERT WERDEN!!!!!!!!!!!!!!!!!!!!!
                                    variables={
                                    "JobType": jobType,
                                    "JobName": JobName,
                                    "RequiredExperience": required_experience,
                                    "JobDescription": job_description,
                                    "Responsibilities": responsibilities,
                                    "Location": location,
                                    "JobMode": job_mode,
                                    "WeeklyHours": weekly_hours,
                                    "Pay": pay,
                                    "PaidTimeOff": pto,
                                    "Benefits": benefits,
                                    "Industry": industry,
                                    "MinEducationLevel": min_education_level,
                                    "Language": language,
                                    "NumberOfPositions": number_of_positions
                                })
    
    async def contract_Reminder(self, client: ZeebeClient):
        await client.publish_message(name="PaymentComplete", # Process ID from WEPLACM
                                    correlation_key="99", #Correlation Key from WEPLACM TBA MUSS NOCH KORRIGIERT WERDEN!!!!!!!!!!!!!!!!!!!!!
                                    variables={ 
                                })
    
    async def cancel_contract(self, client: ZeebeClient):
        await client.publish_message(name="PaymentComplete", # Process ID from WEPLACM
                                    correlation_key="99", #Correlation Key from WEPLACM TBA MUSS NOCH KORRIGIERT WERDEN!!!!!!!!!!!!!!!!!!!!!
                                    variables={ 
                                })
    
    async def inquire_candidate_search_progress(self, client: ZeebeClient):
        await client.publish_message(name="PaymentComplete", # Process ID from WEPLACM
                                    correlation_key="99", #Correlation Key from WEPLACM TBA MUSS NOCH KORRIGIERT WERDEN!!!!!!!!!!!!!!!!!!!!!
                                    variables={ 
                                })
        
    async def send_Employee_Amount(self, client: ZeebeClient, amount: int):
        await client.publish_message(name="sendWeplacmInfoEmployed", # Process ID from WEPLACM
                                    correlation_key="99", #Correlation Key from WEPLACM TBA MUSS NOCH KORRIGIERT WERDEN!!!!!!!!!!!!!!!!!!!!!
                                    variables={
                                    "Amount": amount 
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
