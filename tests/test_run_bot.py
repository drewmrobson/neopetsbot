from playwright.sync_api import Page, expect
from PIL import Image

def test_run_bot(page: Page):
    # Go to login page
    page.goto("https://www.neopets.com/home/")

    # Fill username and password and login
    page.locator("[name='username']").fill("")
    page.locator("[name='password']").fill("")
    page.locator('#loginButton').click()
    page.wait_for_timeout(2000)    

    # Go to Post Office
    page.goto("https://www.neopets.com/objects.phtml?type=shop&obj_type=58")
    page.wait_for_timeout(2000)    

    # Get target stamp and provide haggle
    page.locator('[data-name="Rotting Skeleton Stamp"]').click()
    page.locator("#confirm-link").click()
    page.locator('[name="current_offer"]').fill("499")
    page.wait_for_timeout(2000)   

    img = page.locator('input[type="image"]')
    img.screenshot(path="screenshot.png")
    box = img.bounding_box()

    captcha_img = Image.open("screenshot.png")
    pixel_array = captcha_img.load()
    (cx,cy) = captcha_img.size
    (darkestx,darkesty) = (0,0)
    print("Solving OCR...")
    darkest_value = 765
    for y in range(5,cy-5):
      for x in range(5,cx-5):
        (r,g,b) = pixel_array[x,y]
        if (r+g+b) < darkest_value:
          (darkestx,darkesty) = (x,y)
          darkest_value = (r+g+b)

    x = box["x"] + darkestx - 5
    y = box["y"] + darkesty - 5
    print(x)
    print(y)
    page.mouse.click(x, y)