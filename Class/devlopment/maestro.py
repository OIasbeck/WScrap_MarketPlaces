import pandas as pd
from bs4 import BeautifulSoup
import time
import re
from datetime import datetime
import numpy as np

from Class.devlopment import selenium_aux as aux

class BusinessDetail:
    def __init__(self):
        self.nome = None
        self.endereco = None
        self.web_site = None
        self.telefone = None
        self.qtd_review = None
        self.nota_review = None
        self.maior_movimento = None
        self.detalhes = None
        self.hr_funcionamento = None
        self.latitude = None
        self.longitude = None


class ListBusiness:
    def __init__(self):
        self.business_list = []

    def dataframe(self):
        return pd.DataFrame([vars(business) for business in self.business_list])

    def export_excel(self, filename):
        self.dataframe().to_excel(f"{filename}.xlsx", index=False)

    def export_csv(self, filename):
        self.dataframe().to_csv(f"{filename}.csv", index=False)


def horario_funcionamento(driver,
                          html):

    def v_padrao():
    
        for linha in tabela.find_all('tr', class_='y0skZc'):
            dia_semana = linha.find('td', class_= path_dia_semana).text.strip()

            horario = linha.find('td', class_= path_horario).text.strip()

            if len(horario) > 11:
                horario = horario[:11] + '-' + horario[11:]

            horarios_funcionamento[dia_semana.lower()[:3]] = horario  

        return 'padrao', horarios_funcionamento   


    def v_tabela():

        time.sleep(1)

        botao = aux.xpath(driver, '//button[@data-item-id="oh"]')
        botao.click()
        
        time.sleep(1)

        horarios_funcionamento = {}

        for linha in aux.class_name(driver, 'y0skZc', True):

            dia_semana = aux.class_name(linha, path_dia_semana).text.strip()
            horario = aux.class_name(linha, path_horario).text.strip()

            if len(horario) > 11:
                horario = horario[:11] + '-' + horario[11:]

            horarios_funcionamento[dia_semana.lower()[:3]] = horario

        return 'tabela', horarios_funcionamento

    soup = BeautifulSoup(html, 'html.parser')
    path_dia_semana = 'ylH6lf'
    path_horario = 'mxowUb'
    
    horarios_funcionamento= {}

    try:
        tabela_div = soup.find('div', class_='t39EBf')
        tabela = tabela_div.find('table', class_='eK4R0e')

        valor, horarios = v_padrao()

    except:
        botao = aux.class_name(driver, 'CsEnBe')
        driver.execute_script("arguments[0].scrollIntoView();", botao)

        valor, horarios = v_tabela()

    return valor, horarios


def horario_movimento(html):

    def extrair_hora_porcentagem(aria_label):
        partes = aria_label.split(':')
        hora = partes[0][-2:].strip()
        porcentagem = int(partes[-1].split('%')[0].strip())

        return hora, porcentagem
    
    soup = BeautifulSoup(html, 'html.parser')

    divs_movimento = soup.find_all('div', class_='dpoVLd')

    porcentagens = []
    porcentagens_por_hora = {}

    for div in divs_movimento:
        aria_label = div.get('aria-label', '')
        hora, porcentagem = extrair_hora_porcentagem(aria_label)
        
        if hora not in porcentagens_por_hora:
            porcentagens_por_hora[hora] = []
        porcentagens_por_hora[hora].append(porcentagem)

    medias_por_hora = {}
    for hora, porcentagens in porcentagens_por_hora.items():
        media_por_hora = sum(porcentagens) / len(porcentagens)
        medias_por_hora[hora] = media_por_hora

    horario_maior_media = max(medias_por_hora, key=medias_por_hora.get)
    media_maior_movimento = medias_por_hora[horario_maior_media]

    return horario_maior_media, media_maior_movimento


def sobre_detalhes(html):

    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.find_all('h2', class_='iL3Qke fontTitleSmall')

    result_dict = {}

    for element in elements:
        element_text = element.get_text(strip=True)
        values = []

        span_elements = element.find_next('ul', class_='ZQ6we').find_all('span', {'aria-label': True})

        values = [span['aria-label'] for span in span_elements]

        result_dict[element_text] = values

    return result_dict


def coordenadas(url):

    latitude = re.search(r'!3d([-+]?.*?)!4d', url).group(1)
    longitude = re.search(r"!4d([-+]?[\d.]+)!.*", url).group(1)

    return latitude, longitude


