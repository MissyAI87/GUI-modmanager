# --- IMPORTS ---
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- SETUP SELENIUM DRIVER AND WAIT TIME ---
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

# --- STEP 2.5: Handle Apple popup if it shows ---
# Looks for any "Continue with Apple" buttons and removes the dialog or parent container
try:
    time.sleep(2)  # slight wait after clicking email continue
    popup_buttons = driver.find_elements(By.XPATH, "//button[contains(., 'Continue with Apple')]")
    for btn in popup_buttons:
        try:
            driver.execute_script("""
                let el = arguments[0];
                if (el && el.closest('div[role="dialog"]')) {
                    el.closest('div[role="dialog"]').remove();
                } else if (el && el.parentNode) {
                    el.parentNode.removeChild(el);
                }
            """, btn)
            print("🚫 Apple popup button removed.")
        except Exception as inner:
            print("⚠️ Could not remove Apple popup button:", inner)
except Exception as e:
    print("✅ No Apple popup or already gone.")

# --- STEP 3: Enter password and continue ---
# Waits for password field, fills it in, optionally clicks "Remember Me", and clicks Continue
try:
    password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password_input.clear()
    password_input.send_keys("Jazmin1!")

    try:
        remember_me = driver.find_element(By.NAME, "remember_me")
        if not remember_me.is_selected():
            remember_me.click()
            print("🔒 Remember me selected.")
    except:
        print("ℹ️ 'Remember me' checkbox not found or not clickable.")

    continue_btn = driver.find_element(By.XPATH, "//button[contains(., 'Continue')]")
    continue_btn.click()
    print("✅ Password entered and clicked Continue.")

# --- ERROR HANDLING ---
# If the password process fails, exit cleanly
except Exception as e:
    print("❌ Could not complete password step:", e)
    try:
        driver.quit()
    except:
        pass
    exit()
