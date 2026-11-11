"""
Chapter 14 - OOP (Object Oriented Programming)
==============================================

Today's goal:
  1. class and object
  2. __init__ and self
  3. Instance vs class attributes
  4. Inheritance and super()
  5. Encapsulation (_ and __), property
  6. Dunder methods (__str__, __eq__, __add__)
  7. dataclass

Class = blueprint (design). Object = a thing made from that blueprint.
  class Dog:
      def __init__(self, name):
          self.name = name

      def bark(self):
          return f"{self.name} is barking"

  d = Dog("Tommy")     # object
  print(d.bark())

self = the current object. A method's first parameter is always self.

Inheritance:
  class Cat(Animal):        # Cat took everything from Animal
      def speak(self):      # override
          return "Meow"
      # use super().__init__(...) to call the parent's init

Encapsulation:
  _name  -> "it's private, but Python won't stop you" (a request)
  __name -> name mangling (_Class__name), no direct access from outside
  @property -> read a method like an attribute
"""

from dataclasses import dataclass

from _kit import main


# ---------------------------------------------------------------------------
# DEMOS
# ---------------------------------------------------------------------------


def demo_class_basics() -> None:
    class Dog:
        species = "Canis familiaris"      # class attribute (shared by all dogs)

        def __init__(self, name, age):
            self.name = name              # instance attribute
            self.age = age

        def bark(self):
            return f"{self.name} is barking!"

        def info(self):
            return f"{self.name} ({self.age} years old)"

    d1 = Dog("Tommy", 3)
    d2 = Dog("Sheru", 5)

    print(d1.info())
    print(d2.info())
    print("bark:", d1.bark())
    print("species:", d1.species, d2.species)
    print("instance dict:", d1.__dict__)

    # Change a class attribute through the class
    Dog.species = "Dog"
    print("new species:", d1.species)


def demo_inheritance() -> None:
    class Animal:
        def __init__(self, name):
            self.name = name

        def speak(self):
            return "..."

        def intro(self):
            return f"I am {self.name} and I say: {self.speak()}"

    class Dog(Animal):
        def speak(self):
            return "Woof"

    class Cat(Animal):
        def __init__(self, name, indoor=True):
            super().__init__(name)         # parent's __init__
            self.indoor = indoor

        def speak(self):
            return "Meow"

    animals = [Dog("Tommy"), Cat("Kitty"), Animal("Unknown")]
    for a in animals:
        print(a.intro())                   # polymorphism

    kitty = Cat("Kitty")
    print("kitty.indoor:", kitty.indoor)
    print("isinstance(kitty, Animal):", isinstance(kitty, Animal))
    print("issubclass(Cat, Animal):", issubclass(Cat, Animal))


def demo_encapsulation() -> None:
    class Account:
        def __init__(self, owner, balance):
            self.owner = owner
            self._balance = balance        # protected (a request)
            self.__pin = "1234"            # private (mangled)

        def get_balance(self):
            return self._balance

        def check_pin(self, pin):
            return pin == self.__pin

    acc = Account("Ravi", 500)
    print("owner:", acc.owner)
    print("balance (method):", acc.get_balance())
    print("_balance:", acc._balance)        # it works, but don't do it
    print("pin check:", acc.check_pin("1234"))

    try:
        print(acc.__pin)
    except AttributeError as e:
        print("AttributeError:", e)
    print("mangled name:", acc._Account__pin)   # technically possible


def demo_property() -> None:
    class Temperature:
        def __init__(self, celsius):
            self.celsius = celsius

        @property
        def celsius(self):
            return self._celsius

        @celsius.setter
        def celsius(self, value):
            if value < -273.15:
                raise ValueError("Cannot go below absolute zero")
            self._celsius = value

        @property
        def fahrenheit(self):
            return self._celsius * 9 / 5 + 32

    t = Temperature(25)
    print("C:", t.celsius, "| F:", t.fahrenheit)
    t.celsius = 30
    print("C:", t.celsius, "| F:", t.fahrenheit)

    try:
        t.celsius = -300
    except ValueError as e:
        print("ValueError:", e)


def demo_dunder() -> None:
    class Vector:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __str__(self):
            return f"Vector({self.x}, {self.y})"

        def __repr__(self):
            return f"Vector(x={self.x}, y={self.y})"

        def __eq__(self, other):
            if not isinstance(other, Vector):
                return NotImplemented
            return self.x == other.x and self.y == other.y

        def __add__(self, other):
            return Vector(self.x + other.x, self.y + other.y)

        def __len__(self):
            return 2

    v1 = Vector(1, 2)
    v2 = Vector(3, 4)
    print("str:", str(v1))
    print("repr:", repr(v1))
    print("v1 + v2:", v1 + v2)
    print("v1 == Vector(1, 2):", v1 == Vector(1, 2))
    print("len(v1):", len(v1))


def demo_dataclass() -> None:
    @dataclass
    class Point:
        x: int
        y: int

        def distance_from_origin(self):
            return (self.x ** 2 + self.y ** 2) ** 0.5

    p = Point(3, 4)
    print("point:", p)
    print("distance:", p.distance_from_origin())
    print("equality:", p == Point(3, 4))


# ---------------------------------------------------------------------------
# EXERCISES - complete the classes yourself
# ---------------------------------------------------------------------------


