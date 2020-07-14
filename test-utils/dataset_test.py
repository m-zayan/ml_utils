from requests_utils.data_request import Download

metadata = Download.get_datasets_metadata('./datasets_metadata.json', dname=None)

Download.download_from_url(metadata['AReM']['download_url'], to_path='../AReM.zip', chunk_size=1024)