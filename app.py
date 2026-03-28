import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import requests
from datetime import date

st.set_page_config(page_title="PescuitRO", page_icon="🎣", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #f7f8fa; }
[data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e4e7ec; }
.card {
    background: white; border-radius: 12px; padding: 16px;
    margin-bottom: 10px; border: 1px solid #e4e7ec;
    box-shadow: 0 1px 3px rgba(0,0,0,0.07);
}
.card:hover { border-color: #16a34a; box-shadow: 0 4px 12px rgba(22,163,74,0.1); }
.stButton>button {
    background-color: #16a34a; color: white;
    border-radius: 8px; border: none; font-weight: 600;
    transition: all 0.2s;
}
.stButton>button:hover { background-color: #15803d; transform: translateY(-1px); }
.metric-card {
    background: white; border-radius: 10px; padding: 14px;
    border: 1px solid #e4e7ec; text-align: center;
}
.badge-green  { background:#dcfce7; color:#15803d; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:600; }
.badge-blue   { background:#dbeafe; color:#1d4ed8; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:600; }
.badge-amber  { background:#fef3c7; color:#92400e; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:600; }
.badge-red    { background:#fee2e2; color:#dc2626; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:600; }
h1, h2, h3 { color: #111827; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# DATE LOCATII
# ═══════════════════════════════════════════════════════════
LOCATII = [
    {"id":1,"name":"Balta Corbu","county":"Ilfov","type":"premium","lat":44.55,"lon":26.40,
     "fish":["Crap oglindă","Crap comun","Știucă","Caras","Somn","Amur"],
     "area":"12 ha","depth":"max. 4m","rating":4.8,"fi":92,"night":True,"boat":True,"cr":False,
     "tariffs":[("Zi (1 undiță)","60 RON"),("Noapte","80 RON"),("Weekend","180 RON"),("Lunar","600 RON")],
     "allowed":["Vapoare electrice","Pescuit noapte","Câini în lesă","Cort"],
     "forbidden":["Plase și setci","Foc deschis","Zgomot după 23:00"],
     "facilities":["🚿 Dușuri","🚽 Toalete","🍽 Restaurant","⚡ Curent electric"],
     "contact":"0722 345 678","web":"baltacorbu.ro","season":"Tot anul","access":"DN2A + drum comunal 3km"},
    {"id":2,"name":"Râul Olt – Turnu Roșu","county":"Sibiu","type":"gratis","lat":45.60,"lon":24.20,
     "fish":["Păstrăv curcubeu","Păstrăv indigen","Lipan","Clean"],
     "area":"15km sector","depth":"0.5–3m","rating":4.6,"fi":85,"night":False,"boat":False,"cr":True,
     "tariffs":[("Permis zilnic AGVPS","30 RON"),("Anual ANPA","100 RON")],
     "allowed":["Fly fishing","Năluci oscilante","Camping pe maluri"],
     "forbidden":["Vapoare cu motor","Momeli naturale (sector special)"],
     "facilities":["🏕 Zone campare","🗑 Pubele ecologice"],
     "contact":"0269 211 555","web":"","season":"Mai–Oct","access":"DN7 Sibiu–Rm. Vâlcea"},
    {"id":3,"name":"Heleșteu Brăila","county":"Brăila","type":"premium","lat":45.20,"lon":27.80,
     "fish":["Crap oglindă 25kg+","Amur alb","Somn african"],
     "area":"20 ha","depth":"max. 5m","rating":4.9,"fi":97,"night":True,"boat":True,"cr":True,
     "tariffs":[("Stand 24h","150 RON"),("Stand 48h","260 RON"),("Stand 72h","350 RON")],
     "allowed":["Vapoare electrice","Boilies și pellets","Corturi și bivouac"],
     "forbidden":["Foc deschis","Hrănire excesivă","Pescuitul somnului"],
     "facilities":["🚿 Dușuri calde","⚡ Curent la fiecare stand","❄ Frigider","☕ Automat cafea"],
     "contact":"0740 999 888","web":"heleseu-braila.ro","season":"Tot anul","access":"DN22 Brăila–Galați, km 18"},
    {"id":4,"name":"Lacul Snagov","county":"Ilfov","type":"gratis","lat":44.73,"lon":26.15,
     "fish":["Crap","Știucă","Somn","Roșioară","Biban","Plătică"],
     "area":"575 ha","depth":"max. 9m","rating":3.9,"fi":70,"night":True,"boat":True,"cr":False,
     "tariffs":[("Permis ANPA anual","100 RON"),("Timbru piscicol","50 RON")],
     "allowed":["Barcă personală cu aviz","Pescuit din mal sau barcă"],
     "forbidden":["Plase și vintire","Motor >9.9 CP","Zona rezervației"],
     "facilities":["🏖 Plajă","🍽 Restaurante","⛵ Închirieri bărci"],
     "contact":"021 350 xxxx","web":"snagov.ro","season":"Tot anul","access":"DN1 București–Ploiești, ieșire Snagov"},
    {"id":5,"name":"Dunărea – Delta Tulcea","county":"Tulcea","type":"gratis","lat":45.18,"lon":28.80,
     "fish":["Somn 100kg+","Știucă","Crap","Plătică","Morunaș"],
     "area":"Delta Dunării","depth":"5–25m","rating":4.7,"fi":88,"night":True,"boat":True,"cr":False,
     "tariffs":[("Permis ANPA anual","100 RON"),("Timbru piscicol","50 RON"),("Ghid local","300–500/zi")],
     "allowed":["Barcă cu motor cu acte","Pescuit noapte","Campare pe insule zone permise"],
     "forbidden":["Sturioni (INTERZIS TOTAL)","Plase în zona protejată"],
     "facilities":["⛵ Închirieri bărci","🏠 Pensiuni pescărești","🍽 Restaurante pește"],
     "contact":"0240 515 xxx","web":"ddbra.ro","season":"Tot anul","access":"Port Tulcea – navete spre brațe"},
    {"id":6,"name":"Balta Voluntari Elite","county":"Ilfov","type":"premium","lat":44.49,"lon":26.18,
     "fish":["Crap oglindă","Amur","Șalău"],
     "area":"7 ha","depth":"max. 4m","rating":4.7,"fi":95,"night":True,"boat":True,"cr":True,
     "tariffs":[("Zi (1 undiță)","80 RON"),("Noapte premium","150 RON"),("Lunar","800 RON")],
     "allowed":["Vapoare electrice","Pescuit noapte cu cort","Drone personale","WiFi inclus"],
     "forbidden":["Hrănire excesivă","Câini"],
     "facilities":["🚿 Dușuri","⚡ Curent 220V la fiecare stand","📶 WiFi gratuit","☕ Cafenea"],
     "contact":"0731 888 777","web":"voluntarielite.ro","season":"Tot anul","access":"Bd. Voluntari, ieșire A3"},
    {"id":7,"name":"Lacul Vidraru","county":"Argeș","type":"gratis","lat":45.35,"lon":24.63,
     "fish":["Păstrăv curcubeu","Șalău","Biban","Clean"],
     "area":"870 ha","depth":"max. 155m","rating":4.7,"fi":88,"night":False,"boat":True,"cr":False,
     "tariffs":[("Permis ANPA anual","100 RON"),("Timbru piscicol","50 RON")],
     "allowed":["Barcă cu aviz","Pescuit din mal","Spinning"],
     "forbidden":["Lostrița (protejată)","Motor >9.9 CP","Zona barajului 500m"],
     "facilities":["🏕 Camping Vidraru","🍽 Restaurante zona"],
     "contact":"0248 xxx xxx","web":"","season":"Mai–Oct","access":"DN7C Curtea de Argeș–Transfăgărășan"},
    {"id":8,"name":"Lacul Stânca-Costești","county":"Botoșani","type":"gratis","lat":47.87,"lon":26.91,
     "fish":["Șalău","Somn","Crap","Amur","Plătică"],
     "area":"5900 ha","depth":"max. 30m","rating":4.6,"fi":86,"night":True,"boat":True,"cr":False,
     "tariffs":[("Permis ANPA anual","100 RON"),("Timbru piscicol","50 RON"),("Viză frontieră","30 RON")],
     "allowed":["Barcă cu motor cu aviz","Pescuit noapte","Spinning din barcă"],
     "forbidden":["Fără viză de frontieră","Plase","Sturioni"],
     "facilities":["🏕 Zone campare","🗑 Pubele"],
     "contact":"0231 xxx xxx","web":"","season":"Tot anul","access":"DN29 Botoșani–Stânca, 25km"},
    {"id":9,"name":"Lacul Țaga Mică","county":"Cluj","type":"privata","lat":47.00,"lon":23.97,
     "fish":["Crap","Șalău","Somn","Ctenofaring","Caras"],
     "area":"24 ha","depth":"6m","rating":4.8,"fi":92,"night":True,"boat":False,"cr":False,
     "tariffs":[("Ponton 24h","50 RON"),("Căbănuță 24h (2 pers)","250 RON"),("Lunar","700 RON")],
     "allowed":["Căbănuțe dotate pe mal","Pescuit noapte","Boilies"],
     "forbidden":["Navomodele","Porumb uscat"],
     "facilities":["🏠 Căbănuțe cu frigider și TV","🚽 Grup sanitar propriu","⚡ Curent"],
     "contact":"0264 xxx xxx","web":"lactagamica.ro","season":"Tot anul","access":"DN16 Cluj-Napoca–Gherla, 62km"},
    {"id":10,"name":"Dunărea – Cazanele Mari","county":"Mehedinți","type":"gratis","lat":44.67,"lon":22.38,
     "fish":["Somn","Crap","Avat","Morunaș","Clean","Mreană"],
     "area":"Defileu Dunăre","depth":"50–90m","rating":4.8,"fi":91,"night":True,"boat":True,"cr":False,
     "tariffs":[("Permis ANPA anual","100 RON"),("Timbru piscicol","50 RON"),("Ghid local","200–400/zi")],
     "allowed":["Barcă cu motor cu aviz","Pescuit din mal","Spinning din barcă"],
     "forbidden":["Sturioni (INTERZIS TOTAL)","Plase"],
     "facilities":["🍽 Restaurante Dubova","🏠 Pensiuni zona"],
     "contact":"0252 xxx xxx","web":"","season":"Tot anul","access":"DN57 Orșova–Moldova Nouă, zona Dubova"},
    {"id":11,"name":"Brațul Sulina","county":"Tulcea","type":"gratis","lat":45.15,"lon":29.40,
     "fish":["Somn","Știucă","Crap","Șalău","Biban","Văduviță"],
     "area":"Brațul Sulina","depth":"10–20m","rating":4.9,"fi":95,"night":True,"boat":True,"cr":False,
     "tariffs":[("Permis ANPA anual","100 RON"),("Timbru piscicol","50 RON"),("Ghid local","400–600/zi")],
     "allowed":["Barcă cu motor","Pescuit noapte","Camping pe insulă zone permise"],
     "forbidden":["Sturioni (INTERZIS TOTAL)","Plase în zone protejate"],
     "facilities":["⛵ Închirieri bărci","🏠 Pensiuni pescărești","🍽 Restaurante pește"],
     "contact":"0240 516 xxx","web":"ddbra.ro","season":"Tot anul","access":"Naveta Tulcea–Sulina (2.5h)"},
    {"id":12,"name":"Lacul Colibița","county":"Bistrița-Năsăud","type":"gratis","lat":47.10,"lon":24.95,
     "fish":["Păstrăv curcubeu","Biban","Șalău"],
     "area":"440 ha","depth":"max. 42m","rating":4.7,"fi":88,"night":True,"boat":True,"cr":False,
     "tariffs":[("Permis ANPA anual","100 RON"),("Timbru piscicol","50 RON")],
     "allowed":["Barcă cu aviz","Pescuit din mal","Camping autorizat"],
     "forbidden":["Motor >5 CP","Lostrița (protejată)","Foc pe maluri"],
     "facilities":["🏕 Camping Colibița","🍽 Restaurante zona"],
     "contact":"0263 xxx xxx","web":"","season":"Mai–Oct","access":"DJ172C Bistrița–Colibița"},
    {"id":13,"name":"Lacul Roșu","county":"Harghita","type":"gratis","lat":46.77,"lon":25.76,
     "fish":["Păstrăv curcubeu","Biban","Păstrăv indigen"],
     "area":"12.6 ha","depth":"max. 10m","rating":4.8,"fi":86,"night":False,"boat":True,"cr":False,
     "tariffs":[("Permis ANPA anual","100 RON"),("Timbru piscicol","50 RON")],
     "allowed":["Pescuit din mal","Barcă cu vâsle"],
     "forbidden":["Motor","Campare pe mal","Foc"],
     "facilities":["🍽 Restaurante Lacu Roșu","🏠 Pensiuni zona"],
     "contact":"0266 xxx xxx","web":"","season":"Mai–Sept","access":"DN12B Gheorgheni–Lacu Roșu"},
    {"id":14,"name":"Balta Fibis","county":"Timiș","type":"privata","lat":45.71,"lon":21.42,
     "fish":["Crap","Somn","Caras","Biban","Roșioară"],
     "area":"18 ha","depth":"4m","rating":4.4,"fi":80,"night":True,"boat":False,"cr":False,
     "tariffs":[("Zi (1 undiță)","45 RON"),("Noapte","70 RON"),("Lunar","400 RON")],
     "allowed":["Pescuit noapte","2 undițe","Cort"],
     "forbidden":["Vapoare","Foc deschis"],
     "facilities":["🚽 Toalete","🗑 Pubele"],
     "contact":"0256 xxx xxx","web":"","season":"Tot anul","access":"DN6 Timișoara–Lugoj, ieșire Fibis, 18km"},
    {"id":15,"name":"Laguna Verde Balotești","county":"Ilfov","type":"privata","lat":44.65,"lon":26.07,
     "fish":["Crap oglindă","Amur","Caras","Știucă","Somn"],
     "area":"20 ha","depth":"4m","rating":4.6,"fi":88,"night":True,"boat":True,"cr":False,
     "tariffs":[("Zi (1 undiță)","60 RON"),("Noapte","90 RON"),("Căsuță 24h","250 RON")],
     "allowed":["Căsuțe pe mal","Pescuit noapte","Vapoare electrice","Boilies"],
     "forbidden":["Motor termic","Foc deschis"],
     "facilities":["🏠 Căsuțe moderne","🚿 Dușuri","🌳 Umbrar","🅿 Parcare asfaltată"],
     "contact":"0721 xxx xxx","web":"lagunacarpfishing.ro","season":"Tot anul","access":"DN1 București–Ploiești, ieșire Balotești, 20km"},
    {"id":16,"name":"Lacul Bicaz","county":"Neamț","type":"gratis","lat":46.87,"lon":25.85,
     "fish":["Păstrăv curcubeu","Biban","Șalău","Clean"],
     "area":"3100 ha","depth":"max. 90m","rating":4.5,"fi":80,"night":True,"boat":True,"cr":False,
     "tariffs":[("Permis ANPA anual","100 RON"),("Timbru piscicol","50 RON")],
     "allowed":["Pescuit din mal","Barcă cu aviz","Camping zone permise"],
     "forbidden":["Zona barajului 500m","Motoare >15 CP","Lostrița (protejată)"],
     "facilities":["🏕 Camping Izvorul Muntelui","🍽 Restaurante Bicaz Chei"],
     "contact":"0233 251 xxx","web":"","season":"Mai–Oct","access":"DN15B de la Piatra Neamț"},
    {"id":17,"name":"Balta Comana","county":"Giurgiu","type":"gratis","lat":44.17,"lon":26.15,
     "fish":["Crap","Caras","Biban","Știucă","Roșioară"],
     "area":"480 ha","depth":"max. 3m","rating":4.4,"fi":76,"night":False,"boat":False,"cr":False,
     "tariffs":[("Permis ANPA anual","100 RON"),("Timbru piscicol","50 RON")],
     "allowed":["Pescuit din mal","Barcă cu vâsle","Camping autorizat"],
     "forbidden":["Bărci cu motor","Plase","Zone strict protejate"],
     "facilities":["🌳 Parc natural","🍽 Restaurant Comana","🗑 Pubele"],
     "contact":"0246 xxx xxx","web":"parccomana.ro","season":"Tot anul","access":"DN5 București–Giurgiu, ieșire Comana"},
    {"id":18,"name":"Balta Albă Buzău","county":"Buzău","type":"gratis","lat":45.37,"lon":27.10,
     "fish":["Crap","Caras","Biban","Roșioară","Știucă"],
     "area":"280 ha","depth":"max. 6m","rating":4.2,"fi":73,"night":True,"boat":True,"cr":False,
     "tariffs":[("Permis ANPA anual","100 RON"),("Timbru piscicol","50 RON")],
     "allowed":["Barcă cu aviz","Camping zone permise","Pescuit noapte"],
     "forbidden":["Plase","Motor >5 CP","Zona rezervație (vest)"],
     "facilities":["🏕 Zone camping","🗑 Pubele"],
     "contact":"0238 xxx xxx","web":"","season":"Tot anul","access":"DJ203D Buzău–Ciorăști"},
    {"id":19,"name":"Lacul Strejești","county":"Olt","type":"gratis","lat":44.43,"lon":24.50,
     "fish":["Crap","Somn","Șalău","Avat","Plătică","Biban"],
     "area":"1760 ha","depth":"max. 20m","rating":4.3,"fi":81,"night":True,"boat":True,"cr":False,
     "tariffs":[("Permis ANPA anual","100 RON"),("Timbru piscicol","50 RON")],
     "allowed":["Barcă cu motor cu aviz","Pescuit noapte","Spinning"],
     "forbidden":["Plase","Zona barajului"],
     "facilities":["🅿 Parcare Strejești","🍽 Restaurante zona"],
     "contact":"0249 xxx xxx","web":"","season":"Tot anul","access":"DN65B Slatina–Strejești, 15km"},
    {"id":20,"name":"Lacul Firiza","county":"Maramureș","type":"gratis","lat":47.67,"lon":23.56,
     "fish":["Păstrăv curcubeu","Biban","Șalău","Clean"],
     "area":"280 ha","depth":"max. 45m","rating":4.3,"fi":79,"night":False,"boat":True,"cr":False,
     "tariffs":[("Permis ANPA anual","100 RON"),("Timbru piscicol","50 RON")],
     "allowed":["Barcă cu aviz","Pescuit din mal","Spinning"],
     "forbidden":["Motor >5 CP","Zona barajului"],
     "facilities":["🅿 Parcare Firiza","🍽 Restaurante Baia Mare"],
     "contact":"0262 xxx xxx","web":"","season":"Mai–Oct","access":"DJ182 Baia Mare–Firiza, 10km"},
    {"id":21,"name":"Râul Iza – Maramureș","county":"Maramureș","type":"gratis","lat":47.72,"lon":24.26,
     "fish":["Păstrăv indigen","Lipan","Clean","Mreană","Scobar"],
     "area":"45km sector","depth":"0.3–3m","rating":4.6,"fi":87,"night":False,"boat":False,"cr":False,
     "tariffs":[("Permis zilnic AGVPS","25 RON"),("Anual ANPA","100 RON")],
     "allowed":["Fly fishing","Năluci mici","Momeli naturale"],
     "forbidden":["Plase","Electropescuit","Motor"],
     "facilities":["🏕 Zone campare","🍽 Restaurante zona"],
     "contact":"0262 xxx xxx","web":"","season":"Mart–Oct","access":"DN18 Sighetul Marmației–Borșa"},
    {"id":22,"name":"Lacul Razim","county":"Tulcea","type":"gratis","lat":44.90,"lon":29.00,
     "fish":["Somn","Crap","Biban","Știucă","Roșioară","Guvid"],
     "area":"41500 ha","depth":"max. 3.5m","rating":4.5,"fi":82,"night":True,"boat":True,"cr":False,
     "tariffs":[("Permis ANPA anual","100 RON"),("Timbru piscicol","50 RON")],
     "allowed":["Barcă cu motor cu aviz","Pescuit noapte","Spinning"],
     "forbidden":["Plase","Zona protejată DDBRA","Sturioni"],
     "facilities":["🅿 Parcare Jurilovca","🍽 Restaurante pește"],
     "contact":"0240 xxx xxx","web":"","season":"Tot anul","access":"DN22 Tulcea–Constanța, ieșire Jurilovca"},
    {"id":23,"name":"Lacul Turulung","county":"Satu Mare","type":"privata","lat":47.87,"lon":22.88,
     "fish":["Crap","Caras","Ctenofaring","Biban","Somn"],
     "area":"30 ha","depth":"5m","rating":4.4,"fi":82,"night":True,"boat":False,"cr":True,
     "tariffs":[("Stand 24h","100 RON"),("Stand 48h","180 RON"),("Lunar","500 RON")],
     "allowed":["Pescuit noapte","Bivouac","Boilies","C&R opțional"],
     "forbidden":["Foc deschis","Navomodele"],
     "facilities":["🅿 Parcare securizată","🚽 Toalete","🗑 Pubele"],
     "contact":"0261 xxx xxx","web":"","season":"Tot anul","access":"DN19 Satu Mare–Turulung, 18km"},
    {"id":24,"name":"Paradisul Verde Iași","county":"Iași","type":"privata","lat":47.05,"lon":27.35,
     "fish":["Crap oglindă","Somn","Șalău","Caras"],
     "area":"15 ha","depth":"5m","rating":4.7,"fi":89,"night":True,"boat":False,"cr":True,
     "tariffs":[("Stand 24h","130 RON"),("Stand 48h","220 RON"),("Lunar","600 RON")],
     "allowed":["Pescuit noapte","Bivouac","Boilies","2 lansete"],
     "forbidden":["Foc deschis","Câini","Navomodele"],
     "facilities":["🅿 Parcare securizată 24h","⚡ Curent electric","🚽 Toalete moderne"],
     "contact":"0745 111 222","web":"paradisverde-iasi.ro","season":"Tot anul","access":"IE58 Iași–Ungheni, km 12"},
    {"id":25,"name":"Barajul Poiana Mărului","county":"Caraș-Severin","type":"gratis","lat":45.35,"lon":22.57,
     "fish":["Păstrăv curcubeu","Caras","Clean","Oblete"],
     "area":"240 ha","depth":"max. 65m","rating":4.4,"fi":77,"night":False,"boat":True,"cr":False,
     "tariffs":[("Permis ANPA anual","100 RON"),("Timbru piscicol","50 RON")],
     "allowed":["Barcă cu aviz","Pescuit din mal"],
     "forbidden":["Motor >5 CP","Lostrița (protejată)"],
     "facilities":["🅿 Parcare Zavoi","🍽 Restaurante zona"],
     "contact":"0255 xxx xxx","web":"","season":"Mai–Oct","access":"DN68 Hațeg–Caransebeș, ieșire Zavoi"},
]

# ═══════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════
if "selected" not in st.session_state:
    st.session_state.selected = None
if "user" not in st.session_state:
    st.session_state.user = None
if "jurnal" not in st.session_state:
    st.session_state.jurnal = []
if "page" not in st.session_state:
    st.session_state.page = "Hartă"
if "favorite" not in st.session_state:
    st.session_state.favorite = []

# ═══════════════════════════════════════════════════════════
# METEO REAL
# ═══════════════════════════════════════════════════════════
@st.cache_data(ttl=1800)
def get_meteo(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weathercode,windspeed_10m,relativehumidity_2m&wind_speed_unit=kmh&timezone=auto"
        r = requests.get(url, timeout=5)
        d = r.json()["current"]
        codes = {0:"☀️ Cer senin",1:"🌤 Parțial noros",2:"⛅ Noros",3:"☁️ Înnorat",
                 45:"🌫 Ceață",48:"🌫 Ceață",51:"🌦 Burnițe",53:"🌦 Burnițe",
                 61:"🌧 Ploaie",63:"🌧 Ploaie moderată",65:"🌧 Ploaie puternică",
                 71:"❄️ Ninsoare",73:"❄️ Ninsoare",80:"🌦 Averse",81:"🌦 Averse",
                 95:"⛈ Furtună",96:"⛈ Furtună cu grindină"}
        desc = codes.get(d["weathercode"], "🌤 Variabil")
        return {
            "temp": round(d["temperature_2m"]),
            "wind": round(d["windspeed_10m"]),
            "hum": d["relativehumidity_2m"],
            "desc": desc
        }
    except:
        return None

# ═══════════════════════════════════════════════════════════
# NAVBAR
# ═══════════════════════════════════════════════════════════
col_logo, col_nav, col_auth = st.columns([2, 6, 2])
with col_logo:
    st.markdown("# 🎣 PescuitRO")
with col_nav:
    pages = ["Hartă", "Jurnal", "Concursuri", "Magazin", "Forum", "Regulamente"]
    cols = st.columns(len(pages))
    icons = {"Hartă":"🗺","Jurnal":"📓","Concursuri":"🏆","Magazin":"🛒","Forum":"💬","Regulamente":"📋"}
    for i, p in enumerate(pages):
        with cols[i]:
            label = f"{icons[p]} {p}"
            if st.button(label, key=f"nav_{p}",
                        use_container_width=True):
                st.session_state.page = p
                st.rerun()
with col_auth:
    if st.session_state.user:
        st.markdown(f"👤 **{st.session_state.user}**")
        if st.button("Ieșire cont", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    else:
        if st.button("🔐 Intră în cont", use_container_width=True):
            st.session_state.page = "Login"
            st.rerun()

st.divider()

# ═══════════════════════════════════════════════════════════
# PAGE: HARTĂ
# ═══════════════════════════════════════════════════════════
if st.session_state.page == "Hartă":

    with st.sidebar:
        st.markdown("### 🔍 Filtre")
        tip_filter   = st.selectbox("Tip locație", ["Toate","Gratuit","Privată","Premium"])
        night_filter = st.checkbox("🌙 Pescuit noapte")
        boat_filter  = st.checkbox("⛵ Permite vapoare")
        cr_filter    = st.checkbox("🔄 Catch & Release")
        search_q     = st.text_input("🔎 Caută (județ, specie...)")
        st.divider()
        st.markdown("### 📊 Statistici")
        st.metric("Total locații", len(LOCATII))
        st.metric("Gratuite", sum(1 for l in LOCATII if l["type"] == "gratis"))
        st.metric("Private", sum(1 for l in LOCATII if l["type"] == "privata"))
        st.metric("Premium", sum(1 for l in LOCATII if l["type"] == "premium"))

    filtered = LOCATII[:]
    if tip_filter == "Gratuit":
        filtered = [l for l in filtered if l["type"] == "gratis"]
    elif tip_filter == "Privată":
        filtered = [l for l in filtered if l["type"] == "privata"]
    elif tip_filter == "Premium":
        filtered = [l for l in filtered if l["type"] == "premium"]
    if night_filter:
        filtered = [l for l in filtered if l["night"]]
    if boat_filter:
        filtered = [l for l in filtered if l["boat"]]
    if cr_filter:
        filtered = [l for l in filtered if l["cr"]]
    if search_q:
        q = search_q.lower()
        filtered = [l for l in filtered if q in l["name"].lower()
                    or q in l["county"].lower()
                    or any(q in f.lower() for f in l["fish"])]

    col_map, col_list = st.columns([3, 2])

    with col_map:
        st.markdown(f"**{len(filtered)} locații afișate**")
        m = folium.Map(location=[45.9, 24.9], zoom_start=7, tiles="CartoDB positron")
        color_map = {"gratis":"green","privata":"blue","premium":"orange"}
        icon_map  = {"gratis":"leaf","privata":"info-sign","premium":"star"}
        for loc in filtered:
            c = color_map.get(loc["type"], "gray")
            ic = icon_map.get(loc["type"], "map-marker")
            popup_html = f"""
            <div style='font-family:Arial;min-width:200px;padding:4px'>
              <b style='font-size:14px'>{loc['name']}</b><br>
              <span style='color:#6b7280;font-size:12px'>📍 {loc['county']} · {loc['area']}</span><br>
              <span style='font-size:11px;color:#374151'>{' · '.join(loc['fish'][:3])}</span><br>
              <span style='color:#f59e0b;font-size:13px'>{'★' * int(loc['rating'])}{'☆'*(5-int(loc['rating']))}</span>
              <span style='font-size:12px'> {loc['rating']}</span><br>
              <span style='color:#16a34a;font-size:11px;font-weight:600'>Indice pescuit: {loc['fi']}/100</span>
            </div>
            """
            folium.Marker(
                location=[loc["lat"], loc["lon"]],
                popup=folium.Popup(popup_html, max_width=240),
                tooltip=f"🎣 {loc['name']}",
                icon=folium.Icon(color=c, icon=ic, prefix="glyphicon")
            ).add_to(m)
        st_folium(m, width=720, height=520, returned_objects=[])

    with col_list:
        st.markdown("### 📋 Locații")
        for loc in filtered:
            badge = {"gratis":"🟢 Gratuit","privata":"🔵 Privată","premium":"⭐ Premium"}.get(loc["type"],"")
            stars = "★" * int(loc["rating"]) + "☆" * (5 - int(loc["rating"]))
            is_fav = loc["id"] in st.session_state.favorite
            st.markdown(f"""
            <div class='card'>
              <div style='display:flex;justify-content:space-between;align-items:flex-start'>
                <b style='font-size:14px'>{loc['name']}</b>
                <span style='font-size:11px'>{badge} {'❤️' if is_fav else ''}</span>
              </div>
              <div style='color:#6b7280;font-size:12px;margin:3px 0'>
                📍 {loc['county']} · {loc['area']}
                {'· 🌙' if loc['night'] else ''}
                {'· ⛵' if loc['boat'] else ''}
                {'· 🔄' if loc['cr'] else ''}
              </div>
              <div style='font-size:11px;color:#9ca3af'>{' · '.join(loc['fish'][:3])}</div>
              <div style='margin-top:5px;display:flex;justify-content:space-between;align-items:center'>
                <span style='color:#f59e0b'>{stars} <span style='color:#374151'>{loc['rating']}</span></span>
                <span style='color:#16a34a;font-size:11px;font-weight:700'>Ind.{loc['fi']}/100</span>
              </div>
            </div>
            """, unsafe_allow_html=True)
            cb1, cb2 = st.columns([3,1])
            with cb1:
                if st.button(f"🔍 Detalii", key=f"det_{loc['id']}", use_container_width=True):
                    st.session_state.selected = loc["id"]
                    st.rerun()
            with cb2:
                fav_label = "❤️" if not is_fav else "💔"
                if st.button(fav_label, key=f"fav_{loc['id']}"):
                    if is_fav:
                        st.session_state.favorite.remove(loc["id"])
                    else:
                        st.session_state.favorite.append(loc["id"])
                    st.rerun()

    # Detalii locatie selectata
    if st.session_state.selected:
        loc = next((l for l in LOCATII if l["id"] == st.session_state.selected), None)
        if loc:
            st.divider()
            st.markdown(f"## 📍 {loc['name']} — {loc['county']}")

            # Meteo real
            with st.spinner("Se încarcă meteo..."):
                meteo = get_meteo(loc["lat"], loc["lon"])

            mc1, mc2, mc3, mc4, mc5 = st.columns(5)
            mc1.metric("⭐ Rating", f"{loc['rating']}")
            mc2.metric("📐 Suprafață", loc["area"])
            mc3.metric("🌊 Adâncime", loc["depth"])
            mc4.metric("🎣 Indice", f"{loc['fi']}/100")
            if meteo:
                mc5.metric(meteo["desc"], f"{meteo['temp']}°C")
            else:
                mc5.metric("🌤 Meteo", "N/A")

            if meteo:
                st.info(f"🌡 {meteo['temp']}°C · 💨 {meteo['wind']} km/h · 💧 Umiditate {meteo['hum']}% · {meteo['desc']}")

            tab1, tab2, tab3, tab4, tab5 = st.tabs(["🐟 Pești & Info","💰 Tarife","📜 Reguli","🏗 Facilități","🗺 Navigare"])

            with tab1:
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("**Specii de pești:**")
                    for f in loc["fish"]:
                        st.markdown(f"🐟 {f}")
                with col_b:
                    st.markdown("**Caracteristici:**")
                    st.markdown(f"🌙 Pescuit noapte: {'✅ Da' if loc['night'] else '❌ Nu'}")
                    st.markdown(f"⛵ Vapoare: {'✅ Permis' if loc['boat'] else '❌ Interzis'}")
                    st.markdown(f"🔄 Catch & Release: {'✅ Da' if loc['cr'] else '➡ Nu'}")
                    st.markdown(f"📅 Sezon: {loc['season']}")
                    st.markdown(f"🛣 Acces: {loc['access']}")

            with tab2:
                if loc["type"] == "gratis":
                    st.info("ℹ️ Locație de stat — necesită permis ANPA + timbru piscicol. Cumpără pe anpa.ro")
                for label, price in loc["tariffs"]:
                    c1, c2 = st.columns([3,1])
                    c1.write(label)
                    c2.markdown(f"**{price}**")

            with tab3:
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("**✅ Ce este permis:**")
                    for r in loc.get("allowed", []):
                        st.markdown(f"✅ {r}")
                with col_b:
                    st.markdown("**🚫 Ce este interzis:**")
                    for r in loc.get("forbidden", []):
                        st.markdown(f"🚫 {r}")
                st.warning("⚠️ Sturionii sunt interzis la pescuit în toată România. Permis obligatoriu.")

            with tab4:
                for f in loc.get("facilities", []):
                    st.markdown(f"• {f}")
                if loc.get("web"):
                    st.markdown(f"🌐 Website: [{loc['web']}](https://{loc['web']})")
                st.markdown(f"📞 Contact: **{loc['contact']}**")

            with tab5:
                gmap = f"https://www.google.com/maps/search/?api=1&query={loc['lat']},{loc['lon']}"
                waze = f"https://waze.com/ul?ll={loc['lat']},{loc['lon']}&navigate=yes"
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"[🗺 Deschide Google Maps]({gmap})")
                with col_b:
                    st.markdown(f"[🚗 Deschide Waze]({waze})")
                st.markdown(f"**Coordonate GPS:** `{loc['lat']}, {loc['lon']}`")

            if st.button("✕ Închide detalii"):
                st.session_state.selected = None
                st.rerun()

# ═══════════════════════════════════════════════════════════
# PAGE: JURNAL
# ═══════════════════════════════════════════════════════════
elif st.session_state.page == "Jurnal":
    if not st.session_state.user:
        st.warning("⚠️ Trebuie să fii autentificat pentru jurnal.")
        if st.button("🔐 Intră în cont"):
            st.session_state.page = "Login"
            st.rerun()
    else:
        st.markdown("## 📓 Jurnalul Meu de Pescuit")
        j = st.session_state.jurnal
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🎣 Ieșiri totale", len(j))
        c2.metric("🐟 Pești prinși", sum(1 for e in j if e.get("specie")))
        c3.metric("🏆 Record kg", f"{max((e.get('kg',0) for e in j), default=0)} kg")
        c4.metric("🌊 Specii", len(set(e.get("specie","") for e in j if e.get("specie"))))
        st.divider()

        with st.expander("➕ Adaugă o ieșire nouă", expanded=not bool(j)):
            with st.form("jurnal_form"):
                c1, c2 = st.columns(2)
                with c1:
                    data_iesire = st.date_input("Data ieșirii", value=date.today())
                    locatie = st.text_input("Locație", placeholder="Ex: Balta Corbu, Ilfov")
                    specie  = st.selectbox("Specia prinsă", [
                        "","Crap oglindă","Crap comun","Amur","Știucă","Somn","Șalău",
                        "Biban","Caras","Roșioară","Plătică","Babusc",
                        "Păstrăv curcubeu","Păstrăv indigen","Lipan","Clean","Mreană","Scobar"])
                with c2:
                    kg      = st.number_input("Greutate (kg)", min_value=0.0, step=0.1)
                    momeala = st.text_input("Momeala folosită", placeholder="Ex: Boilies usturoi 20mm")
                    meteo_j = st.selectbox("Condiții meteo", ["☀️ Soare","⛅ Parțial noros","☁️ Noros","🌧 Ploaie","💨 Vânt","❄️ Frig"])
                note = st.text_area("Note și observații", placeholder="Tehnici, observații, sfaturi pentru data viitoare...")
                if st.form_submit_button("💾 Salvează ieșirea", use_container_width=True):
                    if locatie and specie:
                        st.session_state.jurnal.append({
                            "data": str(data_iesire), "locatie": locatie, "specie": specie,
                            "kg": kg, "momeala": momeala, "meteo": meteo_j, "note": note
                        })
                        st.success("✅ Ieșire salvată cu succes!")
                        st.rerun()
                    else:
                        st.error("Completează cel puțin locația și specia!")

        if st.session_state.jurnal:
            st.markdown("### 📋 Istoricul tău")
            for i, e in enumerate(reversed(st.session_state.jurnal)):
                with st.container():
                    c1,c2,c3,c4,c5,c6 = st.columns([1,2,2,1,2,1])
                    c1.write(f"📅 {e['data']}")
                    c2.write(f"📍 {e['locatie']}")
                    c3.write(f"🐟 {e['specie']}")
                    c4.write(f"⚖️ {e['kg']}kg" if e['kg'] else "–")
                    c5.write(f"🎣 {e.get('momeala','–')}")
                    if c6.button("🗑", key=f"del_{i}"):
                        st.session_state.jurnal.pop(len(st.session_state.jurnal)-1-i)
                        st.rerun()
                st.divider()

# ═══════════════════════════════════════════════════════════
# PAGE: CONCURSURI
# ═══════════════════════════════════════════════════════════
elif st.session_state.page == "Concursuri":
    st.markdown("## 🏆 Concursuri & Evenimente 2025")
    concursuri = [
        {"name":"Cupa Dunării 2025","date":"15 Iunie 2025","loc":"Delta Tulcea","prize":"5.000 RON","part":64,"cat":"Crap & Somn","emoji":"🏆"},
        {"name":"Campionatul Județean Ilfov","date":"22 Mai 2025","loc":"Balta Corbu, Ilfov","prize":"2.000 RON","part":32,"cat":"Crap","emoji":"🎣"},
        {"name":"Trofeul Păstrăvului","date":"8 Iunie 2025","loc":"Râul Olt, Sibiu","prize":"1.500 RON","part":28,"cat":"Păstrăv","emoji":"🐟"},
        {"name":"Maratonul Somnului","date":"5 Iulie 2025","loc":"Dunăre, Galați","prize":"3.000 RON","part":48,"cat":"Somn","emoji":"🦈"},
        {"name":"Cupă C&R Voluntari","date":"12 Iulie 2025","loc":"Balta Voluntari Elite","prize":"Trofeu + Echipament","part":20,"cat":"Crap C&R","emoji":"🎯"},
        {"name":"Campionat Știucă","date":"29 Iulie 2025","loc":"Lacul Snagov","prize":"800 RON","part":16,"cat":"Știucă","emoji":"🐠"},
    ]
    cols = st.columns(3)
    for i, c in enumerate(concursuri):
        with cols[i % 3]:
            st.markdown(f"""
            <div class='card'>
              <div style='font-size:36px;text-align:center;margin-bottom:8px'>{c['emoji']}</div>
              <div style='margin-bottom:6px'>
                <span class='badge-blue'>{c['cat']}</span>
                {'<span class="badge-red" style="margin-left:4px">Locuri limitate</span>' if c['part']<30 else ''}
              </div>
              <b style='font-size:14px'>{c['name']}</b>
              <div style='font-size:12px;color:#6b7280;margin:4px 0'>📅 {c['date']}</div>
              <div style='font-size:12px;color:#6b7280;margin-bottom:8px'>📍 {c['loc']}</div>
              <div style='display:flex;justify-content:space-between;align-items:center'>
                <span style='color:#16a34a;font-weight:700'>🏆 {c['prize']}</span>
                <span style='font-size:11px;color:#9ca3af'>👥 {c['part']} participanți</span>
              </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Înscrie-te", key=f"c_{i}", use_container_width=True):
                if not st.session_state.user:
                    st.warning("Trebuie să fii autentificat!")
                else:
                    st.success(f"✅ Înscris la {c['name']}!")

# ═══════════════════════════════════════════════════════════
# PAGE: MAGAZIN
# ═══════════════════════════════════════════════════════════
elif st.session_state.page == "Magazin":
    st.markdown("## 🛒 Magazin Pescuit")
    produse = [
        {"name":"Lansetă Crap Master 3.9m 3.5lb","brand":"Shimano","pret":"449 RON","vechi":"599 RON","emoji":"🎣","cat":"Lansete"},
        {"name":"Mulinetă Baitrunner ST 6000","brand":"Shimano","pret":"389 RON","vechi":"","emoji":"🔄","cat":"Mulinete"},
        {"name":"Fir Monofilament 0.35mm 1000m","brand":"Daiwa","pret":"89 RON","vechi":"110 RON","emoji":"🧵","cat":"Fire"},
        {"name":"Cârlige Barbless Curve Nr.6","brand":"Korda","pret":"29 RON","vechi":"","emoji":"🪝","cat":"Cârlige"},
        {"name":"Boilies Usturoi & Ficat 20mm 5kg","brand":"Nash","pret":"149 RON","vechi":"180 RON","emoji":"🍞","cat":"Momeli"},
        {"name":"Bivouac Carp Pro XL","brand":"Fox","pret":"899 RON","vechi":"1199 RON","emoji":"⛺","cat":"Corturi"},
        {"name":"Set 3 Alarme Digitale + Swinger","brand":"Fox","pret":"649 RON","vechi":"","emoji":"🔔","cat":"Electronice"},
        {"name":"Mănuși Pescuit Neopren 3mm","brand":"Carp Spirit","pret":"79 RON","vechi":"","emoji":"🧤","cat":"Îmbrăcăminte"},
        {"name":"Lanternă Frontală LED 300lm","brand":"Nash","pret":"129 RON","vechi":"159 RON","emoji":"🔦","cat":"Electronice"},
        {"name":"Umbrela Carp 2.5m Anti-UV","brand":"Fox","pret":"249 RON","vechi":"299 RON","emoji":"☂️","cat":"Accesorii"},
        {"name":"Scaun Pescuit Deluxe cu spătar","brand":"Carp Spirit","pret":"189 RON","vechi":"","emoji":"🪑","cat":"Accesorii"},
        {"name":"Navomodel Carp Boat GPS 500m","brand":"CarpBoat","pret":"1299 RON","vechi":"1599 RON","emoji":"⛵","cat":"Electronice"},
    ]

    col_filt, col_prod = st.columns([1, 4])
    with col_filt:
        st.markdown("**Categorii**")
        categorii = ["Toate"] + sorted(list(set(p["cat"] for p in produse)))
        cat_sel = st.radio("", categorii, label_visibility="collapsed")

    with col_prod:
        filtered_prod = produse if cat_sel == "Toate" else [p for p in produse if p["cat"] == cat_sel]
        cols = st.columns(3)
        for i, p in enumerate(filtered_prod):
            with cols[i % 3]:
                disc = p.get("vechi","")
                st.markdown(f"""
                <div class='card'>
                  <div style='font-size:40px;text-align:center;margin-bottom:8px'>{p['emoji']}</div>
                  {'<div style="text-align:center"><span class="badge-red">REDUCERE</span></div>' if disc else ''}
                  <b style='font-size:13px'>{p['name']}</b>
                  <div style='font-size:12px;color:#6b7280;margin:4px 0'>{p['brand']} · {p['cat']}</div>
                  <div style='display:flex;justify-content:space-between;align-items:center;margin-top:8px'>
                    <div>
                      <span style='color:#16a34a;font-weight:700;font-size:15px'>{p['pret']}</span>
                      {'<div style="font-size:11px;color:#9ca3af;text-decoration:line-through">'+disc+'</div>' if disc else ''}
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("🛒 Adaugă în coș", key=f"shop_{i}", use_container_width=True):
                    if not st.session_state.user:
                        st.warning("Trebuie să fii autentificat!")
                    else:
                        st.success(f"✅ {p['name']} adăugat în coș!")

# ═══════════════════════════════════════════════════════════
# PAGE: FORUM
# ═══════════════════════════════════════════════════════════
elif st.session_state.page == "Forum":
    st.markdown("## 💬 Forum PescuitRO")
    col_cats, col_threads = st.columns([1, 3])

    with col_cats:
        st.markdown("**Categorii**")
        categorii_forum = [
            ("📌","Anunțuri",3),
            ("🗺","Locații & Bălți",128),
            ("🐟","Tehnici de pescuit",95),
            ("🎣","Echipamente",74),
            ("🍽","Momeli & Nădire",61),
            ("🏆","Capturi record",43),
            ("📸","Galerie foto",112),
            ("❓","Întrebări începători",89),
            ("⚖️","Legislație ANPA",27),
        ]
        for icon, cat, nr in categorii_forum:
            st.markdown(f"{icon} **{cat}** `{nr}`")

    with col_threads:
        if st.button("✏️ Topic nou", use_container_width=False):
            if not st.session_state.user:
                st.warning("Trebuie să fii autentificat!")
            else:
                st.info("Funcționalitate în curând!")

        threads = [
            {"pin":True,"title":"Harta completă bălți crap oglindă 2025","autor":"Admin","timp":"Astăzi","raspunsuri":234,"views":"12.4k","tag":"Sticky"},
            {"pin":False,"title":"Balta Corbu vs Voluntari Elite – comparație detaliată","autor":"Mihai_Pescar","timp":"Acum 2h","raspunsuri":47,"views":"3.2k","tag":"Popular"},
            {"pin":False,"title":"Lacul Snagov 2025 – merită după prohibiție?","autor":"Andrei_T","timp":"Acum 5h","raspunsuri":32,"views":"1.8k","tag":""},
            {"pin":False,"title":"Heleșteu Brăila – crap de 22kg confirmat! Video în interior","autor":"BogdanC","timp":"Ieri","raspunsuri":89,"views":"5.6k","tag":"Hot"},
            {"pin":False,"title":"Ce baltă recomandați lângă Buzău pentru weekend?","autor":"FanPescuit","timp":"Ieri","raspunsuri":18,"views":"890","tag":""},
            {"pin":False,"title":"Bălți noi deschise în Ilfov în 2025 – listă actualizată","autor":"Admin","timp":"Acum 3 zile","raspunsuri":56,"views":"8.1k","tag":"Nou"},
            {"pin":False,"title":"Câte undițe se pot folosi simultan la Snagov?","autor":"Incepator99","timp":"Acum 4 zile","raspunsuri":12,"views":"445","tag":""},
        ]
        tag_colors = {"Sticky":"badge-amber","Popular":"badge-blue","Hot":"badge-red","Nou":"badge-green"}
        for t in threads:
            tag_html = f'<span class="{tag_colors.get(t["tag"],"badge-green")}" style="margin-left:6px">{t["tag"]}</span>' if t["tag"] else ""
            pin_html = "📌 " if t["pin"] else ""
            st.markdown(f"""
            <div class='card'>
              <div style='display:flex;justify-content:space-between;align-items:flex-start'>
                <div style='flex:1'>
                  <b>{pin_html}{t['title']}</b>{tag_html}
                  <div style='font-size:12px;color:#6b7280;margin-top:4px'>
                    👤 {t['autor']} · 🕐 {t['timp']}
                  </div>
                </div>
                <div style='text-align:right;margin-left:16px;flex-shrink:0'>
                  <div style='font-weight:700;font-size:16px'>{t['raspunsuri']}</div>
                  <div style='font-size:10px;color:#9ca3af'>RĂSPUNSURI</div>
                  <div style='font-size:11px;color:#9ca3af'>{t['views']} vizualizări</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# PAGE: REGULAMENTE
# ═══════════════════════════════════════════════════════════
elif st.session_state.page == "Regulamente":
    st.markdown("## 📋 Regulamente Pescuit România")
    st.info("⚠️ Informații orientative ANPA 2024–2025. Verificați întotdeauna pe anpa.ro înainte de pescuit.")

    tab1, tab2, tab3, tab4 = st.tabs(["📏 Dimensiuni minime","💰 Amenzi","📄 Documente obligatorii","💡 Sfaturi"])

    with tab1:
        df = pd.DataFrame([
            ["🐟 Crap","30 cm","1 Apr – 31 Mai",""],
            ["🐟 Caras","15 cm","1 Apr – 15 Mai",""],
            ["🐠 Știucă","40 cm","1 Feb – 31 Mar","Prohibiție iarnă-primăvară"],
            ["🦈 Somn","60 cm","1 Apr – 30 Mai",""],
            ["🐡 Biban","15 cm","1 Mar – 31 Mar",""],
            ["🐟 Șalău","40 cm","1 Apr – 31 Mai",""],
            ["🐟 Păstrăv","22 cm","1 Oct – 28 Feb","Sezon activ: Mart–Sept"],
            ["🐟 Lipan","25 cm","1 Nov – 28 Feb","Sezon activ: Mart–Oct"],
            ["🐟 Mreană","20 cm","1 Apr – 31 Mai",""],
            ["🐟 Amur","40 cm","1 Apr – 30 Mai",""],
            ["🐟 Plătică","20 cm","1 Apr – 15 Mai",""],
            ["⚠️ Sturioni","INTERZIS TOTAL","TOT ANUL","Specii strict protejate prin lege"],
        ], columns=["Specia","Dim. minimă","Prohibiție","Observații"])
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab2:
        for inf, amenda in [
            ("Pescuit fără permis valabil","2.000 – 6.000 RON"),
            ("Pește reținut sub dimensiunea minimă","2.000 – 10.000 RON"),
            ("Pescuit în perioadă de prohibiție","3.000 – 12.000 RON"),
            ("Electropescuit","20.000 – 40.000 RON + dosar penal"),
            ("Plase / setci ilegale","10.000 – 25.000 RON + confiscare"),
            ("Sturioni reținuți","30.000 – 50.000 RON + dosar penal"),
            ("Pescuit în zone strict protejate","5.000 – 15.000 RON"),
        ]:
            c1, c2 = st.columns([3,2])
            c1.write(inf)
            c2.markdown(f"**:red[{amenda}]**")
            st.divider()

    with tab3:
        for ok, text in [
            ("✅","Permis de pescuit sportiv (ANPA sau asociații județene AGVPS)"),
            ("✅","Timbru piscicol (valabil 1 an calendaristic, aplicat pe permis)"),
            ("✅","Act de identitate – buletin sau carte de identitate valabilă"),
            ("✅","Autorizație barcă – obligatorie dacă pescuiești din ambarcațiune"),
            ("ℹ️","Permisul se poate cumpăra online pe anpa.ro sau la sediile județene AGVPS"),
            ("ℹ️","Copiii sub 14 ani pot pescui gratuit însoțiți de un adult cu permis valabil"),
            ("ℹ️","Maximum 3 undițe simultan (regulă generală națională)"),
        ]:
            st.markdown(f"{ok} {text}")

    with tab4:
        for icon, text in [
            ("🌡","Temperatura optimă a apei pentru crap: 15–22°C"),
            ("🌅","Orele de vârf: zorii (4:00–8:00) și amurgul (18:00–22:00)"),
            ("🌧","După ploi ușoare nivelul de oxigen crește — peștele devine mai activ"),
            ("🌬","Vântul de vest și sud aduce aer cald și activitate crescută"),
            ("🌿","Vegetația acvatică deasă — ascunzători pentru știucă și biban"),
            ("❄️","Iarna, carasul și plătica sunt mai active decât crapul"),
            ("🐛","Nada naturală (grâu fiert, porumb, viermi) funcționează întotdeauna"),
            ("🌕","Luna plină poate inhiba activitatea peștelui în bălți mici"),
        ]:
            st.markdown(f"{icon} {text}")

# ═══════════════════════════════════════════════════════════
# PAGE: LOGIN
# ═══════════════════════════════════════════════════════════
elif st.session_state.page == "Login":
    _, col, _ = st.columns([1,2,1])
    with col:
        st.markdown("## 🎣 Bun venit pe PescuitRO!")
        st.markdown("Comunitatea pescarilor din România")
        st.divider()
        tab1, tab2 = st.tabs(["🔐 Intră în cont","📝 Cont nou"])
        with tab1:
            with st.form("login"):
                email  = st.text_input("Email", placeholder="pescar@email.ro")
                parola = st.text_input("Parolă", type="password")
                if st.form_submit_button("🔐 Intră în cont", use_container_width=True):
                    if email and parola:
                        st.session_state.user = email.split("@")[0].capitalize()
                        st.session_state.page = "Hartă"
                        st.success(f"Bun venit, {st.session_state.user}!")
                        st.rerun()
                    else:
                        st.error("Completează email și parolă!")
        with tab2:
            with st.form("register"):
                c1, c2 = st.columns(2)
                prenume  = c1.text_input("Prenume")
                nume     = c2.text_input("Nume")
                email_r  = st.text_input("Email", placeholder="pescar@email.ro")
                parola_r = st.text_input("Parolă", type="password")
                judet    = st.selectbox("Județul tău", [
                    "Alba","Arad","Argeș","Bacău","Bihor","Bistrița-Năsăud","Botoșani",
                    "Brăila","Brașov","București","Buzău","Călărași","Cluj","Constanța",
                    "Covasna","Dâmbovița","Dolj","Galați","Giurgiu","Gorj","Harghita",
                    "Hunedoara","Ialomița","Iași","Ilfov","Maramureș","Mehedinți","Mureș",
                    "Neamț","Olt","Prahova","Sălaj","Satu Mare","Sibiu","Suceava",
                    "Teleorman","Timiș","Tulcea","Vâlcea","Vaslui","Vrancea"])
                if st.form_submit_button("✅ Creează cont gratuit", use_container_width=True):
                    if prenume and email_r and parola_r:
                        st.session_state.user = prenume
                        st.session_state.page = "Hartă"
                        st.success(f"Cont creat! Bun venit, {prenume}!")
                        st.rerun()
                    else:
                        st.error("Completează toate câmpurile!")
        st.divider()
        if st.button("← Înapoi la hartă", use_container_width=True):
            st.session_state.page = "Hartă"
            st.rerun()
