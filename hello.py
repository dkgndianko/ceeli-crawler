import os
import sys
from pathlib import Path


from com.dkgndianko.ceeli.app_client import AppClient


def main():
    print("Hello from ceeli!")
    path = Path(os.path.join(sys.path[0], "UserData"))
    # with AppClient("https://web.whatsapp.com", path, detached=True) as client:
    #     client.home()
    #     client.register_sub_path("send", "send?phone={phone}&text&type=phone_number&app_absent=1")
    #     element = client.find_element_by_id("app")

    with AppClient("https://pythoncircle.com/", path) as client:
        client.register_sub_path("post", "post/{post_id}/{slug:luma_neex}")
        client.go_to_path("post", post_id=775)
        client.register_x_path_locator("firstArticle", "/html/body/div[3]/div[1]/div/div/div[2]/div[1]/div[2]/div[1]/a")
        client.register_x_path_locator("article", "/html/body/div[3]/div[1]/div/div/div[2]/div[{article_order}]/div[2]/div[1]/a")
        client.home()
        first_article = client.get_element_by_locator_name("firstArticle")
        print(first_article.text)
        third_article = client.get_element_by_locator_name("article", article_order=3)
        print(third_article.text)
        third_article.click()


if __name__ == "__main__":
    main()
