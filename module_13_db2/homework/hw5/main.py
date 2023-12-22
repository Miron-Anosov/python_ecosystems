import random
import sqlite3

level: tuple = ('easy', 'hard', 'middle', 'middle')
countries = [
    "Австралия",
    "Австрия",
    "Азербайджан",
    "Албания",
    "Алжир",
    "Ангола",
    "Андорра",
    "Аргентина",
    "Армения",
    "Афганистан",
    "Багамы",
    "Бангладеш",
    "Барбадос",
    "Бахрейн",
    "Беларусь",
    "Бельгия",
    "Бенин",
    "Болгария",
    "Боливия",
    "Босния и Герцеговина",
    "Ботсвана",
    "Бразилия",
    "Бруней",
    "Буркина-Фасо",
    "Бурунди",
    "Бутан",
    "Вануату",
    "Ватикан",
    "Великобритания",
    "Венгрия",
    "Венесуэла",
    "Вьетнам",
    "Габон",
    "Гаити",
    "Гайана",
    "Гамбия",
    "Гана",
    "Гватемала",
    "Гвинея",
    "Гвинея-Бисау",
    "Германия",
    "Гондурас",
    "Гренада",
    "Греция",
    "Грузия",
    "Дания",
    "Джибути",
    "Доминика",
    "Доминиканская Республика",
    "Египет",
    "Замбия",
    "Зимбабве",
    "Израиль",
    "Индия",
    "Индонезия",
    "Иордания",
    "Ирак",
    "Иран",
    "Ирландия",
    "Исландия"
]

teams = [
    "Utah Starzz",
    "San Antonio Spurs",
    "Houston Rockets",
    "Golden State Warriors",
    "Oklahoma City Thunder",
    "Los Angeles Lakers",
    "Los Angeles Clippers",
    "Denver Nuggets",
    "Minnesota Timberwolves",
    "Portland Trail Blazers",
    "Phoenix Suns",
    "Sacramento Kings",
    "Miami Heat",
    "Orlando Magic",
    "Atlanta Hawks",
    "Washington Wizards",
    "Charlotte Hornets",
    "Philadelphia 76ers",
    "New York Knicks",
    "Brooklyn Nets",
    "Boston Celtics",
    "Toronto Raptors",
    "Milwaukee Bucks",
    "Chicago Bulls",
    "Detroit Pistons",
    "Cleveland Cavaliers",
    "Indiana Pacers",
    "San Francisco Giants",
    "Chicago White Sox",
    "Houston Astros",
    "Los Angeles Angels",
    "Seattle Mariners",
    "Texas Rangers",
    "Oakland Athletics",
    "New York Yankees",
    "Boston Red Sox",
    "Toronto Blue Jays",
    "Baltimore Orioles",
    "Tampa Bay Rays",
    "Cleveland Indians",
    "Minnesota Twins",
    "Kansas City Royals",
    "Detroit Tigers",
    "Chicago Cubs",
    "St. Louis Cardinals",
    "Milwaukee Brewers",
    "Cincinnati Reds",
    "Pittsburgh Pirates",
    "Atlanta Braves",
    "Miami Marlins",
    "New York Mets",
    "Washington Nationals",
    "Philadelphia Phillies",
    "Los Angeles Dodgers",
    "Arizona Diamondbacks",
    "San Diego Padres",
    "Colorado Rockies",
    "San Francisco 49ers",
    "Arizona Cardinals",
    "Los Angeles Rams",
]


def _get_country() -> str:
    random_country: str = random.choice(countries)
    countries.remove(random_country)
    return random_country


def _get_name_command() -> str:
    random_name: str = random.choice(teams)
    teams.remove(random_name)
    return random_name


def _get_force(level_command: int) -> str:
    index: int = level_command % len(level)
    return level[index]


def generate_test_data(cur: sqlite3.Cursor, number_of_groups_: int) -> None:
    try:

        cur.executemany((
            """
            INSERT INTO `uefa_commands` (command_number, command_name, command_country, command_level)
            VALUES (?, ?, ?, ?) """),
            [(numbs_command, _get_name_command(), _get_country(), _get_force(numbs_command))
             for numbs_command in range(1, number_of_groups_ * 4 + 1)])

        cur.executemany(("""
                INSERT INTO `uefa_draw` (command_number, group_number) VALUES (?, ?) """),
                        [(numbs_command + 1, (numbs_command // 4) + 1)
                         for numbs_command in range(number_of_groups_ * 4)])

    except sqlite3.Error as err:
        print(f"Ошибка при выполнении запроса: {err}")


if __name__ == '__main__':
    number_of_groups: int = int(input('Введите количество групп (от 4 до 16): '))
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        generate_test_data(cursor, number_of_groups)
        conn.commit()