class Process:

    def __init__(self) -> None:
        
        self.name = '//h1[@class="DUwDvf lfPIob"]'
        # self.name = '//div[@class="tAiQdd"]//h1'
        self.adress = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
        self.website = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
        self.phone_number = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
        self.details = 'hh2c6'
        self.rating = 'jANrlb'
        self.moviment = 'dpoVLd'

        self.export = f"/airflow/dags/Class/Pluxee/Database/Restaurantes_{datetime.today().strftime('%Y-%m-%d')}"
        

    def scrapping_bussines(self, 
            driver,
            wait: float):

        bussiness_list = ListBusiness()
        bussiness = BusinessDetail()

        
        ## Nome 
        time.sleep(2)
        try:driver.execute_script("arguments[0].scrollIntoView();", aux.xpath(driver, self.name))
        except:pass
        bussiness.nome = aux.xpath(driver, self.name).text if  aux.xpath(driver, self.name) else np.nan


        ## Endereco
        time.sleep(wait)
        try:driver.execute_script("arguments[0].scrollIntoView();", aux.xpath(driver, self.adress))
        except:pass
        bussiness.endereco = aux.PreProcessing.string_process(
                                    aux.xpath(driver, self.adress).text,
                                    'endereco') if aux.xpath(driver, self.adress) else np.nan


        ## Website
        time.sleep(wait)
        try:driver.execute_script("arguments[0].scrollIntoView();", aux.xpath(driver, self.website))
        except:pass
        bussiness.web_site = aux.xpath(driver, self.website).text if aux.xpath(driver, self.website) else np.nan


        ## Telefone
        time.sleep(wait)
        try:driver.execute_script("arguments[0].scrollIntoView();", aux.xpath(driver, self.phone_number))
        except:pass
        bussiness.telefone = aux.PreProcessing.string_process(aux.xpath(driver, self.phone_number).text, 'numero') if aux.xpath(driver, self.phone_number) else np.nan


        ## Maior Movimento
        time.sleep(wait)
        try:
            driver.execute_script("arguments[0].scrollIntoView();", aux.class_name(driver, self.moviment))
            bussiness.maior_movimento = horario_movimento(driver.page_source)[0] if aux.class_name(driver, self.moviment) else np.nan

        except: bussiness.maior_movimento = np.nan

        
        time.sleep(wait)
        ## Quantidade Avaliacoes e Nota
        try:
            driver.execute_script("arguments[0].scrollIntoView();", aux.class_name(driver, self.rating))
            avaliacoes = aux.class_name(driver, self.rating).text.replace('.','')

            bussiness.nota_review = re.search(r'([\d,]+)\n', avaliacoes).group(1).replace(',', '.')

            bussiness.qtd_review = re.search(r'\n([\d,]+)', avaliacoes).group(1).replace(',', '.')

        except:
            avaliacoes = None
            bussiness.nota_review = np.nan
            bussiness.qtd_review = np.nan


        ## Horario Funcionamento
        time.sleep(wait)
        try:
            valor, horario = horario_funcionamento(driver, driver.page_source)
            
            bussiness.hr_funcionamento = aux.PreProcessing.string_process(horario, 'funcionamento')

            if valor == 'tabela': aux.css(driver, 'button[aria-label="Voltar"]').click()
            else: pass

        except: bussiness.hr_funcionamento = np.nan


        ## Sobre
        try:
            ## Sobe a pagina se referenciando pelo path do nome
            driver.execute_script("arguments[0].scrollIntoView();", aux.class_name(driver, 'lMbq3e'))
            botao_sobre = aux.xpath(driver, "//div[@class='Gpq6kf fontTitleSmall' and text()='Sobre']")

            time.sleep(wait)
            aux.ActionChains(driver).move_to_element(botao_sobre).perform()

            time.sleep(wait)
            aux.ActionChains(driver).click(botao_sobre).perform()

        except: pass

        time.sleep(wait)
        bussiness.detalhes = sobre_detalhes(driver.page_source) if aux.class_name(driver, self.details) else np.nan
        time.sleep(wait)

        ## Volte para visao geral
        try:aux.class_name(driver, 'LRkQ2').click()
        except:pass
        
        
        ## Latitude e Longitude
        try:
            lat, long  = coordenadas(driver.current_url)
                                                        
            bussiness.latitude = aux.PreProcessing.string_process(lat, 'latitude')
            bussiness.longitude = aux.PreProcessing.string_process(long, 'longitude')

        except:
            print(f"<--- Latitude e Longitude nao foram encontrados!, url do estabelecimento = {driver.current_url}")
            raise Exception

        bussiness_list.business_list.append(bussiness)

        data = bussiness_list.dataframe()

        return data
