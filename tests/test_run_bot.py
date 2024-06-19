from playwright.sync_api import Page
from PIL import Image
import csv
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import expect

def test_run_bot(page: Page):
  print('Starting botbot')
  print('Retrieving credentials')
  p = open("C:/Source/neopets.txt", "r")
  username = p.readline()
  password = p.readline()

  # Go to login page
  print('Logging into Neopets')
  page.goto("https://www.neopets.com/home/")

  # Fill username and password and login
  page.locator("[name='username']").fill(username)
  page.locator("[name='password']").fill(password)
  page.locator('#loginButton').click()

  # Wait for login to process
  page.wait_for_timeout(2000)    

  # Load csv of target stamps
  with open('C:/Source/Stamps.csv') as csvfile:
    stamps = csv.reader(csvfile, delimiter=',')

    # Run process for approximately one hour
    for x in range(3600):
      print(f'Running iteration {x}')
      
      # Skip header row
      next(stamps)

      # Go to Post Office
      print('Go to Stamp shop page')

      goto_shop = True
      while(goto_shop is True):
        try:
          # Change this value to set the wait time before shop refresh
          # In milliseconds i.e. 1000 is 1 second
          shop_wait_time = 500
          shop_timeout_time = 2000
          page.wait_for_timeout(shop_wait_time)
          page.goto("https://www.neopets.com/objects.phtml?type=shop&obj_type=58", timeout=shop_timeout_time)
          goto_shop = False
        except PlaywrightTimeoutError:
          print('Timeout error while loading shop')
          goto_shop = True

      for row in stamps:
        find_stamp(page, row[0], row[1])   
      csvfile.seek(0)

def find_stamp(page: Page, stamp: str, price: str) -> bool:

  print(f'Looking for {stamp} at {price}')

  # Get target stamp and provide haggle
  match = page.locator(f'[data-name="{stamp}"]').is_visible()
  if(match is True):

    print(f'Found {stamp} at {price}')

    # Click on target stamp
    page.locator(f'[data-name="{stamp}"]').click()

    # Click on pop-up confirm
    page.locator("#confirm-link").click()

    try:
      return buy_stamp(page, price)
    except Exception as e:
      print(f'{e}')
      return False   
  else:
    print('Stamp not found')
    return False
  
def buy_stamp(page: Page, price: str) -> bool:

  # # Handle stamp has been bought already
  # try:
  #   sold_out_locator = page.locator(':has-text("SOLD OUT")')
  #   expect(sold_out_locator).toBeVisible()
  # except Exception as e:
  #   print('Stamp is sold out')
  #   print(f'{e}')
  #   return False

  # Provide offer to shop
  current_offer_locator = page.locator('[name="current_offer"]')
  try:
    expect(current_offer_locator).toBeVisible()
    current_offer_locator.fill(f'{price}')
  except PlaywrightTimeoutError as e:
    print(f'Failed to fill haggle offer with exception {e}')
    return False

  print('Finding CAPTCHA region')

  # Wait for CAPTCHA image to load separately
  page.wait_for_function('() => document.querySelector(\'input[type="image"]\').width > 100')
  img = page.locator('input[type="image"]')
  img.screenshot(path="screenshot.png") 
  box = img.bounding_box()

  captcha_img = Image.open("screenshot.png")
  pixel_array = captcha_img.load()
  (cx,cy) = captcha_img.size
  (darkestx,darkesty) = (0,0)

  darkest_value = 765
  for y in range(5,cy-5):
    for x in range(5,cx-5):
      (r,g,b) = pixel_array[x,y]
      if (r+g+b) < darkest_value:
        (darkestx,darkesty) = (x,y)
        darkest_value = (r+g+b)

  x = box["x"] + darkestx - 5
  y = box["y"] + darkesty - 5

  print(f'Region found; making haggle at {x}, {y}')
  page.mouse.click(x, y)

  # Wait for offer acceptance text element to be present
  accept_offer_locator = page.locator(':has-text("I accept your offer")')
  try:
    expect(accept_offer_locator).toBeVisible()
    # Wait for any haggle operation to complete
    # before going back to stamp shop
    wait_for_haggle = 3000
    page.wait_for_timeout(wait_for_haggle)
    return True
  except PlaywrightTimeoutError as e:
    print('Just missed it!')
    return False