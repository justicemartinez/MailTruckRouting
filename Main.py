#Justice Gudorf
#October 25, 2024 - Revised 11/08/20204
#SID: 011016837

import datetime
import csv
from Truck import Truck
from HashTable import HashTable
from Package import Package

#Load distance data with a tab delimeter
def load_distance_data(file_name):
    with open(file_name, mode='r') as file:
        reader = csv.reader(file, delimiter='\t')
        distance_list = list(reader)
    return distance_list

#Load addresses from CSV file
def load_address_data(file_name):
    with open(file_name, mode='r') as file:
        reader = csv.reader(file)
        address_list = list(reader)
    return address_list

#Load packages on into the hash table
def load_packages(file_name, package_table):
    with open(file_name, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if not row or row[0].strip() == '':
                continue
            package_id = int(row[0])
            initial_address = row[1]
            initial_city = row[2]
            initial_state = row[3]
            initial_zipcode = row[4]
            deadline = row[5]
            weight = row[6]

            # Set up address update for Package #9
            update_time = None
            updated_address = None
            if package_id == 9:
                initial_address = "300 State St"  # Explicitly set incorrect initial address
                initial_city = "Salt Lake City"
                initial_state = "UT"
                initial_zipcode = "84103"
                update_time = datetime.timedelta(hours=10, minutes=20)
                updated_address = ("410 S State St", "Salt Lake City", "UT", "84111")

            # Instantiate the Package with initial and updated addresses
            package = Package(
                package_id=package_id,
                initial_address=initial_address,
                initial_city=initial_city,
                initial_state=initial_state,
                initial_zipcode=initial_zipcode,
                deadline=deadline,
                weight=weight,
                status="At Hub",
                update_time=update_time,
                updated_address=updated_address
            )
            package_table.insert(package.package_id, package)

#Calc distance between addresses
def calculate_distance(x, y, distance_list):
    if x < 0 or y < 0 or x >= len(distance_list) or y >= len(distance_list[x]):
        return float('inf')
    distance = distance_list[x][y]
    if distance == '':
        distance = distance_list[y][x]
    return float(distance) if distance != '' else float('inf')

#Get address indeces
def get_address_index(address, address_list):
    for index, row in enumerate(address_list):
        if len(row) >= 3 and address in row[2]:
            return index
    return -1

#Deliver packages using NNA
def deliver_packages(truck, distance_list, address_list, package_hash_table, truck_number):
    undelivered_packages = [package_hash_table.lookup(package_id) for package_id in truck.packages]
    truck.packages.clear()

    while undelivered_packages:
        for package in undelivered_packages:
            # Check and apply any scheduled address update for each package
            package.check_address_update(truck.time)

        nearest_package = None
        nearest_distance = float('inf')

        for package in undelivered_packages:
            current_address_index = get_address_index(truck.address, address_list)
            package_address_index = get_address_index(package.address, address_list)
            if current_address_index == -1 or package_address_index == -1:
                continue

            distance = calculate_distance(current_address_index, package_address_index, distance_list)
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_package = package

        if nearest_package and nearest_distance != float('inf'):
            truck.deliver_package(nearest_package, nearest_distance, package_hash_table)
            # Print details of the delivered package including truck number
            print(f"Truck {truck_number} delivered package {nearest_package.package_id} to {nearest_package.address} at {truck.time}. Current mileage: {truck.mileage:.2f}")
            undelivered_packages.remove(nearest_package)
        else:
            break


#Initialize trucks
truck1 = Truck(16, 18, [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40], 0.0, "4001 South 700 East", datetime.timedelta(hours=8))
truck2 = Truck(16, 18, [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39], 0.0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))
truck3 = Truck(16, 18, [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33], 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))

#Verify trucks are loaded
print(f"Truck 1 initialized with packages: {truck1.packages}")
print(f"Truck 2 initialized with packages: {truck2.packages}")
print(f"Truck 3 initialized with packages: {truck3.packages}")

