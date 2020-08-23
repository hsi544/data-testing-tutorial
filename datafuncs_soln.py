import math
from hashlib import sha256
import pandas as pd
import yaml


def standard_scaler(x):
    return (x - x.mean()) / x.std()


def clip(data, lower, upper):
    data[data < lower] = lower
    data[data > upper] = upper
    return data


def eq_roots(coefficients):
    """
    Returns the non-complex roots of a quadratic equation.
    """
    a, b, c = coefficients
    # there can be an assertion here that mirrors
    # the assumption in the test function.
    discriminant = b ** 2 - 4 * a * c
    assert discriminant >= 0
    assert a > 0
    root1 = (-a + math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    root2 = (-a - math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    return root1, root2


def hash_string(string):
    """
    Convenience wrapper that returns the hash of a string.
    """
    assert isinstance(string, str), f"{string} is not a string!"
    string = string.encode("utf-8")
    return sha256(string).hexdigest()


def hash_data(handle):
    df = pd.read_csv(handle)
    hashes = pd.DataFrame()  # don't modify the original
    hashes["concat"] = df.apply(
        lambda x: "".join(str(x[col]) for col in df.columns), axis=1
    )
    hashes["hash"] = hashes["concat"].apply(lambda x: hash_string(x))
    del hashes["concat"]
    return hashes


def hash_file(fname):
    filehash = sha256()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            filehash.update(chunk)
    return filehash.hexdigest()


def autospec(handle):
    filename = handle.split("/")[-1]
    file_prefix = filename.split(".")[0]
    df = pd.read_csv(handle)
    metadata = dict()
    metadata["filename"] = filename
    metadata["columns"] = df.columns
    yaml_spec = yaml.dump(metadata)
    with open(f"metadata_{file_prefix}.yml", "w+") as f:
        f.write(yaml_spec)
