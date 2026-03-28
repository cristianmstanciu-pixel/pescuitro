import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="PescuitRO", page_icon="🎣", layout="wide")

st.markdown("""
<style>
.card {
    background: white; border-radius: 12px;
    padding: 16px; margin-bottom: 10px;
    border: 1px solid #e4e7ec;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
.stButton>button {
    background-color: #16a34a; color: white;
    border-radius: 8px; border: none; font-weight: 600;
}
.stButton>button:hover { background-color: #15803d; }
</style>
""", unsafe_allow_html=True)

# ── DATE ──────────────────────────────────────────────────────
LOCATII = [
    {"id":1,"name":"Balta Corbu","county":"Ilfov","type":"premium","lat":44.55,"lon":26.40,
     "fish":["Crap oglindă","Crap comun","Știucă","Caras","Somn","Amur"],
     "area":"12 ha","depth":"max. 4m","rating":4.8,"fi":92,"night":True,"boat":True,"cr":False,
     "tariffs":[("Zi (1 undiță)","60 RON"),("Noapte","80 RON"),("Weekend","180 RON")],
     "contact":"0722 345 678","season":"Tot anul"},
    {"id":2,"name":"Râul Olt – Turnu Roșu","county":"Sibiu","type":"gratis","lat":45.60,"lon":24.20,
     "fish":["Păstrăv curcubeu","Păstrăv indigen","Lipan","Clean"],
     "area":"15km sector","depth":"0.5–3m","rating":4.6,"fi":85,"night":False,"boat":False,"cr":True,
     "tariffs":[("Permis zilnic AGVPS","30 RON"),("Anual ANPA","100 RON")],
     "contact":"0269 211 555","season":"Mai–Oct"},
    {"id":3,"name":"Heleșteu Brăila","county":"Brăila","type":"premium","lat":45.20,"lon":27.80,
     "fish":["Crap oglindă 25kg+","Amur alb","Somn african"],
     "area":"20 ha","depth":"max. 5m","rating":4.9,"fi":97,"night":True,"boat":True,"cr":True,
     "tariffs":[("Stand 24h","150 RON"),("Stand 48h","260 RON"),("Stand 72h","350 RON")],
     "contact":"0740 999 888","season":"Tot anul"},
    {"id":4,"name":"Lacul Snagov","county":"Ilfov","type":"gratis","lat":44.73,"lon":26.15,
     "fish":["Crap","Știucă","Somn","Roșioară","Biban","Plătică"],
     "area":"575 ha","depth":"max. 9m","rating":3.9,"fi":70,"night":True,"boat":True,"cr":False,
     "tariffs":[("Permis ANPA anual","100 RON"),("Timbru piscicol","50 RON")],
     "contact":"021 350 xxxx","season":"Tot anul"},
    {"id":5,"name":"Dunărea – Delta Tulcea","county":"Tulcea","type":"gratis","lat":45.18,"lon":28.80,
     "fish":["Somn 100kg+","Știucă","Crap","Plătică"],
     "area":"Delta Dunării","depth":"5–25m","rating":4.7,"fi":88,"night":True,"boat":True,"cr":False,
     "tariffs":[("Permis ANPA anual","100 RON"),("Ghid local","300–500/zi")],
     "contact":"0240 515 xxx","season":"Tot anul"},
    {"id":6,"name":"Balta Voluntari Elite","county":"Ilfov","type":"premium","lat":44.49,"lon":26.18,
     "fish":["Crap oglindă","Amur","Șalău"],
     "area":"7 ha","depth":"max. 4m","rating":4.7,"fi":95,"night":True,"boat":True,"cr":True,
     "tariffs":[("Zi (1 undiță)","80 RON"),("Noapte premium","150 RON"),("Lunar","800 RON")],
     "contact":"0731 888 777","season":"Tot anul"},
    {"id":7,"name":"Lacul Vidraru","county":"Argeș","type":"gratis","lat":45.35,"lon":24.63,
     "fish":["Păstrăv curcubeu","Șalău","Biban","Clean"],
     "area":"870 ha","depth":"max. 155m","rating":4.7,"fi":88,"night":False,"boat":True,"cr":False,
     "tariffs":[("Permis ANPA anual","100 RON"),("Timbru piscicol","50 RON")],
     "contact":"0248 xxx xxx","season":"Mai–Oct"},
    {"id":8,"name":"Lacul Stânca-Costești","county":"Botoșani","type":"gratis","lat":47.87,"lon":26.91,
     "fish":["Șalău","Somn","Crap","Amur","Plătică"],
     "area":"5900 ha","depth":"max. 30m","rating":4.6,"fi":86,"night":True,"boat":True,"cr":False,
     "tariffs":[("Permis ANPA anual","100 RON"),("Viză frontieră","30 RON")],
     "contact":"0231 xxx xxx","season":"Tot anul"},
    {"id":9,"name":"Lacul Țaga Mică","county":"Cluj","type":"privata","lat":47.00,"lon":23.97,
     "fish":["Crap","Șalău","Somn","Ctenofaring"],
     "area":"24 ha","depth":"6m","rating":4.8,"fi":92,"night":True,"boat":False,"cr":False,
     "tariffs":[("Ponton 24h","50 RON"),("Căbănuță 24h","250 RON")],
     "contact":"0264 xxx xxx","season":"Tot anul"},
    {"id":10,"name":"Dunărea – Cazanele Mari","county":"Mehedinți","type":"gratis","lat":44.67,"lon":22.38,
     "fish":["Somn","Crap","Avat","Morunaș","Clean"],
     "area":"Defileu Dunăre","depth":"50–90m","rating":4.8,"fi":91,"night":True,"boat":True,"cr":False,
     "tariffs":[("Permis ANPA anual","100 RON"),("Ghid local","200–400/zi")],
     "contact":"0252 xxx xxx","season":"Tot anul"},
    {"id":11,"name":"Brațul Sulina","county":"Tulcea","type":"gratis","lat":45.15,"lon":29.40,
     "fish":["Somn","Știucă","Crap","Șalău","Biban"],
     "area":"Brațul Sulina","depth":"10–20m","rating":4.9,"fi":95,"night":True,"boat":True,"cr":False,
     "tariffs":[("Permis ANPA anual","100 RON"),("Ghid local","400–600/zi")],
     "contact":"0240 516 xxx","season":"Tot anul"},
    {"id":12,"name":"Lacul Colibița","county":"Bistrița-Năsăud","type":"gratis","lat":47.10,"lon":24.95,
     "fish":["Păstrăv curcubeu","Biban","Șalău"],
     "area":"440 ha","depth":"max. 42m","rating":4.7,"fi":88,"night":True,"boat":True,"cr":False,
     "tariffs":[("Permis ANPA anual","100 RON"),("Timbru piscicol","50 RON")],
     "contact":"0263 xxx xxx","season":"Mai–Oct"},
    {"id":13,"name":"Lacul Roșu","county":"Harghita","type":"gratis","lat":46.77,"lon":25.76,
     "fish":["Păstrăv curcubeu","Biban","Păstrăv indigen"],
     "area":"12.6 ha","depth":"max. 10m","rating":4.8,"fi":86,"night":False,"boat":True,"cr":False,
     "tariffs":[("Permis ANPA anual","100 RON"),("Timbru piscicol","50 RON")],
     "contact":"0266 xxx xxx","season":"Mai–Sept"},
    {"id":14,"name":"Balta Fibis","county":"Timiș","type":"privata","lat":45.71,"lon":21.42,
     "fish":["Crap","Somn","Caras","Biban"],
     "area":"18 ha","depth":"4m","rating":4.4,"fi":80,"night":True,"boat":False,"cr":False,
     "tariffs":[("Zi (1 undiță)","45 RON"),("Noapte","70 RON"),("Lunar","400 RON")],
     "contact":"0256 xxx xxx","season":"Tot anul"},
    {"id":15,"name":"Laguna Verde Balotești","county":"Ilfov","type":"privata","lat":44.65,"lon":26.07,
     "fish":["Crap oglindă","Amur","Caras","Știucă"],
     "area":"20 ha","depth":"4m","rating":4.6,"fi":88,"night":True,"boat":True,"cr":False,
     "tariffs":[("Zi (1 undiță)","60 RON"),("Noapte","90 RON"),("Căsuță 24h","250 RON")],
     "contact":"0721 xxx xxx","season":"Tot anul"},
]

