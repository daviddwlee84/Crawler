# Search result based on combined results
from combine_results import CombineResult
from typing import List
import pandas as pd
import datefinder


class ResultFilter(object):
    def __init__(self, result_tsv: str, update_inplace: bool = False):
        self.data = CombineResult().load_from_tsv(result_tsv)
        self._inplace = update_inplace

    def filter_with_keywords(self, keywords: List[str], search_in_columns: List[str] = ['title', 'content']) -> pd.DataFrame:
        """
        https://stackoverflow.com/questions/27975069/how-to-filter-rows-containing-a-string-pattern-from-a-pandas-dataframe
        """
        result = self.data.set_index(['title', 'content']).filter(
            regex=r'|'.join(keywords), axis=0)
        if self._inplace:
            self.data = result

        return result

    def filter_author(self):
        pass

    def filter_domain(self):
        """
        Note: simplified result doesn't contain url domain, remember to store full version.
        """
        pass

    def filter_date_range(self, from_date: str, to_date: str, date_col: str = 'date'):
        """
        date_col can be date, parsed_date, ...

        Note: from_date (include), to_date (exclude)

        TODO: accept either string or datetime object, and convert automatically

        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.date_range.html
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.between_time.html

        https://stackoverflow.com/questions/29370057/select-dataframe-rows-between-two-dates
        """
        from_date = list(datefinder.find_dates(from_date))[0]
        to_date = list(datefinder.find_dates(to_date))[0]

        mask = (from_date <= self.data[date_col]) & (
            self.data[date_col] <= to_date)

        result = self.data[mask]

        if self._inplace:
            self.data = result

        return result


if __name__ == "__main__":
    manager = ResultFilter('../../result/news/all_news.tsv')
    print(manager.filter_with_keywords(['日本女高中生', 'TikTok']))
    print(manager.filter_date_range('2020/8/19', '2020/8/20'))
