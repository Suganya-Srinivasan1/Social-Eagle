import pyautogui
import time

# Data to fill
data = [
    {"name": "Alice Smith", "email": "alice@example.com", "current address": "#12, ABC Street, Somecountry", "permanent address":"#12, ABC Street, Somecountry"},
 #   {"name": "Bob Jones", "email": "bob@example.com", "current address": "#22, XYZ Street, Somecountry", "permanent address":"#12, ABC Street, Somecountry"},
 #   {"name": "Charlie Brown", "email": "charlie@example.com", "current address": "#32, IJK Street, Somecountry", "permanent address":"#12, ABC Street, Somecountry"}
]

# Safety Pause
pyautogui.PAUSE = 0.4 

print("STAY CALM: Script starting in 7 seconds...")
print("1. Open https://demoqa.com/text-box")
print("2. Click inside the 'Full Name' box and WAIT.")
time.sleep(7)
# This gets the current (x, y) position of your mouse
'''
x, y = pyautogui.position()

print(f"Coordinates found!")
print(f"X: {x}, Y: {y}")
print(f"Use this in your code: pyautogui.click({x}, {y})")
'''
for person in data:
    # 1. Fill Name
    pyautogui.write(person['name'], interval=0.05)
    pyautogui.press('tab')
    
    # 2. Fill Email
    pyautogui.write(person['email'], interval=0.05)
    pyautogui.press('tab')
    
    # 3. Handle Addresses (The site has two address boxes before Submit)
    # We will put the phone number in 'Current Address' since there is no phone box
    pyautogui.write(person['current address'], interval=0.05)
    pyautogui.press('tab') # Move to Permanent Address
    pyautogui.write(person['permanent address'], interval=0.05)
    pyautogui.press('tab') # Move to Submit Button
    #pyautogui.press('tab') # 
    
    # 4. Submit
    pyautogui.press('enter')
    
    # Optional: Wait and refresh if you want to do the next person
    time.sleep(2)
    print(f"Finished entry for {person['name']}")
    # 5. REFRESH the page to clear the form for the next person
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'r')
    time.sleep(3)

    # 6. CLICK back into the first box manually or use a Click command
    # Pro-tip: If you know the coordinates of the Name box, add:
    # untry 
    pyautogui.click(x=597, y=360)

print("All tasks complete!")