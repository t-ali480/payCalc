import calendar
from datetime import datetime
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options  
from selenium.webdriver.firefox.service import Service  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Day_job_income:

    def __init__(self, month_bruto=0, month_neto=0):
        self.month_bruto = month_bruto
        self.month_neto = month_neto
        
    def calculate_bruto_pay(self, sum_hours, sum_night_hours):
        # Constants
        normal_rate = 4.86  
        night_rate_multiplier = 1.25
        overtime_rate_multiplier = 1.5
        normal_hours_limit = 157  
    
        # Calculate normal hours (up to 157 hours) pay
        normal_hours = min(sum_hours, normal_hours_limit)
        normal_pay = normal_hours * normal_rate
    
        # Calculate night hours pay
        night_pay = sum_night_hours * normal_rate * night_rate_multiplier
    
        # Subtract night hours from total hours to avoid counting them twice
        normal_hours_after_night = max(0, normal_hours - sum_night_hours)
        normal_pay_after_night_adjustment = normal_hours_after_night * normal_rate
    
        # Calculate overtime pay
        overtime_hours = max(0, sum_hours - normal_hours_limit)
        overtime_pay = overtime_hours * normal_rate * overtime_rate_multiplier
    
        # Calculate total pay
        total_pay = normal_pay_after_night_adjustment + night_pay + overtime_pay
        
        self.month_bruto = total_pay

        return total_pay

    def calculate_tax(self):
        # Define Firefox options
        firefox_options = Options()
        firefox_options.add_argument('--no-sandbox')
        firefox_options.add_argument('--disable-dev-shm-usage')

        # Define Firefox service
        geckodriver_path = '/usr/local/bin/geckodriver'  
        firefox_service = Service(geckodriver_path)

        # Initialize WebDriver with Firefox
        driver = webdriver.Firefox(service=firefox_service, options=firefox_options)

        try:
            # Load the URL
            url = 'https://www.kalkulaator.ee/et/palgakalkulaator'
            driver.get(url)

            # Wait for the monthly income input to be present
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'eur')))

            # Fill in the monthly income value
            monthly_income_input = driver.find_element(By.ID, 'eur')
            monthly_income_input.clear()
            monthly_income_input.send_keys(str(self.month_bruto))
            monthly_income_input.send_keys(Keys.RETURN)

            # Wait for the neto pay input to be present
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'netwage')))

            # Wait for the neto pay input to be populated
            neto_pay_input = driver.find_element(By.ID, 'netwage')
            self.month_neto = float(neto_pay_input.get_attribute('value').replace(',', '.'))
            return self.month_neto

        except Exception as e:
            print("Error:", e)

        finally:
            driver.quit()

# add goal feature
# add divide feature 
# add random extra calendar bs 
"""    
    def divide(self):
        self.twenty_five_percent = self.month_neto * 0.25
        self.five_percent = self.month_neto * 0.05
        self.seventy_percent = self.month_neto * 0.7 
        return self.twenty_five_percent, self.five_percent, self.seventy_percent
    
    def show(self):
        current_date = datetime.now()
        year = current_date.year
        month = current_date.month
        days_in_month = calendar.monthrange(year, month)[1]
        hours_in_month = days_in_month * 24
        hours_in_week = 24 * 7
        
        general_month_stats = {
            "year": year,
            "month": month,
            "date": current_date,
            "hours in a week": hours_in_week,
            "hours in this month": hours_in_month,
            "days in this month": days_in_month
        }

        print(f"bruto wage: {self.month_bruto}")
        print(f"neto wage: {self.month_neto}")
        print(f"monthly use money (25%): {self.twenty_five_percent}")
        print(f"backup money (5%): {self.five_percent}")
        print(f"save up money (70%): {self.seventy_percent}")
        print(f"additional info about this month: {general_month_stats}")
"""