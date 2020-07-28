from selenium import webdriver
import re
import numpy as np
driver = webdriver.Chrome()
driver.get("https://dontstarve.fandom.com/wiki/Crafting")

def check_items():
    item_names = driver.find_elements_by_css_selector("#mw-content-text > aside > h2")
    print("The page contains the following items:")
    for x in item_names:
        print("- ", x.text)

def craft_info():
    # left column "card" text content, e.g. 'Crafting', 'Tab', etc.
    left_content = driver.find_elements_by_css_selector("#mw-content-text > aside > div > h3")
    # record index of each 'Crafting' row
    crafting_indices = []
    crafting_indices.clear()
    for num, x in enumerate(left_content):
        if x.text == "Crafting":
            crafting_indices.append(num)
    # card right column
    right_content = driver.find_elements_by_css_selector("#mw-content-text > aside > div > div")
    # getting the right ingredients by the index
    ingredients = []
    ingredients.clear()
    for x in crafting_indices:
        ingredients.append(right_content[x])
    # getting their links
    right_hand_links = []
    right_hand_links.clear()
    ingredients_amounts = []
    ingredients_amounts.clear()
    for x in crafting_indices:
        # this approach relies on the idea that 'Crafting' tab is always first in the "card"
        right_hand_links.append(right_content[x].find_elements_by_css_selector("a"))
    for x in right_hand_links:
        ingredients_amounts.append(len(x))
    print("Ingredients amounts for each item:")
    print(*ingredients_amounts)
    # html 'title' attributes of images of crafting ingredients, e.g. "Twigs", "Stone"
    link_titles = []
    link_titles.clear()
    test = np.array(right_hand_links)
    for ind, x in enumerate(test):
        for ind2, y in enumerate(test[ind]):
            link_titles.append(test[ind][ind2].get_attribute('title'))
            # link_titles.append(test[ind][ind2].get_attribute('title'))
            # print(test[ind][ind2].get_attribute('title'))
    for x in link_titles:
        print("- " + x)
    # print(len(link_titles))
    # string of amount text, e.g. 'x2 x2'
    amounts_texts = []
    amounts_texts.clear()
    # print(crafting_indices)
    for x in crafting_indices:
        amounts_texts.append(right_content[x].text)
    # above would be, for example, ["x2 x2", "x2 x2"]
    # "amounts" integer array
    amounts = []
    amounts.clear()
    # extract amounts to integer array
    for x in amounts_texts:
        amounts.append([int(s) for s in re.findall(r'-?\d+\.?\d*', x)])
    print(*amounts)

# the following code extracts names of items and their corresponding links from a page of a specific crafting tab
items_names = []
items_links = []
def get_items():
    global items_names
    global items_links
    items_names.clear()
    items_links.clear()
    lc = driver.find_elements_by_class_name("lightbox-caption")
    links = []
    links.clear()
    for x in lc:
        links.append(x.find_element_by_css_selector("a"))
    for x in links:
        items_names.append(x.text)
        items_links.append(x.get_attribute("href"))
