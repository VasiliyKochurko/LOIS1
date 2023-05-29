from Formula import *


if __name__ == "__main__":
    while True:
        inp_formula = input("Введите формулу: ")
        a = Formula(inp_formula)
        if a.main():
            print("Верный ввод")
        else:
            print("Error!")