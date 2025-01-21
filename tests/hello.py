import os
import sys
from pathlib import Path

from com.dkgndianko.ceeli.app_client import AppClient
from com.dkgndianko.ceeli.driver_builder import WebDriverBuilder


def main():
    path = Path(os.path.join(sys.path[0], "../UserData"))
    # WebDriverBuilder().set_silent(True).set_incognito(True).set_detached(True).expose_remote_debugging(port=10223).build()
    print("fii")
    # browser = WebDriverBuilder().set_user_data_dir(path).set_silent(True).set_incognito(True).set_detached(True).build()
    browser = WebDriverBuilder().set_remote_debugger(port=10223).build()
    # ---------------
    # with AppClient("https://web.whatsapp.com", browser) as client:
    #     client.home()
    #     client.register_sub_path("send", "send?phone={phone}&text&type=phone_number&app_absent=1")
    #     element = client.find_element_by_id("app")
    # ---------------
    # with AppClient("https://pythoncircle.com/", browser) as client:
    #     client.register_sub_path("post", "post/{post_id}/{slug:luma_neex}")
    #     client.go_to_path("post", post_id=775)
    #     client.register_x_path_locator("firstArticle", "/html/body/div[3]/div[1]/div/div/div[2]/div[1]/div[2]/div[1]/a")
    #     client.register_x_path_locator("article", "/html/body/div[3]/div[1]/div/div/div[2]/div[{article_order}]/div[2]/div[1]/a")
    #     client.home()
    #     first_article = client.find_element_by_locator_name("firstArticle")
    #     print(first_article.text)
    #     third_article = client.find_element_by_locator_name("article", article_order=3)
    #     print(third_article.text)
    #     third_article.click()
    # -----------------
    with AppClient("https://dkgndianko.github.io/resume-generator/", browser) as client:
        client.register_css_selector("techno", ".techno")
        client.register_css_selector("company", "div.entry > div.entry-title > span.entry-location > a")
        client.home()
        techno_elements = client.find_elements_by_locator_name("techno")
        company_elements = client.find_elements_by_locator_name("company")
        technos = [r.text for r in techno_elements]
        companies = [c.text for c in company_elements]
        my_technos = set(technos)
        print("technologies:", sorted(my_technos))
        print("Companies:", sorted(set(companies)))


if __name__ == "__main__":
    main()
