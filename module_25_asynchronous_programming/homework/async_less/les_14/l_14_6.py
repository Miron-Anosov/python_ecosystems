from typing import Generator


def generator(start: int, end: int):
    for i in range(start, end):
        yield i


one_to_five = generator(1, 5)
five_to_ten = generator(5, 10)


def run_generator_step(gen: Generator[int, None, None]):
    try:
        return gen.send(None)
    except StopIteration as si:
        return si.value


while True:
    one_to_five_result = run_generator_step(one_to_five)
    five_to_ten_result = run_generator_step(five_to_ten)
    print(one_to_five_result)
    print(five_to_ten_result)

    if one_to_five_result is None and five_to_ten_result is None:
        break


"""
Здесь мы написали простой генератор, который проходит через диапазон целых чисел от начального до конечного значения, 
отдавая по дороге каждое число. Затем создаем два экземпляра этого генератора: один для диапазона от одного до четырех, 
а другой от пяти до девяти.
Мы также написали вспомогательную функцию `run_generator_step`, которая выполняет один шаг генератора. 
В классе генератора есть метод `send`, который продвигает генератор к следующему `yield`, выполняя весь 
промежуточный код. После вызова `send` можно быть уверенным, что генератор приостановлен до следующего вызова `send`, 
что позволяет выполнить код в других генераторах. Метод `send` принимает параметр, равный значению, которое мы хотим 
передать генератору в качестве аргумента. В данном случае мы не передаем ничего, поэтому параметр равен `None`. 
Когда генератор достигает конца, возникает исключение `StopIteration`. Это исключение содержит значение, 
возвращенное итератором, и мы его обрабатываем. Наконец, мы запускаем оба генератора в бесконечном цикле.
"""
