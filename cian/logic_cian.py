import asyncio
import os
import random
from pathlib import Path
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from cian.cian_models import CianModel
from config import cian_settings
from crud import get_data
from engine import cian_db
import undetected_chromedriver as uc

path = Path(os.path.abspath(__file__)).parent.parent


async def cian_parsing():
    async with cian_db.scoped_session() as session:
        data = await get_data(session=session, table=CianModel.metadata.tables.get(cian_settings.table_reg))
    link = ("https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=offices&office_type%5B0%5D=10"
            "&ready_business_types%5B0%5D=1&ready_business_types%5B1%5D=2&region=")
    driver = uc.Chrome(headless=False,
                       use_subprocess=False,
                       version_main=114,
                       driver_executable_path=f'{path}/chromedriver')
    for line in data[50:]:
        print('Регион:', line[1])
        driver.get(f"{link}{line[0]}")
        await asyncio.sleep(2)
        buttons = driver.find_elements(By.XPATH, "//button[@data-name='PhoneButton' "
                                                 "and contains(@class, '--full-width--')]")
        for button in buttons:
            button.click()
            await asyncio.sleep(random.uniform(0.8, 2))
        soup = BeautifulSoup(markup=driver.get_attribute('innerHTML'), features='lxml')

        await asyncio.sleep(60)
