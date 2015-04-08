import random
import sys
 
class multiplicationMatrix:


    def generateMatrix(self, lines, rows):
        self.lines = lines
        self.rows = rows
        self.createdMatrix = []
        self.intermediateMatrix = []
        for line in range(int(self.lines)):
            for row in range(int(self.rows)):
                self.intermediateMatrix.append(random.randint(1,10))
            self.createdMatrix.append(self.intermediateMatrix)
            self.intermediateMatrix = []
        return self.createdMatrix


    def multiplicationMatrix(self, matrix_A, matrix_B):
        self.summ = 0
        self.intermediateMatrix = []
        self.finiteMatrix = []
        if len(matrix_B) != len(matrix_A):
            print("Невозможно перемножить данные матрицы. Повторите ввод.")
            sys.exit()
        else:
            self.matrix_A_lines = len(matrix_A)
            self.matrix_A_rows = len(matrix_A[0])
            self.matrix_B_lines = self.matrix_A_rows
            self.matrix_B_rows = len(matrix_B[0])
            for x in range(int(self.matrix_A_lines)):
                for y in range(int(self.matrix_B_rows)):
                    for z in range(int(self.matrix_A_rows)):
                        self.summ += matrix_A[x][z] * matrix_B[z][y]
                    self.intermediateMatrix.append(self.summ)
                    self.summ = 0
                self.finiteMatrix.append(self.intermediateMatrix)
                self.intermediateMatrix = []
        return self.finiteMatrix


def main():
    while True:
        try:
            linesA = input("Enter amount of lines of the first matrix: ")
            rowsA = input("Enter amount of rows of the first matrix: ")
            linesB = input("Enter amount of lines of the second matrix: ")
            rowsB = input("Enter amount of rows of the second matrix: ")
        

            matrixA = multiplicationMatrix().generateMatrix(linesA, rowsA)
            print("Матрица А: ", matrixA)
            matrixB = multiplicationMatrix().generateMatrix(linesB, rowsB)
            print("Матрица В: ", matrixB)
            print("Итоговая матрица: ", multiplicationMatrix().multiplicationMatrix(matrixA, matrixB))
        except ValueError:
            print("Неверно введены значения. Повторите ввод.")

if __name__ == '__main__':
    main()
