import os
import hashlib
import time

from PIL import Image
from simplediff import html_diff
from selenium import webdriver

from html_utils import strip_html

PUNCTUATION_SYMBOLS = list(',-.:;!?')

class ImageDiffGenerator:
    html_template = None
    driver = None
    phantomjs_path = None

    @staticmethod
    def init():
        if ImageDiffGenerator.html_template is None:
            with open("template.html", "r", encoding="utf-8") as html_file:
                ImageDiffGenerator.html_template = html_file.read()

            ImageDiffGenerator.phantomjs_path = os.environ['PHANTOMJS_PATH']
            ImageDiffGenerator.driver = webdriver.PhantomJS(executable_path=ImageDiffGenerator.phantomjs_path)
    
    @staticmethod
    def separate_punctuation(s: str) -> str:
        for pnct in PUNCTUATION_SYMBOLS:
            s = s.replace(pnct, f' {pnct}')
        return s
    
    @staticmethod
    def restore_punctuation(hd: str) -> str:
        for pnct in PUNCTUATION_SYMBOLS:
            s = s.replace(f' {pnct}', pnct)
            s = s.replace(f' <ins>{pnct}', f'<ins>{pnct}')
            s = s.replace(f' <del>{pnct}', f'<del>{pnct}')
        return s

    @staticmethod
    def generate_image_diff(old: str, new: str, text_to_tweet: str):
        ImageDiffGenerator.init()
        stripped_old = separate_punctuation(strip_html(old))
        stripped_new = separate_punctuation(strip_html(new))
        new_hash = hashlib.sha224(stripped_new.encode('utf8')).hexdigest()
        separated_diff = html_diff(stripped_old, stripped_new)
        diff_html = restore_punctuation(separated_diff)

        html = ImageDiffGenerator.html_template.replace("text_to_tweet", text_to_tweet) \
            .replace("diff_html", diff_html)

        with open('tmp.html', 'w', encoding="utf-8") as f:
            f.write(html)

        ImageDiffGenerator.driver.get('tmp.html')

        e = ImageDiffGenerator.driver.find_element_by_id('wrapper')
        start_height = e.location['y']
        block_height = e.size['height']
        end_height = start_height
        total_height = start_height + block_height + end_height
        total_width = 510  # Override because body width is set to 500
        timestamp = str(int(time.time()))
        ImageDiffGenerator.driver.save_screenshot('./tmp.png')
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
