from Class.devlopment import selenium_aux as aux

from selenium import webdriver
from fake_useragent import UserAgent

import time

from Class.inputs.keys_database import *
from pymongo import MongoClient

class Get_connection:

    def __init__(self):

        self.clinet = MongoClient(string_connection)
    
class Driver:

    def __init__(self,
                 url: str) -> None: 
        
        self.url = url
    
    def random_user(self):
        return UserAgent().random

    def inicialize_driver(self,
                         ru: bool = True,
                         show_page: bool = False):

        options_ = webdriver.ChromeOptions()

        if ru: options_.add_argument(f'--user-agent={self.random_user()}')

        if show_page: pass
        else: options_.add_argument("--headless") ## Mostra tela

        options_.add_argument('--no-sandbox') ## Ambiente Sandbox desabilitado
        options_.add_argument('--disable-gpu') ## Desabilita uso de GPU 
        options_.add_argument("--disable-notifications") ## Desabilita notificacoes do navegador
        options_.add_argument("--start-maximized") ## Comeca com a pagina maximizada
        options_.add_experimental_option("prefs", {
                                                # "directory_upgrade": True, ## Permite alterar diretorio de onde os dowloads vao
                                                # "download.default_directory": fr'{self.dirFolder}', ## Seta novo diretorio para dowloads
                                                # "download.prompt_for_download": False, ## Desabilita confirmacao para realizacao de dowload
                                                # "download.open_pdf_in_system_reader": True, ## Abre PDFS no sistema de leitor de PDFS do sistema
                                                # "plugins.always_open_pdf_externally": True, ## Abre PDFS de forma externa ao navegador
                                                "safebrowsing.enabled": True ## Ativa Safe Browsing para navegacao
                                            })


        # service_ = Service(executable_path={self.dir_chromedriver})
        # driver = webdriver.Chrome(service=service_, options=options_)
        driver = webdriver.Chrome(options=options_)
        
        driver.implicitly_wait(2)
        
        driver.get(self.url)

        ## Retirando anúncio
        try:driver.execute_script("arguments[0].remove();", aux.xpath('//*[@id="app"]/div[22]/div'))
        except: pass

        return driver
    

    def prepare_scrapping(self, driver, locate):
        
        try:
            aux.search_field(driver, locate)
            aux.enter(driver)

            ## Se o endereco nao levar à um local, mas sim uma rua, encontro o estabelecimento que se encontra neste local
            try:
                time.sleep(3)
                driver.execute_script("arguments[0].scrollIntoView();", aux.class_name(driver, 'lI9IFe'))
                aux.class_name(driver, 'lI9IFe').click() 

            except Exception as error: 
                print(f'Nao foi possivel acessar o estabelecimento do endereco, vide error: {error}')
                raise Exception

        except Exception as error:
            raise Exception

        return driver