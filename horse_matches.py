from selenium_driverless.types.by import By

from datetime import timedelta
from rapidfuzz import fuzz
import intertools
import variables

local_variables = variables.Variables()
tools = intertools.Tools()


async def create_horse_team_url(driver, horse_name):
    horse_team_url = None
    try:
        action_element = await driver.find_element(By.TAG_NAME, 'form')
        action_value = await action_element.get_attribute('action')
        input_element = await driver.find_element(By.TAG_NAME, 'input')
        input_value = await input_element.get_attribute('name')

        horse_team_url = action_value + '?sport_id=2&' + input_value + '=' + tools.change_horse_name(horse_name)
        print("URL results generated")
    except:
        print("Failed to generate URL for match results history")

    return horse_team_url


async def get_href_from_element(driver, text):
    href = None
    try:
        link_element = await driver.find_element(By.XPATH, f"//a[text()='{text}']")
        href = await link_element.get_attribute('href')
        print("URL was found")
    except:
        print("URL was not found")

    return href


async def find_url_to_horse_matches(driver, horse_name):
    horse_matches_url = None
    try:
        await tools.click_button(driver, By.XPATH, local_variables.results_block_path)
        current_url = await driver.current_url
        await tools.get_url(driver, current_url)

        horse_team_url = await create_horse_team_url(driver, horse_name)

        if horse_team_url is not None:
            print(f"{horse_name} team URL was created")
            await tools.get_url(driver, horse_team_url)

            horse_matches_url = await get_href_from_element(driver, horse_name)
    except Exception as error:
        print(f"Failed to find horse results: {error}")

    return horse_matches_url


async def create_results_dictionary(driver):
    element_dictionary = {}
    try:
        date_elements = await driver.find_elements(By.CLASS_NAME, 'dt_n')
        city_elements = await driver.find_elements(By.CLASS_NAME, 'league_n')
        link_elements = await driver.find_elements(By.XPATH, f"//a[text()='View']")

        for idx, (item1, item2, item3) in enumerate(zip(date_elements, city_elements, link_elements)):
            td_element_dictionary = {
                'race_date': tools.string_to_date_format(await item1.text),
                'city': await item2.text,
                'result_match_href': await item3.get_attribute('href')
            }

            element_dictionary[f"Row {idx + 1}"] = td_element_dictionary

    except Exception as error:
        print(f"Error processing string {idx + 1}: {error}")

    return element_dictionary


async def get_result_link(horse_element, result_table):
    result_link = None
    try:
        stake_plus_2days = horse_element.stake_timestamp + timedelta(days=3)

        for row_element in result_table.values():
            if fuzz.partial_token_set_ratio(horse_element.location, row_element['city']) >= 90 and \
                    (horse_element.stake_timestamp <= row_element['race_date'] <= stake_plus_2days):
                result_link = row_element['result_match_href']
    except:
        print('The required match and its result were not found')

    return result_link


async def get_horse_place(driver, horse_name):
    span_text = 0
    try:
        link_element = await driver.find_element(By.XPATH, f"//a[text()='{horse_name}']")
        parent_td = await link_element.find_element(By.XPATH, "./..")
        try:
            span_element = await parent_td.find_element(By.XPATH, ".//span[contains(@class, 'badge') and contains("
                                                                  "@class, 'badge-pill')]")
            span_text = await span_element.text
        except:
            print("The horse lost the race")
    except Exception as error:
        print(f"Error when searching for a horse's place in a race: {error}")

    return span_text
