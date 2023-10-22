from pyairtable import  Api, Base, Table

class AirtableAPIBase():
    def __init__(self, api_key, arg):
        self.api_key = api_key
        self.app = arg['app']              
        self.table = arg['table']
        self.airtable_api_conn = self.connect_api()

    def connect_api(self):
        api = Api(self.api_key)
        return api

    def get_table_data(self):
        table = self.airtable_api_conn.table(self.app, self.table)
        get_records = table.all()
        return get_records