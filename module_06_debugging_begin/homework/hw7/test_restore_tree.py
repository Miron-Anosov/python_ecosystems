import logging
import unittest
import os
from binary_tree_walk import walk, restore_tree, logger, BinaryTreeNode


class MyTestCase(unittest.TestCase):
    log_1 = os.path.abspath(os.path.join('walk_log_1.txt'))
    log_2 = os.path.abspath(os.path.join('walk_log_2.txt'))
    log_3 = os.path.abspath(os.path.join('walk_log_3.txt'))
    log_4 = os.path.abspath(os.path.join('walk_log_4.txt'))
    formatter = logging.Formatter("%(levelname)s:%(message)s")
    text_log_file = os.path.abspath(os.path.join("test_log.txt"))

    def tearDown(self):
        if os.path.exists(self.text_log_file):
            os.remove(self.text_log_file)

    def test_walk_log_1(self):
        """
        Текст проводит сверку результатов выполнения функции, которая воссоздает объект
        бинарного дерева. После воссоздания объекта запускается функция walk, которая в свою очередь обходит узлы
        и логирует все во временный файл test_log.txt. После чего будет построчно проверены результаты временного файла
        с файлом по которому был воссоздан объект walk_log_1.txt.
        """
        logger.setLevel(level=logging.DEBUG)
        fh = logging.FileHandler(filename='test_log.txt', mode='w', encoding='UTF-8')
        fh.setFormatter(fmt=self.formatter)
        fh.setLevel(level=logging.DEBUG)
        logger.addHandler(fh)
        tree: BinaryTreeNode = restore_tree(path_to_log_file=self.log_1)
        walk(tree)
        logger.removeHandler(fh)
        with (open(file=self.log_1, mode='r', encoding="UTF-8") as log_tue,
              open(file=self.text_log_file, mode='r', encoding="UTF-8") as log_test):
            for line_true, line_test in zip(log_tue, log_test):
                self.assertEqual(line_true, line_test)

    def test_walk_log_negative(self):
        """
        Тест проводит сверку с результатом функции, где результат не совпадает с логами.
        """
        logger.setLevel(level=logging.DEBUG)
        fh = logging.FileHandler(filename='test_log.txt', mode='w', encoding='UTF-8')
        fh.setFormatter(fmt=self.formatter)
        fh.setLevel(level=logging.DEBUG)
        logger.addHandler(fh)
        tree = restore_tree(path_to_log_file=self.log_1)
        walk(tree)
        logger.removeHandler(fh)
        with (open(file=self.log_2, mode='r', encoding="UTF-8") as log_tue,
              open(file=self.text_log_file, mode='r', encoding="UTF-8") as log_test):
            for line_true, line_test in zip(log_tue, log_test):
                self.assertNotEqual(line_true, line_test)

    def test_walk_log_2(self):
        """
        Текст проводит сверку результатов выполнения функции, которая воссоздает объект
        бинарного дерева. После воссоздания объекта запускается функция walk, которая в свою очередь обходит узлы
        и логирует все во временный файл test_log.txt. После чего будет построчно проверены результаты временного файла
        с файлом по которому был воссоздан объект walk_log_2.txt.
        """
        logger.setLevel(level=logging.DEBUG)
        fh = logging.FileHandler(filename='test_log.txt', mode='w', encoding='UTF-8')
        fh.setFormatter(fmt=self.formatter)
        fh.setLevel(level=logging.DEBUG)
        logger.addHandler(fh)
        tree = restore_tree(path_to_log_file=self.log_2)
        walk(tree)
        logger.removeHandler(fh)
        with (open(file=self.log_2, mode='r', encoding="UTF-8") as log_tue,
              open(file=self.text_log_file, mode='r', encoding="UTF-8") as log_test):
            for line_true, line_test in zip(log_tue, log_test):
                self.assertEqual(line_true, line_test)

    def test_walk_log_3(self):
        """
        Текст проводит сверку результатов выполнения функции, которая воссоздает объект
        бинарного дерева. После воссоздания объекта запускается функция walk, которая в свою очередь обходит узлы
        и логирует все во временный файл test_log.txt. После чего будет построчно проверены результаты временного файла
        с файлом по которому был воссоздан объект walk_log_3.txt.
        """
        logger.setLevel(level=logging.DEBUG)
        fh = logging.FileHandler(filename='test_log.txt', mode='w', encoding='UTF-8')
        fh.setFormatter(fmt=self.formatter)
        fh.setLevel(level=logging.DEBUG)
        logger.addHandler(fh)
        tree = restore_tree(path_to_log_file=self.log_3)
        walk(tree)
        logger.removeHandler(fh)
        with (open(file=self.log_3, mode='r', encoding="UTF-8") as log_tue,
              open(file=self.text_log_file, mode='r', encoding="UTF-8") as log_test):
            for line_true, line_test in zip(log_tue, log_test):
                self.assertEqual(line_true, line_test)

    def test_walk_log_4(self):
        """
        Текст проводит сверку результатов выполнения функции, которая воссоздает объект
        бинарного дерева. После воссоздания объекта запускается функция walk, которая в свою очередь обходит узлы
        и логирует все во временный файл test_log.txt. После чего будет построчно проверены результаты временного файла
        с файлом по которому был воссоздан объект walk_log_4.txt.
        """
        logger.setLevel(level=logging.DEBUG)
        fh = logging.FileHandler(filename='test_log.txt', mode='w', encoding='UTF-8')
        fh.setFormatter(fmt=self.formatter)
        fh.setLevel(level=logging.DEBUG)
        logger.addHandler(fh)
        tree = restore_tree(path_to_log_file=self.log_4)
        walk(tree)
        logger.removeHandler(fh)
        if os.path.exists(self.text_log_file):
            with (open(file=self.log_4, mode='r', encoding="UTF-8") as log_tue,
                  open(file=self.text_log_file, mode='r', encoding="UTF-8") as log_test):
                for line_true, line_test in zip(log_tue, log_test):
                    self.assertEqual(line_true, line_test)
        else:
            raise FileNotFoundError


if __name__ == '__main__':
    unittest.main()
