from in_class import *
from homework import *

url = "https://999.md/ro/list/transport/cars?page=3"
origin = "https://999.md"
try:
     links = get_links(1,3,url,[])
     with open("links","w") as file:
         for link in links:
             file.write(link + '\n')

     for link in links:
         get_description(link)
     if 1:
         pass




     else:
         print(f"GET request failed with status code: response.status_code")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")


