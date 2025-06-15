print("Hello World")
def greet(name):
    return f"Hello {name}"

print(greet("Abenezer"))

def greeting(name):
    print(f"Hi {name}")

print(greeting("Abenezer"))

# The latter function return None after giving the message cause any function will return None unless
# We define what the function can return

# Optional Parameters
def greetop(name, age=20, course="python"):
    #age = input("Enter your age: ")
    return f"Hello this is {name} who is {age} years old and learning {course}"

print(greetop("Abenezer"))

# Local and global variables
x = 10
def increasex():
    global x # when defining a variable this is the most important thing if we are defining when we are changing the variable that is already defined outside the function
    x += 1
    return x

print(increasex())