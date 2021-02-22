import mmlibrary
import json
import io
import pickle


def load_pickled_model_binary():
    with open(mmlibrary.getModel(), 'rb') as f:
        return pickle.load(f)


def read_table_from_file(name: str, index_col=None):
    """
    Read tabular data into a pandas DataFrame.
    """
    import pandas
    data = mmlibrary.getBinaryFromResource(name)
    sample = data[:500]
    if isinstance(sample, bytes):
        sample = sample.decode("utf-8")
    if sample.startswith("{") and "\t" not in sample:
        # json ({col1=[v, ...], ...})
        return pandas.DataFrame(data=json.loads(data))
    else:
        # csv
        return pandas.read_csv(
            io.BytesIO(data) if isinstance(data, bytes) else io.StringIO(data),
            sep=None, engine='python', index_col=index_col
        )


def write_table_to_file(name: str, data):
    """
    Store tabular data from a pandas DataFrame.
    """
    sbuf = io.StringIO()
    data.to_csv(sbuf, sep='\t', index=False)
    bbuf = io.BytesIO(sbuf.getvalue().encode("utf-8"))
    mmlibrary.saveBinaryToResource(name, bbuf)


