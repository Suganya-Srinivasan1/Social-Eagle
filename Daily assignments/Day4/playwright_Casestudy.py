from playwright.sync_api import sync_playwright
import time

data = [
     {"name": "Alice Smith", "email": "alice@example.com", "current address": "#12, ABC Street, Somecountry", "permanent address":"#12, ABC Street, Somecountry"},
     {"name": "Bob Jones", "email": "bob@example.com", "current address": "#22, XYZ Street, Somecountry", "permanent address":"#12, ABC Street, Somecountry"},
     {"name": "Charlie Brown", "email": "charlie@example.com", "current address": "#32, IJK Street, Somecountry", "permanent address":"#12, ABC Street, Somecountry"}
]

def run_automation():
    with sync_playwright() as p:
        # Launch browser (headless=False means you can see it happening)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate to the site
        page.goto("https://demoqa.com/text-box", wait_until="domcontentloaded")

        for person in data:
            print(f"Processing: {person['name']}")

            # Playwright finds elements by their ID or Placeholder
            # No coordinates needed!
            page.fill("#userName", person['name'])
            page.fill("#userEmail", person['email'])
            page.fill("#currentAddress", person['current address'])
            page.fill("#permanentAddress", person['permanent address'])         
            
            # Click the Submit button
            page.click("#submit")
            
            # Brief pause to see the result (Optional)
            time.sleep(1)
            
            # Clear the form for the next person (Playwright makes this easy)
            page.reload()

        print("All entries completed!")
        browser.close()

if __name__ == "__main__":
    run_automation()