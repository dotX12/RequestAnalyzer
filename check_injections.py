import urllib.parse
from typing import Tuple

import dask.dataframe as dd
import pandas as pd
from diag import create_diagram_requests
import re

class CheckInjections:
    sql_xss_pattern = re.compile(
        r'<(|\/|[^\/>][^>]+|\/[^>][^>]+)>|'
        r'(ALTER|CREATE|DELETE|DROP\+|EXEC(UTE){0,1}|'
        r'INSERT( +INTO){0,1}|MERGE\+|\\/\*\*\\/|CONCAT|\)OR\(|\+OR\+|HAVING|--\+|'
        r'TABLE_SCHEMA|SELECT\+|SELECT\(|SELECT\'|UPDATE\+|1=1|1\+=\+1|--|\*/|TRUNCATE|UNION( +ALL){0,1})')

    def __init__(self):
        self.df: pd.DataFrame = ...
        self.reformat_df: pd.DataFrame = ...

    def validator(self, data_line: str) -> bool:
        upper_text = data_line.upper()
        decode_url = urllib.parse.unquote(upper_text)
        if re.search(self.sql_xss_pattern, decode_url):
            return True
        else:
            return False

    def create_plot(self) -> str:
        all_lines = self.df.count()['request_uri']
        bad_lines = self.reformat_df.count()['request_uri']
        good_lines = all_lines - bad_lines
        url = create_diagram_requests(good_lines, bad_lines)
        return url

    @staticmethod
    def dict_from_pd(df: pd.DataFrame):
        temp_strings = {}
        for i in df['request_uri']:
            temp_strings[i] = {'url': df['request_uri'][i], 'count': 0}
        for i in df['counts']:
            temp_strings[i]['count'] = df['counts'][i]
        return temp_strings

    def get_top_request_uri(self):
        df_start = self.df.groupby(['request_uri']).size().reset_index(name='counts')
        df_start.sort_values(by=['counts'], ascending=False, inplace=True)
        top_frequent = df_start.head(5).to_dict()
        top_rare = df_start.tail(5).to_dict()
        top_frequent_dict = self.dict_from_pd(top_frequent)
        top_rare_dict = self.dict_from_pd(top_rare)
        return top_frequent_dict, top_rare_dict

    def formatted_top_request_uri(self):
        temp_top_urls, temp_rare_urls = '', ''
        top_urls, rare_urls = self.get_top_request_uri()
        for element in top_urls:
            temp_top_urls+= (f'Строка: {element}, Запрос: {top_urls[element]["url"]},'
                            f' Количество повторений : {top_urls[element]["count"]}\n')
        for element in rare_urls:
            temp_rare_urls+= (f'Строка: {element}, Запрос: {rare_urls[element]["url"]},'
                            f' Количество повторений : {rare_urls[element]["count"]}\n')
        return temp_top_urls, temp_rare_urls

    def reformat(self, input_file_name: str, file_name_injects_requests: str) -> None:
        self.df = dd.read_csv(input_file_name, sep=',', quotechar='"').compute(scheduler='threads')
        self.reformat_df = self.df[[self.validator(x) for x in self.df['request_uri']]]
        self.reformat_df.to_csv(file_name_injects_requests, index=False)