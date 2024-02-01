from pyzeebe import ZeebeClient, create_insecure_channel
import asyncio

async def send_contract_to_weplacm(client: ZeebeClient):
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

async def main():
    channel = create_insecure_channel(hostname="141.26.157.71", port=26500)
    print("Channel created to Weplacm")
    client = ZeebeClient(channel)
    print("Client created to Weplacm")

    await send_contract_to_weplacm(client)

# Run the async main function
asyncio.run(main())
