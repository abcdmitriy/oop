class Polynomial:
    def __init__(self, koff):  # инициализатор
        self.koff = koff

    def __add__(self, other):  # сумма
        max_len = max(len(self.koff), len(other.koff))
        nov_koff = [0] * max_len
        self_koff = self.koff[::-1]
        other_koff = other.koff[::-1]

        for i in range(max_len):
            koff_1 = self_koff[i] if i < len(self_koff) else 0
            koff_2 = other_koff[i] if i < len(other_koff) else 0
            nov_koff[i] = koff_1 + koff_2

        return Polynomial(nov_koff[::-1])

    def __sub__(self, other):  # разность
        max_len = max(len(self.koff), len(other.koff))
        nov_koff = [0] * max_len
        self_koff = self.koff[::-1]
        other_koff = other.koff[::-1]

        for i in range(max_len):
            koff_1 = self_koff[i] if i < len(self_koff) else 0
            koff_2 = other_koff[i] if i < len(other_koff) else 0
            nov_koff[i] = koff_1 - koff_2

        return Polynomial(nov_koff[::-1])

    def __mul__(self, other):  # умножение
        new_koff = [0] * (len(self.koff) + len(other.koff) - 1)
        for i in range(len(self.koff)):
            coeff1 = self.koff[i]
            for j in range(len(other.koff)):
                coeff2 = other.koff[j]
                new_koff[i + j] += coeff1 * coeff2

        return Polynomial(new_koff)

    def __truediv__(self, other):
        if len(other.koff) == 0 or (len(other.koff) == 1 and other.koff[0] == 0):
            return Polynomial([])

        if len(other.koff) > len(self.koff):
            return Polynomial([])

        dividend = self.koff[:]
        divisor = other.koff
        quotient = []

        while len(dividend) >= len(divisor):
            lead_coeff = dividend[0] / divisor[0]  # Находим коэффициент для текущего члена частного
            quotient.append(lead_coeff)

            # Вычитаем произведение делителя на текущий член частного из делимого
            for i in range(len(divisor)):
                dividend[i] -= lead_coeff * divisor[i]
            dividend.pop(0)  # удаляем старший нулевой коэффициент

        # Проверяем остался ли остаток
        if any(coef != 0 for coef in dividend):  # остаток - dividend
            # print('остаток', dividend)
            return Polynomial([0])
        else:
            return Polynomial(quotient)

    def get_show(self):
        show = ''
        if self.koff is not None:
            for i in range(len(self.koff)):
                koff_n = self.koff[i]
                if koff_n != 0:
                    top = len(self.koff) - i - 1
                    show += f"{koff_n}x^{top} + "
            show = show[:-3]
        else:
            return "Коэффициенты отсутствуют"
        return show

    def get_file(self, file_name):
        show = self.get_show()
        with open(file_name, 'w') as file:
            file.write(show)

    def get_proiz(self):
        koff_pr = []
        length = len(self.koff)

        for i in range(length):
            if length - 1 - i > 0:
                koff_pr.append(self.koff[i] * (length - 1 - i))

        proiz = Polynomial(koff_pr)
        return proiz.get_show()

    def get_point(self, point: float):
        value = 0.0
        for i in range(len(self.koff)):
            koff_n = self.koff[i]
            if koff_n != 0:
                top = len(self.koff) - i - 1
                value += koff_n * point ** top
        return value

    def get_zero(self):
        def find_divisors(na):
            divisors = []
            for i in range(1, na + 1):
                if na % i == 0:
                    divisors.append(i)
            return divisors

        a_0 = self.koff[-1]
        a_n = self.koff[0]
        if a_0 < 0:
            a_0 = -a_0
        if a_n < 0:
            a_n = -a_n
        a_0_koff = find_divisors(a_0)  # q
        a_n_koff = find_divisors(a_n)  # p

        zero = []
        list_x = []

        for p in a_0_koff:
            for q in a_n_koff:
                list_x.append(p / q)
                list_x.append(-p / q)

        list_x_sort = sorted(set(list_x))

        for x in list_x_sort:
            result = self.get_point(float(x))
            if abs(result) < 0.000000001:
                zero.append(float(round(x, 4)))

        return zero

    def get_factor(self):
        zero = self.get_zero()
        kok = Polynomial(self.koff)
        decay = []

        for root in zero:
            decay.append([1.0, -root])

        for factor in decay:
            kok /= Polynomial(factor)

        if kok.koff == [1.0]:
            return decay
        else:
            decay.append(kok.koff)
            return decay

    def get_nod(self, other):
        n1 = Polynomial(self.koff)
        n2 = Polynomial(other.koff)

        factors1 = n1.get_factor()
        factors2 = n2.get_factor()

        common_factors = []

        for factor1 in factors1:
            if factor1 in factors2:
                common_factors.append(factor1)

        if not common_factors:
            return Polynomial([0])

        n_n = Polynomial([1])

        for factor in common_factors:
            n_n *= Polynomial(factor)

        return n_n.get_show()


k = Polynomial([1, 1, 12, -14])
n = Polynomial([1, 0, 10, -28])
l = n + k
filename = "чупапи.txt"
k.get_file(filename)

print(k.get_show())
print(n.get_show())

print(k.get_zero())
print(n.get_zero())

print(k.get_factor())
print(n.get_factor())

print(k.get_nod(n))



