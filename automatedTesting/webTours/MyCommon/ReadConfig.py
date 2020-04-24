import configparser
import os
def getBrowserInfo(info):
    cf = configparser.ConfigParser()
    cfpath=os.path.dirname(os.path.abspath("."))+r'\config\config.ini'
    cf.read(cfpath)
    browserInfo = cf.get('browser',info)
    return(browserInfo)
