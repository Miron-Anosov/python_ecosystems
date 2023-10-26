import unittest
from redirect import Redirect


class TestRedirect(unittest.TestCase):

    def test_stdout_and_stderr(self) -> None:
        """
        Тест перехватывает оба потока и записывает перехваченные данные в stderr.txt и stdout.txt.
        """
        stdout_text = 'stdout text'
        stderr_text = 'stderr text'
        with open('stdout.txt', 'w', encoding='utf-8') as file_out, open('stderr.txt', 'w',
                                                                         encoding='utf-8') as file_err:
            with Redirect(stdout=file_out, stderr=file_err):
                print(stdout_text)
                raise Exception(stderr_text)

        with open('stdout.txt', 'r', encoding='utf-8') as content_out, open('stderr.txt', 'r',
                                                                            encoding='utf-8') as content_err:
            stdout = content_out.read()
            stderr = content_err.read()

        self.assertTrue(stdout_text in stdout)
        self.assertTrue(stderr_text in stderr)

    def test_stdout_only(self) -> None:
        """
        Тест перехватывает только stdout поток и записывает перехваченные данные в stdout.txt. При этом stderr.txt будет
        пустым, так как сообщение не перехватывается.
        """
        stdout_text = 'stdout text'
        stderr_text = ''
        with self.assertRaises(Exception):
            with open('stdout.txt', 'w', encoding='utf-8') as file_out, open('stderr.txt', 'w',
                                                                             encoding='utf-8') as file_err:
                with Redirect(stdout=file_out):
                    print(stdout_text)
                    raise Exception(stderr_text)
        with open('stdout.txt', 'r', encoding='utf-8') as content_out, open('stderr.txt', 'r',
                                                                            encoding='utf-8') as content_err:
            stdout = content_out.read()
            stderr = content_err.read()
        self.assertTrue(stdout_text in stdout)
        self.assertEqual(stderr_text, stderr)

    def test_stderr_stdout_turn_off(self) -> None:
        """
        Тест не перехватывает потоки. При этом stdout.txt и stderr.txt будет
        пустым, так как сообщения не перехватываются.
        """
        stdout_text = 'stdout text'
        stderr_text = 'stderr text'
        with self.assertRaises(Exception):
            with open('stdout.txt', 'w', encoding='utf-8') as file_out, open('stderr.txt', 'w',
                                                                             encoding='utf-8') as file_err:
                with Redirect():
                    print(stdout_text)
                    raise Exception(stderr_text)
        with open('stdout.txt', 'r', encoding='utf-8') as content_out, open('stderr.txt', 'r',
                                                                            encoding='utf-8') as content_err:
            stdout = content_out.read()
            stderr = content_err.read()
        self.assertFalse(stderr_text in stderr)
        self.assertFalse(stdout_text in stdout)

    def test_stderr_only(self) -> None:
        """
        Тест перехватывает только stderr поток и записывает перехваченные данные в stderr.txt. При этом stdout.txt будет
        пустым, так как сообщение не перехватывается.
        """
        stdout_text = ''
        stderr_text = 'stderr text'
        with open('stdout.txt', 'w', encoding='utf-8') as file_out, open('stderr.txt', 'w',
                                                                         encoding='utf-8') as file_err:
            with Redirect(stderr=file_err):
                print(stdout_text)
                raise Exception(stderr_text)
        with open('stdout.txt', 'r', encoding='utf-8') as content_out, open('stderr.txt', 'r',
                                                                            encoding='utf-8') as content_err:
            stdout = content_out.read()
            stderr = content_err.read()
        self.assertTrue(stderr_text in stderr)
        self.assertEqual(stdout_text, stdout)


if __name__ == '__main__':
    unittest.main()
    # with open('test_results.txt', 'a') as test_file_stream:
    #     runner = unittest.TextTestRunner(stream=test_file_stream)
    #     unittest.main(testRunner=runner)
