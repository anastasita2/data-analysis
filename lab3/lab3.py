import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import os


cities = {
    1: "Черкаси",
    2: "Чернігів",
    3: "Чернівці",
    4: "Крим",
    5: "Дніпропетровськ",
    6: "Донецьк",
    7: "Івано-Франківськ",
    8: "Харків",
    9: "Херсон",
    10: "Хмельницький",
    11: "Київ",
    12: "Місто Київ",
    13: "Кіровоград",
    14: "Луганськ",
    15: "Львів",
    16: "Миколаїв",
    17: "Одеса",
    18: "Полтава",
    19: "Рівне",
    20: "Севастополь",
    21: "Суми",
    22: "Тернопіль",
    23: "Закарпаття",
    24: "Вінниця",
    25: "Волинь",
    26: "Запоріжжя",
    27: "Житомир"
}


def framer():
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'area']
    files_dir = "F:\Яковенко\da\da\lab3\VHI_Files"
    dataframe = pd.DataFrame()
    files = os.listdir(files_dir)
    for file in files:
        path = os.path.join(files_dir, file)
        try:
            df = pd.read_csv(path, header=1, names=headers)
            df = df.drop(df.loc[df["VHI"] == -1].index)
            df["area"] = int(file.split("_")[1])
            df['Year'] = df['Year'].astype(str).str.replace("<tt><pre>", "")
            df = df[~df['Year'].str.contains('</pre></tt>')]
            df['Year'] = df['Year'].astype(int)
            df['Week'] = df['Week'].astype(int)
            dataframe = pd.concat([dataframe, df]).drop_duplicates().reset_index(drop=True)
        except:
            continue
    return dataframe

df = framer()

default_state = {
    "index": "VHI",
    "region_name": list(cities.values())[0],
    "week_range": (1, 52),
    "year_range": (2000, 2021),
    "sort_asc": False,
    "sort_desc": False,
}

for key, val in default_state.items():
    if key not in st.session_state:
        st.session_state[key] = val

if st.button("Скинути фільтри"):
    for key, val in default_state.items():
        st.session_state[key] = val
    st.rerun()


col1, col2 = st.columns([1, 3])

with col1:
    st.session_state.index = st.selectbox("Оберіть індекс:", ["VCI", "TCI", "VHI"], 
                                          index=["VCI", "TCI", "VHI"].index(st.session_state.index))
    st.session_state.region_name = st.selectbox("Оберіть область:", list(cities.values()),
                                                index=list(cities.values()).index(st.session_state.region_name))
    st.session_state.week_range = st.slider("Інтервал тижнів:", 1, 52, st.session_state.week_range)
    st.session_state.year_range = st.slider("Інтервал років:", int(df["Year"].min()), int(df["Year"].max()), 
                                            st.session_state.year_range)
    st.session_state.sort_asc = st.checkbox("Сортувати за зростанням", value=st.session_state.sort_asc)
    st.session_state.sort_desc = st.checkbox("Сортувати за спаданням", value=st.session_state.sort_desc)

    if st.session_state.sort_asc and st.session_state.sort_desc:
        st.warning("Виберіть лише один тип сортування.")

with col2:
    tab1, tab2, tab3 = st.tabs(["Таблиця", "Графік", "Порівняння"])

    region_id = list(cities.keys())[list(cities.values()).index(st.session_state.region_name)]

    filtered = df[
        (df["area"] == region_id) &
        (df["Week"].between(*st.session_state.week_range)) &
        (df["Year"].between(*st.session_state.year_range))
    ][["Year", "Week", st.session_state.index, "area"]]

    if st.session_state.sort_asc:
        filtered = filtered.sort_values(by=st.session_state.index, ascending=True)
    elif st.session_state.sort_desc:
        filtered = filtered.sort_values(by=st.session_state.index, ascending=False)

    with tab1:
        st.dataframe(filtered)

    with tab2:
        plt.style.use("dark_background")
        avg_by_week = filtered.groupby("Week")[st.session_state.index].mean().reset_index()
        plt.figure(figsize=(10, 5))
        sns.lineplot(data=avg_by_week, x="Week", y=st.session_state.index, marker="o")
        plt.title(f"Середнє значення {st.session_state.index} по тижнях ({st.session_state.region_name})")
        plt.xlabel("Тиждень")
        plt.ylabel(st.session_state.index)
        plt.grid(True)
        st.pyplot(plt.gcf())


    with tab3:
        comparison = df[
            (df["Week"].between(*st.session_state.week_range)) &
            (df["Year"].between(*st.session_state.year_range))
        ]
        plt.style.use("dark_background")
        plt.figure(figsize=(16, 6))
        comparison["region"] = comparison["area"].map(cities)
    
        sns.boxplot(data=comparison, x="region", y=st.session_state.index)
        plt.xticks(rotation=90)
        plt.title(f"Boxplot розподілу {st.session_state.index} по всіх областях")
        plt.xlabel("Область")
        plt.ylabel(st.session_state.index)
        st.pyplot(plt.gcf())

