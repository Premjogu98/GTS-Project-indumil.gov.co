from selenium import webdriver
import time
import html
import sys, os
from datetime import datetime,timedelta
import Global_var
import wx
import string
import html
import re
from Insert_On_Datbase import insert_in_Local

app = wx.App()

def ChromeDriver():
    browser = webdriver.Chrome(executable_path=str(f"C:\\chromedriver.exe"))
    browser.get("https://www.indumil.gov.co/INDUMIL.Consulta.Procesos/Inicio.aspx")
    browser.maximize_window()
    time.sleep(5)
    loop = True
    page_count = 2
    while loop == True:
        try:
            tr_count = 0
            for tr in browser.find_elements_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_procesosGridView"]/tbody/tr'):
                if tr_count >= 3:
                    opening_date = ''
                    for opening_date in browser.find_elements_by_xpath(f'//*[@id="ctl00_ContentPlaceHolder1_procesosGridView"]/tbody/tr[{str(tr_count)}]/td[5]'):
                        opening_date = opening_date.get_attribute('innerText').replace('p.','').replace('a.','').replace('m.','').strip()
                        break

                    datetime_object = datetime.strptime(opening_date, '%d-%b-%Y %H:%M')
                    publish_date = datetime_object.strftime("%d-%m-%Y")

                    datetime_object_pub = datetime.strptime(publish_date, '%d-%m-%Y')
                    User_Selected_date = datetime.strptime(str(Global_var.From_Date), '%d-%m-%Y')

                    timedelta_obj = datetime_object_pub - User_Selected_date
                    day = timedelta_obj.days
                    if day >= 0:
                        print('Publish Date Alive')
                        for tender_link in browser.find_elements_by_xpath(f'//*[@id="ctl00_ContentPlaceHolder1_procesosGridView"]/tbody/tr[{str(tr_count)}]/td[1]/input'):
                            tender_link.click()
                            break
                        scrap_data(browser)
                        Global_var.Total +=1
                        print(f'Total: {str(Global_var.Total)} Deadline Not given: {Global_var.deadline_Not_given} duplicate: {Global_var.duplicate} inserted: {Global_var.inserted} expired: {Global_var.expired} QC Tenders: {Global_var.QC_Tenders}')
                        browser.back()
                        time.sleep(2)
                    else:
                        print('Publish Date Dead')
                        wx.MessageBox(f'Total: {str(Global_var.Total)}\nDeadline Not given: {Global_var.deadline_Not_given}\nduplicate: {Global_var.duplicate}\ninserted: {Global_var.inserted}\nexpired: {Global_var.expired}\nQC Tenders: {Global_var.QC_Tenders}','hankintailmoitukset.fi', wx.OK | wx.ICON_INFORMATION)
                        browser.close()
                        sys.exit()
                tr_count += 1
            for next_page in browser.find_elements_by_xpath(f"//*[@class='EstiloPagina']/td/table/tbody/tr/td[{str(page_count)}]"): 
                next_page.click()
                break
            page_count += 1
            loop == False
        except Exception as e:
            exc_type , exc_obj , exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : " , sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname , "\n" ,exc_tb.tb_lineno)
            loop == True