class BankAccount:
    """Start with a balance.

    deposit(amount): add to the balance
    withdraw(amount): raise ValueError if amount > balance, otherwise subtract it
    """

    def __init__(self, balance=0):
        # TODO: set self.balance
        pass

    def deposit(self, amount):
        # TODO
        pass

    def withdraw(self, amount):
        # TODO
        pass


class Rectangle:
    """Take a width and a height.

    area() -> width * height
    perimeter() -> 2 * (width + height)
    is_square() -> width == height (no need to use area)
    """

    def __init__(self, width, height):
        # TODO
        pass

    def area(self):
        # TODO
        pass

    def perimeter(self):
        # TODO
        pass

    def is_square(self):
        # TODO
        pass


class Student:
    """Take a name and a list of marks.

    average() -> average of the marks (0 if the list is empty)
    grade() -> A/B/C/D/F based on the average (90/75/60/40)
    """

    def __init__(self, name, marks):
        # TODO
        pass

    def average(self):
        # TODO
        pass

    def grade(self):
        # TODO
        pass


class Vector:
    """Take x and y. Implement __add__ and __eq__."""

    def __init__(self, x, y):
        # TODO
        pass

    def __add__(self, other):
        # TODO: return a new Vector
        pass

    def __eq__(self, other):
        # TODO
        pass


class Animal:
    def speak(self):
        return "..."


class Cat(Animal):
    """Override speak() and return 'Meow'."""

    def speak(self):
        # TODO
        pass


# Wrappers - you don't need to change these
def check_bank():
    acc = BankAccount(100)
    acc.deposit(50)
    acc.withdraw(30)
    return acc.balance


def check_bank_error():
    acc = BankAccount(50)
    try:
        acc.withdraw(100)
    except ValueError:
        return "ValueError"
    return "no error"


def check_rectangle():
    r = Rectangle(4, 5)
    return (r.area(), r.perimeter(), r.is_square())


def check_student():
    s = Student("Ravi", [90, 80, 70])
    return (s.average(), s.grade())


def check_vector():
    v = Vector(1, 2) + Vector(3, 4)
    return (v.x, v.y, Vector(1, 2) == Vector(1, 2))


def check_cat():
    return (Animal().speak(), Cat().speak())


# Solutions
class SolBankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Not enough balance")
        self.balance -= amount


class SolRectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def is_square(self):
        return self.width == self.height


class SolStudent:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def average(self):
        return sum(self.marks) / len(self.marks) if self.marks else 0

    def grade(self):
        avg = self.average()
        if avg >= 90:
            return "A"
        elif avg >= 75:
            return "B"
        elif avg >= 60:
            return "C"
        elif avg >= 40:
            return "D"
        return "F"


class SolVector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return SolVector(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return isinstance(other, SolVector) and self.x == other.x and self.y == other.y


class SolCat(Animal):
    def speak(self):
        return "Meow"


# Separate wrappers to test the solutions
def sol_check_bank():
    acc = SolBankAccount(100)
    acc.deposit(50)
    acc.withdraw(30)
    return acc.balance


def sol_check_bank_error():
    acc = SolBankAccount(50)
    try:
        acc.withdraw(100)
    except ValueError:
        return "ValueError"
    return "no error"


def sol_check_rectangle():
    r = SolRectangle(4, 5)
    return (r.area(), r.perimeter(), r.is_square())


def sol_check_student():
    s = SolStudent("Ravi", [90, 80, 70])
    return (s.average(), s.grade())


def sol_check_vector():
    v = SolVector(1, 2) + SolVector(3, 4)
    return (v.x, v.y, SolVector(1, 2) == SolVector(1, 2))


def sol_check_cat():
    return (Animal().speak(), SolCat().speak())


EXERCISES = [
    {"id": "14.1", "task": "BankAccount: balance is 120 after deposit/withdraw",
     "func": check_bank, "tests": [((), 120)], "solution": sol_check_bank,
     "starter_name": "BankAccount", "solution_name": "SolBankAccount"},
    {"id": "14.2", "task": "BankAccount: ValueError when withdrawing too much",
     "func": check_bank_error, "tests": [((), "ValueError")], "solution": sol_check_bank_error,
     "starter_name": "BankAccount", "solution_name": "SolBankAccount"},
    {"id": "14.3", "task": "Rectangle(4,5): area, perimeter, is_square",
     "func": check_rectangle, "tests": [((), (20, 18, False))], "solution": sol_check_rectangle,
     "starter_name": "Rectangle", "solution_name": "SolRectangle"},
    {"id": "14.4", "task": "Student average and grade",
     "func": check_student, "tests": [((), (80.0, "B"))], "solution": sol_check_student,
     "starter_name": "Student", "solution_name": "SolStudent"},
    {"id": "14.5", "task": "Vector __add__ and __eq__",
     "func": check_vector, "tests": [((), (4, 6, True))], "solution": sol_check_vector,
     "starter_name": "Vector", "solution_name": "SolVector"},
    {"id": "14.6", "task": "Cat(Animal): override speak()",
     "func": check_cat, "tests": [((), ("...", "Meow"))], "solution": sol_check_cat,
     "starter_name": "Cat", "solution_name": "SolCat"},
]

DEMOS = [
    ("14. Class basics", demo_class_basics),
    ("15. Inheritance and polymorphism", demo_inheritance),
    ("16. Encapsulation", demo_encapsulation),
    ("17. property", demo_property),
    ("18. Dunder methods", demo_dunder),
    ("19. dataclass", demo_dataclass),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
