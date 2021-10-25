import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_bootstrap_components as dbc  
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import xlsxwriter

import json
with open('tr-cities-utf8_v1.json',encoding="utf8") as response:
    counties = json.load(response)
    
df = pd.read_csv('il_verisi_8.csv',sep=',',encoding='latin-1')
df1=df.copy()

df.rename(columns={"il":"İl Adı"},inplace=True)
df.rename(columns={"yil":"Yıl"},inplace=True)

df1=df1.drop(['plaka_kodu','location_code'],axis=1)

app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.CERULEAN],
                meta_tags=[{'name':     'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

server = app.server

all_options = {
    'BANKACILIK': ['Banka Calisan Sayisi', 'ATM Sayisi', 'Pos Sayisi','Uye Isyeri Sayisi', 'Kredi', 'Mevduat'],
    'EGITIM': [u'Okul oncesi / Derslik','Okul oncesi / Erkek ogrenci','Okul oncesi / Erkek ogretmen','Okul oncesi / Kadin ogretmen','Okul oncesi / Kiz ogrenci','Okul oncesi / Okul','Okul oncesi / Sube','Genel Ortaogretim / Derslik','Ilkokul / Derslik','Mesleki ve teknik ortaogretim / Derslik','Ortaokul / Derslik','Genel ortaogretim / Derslik Basina Ogrenci Sayisi','Ilk ve ortaokul / Derslik Basina Ogrenci Sayisi','Mesleki ve teknik ortaogretim / Derslik Basina Ogrenci Sayisi','Toplam ortaogretim / Derslik Basina Ogrenci Sayisi','Genel ortaogretim / Ogretmen Basina Ogrenci Sayisi','Ilkokul / Ogretmen Basina Ogrenci Sayisi','Mesleki ve teknik ortaogretim / Ogretmen Basina Ogrenci Sayisi','Ortaokul / Ogretmen Basina Ogrenci Sayisi','Toplam ortaogretim / Ogretmen Basina Ogrenci Sayisi','Toplam ortaogretim / Okul Basina Ogrenci Sayisi','Ortaokul / Sube Basina Ogrenci Sayisi','Toplam ortaogretim / Sube Basina Ogrenci Sayisi','Diger ogretim elemani','Docent','Doktora mezunu / Erkek','Doktora mezunu / Kadin','Doktora mezunu / Toplam','Yuksekogretim Okuyan Ogrenci','Yuksekogretim Mezun Ogrenci','Profesor','Toplam ogretim elemani','Yuksekogretim Yeni Kayit Ogrenci Sayisi','Yuksek lisans mezunu / Erkek','Yuksek lisans mezunu / Kadin','Yuksek lisans mezunu / Toplam'],
    'EKONOMI': [u'Ihracat', 'Ithalat','Ulke Ihracat Payi', 'Ulke Ithalat Payi', 'Dusuk Teknolojili','Orta-Dusuk Teknolojili', 'Orta-Yuksek Teknolojili','Yuksek Teknolojili', 'Kisi basina GSYH (TL)','Kisi basina GSYH ($)', 'Tarim GSYH', 'Sanayi GSYH','Hizmetler GSYH', 'GSYH', 'Tarim GSYH Payi', 'Sanayi GSYH Payi','Hizmetler GSYH Payi'],
    'GOC': [u'Aldigi Goc','Verdigi Goc','Net Goc','Net Goc Hizi (Binde)'],
    'HABERLESME-ILETISIM': [u'Fiber Abone Sayisi','Fiber-Optik Kablo Uzunlugu-km ','Genisbant Internet Abone Sayisi','Kablo TV Abone Sayisi','Mobil Cepten Internet','Mobil Genisbant Internet Abone Sayisi','Mobil Telefon Abone Sayisi - 2N','Mobil Telefon Abone Sayisi  3N+4.5N','Mobil Telefon Abone Sayisi - Toplam','Sabit Genisbant Internet Abone Sayisi'],
    'HAYVANCILIK': [u'Canli hayvanlar  : Dana ve buzagi: erkek (bas)','Canli hayvanlar  : Dana ve buzagi: disi (bas)','Canli hayvanlar  : Tosun: 1-2 yas (bas)','Canli hayvanlar  : Duve: 1-2 yas (bas)','Canli hayvanlar  : Inek: 2 yas ve uzeri (bas)','Canli hayvanlar  : Boga ve okuz: 2 yas ve uzeri (bas)','Canli hayvanlar  : Manda (bas)','Canli hayvanlar  : Deve (bas)','Canli hayvanlar  : Domuz (bas)','Canli hayvanlar  : Koyun (bas)','Canli hayvanlar  : Keci (bas)','Canli hayvanlar  : At-katir ve esek (bas)','Canli hayvanlar  : Kumes hayvani (bas)','Hayvansal urunler : Inek sutu (ton)','Hayvansal urunler : Manda sutu (ton)','Hayvansal urunler : Koyun sutu (ton)','Hayvansal urunler : Keci sutu (ton)','Hayvansal urunler : Bal (ton)'],
    'KULTUR': [u'Sinema Seyirci sayisi','Tiyatro Seyirci sayisi','Halk kutuphaneleri : Bin kisi basina yararlanma sayisi','Muze ve oren yeri ziyaretci sayisi','Ozel muzeler Ziyaretci sayisi'],
    'NUFUS': [u'Toplam nufus','Nufus 90+ yas / Toplam','Nufus Erkek','Nufus Kadin','Nufus 00-4 yas / Toplam','Nufus 00-4 yas / Erkek','Nufus 00-4 yas / Kadin','Nufus 90+ yas / Erkek','Nufus 90+ yas / Kadin','Toplam yas bagimlilik orani','Yasli bagimlilik orani (65+ yas)','Genc bagimlilik orani (0-14 yas)','Nufus yogunlugu (kilometrekareye dusen kisi sayisi)','Bosandi / Toplam (15 ve uzeri yas)','Bosandi / Erkek (15 ve uzeri yas)','Bosandi / Kadin (15 ve uzeri yas)','Yillik nufus artis hizi (binde)','Ortalama hanehalki buyuklugu','Genc nufusun (15-24 yas grubu) toplam nufus icindeki orani (%)','Cocuk nufusun toplam nufus icindeki orani (%)','Hanehalki tiplerine gore hanehalki sayisi : Tek kisilik hanehalki','Hanehalki tiplerine gore hanehalki sayisi : Cekirdek aileden olusan hanehalki','Hanehalki tiplerine gore hanehalki sayisi : Genis aileden olusan hanehalki','Hanehalki tiplerine gore hanehalki sayisi : Cekirdek aile bulunmayan hanehalki','Nufus Projeksiyonu : Nufus projeksiyonu','Ortanca Yas/Erkek','Ortanca Yas/Toplam','Ortanca Yas/Kadin'],
    'SAGLIK': [u'Hastane ve yatak sayilari : Toplam  / Kurum Sayisi','Hastane ve yatak sayilari : Toplam  / Yatak Sayisi','Hastane ve yatak sayilari : Saglik Bakanligi / Kurum Sayisi','Hastane ve yatak sayilari : Saglik Bakanligi  / Yatak Sayisi','Hastane ve yatak sayilari : Universite / Kurum Sayisi','Hastane ve yatak sayilari : Universite  / Yatak Sayisi','Hastane ve yatak sayilari : Ozel  / Kurum Sayisi','Hastane ve yatak sayilari : Ozel  / Yatak Sayisi','Hastane ve yatak sayilari : Diger Kamu / Kurum Sayisi','Hastane ve yatak sayilari : Diger Kamu  / Yatak Sayisi','Yuzbin kisi basina toplam hastane yatak sayisi','Saglik personeli sayisi : Uzman Hekim','Saglik personeli sayisi : Pratisyen Hekim','Saglik personeli sayisi : Asistan Hekim','Saglik personeli sayisi : Toplam Hekim','Saglik personeli sayisi : Dis Hekimi','Saglik personeli sayisi : Eczaci','Saglik personeli sayisi : Diger saglik personeli','Saglik personeli sayisi : Hemsire','Saglik personeli sayisi : Ebe'],
    'SIRKET': [u'Kurulan Sirket','Tasfiye Edilen Sirket','Kapanan Sirket'],
    'TARIM': [u'Toplam islenen tarim alani ve uzun omurlu bitkiler (hektar)','Tarimsal uretim degeri  : Bitkisel uretim degeri  (1000 TL)','Tarimsal uretim degeri  : Canli hayvanlar degeri (1000 TL)','Tarimsal uretim degeri  : Hayvansal urunler degeri (1000 TL)','Alan kullanimi  : Toplam islenen tarim alani (hektar)','Alan kullanimi  : Islenen tarim alani / Ekilen (hektar)','Alan kullanimi  : Islenen tarim alani / Sebze (hektar)','Alan kullanimi  : Toplam uzun omurlu bitkilerin alani (hektar)','Alan kullanimi  : Uzun omurlu bitkiler  / Bag alani (hektar)','Alan kullanimi  : Uzun omurlu bitkiler / Meyveler-icecek ve baharat bitkileri alani (hektar)','Alan kullanimi  : Uzun omurlu bitkiler / Zeytin agaclarinin kapladigi alani (hektar)','Alan kullanimi  : Islenen tarim alani / Nadas (hektar)','Alan kullanimi  : Yem bitkileri (hektar)','Ortu alti sebze ve meyve uretimi (ton) : Toplam','Ortu alti sebze ve meyve uretimi (ton) : Biber','Ortu alti sebze ve meyve uretimi (ton) : Cilek','Ortu alti sebze ve meyve uretimi (ton) : Domates','Ortu alti sebze ve meyve uretimi (ton) : Fasulye (Taze)','Ortu alti sebze ve meyve uretimi (ton) : Hiyar','Ortu alti sebze ve meyve uretimi (ton) : Kabak (Sakiz)','Ortu alti sebze ve meyve uretimi (ton) : Karpuz','Ortu alti sebze ve meyve uretimi (ton) : Kavun','Ortu alti sebze ve meyve uretimi (ton) : Marul','Ortu alti sebze ve meyve uretimi (ton) : Muz','Ortu alti sebze ve meyve uretimi (ton) : Patlican','Ortu alti sebze ve meyve uretimi (ton) : Diger','Niteliklerine gore ortu alti tarim alanlari (dekar) : Toplam','Niteliklerine gore ortu alti tarim alanlari (dekar) : Cam sera','Niteliklerine gore ortu alti tarim alanlari (dekar) : Plastik sera','Niteliklerine gore ortu alti tarim alanlari (dekar) : Yuksek tunel','Niteliklerine gore ortu alti tarim alanlari (dekar) : Alcak tunel','Tarimsal alet ve makineler : Pulluk','Tarimsal alet ve makineler : Ekim makinesi','Tarimsal alet ve makineler : Gubre dagitma makinesi','Tarimsal alet ve makineler : Su pompasi','Tarimsal alet ve makineler : Sabit sut sagim tesisi','Tarimsal alet ve makineler : Seyyar sut sagim makinesi','Tarimsal alet ve makineler : Bicerdover','Tarimsal alet ve makineler : Traktor','Organik bitkisel uretim (gecis sureci dahil) : Ciftci sayisi','Organik bitkisel uretim (gecis sureci dahil) : Uretim alani (Hektar)','Organik bitkisel uretim (gecis sureci dahil) : Uretim  (Ton)','Tarimsal uretim degeri  : Kisi basina bitkisel uretim degeri (TL)','Tarimsal uretim degeri  : Kisi basina canli hayvanlar degeri (TL)','Tarimsal uretim degeri  : Kisi basina hayvansal urunler degeri (TL)','Alan kullanimi  : Sus bitkileri (hektar)','Tahillar ve diger bitkisel urunlerin hasat edilen alani (hektar) : Toplam','Tahillar ve diger bitkisel urunlerin hasat edilen alani (hektar) : Islenmemis tutun','Tahillar ve diger bitkisel urunlerin hasat edilen alani (hektar) : Parfumeri-eczacilik vb.bitkiler-sekerpancari ve yem bitkileri tohumlari','Tahillar ve diger bitkisel urunlerin hasat edilen alani (hektar) : Patates-kuru baklagiller-yenilebilir kok ve yumrular','Tahillar ve diger bitkisel urunlerin hasat edilen alani (hektar) : Saman ve ot (yem bitkileri)','Tahillar ve diger bitkisel urunlerin hasat edilen alani (hektar) : Seker imalatinda kullanilan bitkiler (seker pancari)','Tahillar ve diger bitkisel urunlerin hasat edilen alani (hektar) : Tahillar','Tahillar ve diger bitkisel urunlerin hasat edilen alani (hektar) : Tekstilde kullanilan ham bitkiler','Tahillar ve diger bitkisel urunlerin hasat edilen alani (hektar) : Yagli tohumlar','Tahillar ve diger bitkisel urunlerin uretim miktari (ton) : Toplam','Tahillar ve diger bitkisel urunlerin uretim miktari (ton) : Islenmemis tutun','Tahillar ve diger bitkisel urunlerin uretim miktari (ton) : Parfumeri-eczacilik vb.bitkiler-sekerpancari ve yem bitkileri tohumlari','Tahillar ve diger bitkisel urunlerin uretim miktari (ton) : Patates-kuru baklagiller-yenilebilir kok ve yumrular','Tahillar ve diger bitkisel urunlerin uretim miktari (ton) : Saman ve ot (yem bitkileri)','Tahillar ve diger bitkisel urunlerin uretim miktari (ton) : Seker imalatinda kullanilan bitkiler (seker pancari)','Tahillar ve diger bitkisel urunlerin uretim miktari (ton) : Tahillar','Tahillar ve diger bitkisel urunlerin uretim miktari (ton) : Tekstilde kullanilan ham bitkiler','Tahillar ve diger bitkisel urunlerin uretim miktari (ton) : Yagli tohumlar','Ekilen Alan (Dekar)-Bugday-Durum Bugdayi Haric','Ekilen Alan (Dekar)-Durum Bugdayi','Ekilen Alan (Dekar)-Misir','Ekilen Alan (Dekar)-Arpa (Biralik)','Ekilen Alan (Dekar)-Arpa (Diger)','Ekilen Alan (Dekar)-Aycicegi Tohumu (Yaglik)','Ekilen Alan (Dekar)-Kanola Veya Kolza Tohumu','Ekilen Alan (Dekar)-Aycicegi Tohumu (Cerezlik)','Ekilen Alan (Dekar)-Celtik','Ekilen Alan (Dekar)-Seker Pancari','Ekilen Alan (Dekar)-Misir (Hasil)','Ekilen Alan (Dekar)-Misir (Slaj)','Ekilen Alan (Dekar)-Adacayi','Ekilen Alan (Dekar)-Lavanta','Ekilen Alan (Dekar)-Gul-Yaglik','Uretim Miktari (Ton)-Durum Bugdayi','Uretim Miktari (Ton)-Bugday-Durum Bugdayi Haric','Uretim Miktari (Ton)-Misir','Uretim Miktari (Ton)-Arpa (Biralik)','Uretim Miktari (Ton)-Arpa (Diger)','Uretim Miktari (Ton)-Kanola Veya Kolza Tohumu','Uretim Miktari (Ton)-Aycicegi Tohumu (Yaglik)','Uretim Miktari (Ton)-Aycicegi Tohumu (Cerezlik)','Uretim Miktari (Ton)-Celtik','Uretim Miktari (Ton)-Seker Pancari','Uretim Miktari (Ton)-Misir (Hasil)','Uretim Miktari (Ton)-Misir (Slaj)','Uretim Miktari (Ton)-Adacayi','Uretim Miktari (Ton)-Lavanta','Uretim Miktari (Ton)-Gul-Yaglik','Verim (Kg/Dekar)-Durum Bugdayi','Verim (Kg/Dekar)-Bugday-Durum Bugdayi Haric','Verim (Kg/Dekar)-Misir','Verim (Kg/Dekar)-Arpa (Biralik)','Verim (Kg/Dekar)-Arpa (Diger)','Verim (Kg/Dekar)-Kanola Veya Kolza Tohumu','Verim (Kg/Dekar)-Aycicegi Tohumu (Yaglik)','Verim (Kg/Dekar)-Aycicegi Tohumu (Cerezlik)','Verim (Kg/Dekar)-Celtik','Verim (Kg/Dekar)-Seker Pancari','Verim (Kg/Dekar)-Misir (Hasil)','Verim (Kg/Dekar)-Misir (Slaj)','Verim (Kg/Dekar)-Adacayi','Verim (Kg/Dekar)-Lavanta','Verim (Kg/Dekar)-Gul-Yaglik'],
    'TURIZM': [u'Belediye Belgeli konaklama tesislerinde - Geceleme sayisi / Toplam','Belediye Belgeli konaklama tesislerinde - Geceleme sayisi / Yabanci','Belediye Belgeli konaklama tesislerinde - Geceleme sayisi / Vatandas','Turizm Isletme Belgeli konaklama tesislerinde - Geceleme sayisi / Toplam','Turizm Isletme Belgeli konaklama tesislerinde - Geceleme sayisi / Yabanci','Turizm Isletme Belgeli konaklama tesislerinde - Geceleme sayisi / Vatandas','Giris yapan vatandaslar : Hava yolu','Giris yapan vatandaslar : Demir yolu','Giris yapan vatandaslar : Kara yolu','Giris yapan vatandaslar : Deniz yolu','Cikis yapan vatandaslar : Hava yolu','Cikis yapan vatandaslar : Demir yolu','Cikis yapan vatandaslar : Kara yolu','Cikis yapan vatandaslar : Deniz yolu','Giris yapan yabancilar : Hava yolu','Giris yapan yabancilar : Demir yolu','Giris yapan yabancilar : Kara yolu','Giris yapan yabancilar : Deniz yolu','Giris yapan yabancilar : Gunubirlik','Cikis yapan yabancilar : Hava yolu','Cikis yapan yabancilar : Demir yolu','Cikis yapan yabancilar : Kara yolu','Cikis yapan yabancilar : Deniz yolu','Cikis yapan yabancilar : Gunubirlik'],
    'ULASIM': [u'Trafik kazalari : Kaza sayisi','Trafik kazalari : Olu sayisi','Trafik kazalari : Yarali sayisi','Bir milyon nufusta trafik kazalarinda olu sayisi','Bir milyon nufusta trafik kazalarinda yarali sayisi','Bir milyon nufusta trafik kaza sayisi','Bin kisi basina otomobil sayisi','Inis-kalkis yapan ucak sayisi / Toplam','Inis-kalkis yapan ucak sayisi / Turk','Inis-kalkis yapan ucak sayisi / Yabanci','Inis-kalkis yapan ucak sayisi / Diger','Havaalani Yolcu Sayisi / Toplam','Havaalani Yolcu Sayisi / Ic hat gelen','Havaalani Yolcu Sayisi / Ic hat giden','Havaalani Yolcu Sayisi / Dis hat gelen','Havaalani Yolcu Sayisi / Dis hat giden'],
    'VERGI': [u'Vergi Tahakkuk','Vergi Tahsilat'],   
}

app.layout = dbc.Container([
    
    dbc.Row([

        dbc.Col([
            html.H5("Aranan Veri-(Saçılım Grafiğinde Y Ekseni)",
                    className='text-start text-primary mr-4'),
            dcc.Dropdown(
                id='countries-dropdown',
                options=[{'label': k, 'value': k} for k in all_options.keys()],
                value='NUFUS'
                ),
            
            dcc.Dropdown(id='cities-dropdown'),
                      
        ],
            xs=12, sm=12, md=12, lg=12, xl=12
        ),

        dbc.Col([
            html.Hr(),

            dcc.Slider(id = 'slider_year',
                       included = True,
                       updatemode='drag',
                       tooltip={'always_visible': True},
                       min = 2010,
                       max = 2019,
                       step = 1,
                       value = 2019,
                       marks = {str(yr): str(yr) for yr in range(2010, 2020, 1)},
                       className = 'dcc_compon')            
        ],
           xs=12, sm=12, md=12, lg=12, xl=12
        ),
                  
    ],
        style={"position": "fixed",
             "z-index": "999", "background": "#EDF0F6", 
             "width": "99%",
                },
        ),

    html.Hr(),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='my_bee_map', figure={},
                      ),
        ],
           xs=12, sm=12, md=12, lg=11, xl=11
        )
    ], align="center",style={'marginTop': 180}),

    html.Hr(),

    dbc.Row([

        dbc.Col([
            html.H5("Bar Grafiği",
                    className='text-start text-primary mr-4'),
            dcc.Graph(id='bar_graph', figure={}),
        ],
           xs=12, sm=12, md=12, lg=12, xl=12
        ),
                       
    ], align="center"),

    html.Hr(),
    
    dbc.Row([

        dbc.Col([
            html.H5("Ağaç Haritası",
                    className='text-start text-primary mr-4'),
            dcc.Graph(id='tree_map', figure={},
                      ),
        ],
           xs=12, sm=12, md=12, lg=12, xl=12
        )
    ], align="start"),

    html.Hr(),

    dbc.Row([

        dbc.Col([                        
            html.H5("Saçılım Grafiği",
                    className='text-start text-primary mr-4'),  
            dcc.Graph(id='polinom_graph', figure={}),
        ],
           xs=12, sm=12, md=12, lg=12, xl=12
        ),
               
    ], align="start"),

    dbc.Row([
        
        dbc.Col([
                        
            html.H5("X Ekseni",
                    className='text-right text-primary mt-4'),         
                           
        ],
           xs=12, sm=12, md=12, lg=2, xl=2
        ),

        dbc.Col([

            dcc.Dropdown(
                id='countries-dropdown1',
                options=[{'label': k, 'value': k} for k in all_options.keys()],
                value='NUFUS'
                ),
            
            dcc.Dropdown(id='cities-dropdown1', value='Toplam Nufus'),
                              
        ],
           xs=12, sm=12, md=12, lg=7, xl=7
        ),
    ], no_gutters=False, justify='start'),

    html.Hr(),

    dbc.Row([

        dbc.Col([                        
            html.Button("Tüm veritabanını CSV olarak indir", id="btn_csv"),
            dcc.Download(id="download-dataframe-csv"),
        ],
            xs=12, sm=12, md=12, lg=3, xl=3
        ),

        dbc.Col([                        
            html.Button("Tüm veritabanını Excel olarak indir", id="btn_xlsx"),
            dcc.Download(id="download-dataframe-xlsx"),
        ],
            xs=12, sm=12, md=12, lg=3, xl=3
        ),
               
    ], no_gutters=True, justify='center'),
    
    html.Hr(),

    dbc.Row([

        dbc.Col([
            html.Label(['Görüş ve öneri için: ', 
                        html.A('bilgi@trakyaka.org.tr',
                               href='mailto:bilgi@trakyaka.org.tr;eguney@trakyaka.org.tr;ssimsek@trakyaka.org.tr')],
                        className="font-weight-bold text-dark"
                       )   
        ],
           xs=12, sm=12, md=12, lg=4, xl=4
        ),
    ], no_gutters=False, justify='center'),
   
], fluid=True)   

