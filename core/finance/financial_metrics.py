import os
import pickle

from core.utils.read_csv import read_csv, read_csv_with_different_type, PROJECT_ROOT
from core.finance.metrics.number_of_items import NumberOfItems
from core.finance.metrics.verified_funds import VerifiedFunds
from core.finance.metrics.raised_funds import RaisedFunds
from core.finance.metrics.common_items_ratio import CommonItemsRatio
from core.finance.metrics.proponent_projects import ProponentProjects
from core.finance.metrics.total_receipts import TotalReceipts
from core.finance.metrics.new_providers import NewProviders
from core.finance.metrics.approved_funds import ApprovedFunds


class FinancialMetrics():
    PROCESSED_FILE_PATH = os.path.join(PROJECT_ROOT, 'data', 'processed',
                                       'financial_metrics.pickle')

    def __init__(self):
        self.load()

    def initialize(self):
        print('****** Reading CSVs ******')
        self._init_datasets()
        print('****** Computing Metrics ******')
        self._init_metrics()

    def get_metrics(self, pronac, metrics=[]):

        if not isinstance(pronac, str):
            raise ValueError('PRONAC type must be str (string)')
        results = {}

        if metrics is []:
            metrics = self.metrics.keys()

        for metric in metrics:
            if metric in self.metrics:
                print('Getting Metrics for [{}]'.format(metric))
                results[metric] = self.metrics[metric].get_metrics(pronac)
            else:
                raise Exception('metricNotFound: {}'.format(metric))

        return results

    def _init_datasets(self):
        self.datasets = {
           'orcamento': read_csv_with_different_type('planilha_orcamentaria.csv', {'PRONAC': str}),
           'comprovacao': read_csv_with_different_type('planilha_comprovacao.csv', {'PRONAC': str, 'proponenteCgcCpf': str}),
           'captacao': read_csv_with_different_type('planilha_captacao.csv', {'Pronac': str, 'CgcCpfMecena': str}),
           'projetos': read_csv_with_different_type('planilha_projetos.csv', {'PRONAC': str, 'CgcCpf': str})
        }

    def _init_metrics(self):
        self.metrics = {
           'items': NumberOfItems(self.datasets['orcamento'].copy()),
           'approved_funds': ApprovedFunds(self.datasets['orcamento'].copy()),
           'verified_funds': VerifiedFunds(self.datasets['comprovacao'].copy()),
           'raised_funds': RaisedFunds(self.datasets['captacao'].copy()),
           'common_items_ratio': CommonItemsRatio(self.datasets['orcamento'].copy()),
           'total_receipts': TotalReceipts(self.datasets['comprovacao'].copy()),
           'new_providers': NewProviders(self.datasets['comprovacao'].copy()),
           'proponent_projects': ProponentProjects(self.datasets['comprovacao'].copy(), \
                                                   self.datasets['projetos'].copy())
        }

    def save(self):
        with open(FinancialMetrics.PROCESSED_FILE_PATH, 'wb') as ofile:
            pickle.dump(self, ofile, pickle.HIGHEST_PROTOCOL)

    def load(self):
        if os.path.isfile(FinancialMetrics.PROCESSED_FILE_PATH):
            with open(FinancialMetrics.PROCESSED_FILE_PATH, 'rb') as ifile:
                financial_metrics = pickle.load(ifile)
                self.__dict__.update(financial_metrics.__dict__)
        else:
            self.initialize()
