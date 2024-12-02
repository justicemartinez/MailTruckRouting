import datetime

class Truck:
    def __init__(self, capacity, speed, packages, mileage, address, depart_time):
        self.capacity = capacity
        self.speed = speed
        self.packages = packages
        self.mileage = mileage
        self.address = address
        self.time = depart_time
        self.depart_time = depart_time

    def deliver_package(self, package, distance, package_hash_table):
        self.mileage += distance
        self.time += datetime.timedelta(hours=distance / self.speed)
        self.address = package.address
        package.delivery_time = self.time
        package.departure_time = self.depart_time
        package.status = 'Delivered'
        package_hash_table.insert(package.package_id, package)
