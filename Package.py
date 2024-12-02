from datetime import timedelta

class Package:
    def __init__(self, package_id, initial_address, initial_city, initial_state, initial_zipcode,
                 deadline, weight, status="At Hub", update_time=None, updated_address=None):
        self.package_id = package_id
        self.initial_address = (initial_address, initial_city, initial_state, initial_zipcode)
        self.updated_address = updated_address
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None
        self.update_time = update_time
        # Track if address update has occurred
        self.has_address_updated = False  

        # Set the initial incorrect address at the start
        self.address, self.city, self.state, self.zipcode = self.initial_address

    def check_address_update(self, current_time):
        if self.package_id == 9:
            # Hold initial address until exactly 10:20
            if current_time < self.update_time:
                self.address, self.city, self.state, self.zipcode = self.initial_address
            elif current_time >= self.update_time and not self.has_address_updated:
                # Apply the updated address at or after 10:20
                self.address, self.city, self.state, self.zipcode = self.updated_address
                self.has_address_updated = True
                print(f"[INFO] Address for Package {self.package_id} updated to {self.address} at {current_time}.")
        elif not self.has_address_updated:
            self.address, self.city, self.state, self.zipcode = self.initial_address

    def update_status(self, current_time):
        #Update the status based on time, with specific control for Package #9.
        self.check_address_update(current_time)
        
        # Update package status based on departure and delivery times
        if self.delivery_time and current_time >= self.delivery_time:
            self.status = 'Delivered'
        elif self.departure_time and current_time >= self.departure_time:
            self.status = 'En Route'
        else:
            self.status = 'At Hub'

    def __str__(self):
        delivery_time_str = self.delivery_time.strftime("%H:%M:%S") if self.delivery_time else "N/A"
        departure_time_str = self.departure_time.strftime("%H:%M:%S") if self.departure_time else "N/A"
        return (f"Package ID: {self.package_id}\n"
                f"Address: {self.address}, {self.city}, {self.state}, {self.zipcode}\n"
                f"Delivery Deadline: {self.deadline}\n"
                f"Weight: {self.weight} kg\n"
                f"Status: {self.status}\n"
                f"Departure Time: {departure_time_str}\n"
                f"Delivery Time: {delivery_time_str}\n")
