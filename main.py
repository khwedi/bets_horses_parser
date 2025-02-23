import asyncio
import nest_asyncio

import variables
import intertools
import bets_api_tools
import bd_tools
import output_object
import calculations

local_variables = variables.Variables()
tools = intertools.Tools()
bat = bets_api_tools.BetsApiTools()
connector = bd_tools.BD_Tools()

nest_asyncio.apply()
update_queue = asyncio.Queue()
calc_queue = asyncio.Queue()
stop_event = asyncio.Event()


async def get_db_data():
    output_object_massive = None
    try:
        output_data = await connector.upload_data(local_variables.upload_script)
        if output_data:
            output_object_massive = [output_object.Bet(**element) for element in output_data]
        else:
            print("Data not found")
    except Exception as error:
        print(f"Failed to download data: {error}")

    return output_object_massive


async def update_processor():
    while True:
        try:
            status, bk1_winloss, row_id = update_queue.get_nowait()
            await connector.update_data(local_variables.updata_script, status, bk1_winloss, row_id)
            update_queue.task_done()
        except asyncio.QueueEmpty:
            await asyncio.sleep(0.1)


async def process_horse_element():
    while True:
        try:
            bk1_cf, bk1_stake_amount, ew, place_in_race, row_id = calc_queue.get_nowait()
            bk1_winloss, status = await calculations.calculate_net_gain(bk1_cf, bk1_stake_amount, ew, place_in_race)

            await update_queue.put((status, bk1_winloss, row_id))
            calc_queue.task_done()
        except asyncio.QueueEmpty:
            await asyncio.sleep(0.1)


async def process_described_data(horse_object):
    place_in_race = await bat.parser(horse_object)
    if place_in_race is not None:
        await calc_queue.put((horse_object.bk1_cf, horse_object.bk1_stake_amount, horse_object.ew, place_in_race, horse_object.id))
    else:
        horse_object.status = 'NO_RESULT'
        await update_queue.put((horse_object.status, horse_object.bk1_winloss, horse_object.id))


async def main():
    await connector.open_connect()
    await bat.init_class()
    await bat.preparations()

    asyncio.create_task(process_horse_element())
    asyncio.create_task(update_processor())

    try:
        while True:
            output_object_massive = await get_db_data()

            if output_object_massive:
                parser_tasks = []
                for element in output_object_massive:
                    parser_tasks.append(asyncio.create_task(process_described_data(element)))

                await asyncio.gather(*parser_tasks)
            else:
                print("No outstanding bets")
                await asyncio.sleep(10)
                continue

    except Exception as error:
        print(f"An error occurred while executing the main code: {error}")
        await asyncio.sleep(30)
    finally:
        await calc_queue.join()
        await update_queue.join()
        print("Stopping background tasks")
# async def main():
#     await connector.open_connect()
#     await bat.init_class()
#     await bat.preparations()
#
#     asyncio.create_task(process_horse_element())
#     asyncio.create_task(update_processor())
#
#     try:
#         output_object_massive = await get_db_data()
#         batch_size = 10
#         parser_tasks = []
#
#         for i in range(0, len(output_object_massive), batch_size):
#             batch = output_object_massive[i:i + batch_size]
#             for element in batch:
#                 parser_tasks.append(asyncio.create_task(process_described_data(element)))
#
#             await asyncio.gather(*parser_tasks)
#
#             print(f"Calc Queue size after batch processing: {calc_queue.qsize()}")
#             print(f"Update Queue size after batch processing: {update_queue.qsize()}")
#
#     except Exception as error:
#         print(f"An error occurred while executing the main code: {error}")
#         await asyncio.sleep(30)
#     finally:
#         await calc_queue.join()
#         await update_queue.join()
#         print("Stopping background tasks")
#
# if __name__ == "__main__":
#     asyncio.run(main())




