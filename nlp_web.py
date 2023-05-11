import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
import emoji
import gspread
from google.oauth2.service_account import Credentials


st.set_page_config(page_title='Quiz', page_icon=':bar_chart:', layout="wide")

st.title("🧠Quiz Neuro-Linguistic Programming")
st.write(
    """
Hai! Adakah anda ingin tahu bagaimana anda berkomunikasi dan membuat keputusan?
    Kuiz ini direka untuk membantu anda mengenal pasti kecenderungan anda dalam berkomunikasi dan membuat keputusan yang terbahagi kepada empat kategori: **Visual** (**V**), **Auditori** (**A**), **Kinestetik** (**K**), **Digital** (**D**). Dengan memahami gaya unik anda, anda boleh meningkatkan kesedaran diri, memperbaiki interaksi dengan orang lain, dan membuat keputusan yang lebih efektif dalam pelbagai situasi. Ikuti kuiz ini untuk mengetahui gaya peribadi anda dan membuka kunci ke arah komunikasi dan kerjasama dalam organisasi yang lebih baik!
""")
st.subheader("📝Sila isikan maklumat anda:")

name = st.text_input("Nama:")

gender_age_columns = st.columns(2, gap='medium')  # create two columns for gender and age

# Jantina input box in the first column
gender_options = ["--Pilih jantina--", "LELAKI", "PEREMPUAN"]
gender = gender_age_columns[0].selectbox("Jantina:", gender_options)

# Umur input box in the second column
age = gender_age_columns[1].number_input("Umur:", min_value=1, max_value=80, step=1)
st.markdown("<br>", unsafe_allow_html=True)  # Add an empty line or spacing before the "Submit" button

def write_to_sheet(client, url, data):
    sheet = client.open_by_url(url).sheet1  # If your worksheet has a different name, replace 'sheet1' with the name of your worksheet
    sheet.append_row(data)

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
]

skey = st.secrets["gcp_service_account"]
credentials = Credentials.from_service_account_info(
    skey,
    scopes=scopes,
)
client = gspread.authorize(credentials)

if st.button("Hantar Maklumat"):
    if name and gender != "--Pilih jantina--" and age:
        st.success(f"Maklumat berjaya direkod.")

    else:
        st.warning("Sila isikan semua butiran di atas.")


sub_questions = [
    {"question": "Rasa hati & keselesaan", "category": "K"},
    {"question": "Bunyi idea", "category": "A"},
    {"question": "Gambaran terhadap idea", "category": "V"},
    {"question": "Kajian mendalam tentang isu", "category": "D"},
    {"question": "Nada dan intonasi orang", "category": "A"},
    {"question": "Sama ada saya boleh melihat pandangan orang atau tidak", "category": "V"},
    {"question": "Logik dan rasional pandangan orang", "category": "D"},
    {"question": "Sama ada orang sensitif atau tdak terhadap perasaan saya", "category": "K"},
    {"question": "Rupa dan pemakaian saya", "category": "V"},
    {"question": "Berkongsi perasaan dan pengalaman", "category": "K"},
    {"question": "Mengetahui maksud perkataan saya difahami", "category": "D"},
    {"question": "Didengari dan diberi perhatian", "category": "A"},
    {"question": "Dengar dengan teliti dan bertanya soalan,untuk memastikan saya faham", "category": "A"},
    {"question": "Lebih suka untuk memikirkanya dahulu,dan memilih perkataan sesuai", "category": "D"},
    {"question": "Dihargai apabila diberi masa untuk mencari jawapannya dahulu", "category": "K"},
    {"question": "Jawab dengan cepat, dengan cara menggambarkan jawapanya", "category": "V"},
    {"question": "Peka terhadap bunyi di sekitar", "category": "A"},
    {"question": "Mudah memahami fakta dan maklumat", "category": "D"},
    {"question": "Sensitif dan fleksibel dalam perhubungan", "category": "K"},
    {"question": "Kreatif dan mampu menguruskan jumlah maklumat yang baik", "category": "V"},
    {"question": "Boleh menghubungkan diri dengan perasaan saya", "category": "K"},
    {"question": "Boleh melihat pandangan saya", "category": "V"},
    {"question": "Dengar dengan baik apa yang saya perkatakan dan cara disampaikan", "category": "A"},
    {"question": "Berminat dengan maksud perkara yang saya sampaikan", "category": "D"},
    {"question": "Memperbaiki proses dengan idea saya", "category": "A"},
    {"question": "Terlibat dengan proses perancangan dan menentukan visi", "category": "V"},
    {"question": "Mengatur perjalanan program dan menyusunnya", "category": "D"},
    {"question": "Membina perhubungan yang lebih baik antara ahli", "category": "K"},
    {"question": "Menunjukkannya kepada saya adalah paling jelas", "category": "V"},
    {"question": "Saya boleh ingat dengan baik hanya dengan mendengar", "category": "A"},
    {"question": "Menuliskannya membantu saya untuk memahaminya", "category": "K"},
    {"question": "Menerangkan fakta dengan cara logikal adalah lebih bermakna", "category": "D"},
    {"question": "Mempercayai orang lain, situasi atau konsep", "category": "D"},
    {"question": "Menjadi diplomatik, sebaliknya akan beterus terang", "category": "A"},
    {"question": "Memisahkan emosi diri dengan perasaan orang lain", "category": "K"},
    {"question": "Menjadi fleksibel dan menukar rancangan", "category": "V"},
    {"question": "Menerima inspirasi dari dalam", "category": "D"},
    {"question": "Memberitahu di mana idea baru boleh digunakan", "category": "A"},
    {"question": "Mengikuti kaedah yang telah dibuktikan berkesan", "category": "K"},
    {"question": "Merancang dan menguruskan aktiviti", "category": "V"}
]

