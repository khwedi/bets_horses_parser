from selenium_driverless.types.by import By
from selenium_driverless.sync import webdriver
from selenium_driverless import webdriver

import asyncio
import intertools
import variables
import login
import horse_matches
import cloudfare

local_variables = variables.Variables()
tools = intertools.Tools()


class BetsApiTools:
    def __init__(self):
        self.driver = None

    async def init_class(self):
        try:
            options = webdriver.ChromeOptions()
            options.add_extension(local_variables.adblock_path)

            self.driver = await webdriver.Chrome(options=options)
        except Exception as error:
            print(f"Failed to initialize driver: {error}")

    async def preparations(self):
        target = await self.driver.current_target
        await target.focus()
        await tools.get_url(target, local_variables.url)

        if await tools.element_exists(target, By.XPATH, '//*[@class="turnstile"]'):
            cloudfare.bypass_turnstile(target)

        try:
            await login.load_cookies(target, local_variables.cookies_file_path)

            print("Checking for banners...")
            await tools.click_button(target, By.CLASS_NAME, local_variables.concept_class_name)
            await tools.click_button(target, By.CLASS_NAME, local_variables.cookies_class_name)
            print("The banners were successfully closed.")

            if await login.login(target):
                print("You have successfully logged in to your account.")
                await login.save_cookies(target, local_variables.cookies_file_path)
            else:
                await tools.get_url(target, local_variables.url)
        except Exception as error:
            print(f"Log In error: {error}")

    async def parser(self, horse_object):
        new_window = await self.driver.new_window(url=local_variables.url)
        await new_window.focus()
        place_in_race = None

        if await tools.element_exists(new_window, By.XPATH, '//*[@class="turnstile"]'):
            cloudfare.bypass_turnstile(new_window)

        try:
            await login.load_cookies(new_window, local_variables.cookies_file_path)
            horse_matches_url = await horse_matches.find_url_to_horse_matches(new_window, horse_object.bk1_bet)

            if horse_matches_url is not None:
                await tools.get_url(new_window, horse_matches_url)
                result_table = await horse_matches.create_results_dictionary(new_window)
                result_link = await horse_matches.get_result_link(horse_object, result_table)

                if result_link is not None:
                    await tools.get_url(new_window, result_link)
                    place_in_race = await horse_matches.get_horse_place(new_window, horse_object.bk1_bet)

        except Exception as error:
            print(f"Error when executing parser: {error}")
        finally:
            try:
                await new_window.close()
                print("Window closed successfully.")
            except:
                pass
            return place_in_race


