class Chemistry():
    def __init__(self, known=None, X='NaCl'):
        self.GT, self.KL, self.EQ = self.create_rule()
        self.known = known.copy()
        self.known_forward = known.copy()
        self.result = X
        self.X = X
        self.BW = []
        pass

    def create_rule(self):
        GT = {
            '1': ['H2O'],
            '2': ['S', 'O2'],
            '3': ['SO2', 'O2', 'H2O'],
            '4': ['NaCl'],
            '5': ['NaCl', 'H2O'],
            '6': ['NaOH', 'H2SO4'],
            '7': ['Cl2', 'H2O'],
            '8': ['Na', 'Cl2'],
            '9': ['Fe', 'Cl2'],
            '10': ['Cu', 'Cl2'],
            '11': ['MnO2', 'HCl'],
            '12': ['HCl', 'KMnO4'],
            '13': ['K', 'Cl2']
        }
        KL = {
            '1': ['H2', 'O2'],
            '2': ['SO2'],
            '3': ['H2SO4'],
            '4': ['Na', 'Cl2'],
            '5': ['NaOH', 'H2', 'Cl2'],
            '6': ['Na2SO4', 'H2O'],
            '7': ['HCl', 'HClO'],
            '8': ['NaCl'],
            '9': ['FeCl3'],
            '10': ['CuCl2'],
            '11': ['MnCl2', 'Cl2', 'H2O'],
            '12': ['KCl', 'MnCl2', 'Cl2', 'H2O'],
            '13': ['KCl']
        }

        EQ = {
            '1': '2H2O ---> 2H2 + O2',
            '2': 'S + O2 ---> SO2',
            '3': 'SO2 + O2 + H2O ---> H2SO4',
            '4': '2NaCl ---> 2Na + Cl2',
            '5': '2NaCl + 2H2O ---> 2NaOH + H2 + Cl2',
            '6': '2NaOH + H2SO4 ---> Na2SO4 + 2H2O',
            '7': 'Cl2 + H2O ---> HCl + HClO',
            '8': '2Na + Cl2 ---> 2NaCl',
            '9': '2Fe + 3Cl2 ---> 2FeCl3',
            '10': 'Cu + Cl2 ---> CuCl2',
            '11': 'MnO2 + 4HCl ---> MnCl2 + Cl2 + 2H2O',
            '12': '16HCl + 2KMnO4 ---> 2KCl + 2MnCl2 + 5Cl2 + 8H2O',
            '13': '2K + Cl2 ---> 2KCl'
        }
        return GT, KL, EQ

    def create_equation(self):
        pass

    def is_subset(self, A, B):
        if len(A) > len(B):
            return False
        else:
            for e in A:
                if e not in B:
                    return False
            return True

    def find_initial(self, A):
        ans = []
        for key in self.KL:
            if A in self.KL[key]:
                ans.append(key)
        return ans

    def forward(self):
        flag = True
        while flag:
            flag = False
            for key, value in self.GT.items():
                if self.is_subset(value, self.known_forward):
                    if not self.is_subset(self.KL[key], self.known_forward):
                        flag = True
                        self.known_forward += self.KL[key]

    def backward(self):
        if self.X in self.known:
            pass
        else:
            initial = self.find_initial(self.X)

            for key in initial:
                if self.GT[key] not in self.BW:
                    self.BW.append(self.GT[key])
                    for e in self.GT[key]:
                        if e == self.result:
                            break
                        self.X = e
                        self.backward()

    def write_chemical_equation(self):
        if len(self.BW) == 0:
            print('{} đã có!'.format(self.result))
        else:
            check = []
            for i in range(1, len(self.BW)+1):
                if self.BW[-i] not in check:
                    for key, value in self.GT.items():
                        if value == self.BW[-i]:
                            check.append(value)
                            if self.is_subset(self.GT[key], self.known_forward):
                                print(self.EQ[key])
            print("Từ các phản ứng hóa học trên. Ta đã điều chế được {}.".format(self.result))

    def run(self):
        self.forward()
        if self.result not in self.known_forward:
            print("Không thể điều chế {}!".format(self.result))
        else:
            self.backward()
            self.write_chemical_equation()


if __name__ == '__main__':
    n = int(input("> Nhập số lượng chất đã có: "))
    print("> Nhập các chất đã có: ")
    known = [input("> ") for _ in range(n)]
    while True:
        print("Từ các chất đã có gồm: {}.".format(', '.join(known)))
        X = input("> Nhập vào chất cần điều chế: ")
        C = Chemistry(known=known, X=X)
        C.run()
        print("Nhập 'continue' để điều chế tiếp")
        tieptuc = input('> ')
        if tieptuc != 'continue':
            break