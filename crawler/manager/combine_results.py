# Combine parsed results
import pandas as pd
import json

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
}


class CombineResult(object):
    def __init__(self):
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
        # self.data = pd.DataFrame(columns=list(
        #     data_type.keys())).astype(default_data_type)
        self.data = pd.DataFrame()

    def load_from_json(self, json_path: str) -> pd.DataFrame:
        """
        The file format of json is each single crawling result one row
        """
        with open(json_path, 'r', encoding='utf-8') as fp:
            for line in fp:
                single_result = json.loads(line.strip(), encoding='utf-8')
                # self.data = self.data.append(
                #     single_result, ignore_index=True).astype(default_data_type)
                to_append = pd.DataFrame(
                    single_result).astype(default_data_type)
                self.data = self.data.append(to_append, ignore_index=True)

        return self.data.copy()

    def save(self, tsv_path: str):
        self.data.to_csv(tsv_path, sep='\t')


if __name__ == "__main__":
    from glob import glob
    manager = CombineResult()
    for json_file in glob('../../result/news/*.json'):
        manager.load_from_json(json_file)

    print(manager.data)
    manager.save('../../result/news/all_news.tsv')
    import ipdb
    ipdb.set_trace()