# ── SESSION STATE ─────────────────────────────────────────────
if "selected" not in st.session_state:
    st.session_state.selected = None
if "user" not in st.session_state:
    st.session_state.user = None
if "jurnal" not in st.session_state:
    st.session_state.jurnal = []
if "page" not in st.session_state:
    st.session_state.page = "Hartă"

# ── NAVBAR ────────────────────────────────────────────────────
col_logo, col_nav, col_auth = st.columns([2, 5, 2])
with col_logo:
    st.markdown("## 🎣 **PescuitRO**")
with col_nav:
    pages = ["Hartă", "Jurnal", "Concursuri", "Regulamente"]
    cols = st.columns(len(pages))
    for i, p in enumerate(pages):
        with cols[i]:
            if st.button(p, key=f"nav_{p}"):
                st.session_state.page = p
                st.rerun()
with col_auth:
    if st.session_state.user:
        st.markdown(f"👤 **{st.session_state.user}**")
        if st.button("Deconectare"):
            st.session_state.user = None
            st.rerun()
    else:
        if st.button("🔐 Intră în cont"):
            st.session_state.page = "Login"
            st.rerun()

st.divider()

# ════════════════════════════════════════════════════════════
# PAGE: HARTA
# ════════════════════════════════════════════════════════════
if st.session_state.page == "Hartă":

    with st.sidebar:
        st.markdown("### 🔍 Filtre")
        tip_filter   = st.selectbox("Tip locație", ["Toate","Gratuit","Privată","Premium"])
        night_filter = st.checkbox("🌙 Pescuit noapte")
        boat_filter  = st.checkbox("⛵ Permite vaporașe")
        cr_filter    = st.checkbox("🔄 Catch & Release")
        search_q     = st.text_input("🔎 Caută")
        st.divider()
        st.metric("Total locații", len(LOCATII))
        st.metric("Gratuite", sum(1 for l in LOCATII if l["type"] == "gratis"))
        st.metric("Premium", sum(1 for l in LOCATII if l["type"] == "premium"))

    filtered = LOCATII
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
            i = icon_map.get(loc["type"], "map-marker")
            popup_html = f"""
            <div style='font-family:Arial;min-width:180px'>
              <b style='font-size:14px'>{loc['name']}</b><br>
              <span style='color:#6b7280;font-size:12px'>📍 {loc['county']} · {loc['area']}</span><br>
              <span style='font-size:11px'>{' · '.join(loc['fish'][:3])}</span><br>
              <span style='color:#f59e0b'>{'★' * int(loc['rating'])}</span>
              <span style='font-size:12px'> {loc['rating']}</span>
            </div>
            """
            folium.Marker(
                location=[loc["lat"], loc["lon"]],
                popup=folium.Popup(popup_html, max_width=220),
                tooltip=loc["name"],
                icon=folium.Icon(color=c, icon=i, prefix="glyphicon")
            ).add_to(m)
        st_folium(m, width=700, height=500)

    with col_list:
        st.markdown("### 📋 Locații")
        for loc in filtered:
            badge = {"gratis":"🟢 Gratuit","privata":"🔵 Privată","premium":"⭐ Premium"}.get(loc["type"],"")
            stars = "★" * int(loc["rating"]) + "☆" * (5 - int(loc["rating"]))
            st.markdown(f"""
            <div class='card'>
              <div style='display:flex;justify-content:space-between'>
                <b>{loc['name']}</b>
                <span style='font-size:11px'>{badge}</span>
              </div>
              <div style='color:#6b7280;font-size:12px'>📍 {loc['county']} · {loc['area']}</div>
              <div style='font-size:11px;color:#9ca3af'>{' · '.join(loc['fish'][:3])}</div>
              <div style='margin-top:4px'>
                <span style='color:#f59e0b'>{stars}</span>
                <span style='font-size:12px'> {loc['rating']}</span>
                <span style='float:right;color:#16a34a;font-size:11px;font-weight:600'>Ind.{loc['fi']}/100</span>
              </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔍 Detalii", key=f"btn_{loc['id']}"):
                st.session_state.selected = loc["id"]
                st.rerun()

    if st.session_state.selected:
        loc = next((l for l in LOCATII if l["id"] == st.session_state.selected), None)
        if loc:
            st.divider()
            st.markdown(f"## 📍 {loc['name']} — {loc['county']}")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Rating", f"{loc['rating']} ⭐")
            c2.metric("Suprafață", loc["area"])
            c3.metric("Adâncime", loc["depth"])
            c4.metric("Indice pescuit", f"{loc['fi']}/100")
            tab1, tab2, tab3, tab4 = st.tabs(["🐟 Pești","💰 Tarife","📜 Info","🗺 Navigare"])
            with tab1:
                for f in loc["fish"]:
                    st.markdown(f"🐟 {f}")
                c1, c2, c3 = st.columns(3)
                c1.markdown(f"🌙 Noapte: {'✅' if loc['night'] else '❌'}")
                c2.markdown(f"⛵ Vaporașe: {'✅' if loc['boat'] else '❌'}")
                c3.markdown(f"🔄 C&R: {'✅' if loc['cr'] else '❌'}")
            with tab2:
                if loc["type"] == "gratis":
                    st.info("ℹ️ Necesită permis ANPA + timbru piscicol (anpa.ro)")
                for label, price in loc["tariffs"]:
                    c1, c2 = st.columns([3,1])
                    c1.write(label)
                    c2.markdown(f"**{price}**")
            with tab3:
                st.markdown(f"**Sezon:** {loc['season']}")
                st.markdown(f"**📞 Contact:** {loc['contact']}")
            with tab4:
                gmap = f"https://www.google.com/maps/search/?api=1&query={loc['lat']},{loc['lon']}"
                waze = f"https://waze.com/ul?ll={loc['lat']},{loc['lon']}&navigate=yes"
                st.markdown(f"[🗺 Google Maps]({gmap})")
                st.markdown(f"[🚗 Waze]({waze})")
            if st.button("✕ Închide"):
                st.session_state.selected = None
                st.rerun()

# ════════════════════════════════════════════════════════════
# PAGE: JURNAL
# ════════════════════════════════════════════════════════════
elif st.session_state.page == "Jurnal":
    if not st.session_state.user:
        st.warning("⚠️ Trebuie să fii autentificat pentru jurnal.")
        if st.button("🔐 Intră în cont"):
            st.session_state.page = "Login"
            st.rerun()
    else:
        st.markdown("## 📓 Jurnalul Meu")
        j = st.session_state.jurnal
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Ieșiri", len(j))
        c2.metric("Pești", sum(1 for e in j if e.get("specie")))
        c3.metric("Record", f"{max((e.get('kg',0) for e in j), default=0)} kg")
        c4.metric("Specii", len(set(e.get("specie","") for e in j if e.get("specie"))))

        with st.expander("➕ Adaugă ieșire", expanded=True):
            with st.form("jurnal_form"):
                c1, c2 = st.columns(2)
                with c1:
                    data    = st.date_input("Data")
                    locatie = st.text_input("Locație")
                    specie  = st.selectbox("Specia", ["","Crap oglindă","Crap comun","Amur",
                                "Știucă","Somn","Șalău","Biban","Caras","Pástrăv","Lipan","Mreană"])
                with c2:
                    kg      = st.number_input("Greutate (kg)", min_value=0.0, step=0.1)
                    momeala = st.text_input("Momeala")
                    meteo   = st.selectbox("Meteo", ["☀️ Soare","⛅ Noros","🌧 Ploaie","❄️ Frig"])
                note = st.text_area("Note")
                if st.form_submit_button("💾 Salvează"):
                    if locatie and specie:
                        st.session_state.jurnal.append({
                            "data":str(data),"locatie":locatie,"specie":specie,
                            "kg":kg,"momeala":momeala,"meteo":meteo,"note":note
                        })
                        st.success("✅ Salvat!")
                        st.rerun()
                    else:
                        st.error("Completează locația și specia!")

        if st.session_state.jurnal:
            st.markdown("### Istoricul tău")
            for i, e in enumerate(reversed(st.session_state.jurnal)):
                c1, c2, c3, c4, c5 = st.columns([2,3,2,2,1])
                c1.write(e["data"])
                c2.write(f"📍 {e['locatie']}")
                c3.write(f"🐟 {e['specie']}")
                c4.write(f"⚖️ {e['kg']} kg" if e['kg'] else "–")
                if c5.button("🗑", key=f"del_{i}"):
                    st.session_state.jurnal.pop(len(st.session_state.jurnal)-1-i)
                    st.rerun()
                st.divider()

# ════════════════════════════════════════════════════════════
# PAGE: CONCURSURI
# ════════════════════════════════════════════════════════════
elif st.session_state.page == "Concursuri":
    st.markdown("## 🏆 Concursuri & Evenimente 2025")
    concursuri = [
        {"name":"Cupa Dunării 2025","date":"15 Iunie 2025","loc":"Delta Tulcea","prize":"5.000 RON","part":64,"emoji":"🏆"},
        {"name":"Campionatul Județean Ilfov","date":"22 Mai 2025","loc":"Balta Corbu","prize":"2.000 RON","part":32,"emoji":"🎣"},
        {"name":"Trofeul Păstrăvului","date":"8 Iunie 2025","loc":"Râul Olt, Sibiu","prize":"1.500 RON","part":28,"emoji":"🐟"},
        {"name":"Maratonul Somnului","date":"5 Iulie 2025","loc":"Dunăre, Galați","prize":"3.000 RON","part":48,"emoji":"🦈"},
        {"name":"Cupă C&R Voluntari","date":"12 Iulie 2025","loc":"Balta Voluntari Elite","prize":"Trofeu","part":20,"emoji":"🎯"},
    ]
    cols = st.columns(3)
    for i, c in enumerate(concursuri):
        with cols[i % 3]:
            st.markdown(f"""
            <div class='card'>
              <div style='font-size:32px;text-align:center'>{c['emoji']}</div>
              <b>{c['name']}</b>
              <div style='font-size:12px;color:#6b7280'>📅 {c['date']}</div>
              <div style='font-size:12px;color:#6b7280'>📍 {c['loc']}</div>
              <div style='color:#16a34a;font-weight:600;margin-top:6px'>🏆 {c['prize']}</div>
              <div style='font-size:11px;color:#9ca3af'>👥 {c['part']} participanți</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Înscrie-te", key=f"c_{i}"):
                if not st.session_state.user:
                    st.warning("Trebuie să fii autentificat!")
                else:
                    st.success(f"✅ Înscris la {c['name']}!")

# ════════════════════════════════════════════════════════════
# PAGE: REGULAMENTE
# ════════════════════════════════════════════════════════════
elif st.session_state.page == "Regulamente":
    st.markdown("## 📋 Regulamente Pescuit România")
    st.info("⚠️ Informații ANPA 2024–2025. Verificați pe anpa.ro.")
    import pandas as pd
    tab1, tab2, tab3 = st.tabs(["📏 Dimensiuni","💰 Amenzi","💡 Sfaturi"])
    with tab1:
        df = pd.DataFrame([
            ["🐟 Crap","30 cm","1 Apr – 31 Mai"],
            ["🐟 Caras","15 cm","1 Apr – 15 Mai"],
            ["🐠 Știucă","40 cm","1 Feb – 31 Mar"],
            ["🦈 Somn","60 cm","1 Apr – 30 Mai"],
            ["🐟 Șalău","40 cm","1 Apr – 31 Mai"],
            ["🐟 Păstrăv","22 cm","1 Oct – 28 Feb"],
            ["⚠️ Sturioni","INTERZIS","TOT ANUL"],
        ], columns=["Specia","Dim. minimă","Prohibiție"])
        st.dataframe(df, use_container_width=True, hide_index=True)
    with tab2:
        for inf, amenda in [
            ("Pescuit fără permis","2.000–6.000 RON"),
            ("Pește sub dimensiunea minimă","2.000–10.000 RON"),
            ("Pescuit în prohibiție","3.000–12.000 RON"),
            ("Electropescuit","20.000–40.000 RON + dosar penal"),
            ("Sturioni reținuți","30.000–50.000 RON + dosar penal"),
        ]:
            c1, c2 = st.columns([3,2])
            c1.write(inf)
            c2.markdown(f"**:red[{amenda}]**")
            st.divider()
    with tab3:
        for icon, text in [
            ("🌡","Temperatura optimă apă: 15–22°C"),
            ("🌅","Zorii (4–8) și amurgul (18–22) = ore de vârf"),
            ("🌧","După ploaie ușoară: pești mai activi"),
            ("🌿","Vegetație deasă = ascunzători pentru știucă"),
            ("❄️","Iarna: carasul și plătica > crapul"),
            ("🐛","Nada naturală funcționează întotdeauna"),
        ]:
            st.markdown(f"{icon} {text}")

# ════════════════════════════════════════════════════════════
# PAGE: LOGIN
# ════════════════════════════════════════════════════════════
elif st.session_state.page == "Login":
    _, col, _ = st.columns([1,2,1])
    with col:
        st.markdown("## 🎣 Intră în cont")
        tab1, tab2 = st.tabs(["Intră în cont","Cont nou"])
        with tab1:
            with st.form("login"):
                email = st.text_input("Email")
                parola = st.text_input("Parolă", type="password")
                if st.form_submit_button("🔐 Intră"):
                    if email and parola:
                        st.session_state.user = email.split("@")[0].capitalize()
                        st.session_state.page = "Hartă"
                        st.rerun()
                    else:
                        st.error("Completează email și parolă!")
        with tab2:
            with st.form("register"):
                c1, c2 = st.columns(2)
                prenume = c1.text_input("Prenume")
                nume    = c2.text_input("Nume")
                email_r = st.text_input("Email")
                parola_r = st.text_input("Parolă", type="password")
                if st.form_submit_button("✅ Creează cont"):
                    if prenume and email_r and parola_r:
                        st.session_state.user = prenume
                        st.session_state.page = "Hartă"
                        st.rerun()
                    else:
                        st.error("Completează toate câmpurile!")
        if st.button("← Înapoi"):
            st.session_state.page = "Hartă"
            st.rerun()