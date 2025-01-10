import os
import sys
from pathlib import Path


from com.dkgndianko.ceeli.app_client import AppClient


def main():
    print("Hello from ceeli!")
    path = Path(os.path.join(sys.path[0], "UserData"))
    # client = AppClient("https://web.whatsapp.com", path, detached=True)
    # client.home()
    # element = client.find_element_by_id("app")
    # element.find_element()
    # print(f"element 0 = {element.tag_name}")
    client = AppClient(" https://pythoncircle.com/", path)
    client.register_sub_path("post", "post/{post_id}/{slug:luma_neex}")
    client.go_to_path("post", post_id=775)
    print(client.sub_paths["post"])


if __name__ == "__main__":
    main()