likert_scale = [
    "--Sila pilih--",
    "Sebijik macam saya",
    "Hampir macam saya",
    "Lebih kurang macam saya",
    "Jauh sekali macam saya"
]

likert_scale_values = {
    "--Sila pilih--": 0,
    "Sebijik macam saya": 4,
    "Hampir macam saya": 3,
    "Lebih kurang macam saya": 2,
    "Jauh sekali macam saya": 1
}

scores = {"V": 0, "A": 0, "K": 0, "D": 0, "total": 0}
st.markdown("<br>", unsafe_allow_html=True)  # Add an empty line 
st.subheader("📋Sila jawab semua soalan di bawah")
st.markdown("<br>", unsafe_allow_html=True)  # Add an empty line 

main_question = {
    0: "<b style='font-size: 19px; color: #0000FF;'>1. Saya membuat keputusan penting bedasarkan:</b>",
    4: "<b style='font-size: 19px; color: #0000FF;'>2. Ketika berlaku pertelingkahan, saya akan paling dipengaruhi oleh:</b>",
    8: "<b style='font-size: 19px; color: #0000FF;'>3. Apabila berkomunikasi dengan orang, apa yang penting kepada saya ialah:</b>",
    12: "<b style='font-size: 19px; color: #0000FF;'>4. Apabila orang bertanya soalan yang penting, saya akan:</b>",
    16: "<b style='font-size: 19px; color: #0000FF;'>5. Saya anggap diri saya:</b>",
    20: "<b style='font-size: 19px; color: #0000FF;'>6. Orang lain akan dapat mengenali saya dengan baik apabila mereka:</b>",
    24: "<b style='font-size: 19px; color: #0000FF;'>7. Apabila menjalankan projek dengan orang lain, saya lebih suka:</b>",
    28: "<b style='font-size: 19px; color: #0000FF;'>8. Apabila menerangkan sesuatu kepada saya:</b>",
    32: "<b style='font-size: 19px; color: #0000FF;'>9. Ketika stress, cabaran paling utama buat saya ialah:</b>",
    36: "<b style='font-size: 19px; color: #0000FF;'>10. Saya menanggap mudah dan selesa untuk:</b>"
}

responses = {}
current_main_question_index = 0
question_containers = []

# Create containers for each main question

for i in range(len(main_question)):  # Change this to the number of main questions
    container = st.container()
    question_containers.append(container)
    st.markdown("<br>", unsafe_allow_html=True) # Add an empty line