@app.callback(
    dash.dependencies.Output('cities-dropdown', 'options'),
    [dash.dependencies.Input('countries-dropdown', 'value')])
def set_cities_options(selected_country):
    return [{'label': i, 'value': i} for i in all_options[selected_country]]

@app.callback(
    dash.dependencies.Output('cities-dropdown', 'value'),
    [dash.dependencies.Input('cities-dropdown', 'options')])
def set_cities_value(available_options):
    return available_options[0]['value']

@app.callback(
    dash.dependencies.Output('cities-dropdown1', 'options'),
    [dash.dependencies.Input('countries-dropdown1', 'value')])
def set_cities_options1(selected_country1):
    return [{'label': i, 'value': i} for i in all_options[selected_country1]]

@app.callback(
    dash.dependencies.Output('cities-dropdown1', 'value'),
    [dash.dependencies.Input('cities-dropdown1', 'options')])
def set_cities_value1(available_options1):
    return available_options1[0]['value']

@app.callback(
    dash.dependencies.Output("download-dataframe-csv", "data"),
    dash.dependencies.Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,)
def func(n_clicks):
    return dcc.send_data_frame(df1.to_csv, "il_istatistikleri.csv")

@app.callback(
    dash.dependencies.Output("download-dataframe-xlsx", "data"),
    dash.dependencies.Input("btn_xlsx", "n_clicks"),
    prevent_initial_call=True,)
