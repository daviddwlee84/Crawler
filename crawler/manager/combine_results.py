# Combine parsed results
import pandas as pd
import json
from typing import List, Dict

# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.astype.html
# https://pandas.pydata.org/pandas-docs/stable/user_guide/basics.html#basics-dtypes
# https://pbpython.com/pandas_dtypes.html
default_data_type = {
    # 'url': 'str',
    # 'domain': 'str',
    # 'html_title': 'str',
    # 'html_body': 'str',
    # 'title': 'str',
    # 'author': 'str',
    'date': 'datetime64[ns]',
    # 'content': 'str',
    'parse_date': 'datetime64[ns]',
    # 'meta': 'object',  # there is some problem of storing dict in pandas
}


class CombineResult(object):
    def __init__(self, simplify: bool = False, simplify_columns: List[str] = ['title', 'author', 'date', 'content'],
                 default_data_type: Dict[str, str] = default_data_type):
        """
        Set simplify to true to only load simplify_columns, it can be helpful when data amount is very large
        """
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
        # self.data = pd.DataFrame(columns=list(
        #     data_type.keys())).astype(default_data_type)
        self.data = pd.DataFrame()
        self._simplify = simplify
        self._simplify_columns = simplify_columns
        if simplify:
            self._default_data_type = {
                key: value for key, value in default_data_type.items() if key in simplify_columns}
        else:
            self._default_data_type = default_data_type

    def load_from_json(self, json_path: str) -> pd.DataFrame:
        """
        The file format of json is each single crawling result one row

        TODO: see if pd.read_json can simplify this code

        TODO: add tqdm
        """
        with open(json_path, 'r', encoding='utf-8') as fp:
            for line in fp:
                single_result = json.loads(line.strip(), encoding='utf-8')
                if self._simplify:
                    # ValueError: If using all scalar values, you must pass an index
                    # https://stackoverflow.com/questions/17839973/constructing-pandas-dataframe-from-values-in-variables-gives-valueerror-if-usi
                    single_result = {
                        key: value for key, value in single_result.items() if key in self._simplify_columns}
                to_append = pd.DataFrame(
                    single_result, index=[0]).astype(self._default_data_type)
                self.data = self.data.append(to_append, ignore_index=True)

        return self.data.copy()

    def load_from_tsv(self, tsv_path: str) -> pd.DataFrame:
        self.data = pd.read_csv(tsv_path, sep='\t')
        data_type = {key: value for key, value in self._default_data_type.items(
        ) if key in self.data.columns.to_list()}
        self.data = self.data.astype(data_type, copy=False)

        return self.data.copy()

    def save(self, tsv_path: str, store_simplify: bool = True):
        if not self._simplify and store_simplify:
            # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop.html
            # https://stackoverflow.com/questions/13411544/delete-column-from-pandas-dataframe
            self.data[self._simplify_columns].to_csv(
                tsv_path, sep='\t', index=False)
        else:
            self.data.to_csv(tsv_path, sep='\t', index=False)


if __name__ == "__main__":
    from glob import glob
    manager = CombineResult(simplify=False)
    for json_file in glob('../../result/news/*.json'):
        manager.load_from_json(json_file)

    print(manager.data)
    manager.save('../../result/news/all_news.tsv', store_simplify=True)
    # manager.save('../../result/news/all_news.tsv', store_simplify=False)

    manager.load_from_tsv('../../result/news/all_news.tsv')
    import ipdb
    ipdb.set_trace()
