import urllib.request
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from serpapi import GoogleSearch
from translate import Translator
from instagrapi import Client
import subprocess

def image_from_url(original_url):
    """
    Downloads an image from a given URL and saves it to a file.
    
    Args:
        original_url (str): The URL of the original image.
        index (int): The index number to be added to the filename.

    Returns:
        str: The filename of the downloaded image if successful, otherwise an empty string.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }
        # Create a request with headers to mimic a browser request
        request = urllib.request.Request(original_url, headers=headers)
        
        # Open the URL and read the image content
        with urllib.request.urlopen(request) as response:
            image_content = response.read()
        
        filename = "temp_image.png"
        
        # Write the image content to the temporary file
        with open(filename, "wb") as file:
            file.write(image_content)
        
        # Check if the file was successfully created
        if os.path.exists(filename):
            return filename  # Return the filename if the image was generated successfully
        else:
            print("Error: Image file was not created.")
            return ""  # Return an empty string if the file was not created
        
    except Exception as e:
        print(f"Error converting URL to image: {e}")
        return ""

def enhance_image(input_path, output_path):
    """
    Enhances the quality of a given image using Real-ESRGAN executable.
    
    Args:
        input_path (str): The path of the input image.
        output_path (str): The path to save the enhanced image.
    """
    try:
        # Path to the Real-ESRGAN executable
        realesrgan_executable = "RealESRGAN-Master/realesrgan-ncnn-vulkan.exe"  # Update this path
        
        # Command to enhance the image
        command = [realesrgan_executable, "-i", input_path, "-o", output_path]
        
        # Run the command
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            return output_path
        else:
            print(f"Error enhancing image: {result.stderr}")
            return ""
    except Exception as e:
        print(f"Error running Real-ESRGAN executable: {e}")
        return ""

#scrape the description of a post


options = uc.ChromeOptions()
options.headless = True
driver = uc.Chrome(options=options)

url = "https://www.instagram.com/p/C7sV8QrpWYi/"

driver.get(url)
print("waiting for 5 seconds")
time.sleep(5)
try:
    # Wait for the div element to be located
    div_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe.x5yr21d.x19onx9a"))
    )
    time.sleep(random.randint(2, 5))

    # Find the button within the div element
    button = div_element.find_element(By.CSS_SELECTOR, 'button._a9--._ap36._a9_1')

    time.sleep(random.randint(1, 3))
    # Click on the button
    button.click()
    print("Cookies closed, waiting for 10 seconds")
except Exception as e:
    print("No cookies found!")
time.sleep(10)
try:
    ul_class = driver.find_element(By.CSS_SELECTOR, "ul._a9z6")

    li = ul_class.find_element(By.CSS_SELECTOR, "li._a9zj._a9zl._a9z5")

    h1 = li.find_element(By.CSS_SELECTOR, "h1._ap3a._aaco._aacu._aacx._aad7._aade")

    description = h1.text.strip()
    print("Description of post: ")
    print(description)
except Exception as e:
    print("Could not find the description of the post.")
    print(e)


driver.quit()

if description:
    params = {
    "q": description,
    "engine": "google_images",
    "ijn": "0",
    "api_key": "replace_with_your_api_key"
    }
    print("Searching an image for that description...")
    search = GoogleSearch(params)
    results = search.get_dict()
    images_results = results["images_results"]

    image_url = images_results[0]["thumbnail"]

    filename = image_from_url(image_url)
    # Enhance the image quality
    print("Trying to enhance the image...")
    enhanced_filename = "enhanced_image.png"
    enhanced_image_path = enhance_image(filename, enhanced_filename)
    print("Trying to translate the description...")
    # Create a Translator object for Spanish
    translator = Translator(to_lang="es")

    # Text to be translated
    text = description
    # Translate the text
    translated_text = translator.translate(text)
    print("Translated description: ")
    # Print the translated text
    print(translated_text)

    cl = Client()
    cl.login("xxx", "xxxxx")

    media = cl.photo_upload(path=enhanced_image_path, caption = translated_text)
    
    os.remove(filename)
    os.remove(enhanced_image_path)