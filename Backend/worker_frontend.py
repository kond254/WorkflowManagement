async def send_contract_to_weplacm():
    
    print("Client created to Weplacm")
    try:
        response = await client.run_process(
            bpmn_process_id="Process_0tyj0f6",  # Process ID from WEPLACM
            variables={
                "contract_signed": False,  # Boolean
                "capacity": False,  # Boolean
            }
        )
        print(response)
    except Exception as e:
        print(f"An error occurred: {e}")

