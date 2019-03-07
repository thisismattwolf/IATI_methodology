# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 15:25:18 2019

@author: Matthew Wolf
"""

# Data structure and methods for ANDE methodology

class donor_activity(object):
    def __init__(self, donor, year, title, description, total_commitment, \
                 total_duration, annual_commitment, currency, country, region):
        self.donor = donor
        self.year = year
        self.title = title
        self.description = description
        self.total_commitment = total_commitment
        self.total_duration = total_duration
        self.annual_commitment = annual_commitment
        self.currency = currency
        self.country = country
        self.region = region


        