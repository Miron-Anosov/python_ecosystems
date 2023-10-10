from decrypt import decrypt
import unittest


class TestDecrypt(unittest.TestCase):

    def test_decrypt_true_result(self):
        text = 'абра-кадабра'
        result = decrypt(text)
        true_result = 'абра-кадабра'
        self.assertEqual(true_result, result)

    def test_decrypt_1(self):
        text = 'абра-кадабра.'
        result = decrypt(text)
        true_result = 'абра-кадабра'
        self.assertEqual(true_result, result)

    def test_decrypt_2(self):
        text = 'абраа..-кадабра'
        result = decrypt(text)
        true_result = 'абра-кадабра'
        self.assertEqual(true_result, result)

    def test_decrypt_3(self):
        text = 'абраа..-.кадабра'
        result = decrypt(text)
        true_result = 'абра-кадабра'
        self.assertEqual(true_result, result)

    def test_decrypt_4(self):
        text = 'абра--..кадабра'
        result = decrypt(text)
        true_result = 'абра-кадабра'
        self.assertEqual(true_result, result)

    def test_decrypt_5(self):
        text = 'абрау...-кадабра'
        result = decrypt(text)
        true_result = 'абра-кадабра'
        self.assertEqual(true_result, result)

    def test_decrypt_6(self):
        text = 'абра........'
        result = decrypt(text)
        true_result = ''
        self.assertEqual(true_result, result)

    def test_decrypt_7(self):
        text = 'абр......a.'
        result = decrypt(text)
        true_result = 'a'
        self.assertEqual(true_result, result)

    def test_decrypt_8(self):
        text = '1..2.3'
        result = decrypt(text)
        true_result = '23'
        self.assertEqual(true_result, result)

    def test_decrypt_9(self):
        text = '.'
        result = decrypt(text)
        true_result = ''
        self.assertEqual(true_result, result)

    def test_decrypt_10(self):
        text = '1.......................'
        result = decrypt(text)
        true_result = ''
        self.assertEqual(true_result, result)

    def test_decrypt_11(self):
        text = '............ ...........'
        result = decrypt(text)
        true_result = ''
        self.assertEqual(true_result, result)

    def test_decrypt_12(self):
        text = '.......................1'
        result = decrypt(text)
        true_result = '1'
        self.assertEqual(true_result, result)

    def test_decrypt_13(self):
        text = '......-  -...............'
        result = decrypt(text)
        true_result = ''
        self.assertEqual(true_result, result)


if __name__ == '__main__':
    unittest.main()
