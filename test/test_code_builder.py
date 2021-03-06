import unittest

from interpreter.CodeBuilder import build_code
import test_scripts.scripts_recursion as test_rec


class TestExpression(unittest.TestCase):
    def test_expression(self):
        script = """
                    $a = 1 + 1 * 2 + (1 + 1)       
                """
        result, dm = build_code(script)
        self.assertEqual(('PUSH', 'CONSTANT', 1), result[0])
        self.assertEqual(('PUSH', 'CONSTANT', 1), result[1])
        self.assertEqual(('PUSH', 'CONSTANT', 2), result[2])
        self.assertEqual(('MULT',), result[3])
        self.assertEqual(('ADD',), result[4])
        self.assertEqual(('PUSH', 'CONSTANT', 1), result[5])
        self.assertEqual(('PUSH', 'CONSTANT', 1), result[6])
        self.assertEqual(('ADD',), result[7])
        self.assertEqual(('ADD',), result[8])
        pass


class TestAssignment(unittest.TestCase):
    def test_assignment(self):
        script = """
            $a = 1
            $b = 2          
        """
        result, dm = build_code(script)
        self.assertEqual(('PUSH', 'CONSTANT', 1), result[0])
        self.assertEqual(('POP', 'ID', '$a'), result[1])
        self.assertEqual(('PUSH', 'CONSTANT', 2), result[2])
        self.assertEqual(('POP', 'ID', '$b'), result[3])


class TestBranching(unittest.TestCase):
    def test_full_branch(self):
        script = """
                    if $a < 3 {
                        $a = 3
                    } elif $b < 4 {
                        $b = 4
                    } elif $c < 5 {
                        $c = 5
                    } else {
                        $d = 6
                    }
                """
        result, dm = build_code(script)

        correct_code = [
            ('PUSH', 'ID', '$a'),
            ('PUSH', 'CONSTANT', 3),
            ('LT',),
            ('JUMPNOT', '#endif-3'),
            ('PUSH', 'CONSTANT', 3),
            ('POP', 'ID', '$a'),
            ('JUMP', '#end-branch-7'),
            ('LABEL', '#endif-3'),
            ('PUSH', 'ID', '$b'),
            ('PUSH', 'CONSTANT', 4),
            ('LT',),
            ('JUMPNOT', '#endelif-11'),
            ('PUSH', 'CONSTANT', 4),
            ('POP', 'ID', '$b'),
            ('JUMP', '#end-branch-7'),
            ('LABEL', '#endelif-11'),
            ('PUSH', 'ID', '$c'),
            ('PUSH', 'CONSTANT', 5),
            ('LT',),
            ('JUMPNOT', '#endelif-19'),
            ('PUSH', 'CONSTANT', 5),
            ('POP', 'ID', '$c'),
            ('JUMP', '#end-branch-7'),
            ('LABEL', '#endelif-19'),
            ('PUSH', 'CONSTANT', 6),
            ('POP', 'ID', '$d'),
            ('LABEL', '#end-branch-7'),
        ]

        for c, t in zip(result, correct_code):
            self.assertEqual(t, c)


class TestLoop(unittest.TestCase):
    def test_while(self):
        script = """
                    while $i < 3 {
                        $i = $i + 1
                    }
                        """
        result, dm = build_code(script)

    def test_repeat(self):
        script = """
                    repeat 20 {
                        $i = $i + 1
                    }
                """
        result, dm = build_code(script)
        # for i, c in zip(range(len(result)), result):
        #     print(f'{i} : {c}')

    def test_for(self):
        script = """
                    for $i = 0 to 10 {
                        $i = $i + 1
                    }
                """
        result, dm = build_code(script)
        # for i, c in zip(range(len(result)), result):
        #     print(f'{i} : {c}')


class TestFunction(unittest.TestCase):
    def test_function(self):
        script = """
                    $a = add(1 + 1, 2)
                    print($b)
                """
        result, dm = build_code(script)
        # for i, c in zip(range(len(result)), result):
        #     print(f'{i} : {c}')
        pass


class TestLearn(unittest.TestCase):
    def test_learn(self):
        script = """
                    learn test $i, $b {
                        $i = 1 + 1
                        $b = 2 
                        $c = 3                      
                    }

                    $i = 0
                """
        result, dm = build_code(script)

        # for i, c in zip(range(len(result)), result):
        #     print(f'{i} : {c}')

        pass

    def test_learn_call(self):
        script = """
                    learn add $a, $b {
                        return $a + $b                  
                    }

                    $i = add(1, 2)
                """
        result, dm = build_code(script)
        # for i, c in zip(range(len(result)), result):
        #     print(f'{i} : {c}')
        # pass


class TestComplexCode(unittest.TestCase):
    def test_complex1(self):
        script = """
                learn add $a, $b {
                    return $a + $b                  
                }

                $a = 1
                $b = 2
                print(add($a, $b))

                    """
        result, dm = build_code(script)
        # for i, c in zip(range(len(result)), result):
        #     print(f'{i} : {c}')
        # pass

    def test_recursion(self):
        result, dm = build_code(test_rec.rec1)

        self.assertEqual(1, len(dm['fac'][2]))
        # for i, c in zip(range(len(result)), result):
        #     print(f'{i} : {c}')
        # pass
        pass


if __name__ == '__main__':
    unittest.main()