def func1(n_clicks):
    return dcc.send_data_frame(df1.to_excel, "il_istatistikleri.xlsx", sheet_name="Sayfa1")


@app.callback(
    [dash.dependencies.Output('my_bee_map', 'figure'),
     dash.dependencies.Output('bar_graph','figure'),
     dash.dependencies.Output('polinom_graph','figure'),     
     dash.dependencies.Output('tree_map','figure'),
     ],
    [dash.dependencies.Input('countries-dropdown', 'value'),
     dash.dependencies.Input('cities-dropdown', 'value'),
     dash.dependencies.Input('countries-dropdown1', 'value'),
     dash.dependencies.Input('cities-dropdown1', 'value'),
     dash.dependencies.Input('slider_year','value'),
     ],
     )

def update_graph(selected_country,selected_city,selected_country1,selected_city1,slider_year):

    dff = df.copy()
    dff = dff[(dff["anabaslik"]==selected_country)&(dff["baslik"]==selected_city)&(dff["Yıl"]==slider_year)]
    dff1 = df.copy()
    dff1 = dff1[(dff1["anabaslik"]==selected_country1)&(dff1["baslik"]==selected_city1)&(dff1["Yıl"]==slider_year)]
    dff1.rename(columns={"deger":"deger1"},inplace=True)

    if len(dff)==0:
        fig4 = go.Figure().add_annotation(x=2, y=2,text="Bu yıl için veri yok",font=dict(family="sans serif",size=25,color="crimson"),showarrow=False,yshift=10),
        fig5 = go.Figure().add_annotation(x=2, y=2,text="Bu yıl için veri yok",font=dict(family="sans serif",size=25,color="crimson"),showarrow=False,yshift=10)
        fig6 = go.Figure().add_annotation(x=2, y=2,text="Bu yıl için veri yok",font=dict(family="sans serif",size=25,color="crimson"),showarrow=False,yshift=10),
        fig7 = go.Figure().add_annotation(x=2, y=2,text="Bu yıl için veri yok",font=dict(family="sans serif",size=25,color="crimson"),showarrow=False,yshift=10)
        return fig4,fig5,fig6,fig7
    else:        
        fig = px.choropleth_mapbox(dff, geojson=counties, locations='location_code', 
                                   color='deger',
                                   color_continuous_scale=px.colors.sequential.YlOrRd,
                                   range_color=(np.quantile(dff["deger"],0.01), np.quantile(dff["deger"],0.92)),
                                   mapbox_style="carto-positron",
                                   hover_name='İl Adı',
                                   hover_data={'location_code':False,
                                               "plaka_kodu":False,"Yıl":True,'deger':':,'},
                                   zoom=5, center={"lat": 38.9597594, "lon": 34.9249653},
                                   opacity=0.5,
                                   labels={'deger':selected_city},
                                   )
        
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_layout(dragmode=False)
        
        fig.update_layout(
            hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Rockwell"
            ))

        fig.update_layout(coloraxis=dict(colorbar_x=-0.1,
                                 colorbar_y=0.57,
                                 colorbar_len=1,
                                 colorbar_thickness=30))

        figure1 = px.bar(
            data_frame=dff,
            x='İl Adı',
            y='deger',
            hover_name='İl Adı', 
            hover_data={'Yıl':True,'İl Adı':False,'deger':':,'},
            labels={'İl Adı': 'İl Adı','deger': selected_city},
            template='ggplot2'
        )

        figure1.update_xaxes(categoryorder='total ascending')

        def format_coefs(coefs):
            equation_list = [f"{coef}x^{i}" for i, coef in enumerate(coefs)]
            equation =" + ".join(equation_list)
        
            replace_map = {"x^0": "", "x^1": "x", '+ -': '- '}
            for old, new in replace_map.items():
                equation = equation.replace(old, new)
                
            return equation
    
        X = dff1.deger1.values.reshape(-1, 1)
        x_range = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
        
        figure3 = px.scatter(x=dff1['deger1'], y=dff['deger'],text=dff['İl Adı'],
                              labels=dict(text='İl',x=selected_city1, y=selected_city),
                              hover_data={'Yıl':dff['Yıl']},
                              opacity=1)
        figure3.update_traces(marker_size=7,textposition='top center')
        
        figure3.update_layout(legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ))

        for degree in [1, 2]:
            poly = PolynomialFeatures(degree)
            poly.fit(X)
            X_poly = poly.transform(X)
            x_range_poly = poly.transform(x_range)
        
            model = LinearRegression(fit_intercept=False)
            model.fit(X_poly, dff.deger)
            y_poly = model.predict(x_range_poly)
    
            equation = format_coefs(model.coef_.round(15))
            figure3.add_traces(go.Scatter(x=x_range.squeeze(), y=y_poly, name=equation))

        dff["Türkiye"] = "Türkiye"
        
        dff = dff.append({'İl Adı': 'Türkiye', 'deger': dff['deger'].sum(),'Türkiye':''}, ignore_index=True)
        
        figure2=go.Figure(go.Treemap(
            labels=dff['İl Adı'],
            parents=dff['Türkiye'],
            values=dff['deger'],
            branchvalues='total',
            hovertemplate='<b>%{label} </b> <br>Değer: %{value:,} <br>Yüzde: %{percentParent:.2%}',
            texttemplate='<b>%{label} </b> <br>Değer: %{value:,} <br>Yüzde: %{percentParent:.2%}',
            ))      
        figure2.update_layout(margin = dict(t=50, l=25, r=25, b=25))

        return (fig,figure1,figure3,figure2,
                # dcc.send_data_frame(dff.to_csv, "mydf.csv"),
                )

if __name__ == '__main__':
    app.run_server(debug=False)
    