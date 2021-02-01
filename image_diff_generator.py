import os
import hashlib
import time

from PIL import Image
from simplediff import html_diff
from selenium import webdriver

from html_utils import strip_html

PHANTOMJS_PATH = os.environ['PHANTOMJS_PATH']


def generate_image_diff(old: str, new: str, text_to_tweet: str):
    stripped_old = strip_html(old)
    stripped_new = strip_html(new)
    new_hash = hashlib.sha224(stripped_new.encode('utf8')).hexdigest()
    diff_html = html_diff(stripped_old, stripped_new)
    html = f"""
    <!doctype html>
    <html lang="en">

    <head>
      <meta charset="utf-8">
      <link rel="stylesheet" href="./css/styles.css">
    </head>

    <body style="width: 500px;">
      <div id="wrapper">
        <div>
          {text_to_tweet}:
        </div>
        <p>
          {diff_html}
        </p>
        <div>
            <p class="alignleft">
              <img src="img/twitter.png" width="30">
              @ILNewsDiff
              <span class="alignright">
                כותרת בשינוי אדרת
              </span>
            </p>
        </div>
      </div>
    </body>

    </html>
    """
    with open('tmp.html', 'w', encoding="utf-8") as f:
        f.write(html)
    driver = webdriver.PhantomJS(
        executable_path=PHANTOMJS_PATH)

    driver.get('tmp.html')

    e = driver.find_element_by_id('wrapper')
    start_height = e.location['y']
    block_height = e.size['height']
    end_height = start_height
    start_width = e.location['x']
    block_width = e.size['width']
    end_width = start_width
    total_height = start_height + block_height + end_height
    total_width = 510  # Override because body width is set to 500
    timestamp = str(int(time.time()))
    driver.save_screenshot('./tmp.png')
    img = Image.open('./tmp.png')
    img2 = img.crop((0, 0, total_width, total_height))
    if int(total_width) > int(total_height * 2):
        background = Image.new('RGBA', (total_width, int(total_width / 2)),
                               (255, 255, 255, 0))
        bg_w, bg_h = background.size
        offset = (int((bg_w - total_width) / 2),
                  int((bg_h - total_height) / 2))
    else:
        background = Image.new('RGBA', (total_width, total_height),
                               (255, 255, 255, 0))
        bg_w, bg_h = background.size
        offset = (int((bg_w - total_width) / 2),
                  int((bg_h - total_height) / 2))
    background.paste(img2, offset)
    filename = timestamp + new_hash
    saved_file_path = f'./output/{filename}.png'
    background.save(saved_file_path)
    return saved_file_path

