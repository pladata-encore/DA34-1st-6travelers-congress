#!/usr/bin/env python
# coding: utf-8

# In[10]:


import pandas as pd
import json
import folium
from zipfile import ZipFile
import os

# Load the election data
election_data_path = r'C:\Users\Playdata\Downloads\21_election.csv'
election_data = pd.read_csv(election_data_path)

# Extract the geojson data
zip_file_path = r'C:\Users\Playdata\Downloads\21_newgeo.zip'
extraction_directory = '/mnt/data/21_newgeo'
with ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extraction_directory)
geojson_path = os.path.join(extraction_directory, '21_newgeo.json')
with open(geojson_path, 'r', encoding='utf-8') as f:
    geo_data = json.load(f)

# Define colors for the major parties
party_colors = {
    '더불어민주당': 'blue',
    '미래통합당': 'red',
    '기타': 'gray'
}

# Function to get color for each district based on the party
def get_color_corrected(district):
    party = election_data.loc[election_data['sido'] == district, 'party'].values
    if len(party) > 0:
        return party_colors.get(party[0], party_colors['기타'])
    return party_colors['기타']

# Create a folium map and add the geojson data with coloring based on party
m_corrected = folium.Map(location=[36.5, 127.5], zoom_start=7)
folium.GeoJson(
    geo_data,
    style_function=lambda feature: {
        'fillColor': get_color_corrected(feature['properties']['SGG_2']),
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.7
    },
    tooltip=folium.GeoJsonTooltip(fields=['SGG_2'], aliases=['지역구:']),
).add_to(m_corrected)


# In[11]:


# Save the map to an HTML file
map_path_corrected = 'korean_political_map_corrected.html'
m_corrected.save(map_path_corrected)


# In[12]:


import pandas as pd
import json
from zipfile import ZipFile
import os
import folium

# Load the election data
election_data_path = r'C:\Users\Playdata\Downloads\21_election.csv'
election_data = pd.read_csv(election_data_path)

# Extract the geojson data
zip_file_path = r'C:\Users\Playdata\Downloads\21_newgeo.zip'
extraction_directory = '/mnt/data/21_newgeo'
with ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extraction_directory)
geojson_path = os.path.join(extraction_directory, '21_newgeo.json')
with open(geojson_path, 'r', encoding='utf-8') as f:
    geo_data = json.load(f)

# Define colors for the major parties
party_colors = {
    '더불어민주당': 'blue',
    '미래통합당': 'red',
    '기타': 'gray'
}

# Function to get color for each district based on the party
def get_color_corrected(district):
    party = election_data.loc[election_data['sido'] == district, 'party'].values
    if len(party) > 0:
        return party_colors.get(party[0], party_colors['기타'])
    return party_colors['기타']

# 각 지역구(SGG_2)에 대한 선거 정보 문자열 생성 및 주입 - sido, party, name 활용
election_info = {}
for _, row in election_data.iterrows():
    # 지역구 이름 추출 및 조정
    sgg_2 = row['sido'].replace('서울특별시', '')  # 예시로 '서울특별시' 제거. 실제 데이터 구조에 맞게 조정 필요
    info = f"당선자: {row['name']}, 정당: {row['party']}"
    election_info[sgg_2] = info

# GeoJSON 데이터에 선거 정보 주입
for feature in geo_data['features']:
    sgg_2_feature = feature['properties']['SGG_2']
    feature['properties']['election_info'] = election_info.get(sgg_2_feature, "정보 없음")

# Folium 지도 생성 및 GeoJSON 레이어 추가
m = folium.Map(location=[36.5, 127.5], zoom_start=7)
folium.GeoJson(
    geo_data,
    style_function=lambda feature: {
        'fillColor': get_color_corrected(feature['properties']['SGG_2']),  # 예시 색상. 실제로는 색상 지정 로직을 사용해야 함
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.7
    },
    tooltip=folium.GeoJsonTooltip(fields=['SGG_2', 'election_info'], aliases=['지역구:', '선거 정보:']),
    popup=folium.GeoJsonPopup(fields=['SGG_2', 'election_info'], aliases=['지역구 이름:', '선거 정보:'])
).add_to(m)

# 지도 저장
map_path = 'congressman.html'
m.save(map_path)

