# Выполнили студенты группы 121703:
# Кочурко В. В. & Гапанович К. В.

class Formula:
    def __init__(self, str):
        self.string_f = str
        self.logic_const = ('0', '1',)
        self.lat_alph = (
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
            'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
            'U', 'V', 'W', 'X', 'Y', 'Z',)
        self.negation = '!'
        self.conjunction = '*'
        self.disjunction = '+'
        self.emplication = '@'
        self.equivalent = '~'
        self.open_bracket = '('
        self.close_brack = ')'
        self._brackets = (self.open_bracket, self.close_brack,)
        self._operations = (self.conjunction, self.disjunction, self.emplication, self.equivalent, self.negation,)
        self._operations_for_check = (self.conjunction, self.disjunction, self.emplication, self.equivalent,)
        self._all_symbols = (*self.lat_alph, *self._brackets, *self._operations,)

    def find_parens(self) -> dict[int:[int, int]]:
        dict_ind_bracket = {}
        bracket_stack, operation_stack = [], []
        for ind, alph in enumerate(self.string_f):
            if alph == '(':
                bracket_stack.append(ind)
                dict_ind_bracket.setdefault(ind, [])
            if alph in self._operations:
                operation_stack.append(ind)
            elif alph == ')':
                if len(bracket_stack) == 0 or len(operation_stack) == 0:
                    return False
                dict_ind_bracket[bracket_stack.pop()].extend([ind, operation_stack.pop()])
        if len(bracket_stack) > 0 or len(operation_stack) > 0:
            return False
        return dict_ind_bracket

    def main(self):
        if self.init_replace(self.string_f) != False:
            self.string_f = self.init_replace(self.string_f)
        else:
            return False
        if self.check_symbols == False or self.check_empty() == False:
                return False
        if not self.atomic_formula(self.string_f):
            if self.find_parens() != False:
                dict_ind_brackets = self.find_parens()
            else:
                return False
            if self.main_brackets() and self.check_dict(dict_ind_brackets):
                if self.check_num_operation(dict_ind_brackets) == False:
                    return False
                check_rule = []
                for key in dict_ind_brackets:
                    try:
                        ind_operation = dict_ind_brackets[key][1]
                        operation = self.string_f[ind_operation]
                        r_alph, l_alph = self.string_f[ind_operation + 1], self.string_f[ind_operation - 1]
                        r_alph_second, l_alph_second = self.string_f[ind_operation + 2], self.string_f[ind_operation - 2]

                        if l_alph == self.open_bracket and \
                                 r_alph == self.open_bracket \
                                and operation == self.negation:
                            check_rule.append(True)
                            continue

                        if (l_alph in self.lat_alph or l_alph in self.logic_const) \
                                and (r_alph in self.lat_alph or r_alph in self.logic_const) \
                                and r_alph_second == self.close_brack and \
                                    l_alph_second == self.open_bracket \
                                and operation in self._operations_for_check:
                            check_rule.append(True)
                            continue

                        if l_alph == self.open_bracket \
                                and (r_alph in self.lat_alph or r_alph in self.logic_const) \
                                and operation == self.negation:
                            check_rule.append(True)
                            continue

                        if (l_alph in self.lat_alph or l_alph in self.logic_const) \
                                and r_alph == self.open_bracket \
                                and l_alph_second == self.open_bracket and \
                                    operation in self._operations_for_check:
                            check_rule.append(True)
                            continue

                        if (r_alph in self.lat_alph or r_alph in self.logic_const) \
                                and l_alph == self.close_brack \
                                and r_alph_second == self.close_brack and operation in self._operations_for_check:
                            check_rule.append(True)
                            continue

                        if l_alph == self.close_brack and r_alph == self.open_bracket \
                                and operation in self._operations_for_check:
                            check_rule.append(True)
                            continue
          
                    except IndexError:
                        return False
                if len(dict_ind_brackets) != len(check_rule):
                    return False
            else:
                return False
        return True


    def check_num_operation(self, dict_: dict):
        for key in dict_:
            sub_formula = self.string_f[key: dict_[key][0] + 1]
            operation = 0
            depth = 0
            for ind, alph in enumerate(sub_formula):
                if alph == self.open_bracket and ind != 0:
                    depth += 1
                if alph == self.close_brack and ind != len(sub_formula):
                    depth -= 1
                if depth == 0 and alph in self._operations:
                    operation += 1
                if operation > 1:
                    return False

    def check_symbols(self):
        for symbol in self.string_f:
            if symbol not in self._all_symbols:
                return False

    def atomic_formula(self, valid_string: str) -> bool:
        return True if (valid_string in self.lat_alph or \
            valid_string in self.logic_const) and \
            len(valid_string) == 1 else False

    def main_brackets(self) -> bool:
        return True if self.string_f[0] == self.open_bracket and self.string_f[-1] == self.close_brack else False

    def check_empty(self) -> bool:
        if self.string_f == "" or self.string_f.isspace():
            return False

    @staticmethod
    def check_dict(dict_: dict[int: [int, int]]) -> bool:
        for key in dict_:
            if dict_[key][1] < key or dict_[key][1] > dict_[key][0]:
                return False
        return True

#(A\/\A) (A/\/A)

    @staticmethod
    def init_replace(inp_str: str) -> str:
        if inp_str.__contains__("*") or inp_str.__contains__('+') or inp_str.__contains__('@'):
            return False
        
        inp_str = inp_str.replace('\/', '+')
        
        inp_str = inp_str.replace('/\\', '*')
        
        inp_str = inp_str.replace('->', '@')
        
        return inp_str