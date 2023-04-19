import streamlit as st
import pandas as pd
import altair as alt
import base64
from PIL import Image
import io  


image_url = "https://www.ttelectronics.com/images/logo-colour.svg"  # Replace this with the URL of your image
st.image(image_url, width=150)


st.subheader("Sila isikan maklumat anda:")

name = st.text_input("Nama:")

gender_options = ["--Pilih jantina--", "LELAKI", "PEREMPUAN"]
gender = st.selectbox("Jantina:", gender_options)

age = st.number_input("Umur:", min_value=1, max_value=120, step=1)

if st.button("Submit Details"):
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

st.header("Quiz Neural Linguistic Programming")


main_question = {
    0: "<b style='font-size: 15px;'>1. Saya membuat keputusan penting bedasarkan:</b>",
    4: "<b style='font-size: 15px;'>2. Ketika berlaku pertelingkahan, saya akan paling dipengaruhi oleh:</b>",
    8: "<b style='font-size: 15px;'>3. Apabila berkomunikasi dengan orang, apa yang penting kepada saya ialah:</b>",
    12: "<b style='font-size: 15px;'>4. Apabila orang bertanya soalan yang penting, saya akan</b>",
    16: "<b style='font-size: 15px;'>5. Saya anggap diri saya:</b>",
    20: "<b style='font-size: 15px;'>6. Orang lain akan dapat mengenali saya dengan baik apabila mereka:</b>",
    24: "<b style='font-size: 15px;'>7. Apabila menjalankan projek dengan orang lain, saya lebih suka:</b>",
    28: "<b style='font-size: 15px;'>8. Apabila menerangkan sesuatu kepada saya:</b>",
    32: "<b style='font-size: 15px;'>9. Ketika stress, cabaran paling utama buat saya ialah:</b>",
    36: "<b style='font-size: 15px;'>10. Saya menanggap mudah dan selesa untuk:</b>"
}

responses = {}
for index, question in enumerate(sub_questions):
    if index in main_question:
        st.markdown(main_question[index], unsafe_allow_html=True)

    response = st.selectbox(question["question"], likert_scale, index=0, key=index)
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

        st.header(f"Susunan anda memproses maklumat ialah: {result}")

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


