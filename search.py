# -*- coding:utf-8 -*-
#@author:zhanhao
#@project:Graduation Project
import math
from Bio import Entrez
import re

max = 9999999


class esearch:
    def __init__(self, query='', gdsType='', species=''):
        """
        :param query:set the query term (disease)
        :param gdsType:set the gds type (miRNA,mRNA and lncRNA)
        :param species:set the species (Homo sapiens )
        """
        gdsType1 = ' '
        gdsType2 = 'miRNA'
        gdsType2 += ' ("Non-coding RNA profiling by array"[Filter] or '
        gdsType2 += ' "Non-coding RNA profiling by high throughput sequencing"[Filter] or '
        gdsType2 += ' "Non-coding RNA profiling by genome tiling array"[Filter])'
        gdsType3 = 'mRNA'
        gdsType3 += ' ("Expression profiling by MPSS"[Filter] or '
        gdsType3 += ' "Expression profiling by RT-PCR"[Filter] or '
        gdsType3 += ' "Expression profiling by SAGE"[Filter] or '
        gdsType3 += ' "Expression profiling by SNP array"[Filter] or '
        gdsType3 += ' "Expression profiling by array"[Filter] or '
        gdsType3 += ' "Expression profiling by genome tiling array"[Filter] or '
        gdsType3 += ' "Expression profiling by high throughput sequencing"[Filter])'
        gdsType4 = 'lncRNA'
        gdsType4 += ' ("Non-coding RNA profiling by array"[Filter] or '
        gdsType4 += ' "Non-coding RNA profiling by high throughput sequencing"[Filter] or '
        gdsType4 += ' "Non-coding RNA profiling by genome tiling array"[Filter])'

        if species == 'Any':
            species = ''
        else:
            species += '[organism]'
        self.query1 = '('+query + ') ("gse"[filter]) ' + gdsType1 + ' ' + species
        self.query2 = '('+query + ') ("gse"[filter]) ' + gdsType2 + ' ' + species
        self.query3 = '('+query + ') ("gse"[filter]) ' + gdsType3 + ' ' + species
        self.query4 = '('+query + ') ("gse"[filter]) ' + gdsType4 + ' ' + species
        self.idlist = 0
        self.idlist1 = self.search(self.query1)['IdList']
        self.idlist2 = self.search(self.query2)['IdList']
        self.idlist3 = self.search(self.query3)['IdList']
        self.idlist4 = self.search(self.query4)['IdList']
        if gdsType == "miRNA":
            self.idlist = self.idlist2
        elif gdsType == "mRNA":
            self.idlist = self.idlist3
        elif gdsType == "lncRNA":
            self.idlist = self.idlist4
        else:
            self.idlist = self.idlist1
        self.pages = math.ceil(len(self.idlist)/20)
        #self.gses = self.fetch_summaries(self.idlist)

    def search(self, query):
        """
        search for GEO entities by given terms
        In order to get GEO ID list
        :param query: query terms
        :return: return the geo entities (idlist is used only)
        """
        Entrez.email = 'WindMelon96@gmail.com'
        handle = Entrez.esearch(db='gds',
                                sort='relevance',
                                retmax=str(max),
                                term=query)
        results = Entrez.read(handle)
        return results

    def fetch_summaries(self, id_list):
        """
        fetch GEO summary by given ID list
        :param id_list: geo idlist
        :return: return the geo summaries
        """
        ids = ','.join(id_list)
        Entrez.email = 'WindMelon96@gmail.com'
        handle = Entrez.esummary(db='gds',
                                 retmode='xml',
                                 id=ids)
        results = Entrez.read(handle)
        return results

    def fetch_by_page(self, page):
        """
        :param id_list:full idlist get after searching
        :param page: current page number(divided by 20)
        :return: return current 20 geo entities as one page
        """
        type_list = list()
        id_list = self.idlist[(page-1)*20:(page-1)*20+20]
        i = 0
        flag = 0
        for id in id_list:
            type_list.append("")
            if id in self.idlist2:
                type_list[i] += "miRNA;"
                flag = 1
            if id in self.idlist3:
                type_list[i] += "mRNA;"
                flag = 1
            if id in self.idlist4:
                type_list[i] += "lncRNA;"
                flag = 1
            if flag == 0:
                type_list[i] += "other;"
            flag = 0
            i += 1
        return (self.fetch_summaries(id_list),type_list)



if __name__ == '__main__':
    search = esearch(query="lung cancer",gdsType="lncRNA",species="human")
    #print(search.query)
    for gse in search.gses:
       print(gse)
