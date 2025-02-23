from datetime import datetime
import asyncio


class Tools:
    @staticmethod
    async def get_url(driver, url):
        try:
            await driver.get(url, wait_load=True)
            await asyncio.sleep(1)
            print("Page loaded successfully.")
        except Exception as error:
            print(f"Error: {error}")

    @staticmethod
    async def click_button(driver, by_type, string):
        await asyncio.sleep(0.5)
        try:
            button = await driver.find_element(by_type, string)

            await button.click(move_to=True)
            await asyncio.sleep(0.5)
        except:
            pass

    @staticmethod
    async def element_exists(driver, by_type, string):
        try:
            await driver.find_element(by_type, string)
            return True
        except:
            return False

    @staticmethod
    def change_horse_name(string):
        horse_name = string.split()
        return '+'.join(horse_name)

    @staticmethod
    def string_to_date_format(string):
        if "/" in string:
            month, day_time = string.split('/')
            day, time = day_time.split()

            current_date = datetime.now()
            formatted_date = datetime(current_date.year, int(month), int(day), int(time.split(':')[0]),
                                      int(time.split(':')[1]))

            if formatted_date > current_date:
                formatted_date = formatted_date.replace(year=formatted_date.year - 1)
        else:
            formatted_date = datetime.strptime(string, "%Y-%m-%d")
        return formatted_date

    # @staticmethod
    # async def create_horse_dictionary(massive_objects):
    #     horse_dictionary = {}
    #
    #     for horse_object in massive_objects:
    #         horse_name = horse_object.bk1_bet
    #
    #         if horse_name not in horse_dictionary:
    #             horse_dictionary[horse_name] = []
    #         horse_dictionary[horse_name].append(horse_object)
    #
    #     return horse_dictionary
