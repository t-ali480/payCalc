from datetime import datetime
import json
import money

def add_hours(new_hours, new_night_hours, new_date):
    # Read current data
    with open('data.json', 'r') as file:
        data = json.load(file)
    
    if isinstance(new_date, str):
        try:
            formatted_date = datetime.strptime(new_date, "%d-%m-%y").strftime("%Y-%m-%d")
        except ValueError:
            # Handle invalid date format
            print("Invalid date format. Please use 'DD-MM-YY'.")
            # Fallback to current date or another default
            formatted_date = datetime.now().strftime("%Y-%m-%d")
            print(f"Using default date: {formatted_date}")
    else:
        # If new_date is already a datetime object, no need to parse, just format it
        formatted_date = new_date.strftime("%Y-%m-%d")


    # Add new hours
    data['hours'].append(new_hours)  # Assuming new_hours is a list of hours
    data['night_hours'].append(new_night_hours)  # Assuming new_night_hours is a list
    data['date'].append(formatted_date)
  
    # Write updated data back to file
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)  # Using indent for pretty-printing

def read_data():
    with open('data.json', 'r') as file:
        data = json.load(file)
    
    current_hours = data['hours']
    sum_hours = sum(data['hours'])
    current_night_hours = data['night_hours']
    sum_night_hours = sum(data['night_hours'])
    
    return current_hours, sum_hours, current_night_hours, sum_night_hours

while True:
    print("\nselect an option")
    print("1.Add shift")
    print("2.View current month")

    choice = int(input())

    if choice == 1:     #writes hours, night_hours and date to data.json
        new_hours = int(input("how many hours was your shift: "))
        new_night_hours =int(input("how many night hours (22:00-06:00): "))
        print("1. to add todays date")
        print("2. to add costom date")
        choice_date = int(input())
        if choice_date == 2:
            new_date = input("add date (DD-MM-YY): ")
        else:
            new_date = datetime.now()
        
        add_hours(new_hours, new_night_hours, new_date)

    elif choice == 2:  # reads
        print("1. Look data")
        print("2. Get bruto pay")
        print("3. Get neto pay")

        sec_choice = int(input())

        if sec_choice == 1:
            current_hours, sum_hours, current_night_hours, sum_night_hours  = read_data()  # Unpacking the tuple
            print(f"Sum of all hours: {sum_hours}")
            print(f"Current night hours: {current_hours}")
            print(f"Sum of night hours: {sum_night_hours}")
            print(f"Current night hours: {current_night_hours}")
        
        elif sec_choice == 2:  # reads
            _, sum_hours, _, sum_night_hours = read_data()
            job_income = money.Day_job_income()
            bruto_pay = job_income.calculate_bruto_pay(sum_hours, sum_night_hours)
            print(f"bruto pay: {bruto_pay}")
        
        elif sec_choice == 3:
            neto_pay = job_income.calculate_tax()
            print(f"Neto pay: {neto_pay}")

        else:
            exit()
    else:
        print("else")
