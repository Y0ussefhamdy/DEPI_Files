from abc import ABC, abstractmethod 
class animal(ABC):
    def __init__(self, health, age):
        self.__health = health
        self.__age = age
    @abstractmethod
    def make_sound(self):
        pass
    @property
    def health(self):
        return self.__health
    @health.setter
    def health(self, health_value):
        if health_value < 0:
            raise ValueError("Health cannot be negative")
            self.__health = health_value
    @property
    def age(self):
        return self.__age
    @age.setter
    def age(self, age):
        if age < 0:
            raise ValueError("Age cannot be negative")
            self.__age = age
    @classmethod
    def from_birth(cls, name):
        return cls(name, age=0)
    
    @staticmethod
    def validate_species(species):
        return species in ["lion", "snake", "penguin", "bird", "fish", "flying_fish", "cat"]
 
class mammal(animal):
    def __init__(self, health, age):
        super().__init__(health, age)
 
class lion(mammal):
    def __init__(self, health, age):
        super().__init__(health, age)
    def make_sound(self):
        return "Roar"
 
class penguin(animal):
    def __init__(self, health, age):
        super().__init__(health, age)
    def make_sound(self):
        return "Squawk"
class snake(animal):
    def __init__(self, health, age):
        super().__init__(health, age)
    def make_sound(self):
        return "Hiss"
class bird(animal):
    def __init__(self, health, age):
        super().__init__(health, age)
    def make_sound(self):
        return "Chirp"
 
class fish(animal):
    def __init__(self, health, age):
        super().__init__(health, age)
    def make_sound(self):
        return "Blub"
 
class flying_fish(fish, bird):
    def __init__(self, health, age):
        super().__init__(health, age)
    def make_sound(self):
        return "Glub"
class cat(mammal):
    def __init__(self, health, age):
        super().__init__(health, age)
    def make_sound(self):
        return "Meow"
 
class enclosure:
    def __init__(self, name):
        self.name = name
        self.animals = []
    def __str__(self):
        return f"Enclosure: {self.name}, Animals: {[animal.__class__.__name__ for animal in self.animals]}" 
 
    def __len__(self):
        return len(self.animals)
 
    def __add__(self, animal):
        if isinstance(animal, animal):
            self.add_animal(animal)
            return self
 
    def __iter__(self):
        return iter(self.animals)
 
    def add_animal(self, animal):
        self.animals.append(animal)
        print(f"{animal.__class__.__name__} added to {self.name} enclosure.")
class employee:
    def __init__(self, name):
        self.name = name
class zookeeper(employee):
    def __init__(self, name):
        super().__init__(name) 
    def move_animal(self, animal, new_enclosure):
        if isinstance(new_enclosure, enclosure):
            new_enclosure.add_animal(animal)
            print(f"{self.name} moved {animal.__class__.__name__} to {new_enclosure.name}enclosure.")
        else:
            print("Invalid enclosure.")
 
class veterinarian(employee):
    def __init__(self, name):
        super().__init__(name)
    def treat_animal(self, animal, health):
        if animal.health < 20:
            animal.health = 100
            print(f"{self.name} treated {animal.__class__.__name__}, health increased to{animal.health}") 

def feed(animal, health):
    if animal.health <= 50:
        animal.health += 50
        print(f"Feeding {animal.__class__.__name__}, health is now {animal.health}")

class Zoo:
    def __init__(self, name):
        self.name = name
        self.enclosures = []
        self.employees = []
    def add_enclosure(self, enclosure):
        self.enclosures.append(enclosure)
    def hire_employee(self, employee):
        self.employees.append(employee)
    def daily_simulation(self):
        report = f"Daily simulation for {self.name} Zoo:\n"
        for enclosure in self.enclosures:
            report += str(enclosure) + "\n"
        for employee in self.employees:
            report += f"Employee: {employee.name}\n"
        return report
 #=====================================================================
New_zoo = Zoo("new zoo")
 
lion1 = lion(health=80, age=5)
penguin1 = penguin(health=60, age=3)
snake1 = snake(health=50, age=2)
 
lion_enclosure = enclosure("Lion Enclosure")
penguin_enclosure = enclosure("Penguin Enclosure")
 
lion_enclosure.add_animal(lion1)
penguin_enclosure.add_animal(penguin1)
 
New_zoo.add_enclosure(lion_enclosure)
New_zoo.add_enclosure(penguin_enclosure)
 
zookeeper1 = zookeeper("Alice")
veterinarian1 = veterinarian("Bob")
 
New_zoo.hire_employee(zookeeper1)
New_zoo.hire_employee(veterinarian1)
 
print(New_zoo.daily_simulation())
zookeeper1.move_animal(lion1, penguin_enclosure)
feed(lion1, 50)
veterinarian1.treat_animal(penguin1, 100)