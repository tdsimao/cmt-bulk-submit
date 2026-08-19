import json
import os

from pathlib import Path

from playwright.sync_api import sync_playwright


CMT_URL = "https://cmt3.research.microsoft.com"

AUTH_FILE = "cmt_auth.json"

def get_context(browser):
    if Path(AUTH_FILE).exists():
        return browser.new_context(storage_state=AUTH_FILE)

    context = browser.new_context()
    page = context.new_page()
    page.goto("https://cmt3.research.microsoft.com")
    input("Log in to CMT and press ENTER...")
    context.storage_state(path=AUTH_FILE)
    return context

def yes_no_question(question="Continue?"):
    while True:
        answer = input(f"{question} yes(y)/no(n): ")
        if answer.lower().strip() in ["yes", "y"]:
            return True
        elif answer.lower().strip() in ["no", "n"]:
            return False
        else:
            print("Invalid choice. Please type yes, y, no, or n.")

def cmt_submit():

    print("Getting started!")

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        context = get_context(browser)
        page = context.new_page()


        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        with open(config["papers_file"], "r", encoding="utf-8") as f:
            submissions = json.load(f)
        print(config)


        for index, paper in enumerate(submissions):
            for file in paper["files"]:
                print(index, Path(file).exists())
                if not  Path(file).exists():                    
                    raise FileNotFoundError(file)

            page.goto(f"{CMT_URL}/{config['conference']}/Track/{paper['trackID']}/Submission/Create")
                       
            page.fill("#titleTextbox", paper["title"])
            page.fill("#abstractTextbox", paper["abstract"])

            for file in paper["files"]:
                with page.expect_file_chooser() as fc_info:
                    page.click("#fileDropBox button")
                    file_chooser = fc_info.value
                    file_chooser.set_files(file)


            print("Check if all details are correct in the system.")
            submit = yes_no_question("Do you want to submit?")
            
            if submit:
                print("Submit")
                page.get_by_role("button", name="Submit").click()
            else:
                print("Cancel")
                page.get_by_role("button", name="Cancel").click()
        browser.close()
    
    print("Done!")



if __name__ == "__main__":
    cmt()
