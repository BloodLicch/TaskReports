from json import loads
from os import path, walk
from re import findall
from datetime import datetime, time


class Queries(object):
    """
    Класс для хранения информации о запросах
    """
    def __init__(self, init_path: str):
        """
        Констуктор класса Queries
        :param init_path: строка с путем к папке с файлами логов
        """
        self.report = {"valid": {}, "invalid": {}}

        for __, __, file_names in walk(init_path):
            if len(file_names):
                for one_file in file_names:
                    self.parse_log_file(init_path, one_file)

    def add_query(self, i_query: dict) -> None:
        """
        Функция добавления запроса в алфавит
        :param i_query: json запроса, который будет добавляться в коллекцию
        """
        selected_dict = self.is_valid_query(i_query)

        query_date = datetime.fromtimestamp(i_query["timestamp"]).date()
        utc_date: int = int(datetime.timestamp(datetime.combine(query_date, time())))

        if utc_date not in self.report[selected_dict]:
            self.report[selected_dict][utc_date] = {"create": 0, "update": 0, "delete": 0}

        self.report[selected_dict][utc_date][i_query["event_type"]] += 1

    @staticmethod
    def is_log_file(file_name: str) -> bool:
        """
        Функция проверяет принадлежность файла к файлам логов
        :param file_name: имя файла лога
        :return: функция вернет True если проверяемый файл логовский и False в противном случае
        """
        return bool(file_name.endswith(".log"))

    @staticmethod
    def is_valid_query(i_query: dict) -> str:
        """
        Функция проверки запроса на валидность
        :param i_query: json запроса, по которому будет проходить проверка
        :return: вернется "valid" для валидного запроса и "invalid" в противном случае
        """
        for user_id in i_query["ids"]:
            find_string = "id={}".format(user_id)
            if find_string not in set(findall("{}\d*".format(find_string), i_query["query_string"])):
                return "invalid"

        return "valid"

    def parse_log_file(self, file_path: str, file_name: str) -> None:
        """
        Функция поиска лог-файлов в папке и их чтения
        :param file_path: путь к каталогу, в котором находится файл для чтнения
        :param file_name: имя файла
        """
        if self.is_log_file(file_name):
            with open(path.join(file_path, file_name), 'r') as input_file:
                for line in input_file:
                    self.add_query(loads(line))


if __name__ == "__main__":
    files_path = path.join(path.abspath(path.dirname(__file__)),
                           "test_files")  # папка text_files и лежит в корне проекта

    queries1 = Queries(files_path)

    print(queries1.report)
