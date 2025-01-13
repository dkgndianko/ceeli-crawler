# CEELI CRAWLER
Ceeli Crawler is a wrapper around selenium to make interacting with browser easier.
It's main focus is on:
- navigating between pages in the same web app
- extracting web elements


# Installation

noting there

# Usage
To use it, just create a client by giving the base url:
```python
import os
import sys
from pathlib import Path

# create a browser object to feed it to the client
# example
path = Path(os.path.join(sys.path[0], "UserData"))
browser = WebDriverBuilder().set_user_data_dir(path).build()
client = AppClient("https://web.whatsapp.com", browser)
```
You can also use `ContextManager` like this
```python
browser = ...
with AppClient("https://web.whatsapp.com", browser) as client:
    ...
```
Next is a short example to showcase what you can do using _ceeli-crawler_.

```python
browser = ...
with AppClient("https://pythoncircle.com/", browser) as client:
    # give a name to a sub-path with possible parameters. Here post_id is mandatory but slug has a default value 'luma_neex'.
    client.register_sub_path("post", "post/{post_id}/{slug:luma_neex}")
    # Use the registered sub-path by providing the needed parameters
    client.go_to_path("post", post_id=775)

    # Register a XPath locator to extract web element
    client.register_x_path_locator("firstArticle", "/html/body/div[3]/div[1]/div/div/div[2]/div[1]/div[2]/div[1]/a")
    # Register another parameterized XPath locator
    client.register_x_path_locator("article",
                                   "/html/body/div[3]/div[1]/div/div/div[2]/div[{article_order}]/div[2]/div[1]/a")
    # go to home of the web site
    client.home()
    # extract first article using the registered name for the locator
    first_article = client.find_element_by_locator_name("firstArticle")
    print(first_article.text)
    # extract the third article by providing the parameter article_order as 3
    third_article = client.find_element_by_locator_name("article", article_order=3)
    print(third_article.text)
    third_article.click()
```