def scrap_data(browser):
    SegField = []
    for data in range(42):
        SegField.append('')
    error = False
    while error == False:
        try:
            get_htmlsource = ''
            for get_htmlsource in browser.find_elements_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_procesoAdquisicionFormView"]/tbody/tr/td/table[1]'):
                get_htmlsource = get_htmlsource.get_attribute('outerHTML').strip().replace('<!---->','').replace('-\t','').replace('-\n','').replace('\t','').replace('\n','')
                break
            
            SegField[1] = 'indumil@indumil.gov.co'
            SegField[2] = 'AA 7272, Bogota DC, Colombia, Tel: (57-1) 2207821 - 2207807 / 018000912986, Fax: (57-1) 2225786'
            SegField[8] = 'https://www.indumil.gov.co/'
            SegField[12] = 'INDUMIL'

            for tender_no in browser.find_elements_by_xpath(f'//*[@id="ctl00_ContentPlaceHolder1_procesoAdquisicionFormView_pad_idLabel"]'):
                tender_no = tender_no.get_attribute('innerText').strip()
                SegField[13] = tender_no
                break

            for Title in browser.find_elements_by_xpath(f'//*[@id="ctl00_ContentPlaceHolder1_procesoAdquisicionFormView_Label1"]'):
                Title = Title.get_attribute('innerText').strip()
                Title = string.capwords(str(Title))
                SegField[19] = Title
                break
            Amount = ''
            Coin = ''
            Copy_value = ''
            Obtaining_place = ''
            Place_of_presentation = ''
            Presentation_city = ''
            Delivery_address = ''
            Opening_date=  ''
            Way_to_pay = ''
            Delivery_term = ''
            for Amount in browser.find_elements_by_xpath(f'//*[@id="ctl00_ContentPlaceHolder1_procesoAdquisicionFormView_Label2"]'):
                Amount = Amount.get_attribute('innerText').strip()
                break
            for Coin in browser.find_elements_by_xpath(f'//*[@id="ctl00_ContentPlaceHolder1_procesoAdquisicionFormView_Label3"]'):
                Coin = Coin.get_attribute('innerText').strip()
                break
            for Copy_value in browser.find_elements_by_xpath(f'//*[@id="ctl00_ContentPlaceHolder1_procesoAdquisicionFormView_Label4"]'):
                Copy_value = Copy_value.get_attribute('innerText').strip()
                break
            for Obtaining_place in browser.find_elements_by_xpath(f'//*[@id="ctl00_ContentPlaceHolder1_procesoAdquisicionFormView_Label5"]'):
                Obtaining_place = Obtaining_place.get_attribute('innerText').strip()
                break
            for Place_of_presentation in browser.find_elements_by_xpath(f'//*[@id="ctl00_ContentPlaceHolder1_procesoAdquisicionFormView_Label6"]'):
                Place_of_presentation = Place_of_presentation.get_attribute('innerText').strip()
                break
            for Presentation_city in browser.find_elements_by_xpath(f'//*[@id="ctl00_ContentPlaceHolder1_procesoAdquisicionFormView_Label7"]'):
                Presentation_city = Presentation_city.get_attribute('innerText').strip()
                break
            for Delivery_address in browser.find_elements_by_xpath(f'//*[@id="ctl00_ContentPlaceHolder1_procesoAdquisicionFormView_Label8"]'):
                Delivery_address = Delivery_address.get_attribute('innerText').strip()
                break
            for Opening_date in browser.find_elements_by_xpath(f'//*[@id="ctl00_ContentPlaceHolder1_procesoAdquisicionFormView_Label10"]'):
                Opening_date = Opening_date.get_attribute('innerText').strip()
                break
            for Way_to_pay in browser.find_elements_by_xpath(f'//*[@id="ctl00_ContentPlaceHolder1_procesoAdquisicionFormView_Label13"]'):
                Way_to_pay = Way_to_pay.get_attribute('innerText').strip()
                break
            for Delivery_term in browser.find_elements_by_xpath(f'//*[@id="ctl00_ContentPlaceHolder1_procesoAdquisicionFormView_Label14"]'):
                Delivery_term = Delivery_term.get_attribute('innerText').strip()
                break

            SegField[18] = f'{SegField[19]}<br>\nAmount: {Amount}<br>\nCoin: {Coin}<br>\nCopy value: {Copy_value}<br>\nObtaining Place: {Obtaining_place}<br>\nPlace Of Presentation: {Place_of_presentation}<br>\nPresentation City: {Presentation_city}<br>\nDelivery Address: {Delivery_address}<br>\nOpening Date: {Opening_date}<br>\nWay To Pay: {Way_to_pay}<br>\nDelivery Term: {Delivery_term}'
            
            
            for Deadline in browser.find_elements_by_xpath(f'//*[@id="ctl00_ContentPlaceHolder1_procesoAdquisicionFormView_Label11"]'):
                Deadline = Deadline.get_attribute('innerText').replace('p.','').replace('a.','').replace('m.','').strip()
                datetime_object = datetime.strptime(Deadline, '%d-%b-%Y %H:%M')
                Deadline = datetime_object.strftime("%Y-%m-%d")
                SegField[24] = Deadline.strip()
                break

            SegField[14] = '2'
            SegField[22] = "0"
            SegField[26] = "0.0"
            SegField[27] = "0"  # Financier
            SegField[7] = 'CO'
            SegField[28] = 'https://www.indumil.gov.co/INDUMIL.Consulta.Procesos/Inicio.aspx'
            SegField[31] = 'indumil.gov.co'
            
            for tender_link in browser.find_elements_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_procesoAdquisicionFormView_documentosButton"]'):
                tender_link.click()
                break
            time.sleep(2)
            for Doument_get_htmlsource in browser.find_elements_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_documentosGridView"]'):
                Doument_get_htmlsource = Doument_get_htmlsource.get_attribute('outerHTML').strip().replace('<!---->','').replace('-\t','').replace('-\n','').replace('\t','').replace('\n','')
                get_htmlsource += Doument_get_htmlsource
                break
            time.sleep(2)
            browser.back()
            for SegIndex in range(len(SegField)):
                print(SegIndex, end=' ')
                print(SegField[SegIndex])
                SegField[SegIndex] = html.unescape(str(SegField[SegIndex]))
                SegField[SegIndex] = str(SegField[SegIndex]).replace("'", "''")

            if len(SegField[19]) >= 200:
                SegField[19] = str(SegField[19])[:200]+'...'

            if len(SegField[18]) >= 1500:
                SegField[18] = str(SegField[18])[:1500]+'...'

            if SegField[19] == '':
                wx.MessageBox(' Short Desc Blank ','indumil.gov.co', wx.OK | wx.ICON_INFORMATION)
            else:
                check_date(get_htmlsource, SegField)
                pass
            error = True
        except Exception as e:
            exc_type , exc_obj , exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : " , sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname , "\n" ,exc_tb.tb_lineno)
            error = False

def check_date(get_htmlSource, SegField):
    deadline = str(SegField[24])
    curdate = datetime.now()
    curdate_str = curdate.strftime("%Y-%m-%d")
    try:
        if deadline != '':
            datetime_object_deadline = datetime.strptime(deadline, '%Y-%m-%d')
            datetime_object_curdate = datetime.strptime(curdate_str, '%Y-%m-%d')
            timedelta_obj = datetime_object_deadline - datetime_object_curdate
            day = timedelta_obj.days
            if day > 0:
                insert_in_Local(get_htmlSource, SegField)
            else:
                print("Expired Tender")
                Global_var.expired += 1
        else:
            print("Deadline Not Given")
            Global_var.deadline_Not_given += 1
    except Exception as e:
        exc_type , exc_obj , exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error ON : " , sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname , "\n" ,exc_tb.tb_lineno)


ChromeDriver()