import os
import io

from zipfile import ZipFile
import requests
import json

__all__ = ['Download', 'Decoder', 'Reader']


class Decoder:
    def __init__(self):
        pass

    @staticmethod
    def bytes_to_str(line, encoding='utf-8'):
        """
        Parameter
        ---------
        line (str): byte string

        Returns
        -------
        str: encoded string, ex. encoding='utf-8'
        """
        line = line.decode(encoding)

        return line


class Writer:

    def __init__(self):
        pass

    @staticmethod
    def download_from_url(url: str, to_path: str, chunk_size: int = 1024):
        """
        Parameter
        ---------
        url (str): file url

        to_path (str): director/fname + file_extension

        chunk_size: request chunk_size, default = 1024

        Returns
        -------
        str: encoded string, ex. encoding='utf-8'
        """
        req = requests.get(url, stream=True)

        if req.status_code != 200:
            raise req.raise_for_status()
        else:

            with open(to_path, "wb") as file:
                for block in req.iter_content(chunk_size=chunk_size):
                    if block:
                        file.write(block)

    @staticmethod
    def write_csv(lines, path, fname):

        fpath = os.path.join(path, fname)

        with open(fpath, 'w') as file:
            for line in lines:
                file.write(line)

    @staticmethod
    def get_zipfile_content(url):
        """
        Parameter
        ---------
        url (str): url for zip-file

        Returns
        -------
        ZipFile: ZipFile Object, of bytes data
        """
        res = requests.get(url, stream=True)

        d_bytes = io.BytesIO(res.content)
        files = ZipFile(d_bytes)

        return files

    @staticmethod
    def get_zipfile_bytes(url, fname):
        """
        Parameter
        ---------
        url (str): url for zip-file

        fname (str): A specific file inside zip file (ex. age.csv, cat_id_1.png, ...etc.)

        Returns
        -------
        list: list of bytes contains, file data as in bytes format
        """

        files = Writer.get_zipfile_content(url)
        d_bytes = None

        try:
            d_bytes = files.open(fname)
        except KeyError as err:
            print(err, '\nAvailable files : \n', '=' * 50,  files.filelist)

        bytes_data = d_bytes.readlines()

        return bytes_data


class Reader:
    def __init__(self):
        pass

    @staticmethod
    def read_json(path):
        """
        Parameter
        ---------
        path (str): json file path

        Returns
        -------
        dict: dictionary of json file data
        """
        with open(path) as file:
            file_data = json.load(file)

        return file_data


class Download(Writer):
    def __init__(self, chunk_size: int):
        super().__init__()
        self.chunk_size = chunk_size

    @staticmethod
    def get_datasets_metadata(metadata_path: str, dname=None):
        """
        Parameter
        ---------
        metadata_path (str): metadata json file path

        dname (str): dataset name

        Returns
        -------
        dict: dataset metadata, if dname=None, return all datasets metadata,
              otherwise return dataset metadata
        """
        metadata = Reader.read_json(metadata_path)

        if dname is None:
            return metadata
        else:
            return metadata[dname]

    def download_dataset(self, dname, reformat=True):
        """
        Parameter
        ---------
        dname (str): dataset name

        reformat (boolean):
        """
        pass
