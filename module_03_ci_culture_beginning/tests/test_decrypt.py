import unittest
from module_03_ci_culture_beginning.homework.hw2.decrypt import decrypt


class TestDecrypt(unittest.TestCase):
    crypt: list = [
        ('абра-кадабра.', 'абра-кадабра'),
        ('абраа..-кадабра', 'абра-кадабра'),
        ('абраа..-.кадабра', 'абра-кадабра'),
        ('абра--..кадабра', 'абра-кадабра'),
        ('абраа..-.кадабра', 'абра-кадабра'),
        ('абра--..кадабра', 'абра-кадабра'),
        ('абрау...-кадабра', 'абра-кадабра'),
        ('абра........', ''),
        ('абр......a.', 'a'),
        ('1..2.3', '23'), ('.', ''),
        ('1.......................', '')
    ]

    def test_decrypt_dot(self):
        crypt_group: list = sorted(self.crypt, key=lambda x: x[0].count('.'))
        for crypt_tuple in crypt_group:
            crypt_text, true_result = crypt_tuple
            with self.subTest(crypt_text=crypt_text):
                result: str = decrypt(crypt_text)
                self.assertEqual(result, true_result)


if __name__ == '__main__':
    unittest.main()
