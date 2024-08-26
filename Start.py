from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

class preco:
    def __init__(self):
        self.preco_ml = []  # Lista para armazenar preços do Mercado Livre
        self.preco_amazon = []  # Lista para armazenar preços da Amazon
        self.preco_zomm = []
        
    def start(self):
        self.driver = None
        self.wait = None
        self.open()
        self.goForPrice()
        self.goForPrice2()
        self.goForPrice3()
        self.sendemail()
        
    def open(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get('https://www.mercadolivre.com.br/')
        
    def goForPrice(self):
        time.sleep(2)
        iptBusca = self.driver.find_element(By.ID, 'cb1-edit')
        iptBusca.send_keys('xbox series x'+ Keys.ENTER)
        time.sleep(1)
        # Captura a URL atual do navegador
        site_atual = self.driver.current_url

        # Localiza todos os preços e nomes dos produtos
        prices = self.driver.find_elements(By.CSS_SELECTOR, '.ui-search-price__part.ui-search-price__part--medium')
        product_elements = self.driver.find_elements(By.CSS_SELECTOR, 'a.ui-search-item__group__element')

        # Mensagem de origem com o site
        print(f"Preços extraídos da página de busca do Xbox Series X no site: {site_atual}\n")
        formatted_message = f"<p>Preços extraídos da página de busca do Xbox Series X no site: {site_atual}</p><br>"
        # Contador de preços encontrados
        count = 0

        # Verifica se a quantidade de preços e produtos é igual
        if len(prices) != len(product_elements):
            print("Aviso: O número de preços e produtos não coincide.")

        for index, price in enumerate(prices):
            try:
                # Pega o valor e o símbolo de reais
                currency_symbol = price.find_element(By.CLASS_NAME, 'andes-money-amount__currency-symbol').text
                fraction = price.find_element(By.CLASS_NAME, 'andes-money-amount__fraction').text

                if 'parcelado' not in price.text.lower():
                  if index < len(product_elements):
                    product_name = product_elements[index].get_attribute('title')
                    if "xbox series x" in product_name.lower():
                        # Pega o valor e o símbolo de reais
                        try:
                            price_value = float(fraction.replace('.', '').replace(',', '.'))  # Converte o preço para float
                            if price_value >= 3000:
                                count += 1
                                preco_info = f'{count}. {product_name} - {currency_symbol} {fraction}'
                                formatted_message += preco_info
                                self.preco_ml.append(preco_info)
                        except ValueError:
                            print("Erro ao converter o valor do preço.")               
            except Exception as e:
                print("Erro ao processar o preço:", e)
        formatted_message += f"<br><p><b>Total de preços encontrados:</b> {count}</p>"
        print(f"\nTotal de preços encontrados: {count}")
        
    def goForPrice2(self):
        time.sleep(1)
        # Abre uma nova aba
        self.driver.execute_script("window.open('');")
        # Alterna para a nova aba (a última aberta)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get('https://www.amazon.com.br/')
        time.sleep(3)

        # Encontra a caixa de pesquisa e faz a busca
        iptBusca = self.driver.find_element(By.ID, 'twotabsearchtextbox')
        iptBusca.send_keys('xbox series x' + Keys.ENTER)
        time.sleep(1)

        # Captura a URL atual do navegador
        site_atual = self.driver.current_url
        print(f"Preços extraídos da página de busca do Xbox Series X no site: {site_atual}\n")

        # Localiza todos os preços e nomes dos produtos
        price_elements = self.driver.find_elements(By.CSS_SELECTOR, '.a-price-whole')
        name_elements = self.driver.find_elements(By.CSS_SELECTOR, '.a-size-base-plus.a-color-base.a-text-normal')

        # Verifica se a quantidade de preços e produtos é igual
        if len(price_elements) != len(name_elements):
            print("Aviso: O número de preços e produtos não coincide.")

        count = 0
        formatted_message = f"<p>Preços extraídos da página de busca do Xbox Series X no site: {site_atual}</p><br>"
        for index, price_element in enumerate(price_elements):
            try:
                # Pega o valor do preço e formata
                price = price_element.text
                if index < len(name_elements):
                    product_name = name_elements[index].text

                    # Verifica se o nome do produto contém "Xbox Series X"
                    if "xbox series x" in product_name.lower():
                        try:
                            # Converte o preço para float
                            price_value = float(price.replace('.', '').replace(',', '.'))

                            # Verifica se o preço é maior ou igual a R$ 3000
                            if price_value >= 3000:
                                count += 1
                                preco_info = f'{count}. {product_name} - R$ {price}'
                                formatted_message += preco_info
                                self.preco_amazon.append(preco_info)
                        except ValueError:
                            print("Erro ao converter o valor do preço.")

            except Exception as e:
                print("Erro ao processar o preço:", e)
        formatted_message += f"<br><p><b>Total de preços encontrados:</b> {count}</p>"
        print(f"\nTotal de preços encontrados: {count}")


    def goForPrice3(self):
        time.sleep(1)
        # Abre uma nova aba
        self.driver.execute_script("window.open('');")
        # Alterna para a nova aba (a última aberta)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get('https://www.zoom.com.br/')
        time.sleep(3)

        # Encontra a caixa de pesquisa e faz a busca
        iptBusca = self.driver.find_element(By.XPATH, '/html/body/div[1]/main/header/div[1]/div/div/div[3]/div/div/div[2]/div/div[1]/input')
        iptBusca.send_keys('xbox series x' + Keys.ENTER)
        time.sleep(1)

        # Captura a URL atual do navegador
        site_atual = self.driver.current_url
        print(f"Preços extraídos da página de busca do Xbox Series X no site: {site_atual}\n")

        # Localiza todos os preços e nomes dos produtos
        price_elements = self.driver.find_elements(By.CSS_SELECTOR, 'p.Text_Text__ARJdp.Text_MobileHeadingS__HEz7L[data-testid="product-card::price"]')
        name_elements = self.driver.find_elements(By.CSS_SELECTOR, 'h2.Text_Text__ARJdp.Text_MobileLabelXs__dHwGG.Text_DesktopLabelSAtLarge__wWsED')

        # Verifica se a quantidade de preços e produtos é igual
        if len(price_elements) != len(name_elements):
            print("Aviso: O número de preços e produtos não coincide.")

        count = 0
        formatted_message = f"<p>Preços extraídos da página de busca do Xbox Series X no site: {site_atual}</p><br>"
        for index, price_element in enumerate(price_elements):
            try:
                # Pega o valor do preço
                preco_str = price_element.text
                print(f"Preço extraído: {preco_str}")  # Adiciona um log para verificar o preço
                preco = extrair_preco(preco_str)
                if preco is not None:
                    print(f"Preço convertido: {preco}")
                    if preco >= 3000:
                        if index < len(name_elements):
                            product_name = name_elements[index].text
                            count += 1
                            preco_info = f'{count}. {product_name} - R$ {preco_str}'
                            formatted_message += preco_info + '<br>'
                            self.preco_zomm.append(preco_info)
                else:
                    print("Falha ao converter o preço.")
            except Exception as e:
                print("Erro ao processar o preço:", e)
        formatted_message += f"<br><p><b>Total de preços encontrados:</b> {count}</p>"
        print(f"\nTotal de preços encontrados: {count}")



    def sendemail(self):
        from_email = "matheusmartinsnoclaf@gmail.com"
        password = "nzdk fmzr qecl rqkt"
        to_email = "xmatheusclm@gmail.com"
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = "Atualização de Preços"
        
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        
        body = f"""
        <html>
            <body>
                <p><b>Atualização de preços - {timestamp}</b></p>
                <br>
                <p><b>Preços extraídos do Mercado Livre:</b></p>
                <p>{'<br>'.join(self.preco_ml)}</p>
                <br>
                <p><b>Preços extraídos da Amazon:</b></p>
                <p>{'<br>'.join(self.preco_amazon)}</p>
                <br>
                <p><b>Preços extraídos do Zoom:</b></p>
                <p>{'<br>'.join(self.preco_zomm)}</p>
                <br>
            </body>
        </html>
        """ 
        msg.attach(MIMEText(body, 'html'))

        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()    
        
    import re

def extrair_preco(preco_str):
    try:
        # Remove o símbolo de moeda e espaços
        preco_limpo = preco_str.replace('').replace(' ', '')
        # Remove pontos de milhar e substitui a vírgula por ponto decimal
        preco_limpo = preco_limpo.replace('.', '').replace(',', '.')
        return float(preco_limpo)
    except ValueError:
        print("Erro ao converter o valor do preço:", preco_str)
        return None

            
if __name__ == "__main__":
    bot = preco()
    bot.start()