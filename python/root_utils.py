# pylint: disable=pointless-string-statement
import re
import pandas as pd
import uproot3

def pandas_to_tree(data, file_name, tree_name):
    """
      Parameters
      ----------
      data : pandas.DataFrame
          Data frame which should be stored as TTree
      file_name : str
          Path and name of root file
      tree_name : str
          Name of TTree
    """
    branch_dict = {data.columns[i]: data.dtypes[i]
                   for i in range(0, len(data.columns))}
    with uproot3.recreate(file_name) as file_output:
        file_output[tree_name] = uproot3.newtree(branches=branch_dict, title=tree_name)
        file_output[tree_name].extend({data.columns[i]:
                                       data[data.columns[i]].to_numpy()
                                       for i in range(0, len(data.columns))})

def tree_to_pandas(file_name, tree_name, columns, exclude_columns="", **kwargs):  # pylint: disable=dangerous-default-value
    """
        Parameters
        ----------
        file_name : str
            Path to root file
        tree_name : str
            Name of TTree
        columns: sequence of str
            Names of branches or aliases to be read. Can also use wildcards like ["*"]
            for all branches or ["*fluc*"] for all branches containing the string "fluc".
        exclude_columns: str
            Regular expression of columns to be ignored, e.g. ".*Id".

        Returns
        --------
        pandas.DataFrame
            Data frame with specified columns
    """
    with uproot3.open(file_name) as file:
        data = file[tree_name].pandas.df(columns, **kwargs)
    if exclude_columns != "":
        data = data.filter([col for col in data.columns
                            if not re.compile(exclude_columns).match(col)])
    return data
