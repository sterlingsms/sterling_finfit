from .airtable_api_base import AirtableAPIBase
import json
import urllib
import urllib.parse
from datetime import datetime
from pytz import timezone, utc
import pytz
from currency_converter import CurrencyConverter
import re
from pprint import pprint

class FinFit(AirtableAPIBase):
    def __init__(self, api_key, arg):
        AirtableAPIBase.__init__(self, api_key, arg)
        self.state_currency = {'US':'USD','CA':'CAD'}

    def get_pst_time(self, date_format='%m/%d/%Y %H:%M:%S'):
        date = datetime.now(tz=pytz.utc)
        date = date.astimezone(timezone('US/Pacific'))
        pstDateTime = date.strftime(date_format)
        return pstDateTime

    def getSVG(self,name='dot'):
        res = {}
        res['dot'] = '<svg width="14" height="14" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg" id="IconChangeColor"> <path d="M9.875 7.5C9.875 8.81168 8.81168 9.875 7.5 9.875C6.18832 9.875 5.125 8.81168 5.125 7.5C5.125 6.18832 6.18832 5.125 7.5 5.125C8.81168 5.125 9.875 6.18832 9.875 7.5Z" fill="currentColor" id="mainIconPathAttribute"></path> </svg>'
        return res[name]

    def get_dynamic_data(self,rid=None):
        get_agents = self.get_table_data()
        orgs = []
        agents = {}
        for ag in get_agents:
            agents[ag['id']] = {}
            mby = agt = ''
            agt = ag['id']
            if 'Agent Name' in ag['fields'].keys():
                agents[ag['id']]['Agent Name'] = ag['fields']['Agent Name']
            if 'Agent Title' in ag['fields'].keys():
                agents[ag['id']]['Agent Title'] = ag['fields']['Agent Title']
            if 'Reports To' in ag['fields'].keys():
                agents[ag['id']]['Reports To'] = mby = ag['fields']['Reports To'][0]
            if 'Prospects Count' in ag['fields'].keys():
                agents[ag['id']]['Prospects Count'] = ag['fields']['Prospects Count']
            if 'Agent Status' in ag['fields'].keys():
                agents[ag['id']]['Agent Status'] = ag['fields']['Agent Status']
            if 'Forecast Sales' in ag['fields'].keys():
                agents[ag['id']]['Forecast Sales'] = ag['fields']['Forecast Sales']
            if 'Agent State' in ag['fields'].keys():
                agents[ag['id']]['Agent State'] = ag['fields']['Agent State']
            if 'Monthly Estimated Revenue' in ag['fields'].keys():
                agents[ag['id']]['Monthly Estimated Revenue'] = ag['fields']['Monthly Estimated Revenue']
            orgs.append({agt:mby})

        start = rid #'recMAs4K7UIJxC4HK'
        top_st = agents[start]['Agent Status'] if 'Agent Status' in agents[start].keys() else ''
        top_status = f' <span style="color:{"green" if top_st=="Active" else "red"}">{self.getSVG()}</span>' if top_st != '' else ''
        top_pc = agents[start]['Prospects Count'] if 'Prospects Count' in agents[start].keys() else 0
        top_state = agents[start]['Agent State'] if 'Agent State' in agents[start].keys() else 'US'
        top_forecast_sales = agents[start]['Forecast Sales'] if 'Forecast Sales' in agents[start].keys() else '$0.00'
        top_CC_amt = self.cc_amt(top_forecast_sales,self.state_currency[top_st]) if top_st != '' and top_st != 'US' and top_st in self.state_currency.keys() else top_forecast_sales
        pprint(agents)
        pprint(orgs)

        hierarchical_json = self.build_hierarchy(start, orgs)
        html_output = self.render_hierarchy(hierarchical_json,agents)
        #print(hierarchical_json)

        prefix = f"<ul class='parent'><li><details><summary>{agents[start]['Agent Name']} {top_status}<br><small>{agents[start]['Agent Title']} - Prospects Count:{top_pc}, Forecast Sales: {top_CC_amt}</small></summary>"
        suffix = "</details></li></ul>"
        print(prefix + html_output + suffix)

        response = {
            "org_chart_html": prefix + html_output + suffix,
            "agents":agents,
            "hierarchical_json":hierarchical_json,
            "tdate": self.get_pst_time('%Y-%m-%d')
        }
        return response

    def cc_amt(self,amt = int, ct_to = 'CAD', ct_from = 'USD'):
        #Substitute all non-digit characters (except the decimal point) with an empty string
        amt_only = amt if isinstance(amt, int) else re.sub("[^\d.]", "", amt)
        cc_amt = f'{amt}'
        # Create a currency converter object
        converter = CurrencyConverter()

        # Convert ex USD to EUR
        ct_amount = converter.convert(amt_only, ct_from, ct_to)
        if ct_amount:
            cc_amt = f'${round(ct_amount, 2)}'
        return cc_amt

    def build_hierarchy(self,category='', data=[]):
        result = {}
        for item in data:
            for key, value in item.items():
                if value == category:
                    result[key] = self.build_hierarchy(key,data)
        return result

    def render_hierarchy(self,hierarchical_json={},agents={}):
        result = "<ul>\n"
        for key, value in hierarchical_json.items():
            st = agents[key]['Agent Status'] if 'Agent Status' in agents[key].keys() else ''
            status = f' <span style="color:{"green" if st=="Active" else "red"}">{self.getSVG()}</span>' if st != '' else ''
            pc = agents[key]['Prospects Count'] if 'Prospects Count' in agents[key].keys() else 0
            sta = agents[key]['Agent State'] if 'Agent State' in agents[key].keys() else 'US'
            fs = agents[key]['Forecast Sales'] if 'Forecast Sales' in agents[key].keys() else 0
            CC_amt = self.cc_amt(fs,self.state_currency[sta]) if sta != '' and sta != 'US' and sta in self.state_currency.keys()  else fs
            result += "<li>\n"
            #if not value:
            result += f"  <details>\n"
            result += f"    <summary>{agents[key]['Agent Name']} {status}<br><small>{agents[key]['Agent Title']} - Prospects Count:{pc}, Forecast Sales: {CC_amt}</small></summary>\n"
            if value:
                result += self.render_hierarchy(value,agents)
            #if not value:
            result += "  </details>\n"
            result += "</li>\n"
        result += "</ul>\n"
        return result
