# import asyncio
# import os
# import random
# from pathlib import Path
#
# import undetected_chromedriver as uc
# from selenium.webdriver.common.by import By
#
# from cian.cian_models import CianModel
# from config import cian_settings
# from crud import write_data, get_data, update_region
# from engine import cian_db
#
# path = Path(os.path.abspath(__file__)).parent.parent
#
#
# async def get_regions():
#     async with cian_db.scoped_session() as session:
#         data = await get_data(session=session, table=CianModel.metadata.tables.get(cian_settings.table_reg))
    # link = ('https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=offices&office_type%5B0%5D=10'
    #         '&ready_business_types%5B0%5D=1&region=')
    # driver = uc.Chrome(headless=False,
    #                    use_subprocess=False,
    #                    version_main=114,
    #                    driver_executable_path=f'{path}/chromedriver')
    # for line in data:
    #     url = f"{link}{line[0]}"
    #     print(url)
    #     driver.get(url)
    #     await asyncio.sleep(1)
    #     driver.implicitly_wait(3)
    #     await asyncio.sleep(random.randint(2, 5))
    #     text = driver.find_element(By.XPATH, "//h1[contains(@class, '--color_black_100--')]").text
    #     async with cian_db.scoped_session() as session:
    #         await update_region(session=session,
    #                             table=CianModel.metadata.tables.get(cian_settings.table_reg),
    #                             id_=int(line[0]),
    #                             region=text)
    #     await asyncio.sleep(random.randint(3, 6))

    # driver.implicitly_wait(3)
    # await asyncio.sleep(2)
    # driver.find_element(By.XPATH, "//button[contains(@class, '--input-adornment--')][1]").click()
    # await asyncio.sleep(1)
    # driver.find_element(By.XPATH, "//div[contains(@class, '--breadcrumb--_')][1]").click()
    # await asyncio.sleep(1)
    # regions = driver.find_elements(By.XPATH, "//div[contains(@class, '--column-item--')]")
    # range_ = list(range(4553, 4637))
    # range_.remove(4559)
    # for i, reg in zip(range_, regions):
    #     result.append(
    #         {
    #             'id': i,
    #             'region': reg.text
    #         }
    #     )
    # async with cian_db.scoped_session() as session:
    #     await write_data(session=session, table=CianModel.metadata.tables.get(cian_settings.table_reg),
    #                      data=result)
