### Результаты Запросов

1. #### Телефоны какого цвета чаще всего покупают?
     ```
    SELECT 
        tp.colour AS colour_phone,
        COUNT(tp.name) AS sell_off
    FROM
        `table_phones` AS tp
    JOIN 
        `table_checkout` AS ts ON 
        tp.id = ts.phone_id
    GROUP BY colour_phone
    ORDER BY sell_off  DESC
    LIMIT 1;
    ```
    В результате получаем список проданных телефонов за весь период отсортированный по цвету.
    Выполняем `JOIN` запрос где `phone_id` из таблицы `table_checkout` будет объединён с таблицей `table_pthone` по `id`. 
    Затем телефоны будут сгруппированы по цветам И отсортированы по убыванию. И в конце результат будет ограничен лимитов в 
    одну запись с полями `colour_phone` & `sell_off`.<br>
    В результате будет получено:
    > `cиний	500`

2. #### Какие телефоны чаще покупают: красные или синие?
    
    ```
    SELECT 
        tp.colour AS colour_phone,
        COUNT(tp.name) AS sell_off
    FROM
        `table_phones` AS tp
    JOIN 
        `table_checkout` AS ts ON 
        tp.id = ts.phone_id
    WHERE 
        colour_phone IN ('синий', 'красный')
    GROUP BY colour_phone
    ORDER BY sell_off;
    
    ```
    Используем добавлен фильтр `WHERE`
    Благодаря данному фильтру мы получаем интересующие нас объекты для сравнения, по итогу которого предоставляются 
    красные и синие телефоны.<br>
    В результате будет получено:
    > `красный	429` <br>
    `синий	500`
   
3. #### Какой самый непопулярный цвет телефона?
    ```
    SELECT 
        tp.colour AS colour_phone,
        COUNT(tp.name) AS sell_off
    FROM
        `table_phones` AS tp
    JOIN 
        `table_checkout` AS ts ON 
        tp.id = ts.phone_id
    GROUP BY colour_phone
    ORDER BY sell_off
    LIMIT 1;
    ```
    Используем запрос аналогичный первому, за исключением использования `DESC`, тогда будет применена сортировка `ASC` как 
    сортировка по умолчанию.<br>
    В результате будет получено:
    > `золотой 28`