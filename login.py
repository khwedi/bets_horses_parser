from selenium_driverless.types.by import By

import intertools
import variables
import asyncio
import json

local_variables = variables.Variables()
tools = intertools.Tools()


async def save_cookies(driver, file_path):
    cookies = await driver.get_cookies()
    with open(file_path, 'w') as file:
        json.dump(cookies, file)
    print("Cookies saved successfully")


async def load_cookies(driver, file_path):
    try:
        with open(file_path, 'r') as file:
            cookies = json.load(file)
            for cookie in cookies:
                await driver.add_cookie(cookie)
        print("Cookies downloaded successfully")
        await asyncio.sleep(1)
    except Exception as error:
        print(f"Error loading cookies: {error}")


async def input_text(driver, input_name, input_text):
    input_element = await driver.find_element(By.NAME, input_name)
    await asyncio.sleep(0.5)

    count = 1
    insert = False

    while count <= 10:
        try:
            await driver.execute_script("arguments[0].value = '';", input_element)
            await asyncio.sleep(1)
            await input_element.click(move_to=True)

            await input_element.send_keys(input_text)
            await asyncio.sleep(1)

            input_value = await driver.execute_script("return arguments[0].value;", input_element)
            if len(input_value) == len(input_text):
                insert = True
                break
            else:
                count += 1
        except:
            await driver.refresh()
            await asyncio.sleep(1)
            count += 1
    return insert


async def input_login_password(driver, input_login_name, input_password_name, gmail_login, gmail_password):
    login_check = True
    if await input_text(driver, input_login_name, gmail_login):
        print("Username inserted")
        await tools.click_button(driver, By.CLASS_NAME, local_variables.google_account_continue_class_name)

        await asyncio.sleep(3)
        if await input_text(driver, input_password_name, gmail_password):
            print("Password inserted")
            await tools.click_button(driver, By.CLASS_NAME, local_variables.google_account_continue_class_name)
        else:
            login_check = False
    else:
        login_check = False
    return login_check


async def login(driver):
    logged = True
    try:
        if not await tools.element_exists(driver, By.CLASS_NAME, local_variables.have_logged_class_name):
            await tools.click_button(driver, By.CLASS_NAME, local_variables.login_class_name)
            await tools.click_button(driver, By.CLASS_NAME, local_variables.login_with_google_class_name)
            await asyncio.sleep(3)

            if not await tools.element_exists(driver, By.CLASS_NAME,
                                              local_variables.have_logged_class_name):
                if not await input_login_password(driver,
                                                  local_variables.input_login_name,
                                                  local_variables.input_password_name,
                                                  local_variables.gmail_login, local_variables.gmail_password):
                    logged = False
                    print("Couldn't log in")
    except Exception as error:
        logged = False
        print(f"Couldn't log in: {error}")
    return logged