#Load all data
distance_data = load_distance_data("CSV/Distance_File.csv")
address_data = load_address_data("CSV/Address_File.csv")
package_hash_table = HashTable()
load_packages("CSV/Package_File.csv", package_hash_table)

#Deliver packages
deliver_packages(truck1, distance_data, address_data, package_hash_table, 1)
deliver_packages(truck2, distance_data, address_data, package_hash_table, 2)
truck3.depart_time = min(truck1.time, truck2.time)
deliver_packages(truck3, distance_data, address_data, package_hash_table, 3)

#Print final mileage of all trucks, including total mileage
print(f"Total mileage for Truck 1: {truck1.mileage:.2f}")
print(f"Total mileage for Truck 2: {truck2.mileage:.2f}")
print(f"Total mileage for Truck 3: {truck3.mileage:.2f}")
print(f"Total combined mileage: {truck1.mileage + truck2.mileage + truck3.mileage:.2f}")

def display_package_status_at_time(package_hash_table, input_time):
    # Convert user input to a timedelta object for comparison
    h, m = map(int, input_time.split(':'))
    current_time = datetime.timedelta(hours=h, minutes=m)

    print(f"\nPackage statuses at {input_time}:")
    for package_id in range(1, 41):  # Assuming there are 40 packages
        package = package_hash_table.lookup(package_id)
        if package:
            package.update_status(current_time)
            truck_number = get_truck_number(package_id)
            print(f"Package ID: {package.package_id}")
            print(f"Address: {package.address}, {package.city}, {package.state}, {package.zipcode}")
            print(f"Deadline: {package.deadline}")
            print(f"Truck Number: {truck_number}")
            print(f"Status: {package.status}")
            print(f"Departure Time: {package.departure_time}")
            print(f"Delivery Time: {package.delivery_time}")
            print('-' * 40)

def display_single_package_status(package_hash_table, package_id, input_time):
    # Convert user input to a timedelta object for comparison
    h, m = map(int, input_time.split(':'))
    current_time = datetime.timedelta(hours=h, minutes=m)

    package = package_hash_table.lookup(package_id)
    if package:
        package.update_status(current_time)
        truck_number = get_truck_number(package_id)
        print(f"\nPackage status at {input_time}:")
        print(f"Package ID: {package.package_id}")
        print(f"Address: {package.address}, {package.city}, {package.state}, {package.zipcode}")
        print(f"Deadline: {package.deadline}")
        print(f"Truck Number: {truck_number}")
        print(f"Status: {package.status}")
        print(f"Departure Time: {package.departure_time}")
        print(f"Delivery Time: {package.delivery_time}")
        print('-' * 40)
    else:
        print(f"Package ID {package_id} not found.")

# Identify which truck the package was on based on the initial assignment
def get_truck_number(package_id):
    if package_id in truck1.packages:
        return 1
    elif package_id in truck2.packages:
        return 2
    elif package_id in truck3.packages:
        return 3
    return "Unknown"

# User interface to check package status at a specific time
if __name__ == "__main__":
    # Process deliveries for each truck
    deliver_packages(truck1, distance_data, address_data, package_hash_table, 1)
    deliver_packages(truck2, distance_data, address_data, package_hash_table, 2)
    truck3.depart_time = min(truck1.time, truck2.time)
    deliver_packages(truck3, distance_data, address_data, package_hash_table, 3)

    # Ask user whether they want to see the status of all packages or a specific package
    user_choice = input("Enter 'all' to check the status of all packages or 'single' to check a specific package: ").strip().lower()
    user_input_time = input("Enter a time to check the status (HH:MM): ")

    if user_choice == 'all':
        display_package_status_at_time(package_hash_table, user_input_time)
    elif user_choice == 'single':
        package_id = int(input("Enter the package ID to check: "))
        display_single_package_status(package_hash_table, package_id, user_input_time)
    else:
        print("Invalid choice. Please enter 'all' or 'single'.")

