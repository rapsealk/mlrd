from abc import ABC


class BaseDatasetRepository(ABC):
    pass


class DatasetRepository(BaseDatasetRepository):
    def __init__(self):
        super(DatasetRepository, self).__init__()
