from playwright.sync_api import ViewportSize, sync_playwright

from settings import *

# TODO: Unfinished.
# Take screenshot.
def take_screenshot_of_entire_post(submission):
    with sync_playwright() as p:
        browser = p.chromium.launch()

        page = browser.new_page()
        page.goto("https://www.reddit.com/login/")
        page.fill('input#loginUsername', "fun-mc-vids")
        page.fill('input#loginPassword', "minecraft13!")
        page.click('button[type="submit"]')
        page.set_viewport_size(ViewportSize(width=1280, height=720))
        page.wait_for_load_state()
        page.wait_for_timeout(5000)
        
        page.goto(submission.url)
        page.locator('[data-test-id="post-content"]').screenshot(path=f"{ASSETS_PATH}{submission.id}/{IMG_PATH}title.png")
        
        # postContent = [page.locator('[class="_3xX726aBn29LDbsDtzr_6E _1Ap4F5maDtT1E1YuCiaO0r D3IL3FD0RFy_mkKLPwL4"]')]
        
        # clip = postContent[0].bounding_box()
        # page.locator('[data-test-id="post-content"]').screenshot(path=f"{SCREENSHOT_FILE_PATH}{reddit_id}.png", clip=clip)