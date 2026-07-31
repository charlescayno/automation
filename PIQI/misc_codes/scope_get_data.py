from equipment_settings import *
scope = Oscilloscope(EQUIPMENT_ADDRESS.SCOPE)

def main():
    scope.run_single()

if __name__ == "__main__":
    main()