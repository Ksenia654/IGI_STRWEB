import os
import importlib
#import time

shape = os.getenv("SHAPE", "circle").lower()
size = os.getenv("SIZE", "10")

available_shapes = ["circle", "square"]

if shape not in available_shapes:
    print(f"Error: Shape '{shape}' not supported. Available: {available_shapes}")
    exit(1)

module = importlib.import_module(f"geometric_lib.{shape}")

area = module.area(float(size))
perimeter = module.perimeter(float(size))

print(f"Figure: {shape}")
print(f"Size: {size}")
print(f"Square: {area}")
print(f"Perimeter: {perimeter}")

#time.sleep(3600)