for index, question in enumerate(sub_questions):
    if index in main_question:
        with question_containers[current_main_question_index]:
            st.write(main_question[index], unsafe_allow_html=True)

        current_main_question_index += 1

    with question_containers[current_main_question_index - 1]:
        columns = st.columns(2, gap='small')
        columns[0].markdown(f"<br><span style='font-size: 17px;'>&nbsp;&nbsp;{question['question']}</span>", unsafe_allow_html=True)
        response = columns[1].selectbox("", likert_scale, index=0, key=index)
        response_value = likert_scale_values[response]
        responses[question["question"]] = {"response": response, "category": question["category"], "value": response_value}
        scores[question["category"]] += response_value
        scores["total"] += response_value
        all_questions_answered = all(response["response"] != "--Sila pilih--" for response in responses.values())

if st.button("Hantar"):
    if not all_questions_answered:
        st.warning("Sila pilih jawapan bagi setiap soalan sebelum menghantar.")
    else:
        sorted_categories = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
        sorted_categories.remove("total")

        result = "".join(sorted_categories) 
        write_to_sheet(client, 'https://docs.google.com/spreadsheets/d/123mW3XWYGA1Zm8_Faa89y9Sus174TSktENaxP1kIjyU/edit?usp=sharing', [name, gender, age, scores["V"], scores["A"], scores["K"], scores["D"], result]) 
        st.header(f"Kecenderungan anda ialah: {result}")

        df = pd.DataFrame.from_dict(scores, orient='index', columns=['score'])
        df = df.reset_index().rename(columns={'index':'category'})

        # Filter the DataFrame to remove the 'total' category
        df = df.loc[df['category'] != 'total']

        chart = alt.Chart(df).mark_bar().encode(
            y='score',
            x=alt.X('category', sort='-y', axis=alt.Axis(labelAngle=0)),
            color=alt.Color('category', scale=alt.Scale(domain=['V', 'A', 'K', 'D'], range=['#fde725', '#35b779', '#31688e', '#443983']))
        )
        st.altair_chart(chart, use_container_width=True)

        # Define the image URLs for each category
        category_images = {
            'V': "https://i.postimg.cc/Lsm3t2wf/e.png",
            'A': "https://i.postimg.cc/fTmT61wD/a.png",
            'K': "https://i.postimg.cc/8zZmmqS0/k.png",
            'D': "https://i.postimg.cc/yYvZMcbJ/r.png"
        }

        # Define the text for each category
        category_texts = {
            'V': '''Ciri-ciri orang **VISUAL**:
- Cakap laju
- Banyak pergerakan tangan
- Berfikir dengan gambar
- Suka pandang ke atas
- Kurang sabar
- Fokus pada hasil
- Menepati masa
- Beri perhatian pada apa yang boleh dilihat
- Suka penjelasan ringkas & padat
''',
            'A': '''Ciri-ciri orang **AUDITORI**:
-Cakap dengan fasih
-Sentuh mulut dan telinga
-Belajar dengan mendengar
-Pandang ke sisi
-Suka berbual
-Vokal dalam memberi pandangan
-Banyak idea dan suka beri cadangan
-Lebih kasual
''',
            'K': '''Ciri-ciri orang **KINESTETIK**:
- Cakap sangat perlahan
- Sentuh dada atau dagu
- Pandang ke bawah
- Belajar dengan membuat
- Sensitif pada orang lain
- Ahli pasukan yang baik
- Teliti dalam pekerjaan yang dilakukan
- Setia
''',
            'D': '''Ciri-ciri orang **DIGITAL**:
- Berfikir dahulu sebelum bercakap
- Berfikir dengan rasional dan logikal
- Sangat teliti
- Suka memahami keadaan sekeliling
- Suka belajar dengan memikirkannya
- Tidak suka di arah
- Perlukan masa untuk memproses maklumat
'''
        }

        # Create a container for the images and text
        result_container = st.container()

        # Create columns inside the container
        result_columns = result_container.columns(len(sorted_categories))

        # Loop through the sorted categories and display the image and text in the same column
        for i, category in enumerate(sorted_categories):
            result_columns[i].image(category_images[category], width=200)
            result_columns[i].markdown(category_texts[category])


   


        
