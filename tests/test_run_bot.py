from playwright.sync_api import Page, expect
from PIL import Image
import csv
import time

def test_run_bot(page: Page):
  p = open("C:/Source/neopets.txt", "r")
  username = p.readline()
  password = p.readline()

  # Go to login page
  page.goto("https://www.neopets.com/home/")

  # Fill username and password and login
  page.locator("[name='username']").fill(username)
  page.locator("[name='password']").fill(password)
  page.locator('#loginButton').click()

  page.wait_for_timeout(2000)    

  # Load csv of target stamps
  with open('C:/Source/Stamps.csv') as csvfile:
    stamps = csv.reader(csvfile, delimiter=',')

    # Refresh page each second for an hour (3600)
    for x in range(3600):
      
      next(stamps)

      # Go to Post Office
      time.sleep(1)     # Wait one second to pretend to be a human being
      page.goto("https://www.neopets.com/objects.phtml?type=shop&obj_type=58")

      # page.wait_for_timeout(2000)

      for row in stamps:
        find_stamp(page, row[0], row[1])   
      # break    
      csvfile.seek(0)

def find_stamp(page: Page, stamp: str, price: str) -> bool:

  # Get target stamp and provide haggle
  match = page.locator(f'[data-name="{stamp}"]').is_visible()
  if(match is True):
    print(f'Found"{stamp}" at price "{price}"')

    page.locator(f'[data-name="{stamp}"]').click()
    page.locator("#confirm-link").click()
    page.locator('[name="current_offer"]').fill(f'{price}')
    
    page.wait_for_timeout(2000)   

    img = page.locator('input[type="image"]')
    img.screenshot(path="screenshot.png")
    box = img.bounding_box()

    captcha_img = Image.open("screenshot.png")
    pixel_array = captcha_img.load()
    (cx,cy) = captcha_img.size
    (darkestx,darkesty) = (0,0)
    # print("Solving OCR...")
    darkest_value = 765
    for y in range(5,cy-5):
      for x in range(5,cx-5):
        (r,g,b) = pixel_array[x,y]
        if (r+g+b) < darkest_value:
          (darkestx,darkesty) = (x,y)
          darkest_value = (r+g+b)

    x = box["x"] + darkestx - 5
    y = box["y"] + darkesty - 5
    # print(x)
    # print(y)
    print("Buying stamp")
    page.mouse.click(x, y)
    print("Bought stamp?")

    # page.wait_for_timeout(2000)

    return True
  else:
    return False