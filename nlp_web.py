import streamlit as st
import pandas as pd
import altair as alt
import base64
from PIL import Image
import io  

from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE =r'C:\Users\user\Desktop\Github projects\Nlp_quiz\nlp-sheet-29485bc0daa8.json'

creds=None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
SAMPLE_SPREADSHEET_ID= "1dMms0EC-i5nr5lTamXMU3zBP2EtOjNivzL7v-exRdKE"
service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range="entry!A1:G33").execute()
values = result.get('values', [])
print(result)



st.markdown(
    '''
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

        .main-question {
            font-family: 'Roboto', sans-serif;
            font-size: 20px;
            font-weight: 700;
        }

        .sub-question {
            font-family: 'Roboto', sans-serif !important;
            font-size: 16px !important;;
        }
        .sub-question select {
            font-family: 'Roboto', sans-serif;
            font-size: 14px;
        }
        
        .question-text {
            font-family: 'Roboto', sans-serif;
            font-size: 16px;
            font-weight: 700;
        }

        .selectbox-width {
            width: 50% !important;
    </style>
    ''',
    unsafe_allow_html=True
)
def display_image_as_base64(image_path, width=None):
    with open(image_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

    img = Image.open(image_path)
    if width is not None:
        aspect_ratio = img.width / img.height
        img = img.resize((width, int(width / aspect_ratio)))

    img_buffer = io.BytesIO()
    img.save(img_buffer, format="PNG")
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

    return f'<div style="text-align: center;"><img src="data:image/png;base64,{img_base64}" /></div>'
logo = r"C:\Users\user\Desktop\Github projects\Nlp_quiz\ttelogo.png"
#st.markdown(display_image_as_base64(logo, width=180), unsafe_allow_html=True)

def update_google_sheet(sheet_service, sheet_id, range_name, values):
    body = {
        'values': values
    }
    result = sheet_service.values().update(
        spreadsheetId=sheet_id, range=range_name,
        valueInputOption='RAW', body=body).execute()
    print(f'Updated {result.get("updatedCells")} cells.')


st.subheader("Sila isikan maklumat anda:")

name = st.text_input("Nama:")

gender_options = ["--Pilih jantina--", "LELAKI", "PEREMPUAN"]
gender = st.selectbox("Jantina:", gender_options)

age = st.number_input("Umur:", min_value=1, max_value=120, step=1)

if st.button("Submit Details"):
    if name and gender != "--Pilih jantina--" and age:
        st.success(f"Maklumat berjaya direkod.")
        update_google_sheet(sheet, SAMPLE_SPREADSHEET_ID, "entry!A1:D1", [[name, gender, age, ""]])
    else:
        st.warning("Sila isikan semua butiran di atas.")



questions = [
    {"question": "rasa hati & keselesaan", "category": "K"},
    {"question": "bunyi idea", "category": "A"},
    {"question": "gambaran terhadap idea", "category": "V"},
    {"question": "kajian mendalam tentang isu", "category": "D"},
    {"question": "nada dan intonasi orang", "category": "A"},
    {"question": "sama ada saya boleh melihat pandangan orang atau tidak", "category": "V"},
    {"question": "logik dan rasional pandangan orang", "category": "D"},
    {"question": "sama ada orang sensitif atau tdak terhadap perasaan saya", "category": "K"},
    {"question": "rupa dan pemakaian saya", "category": "V"},
    {"question": "berkongsi perasaan dan pengalaman", "category": "K"},
    {"question": "mengetahui maksud perkataan saya difahami", "category": "D"},
    {"question": "didengari dan diberi perhatian", "category": "A"},
    {"question": "dengar dengan teliti dan bertanya soalan,untuk memastikan saya faham", "category": "A"},
    {"question": "lebih suka untuk memikirkanya dahulu,dan memilih perkataan sesuai", "category": "D"},
    {"question": "dihargai apabila diberi masa untuk mencari jawapannya dahulu", "category": "K"},
    {"question": "jawab dengan cepat, dengan cara menggambarkan jawapanya", "category": "V"},
    {"question": "peka terhadap bunyi di sekitar", "category": "A"},
    {"question": "mudah memahami fakta dan maklumat", "category": "D"},
    {"question": "sensitif dan fleksibel dalam perhubungan", "category": "K"},
    {"question": "kreatif dan mampu menguruskan jumlah maklumat yang baik", "category": "V"},
    {"question": "boleh menghubungkan diri dengan perasaan saya", "category": "K"},
    {"question": "boleh melihat pandangan saya", "category": "V"},
    {"question": "dengar dengan baik apa yang saya perkatakan dan cara disampaikan", "category": "A"},
    {"question": "berminat dengan maksud perkara yang saya sampaikan", "category": "D"},
    {"question": "memperbaiki proses dengan idea saya", "category": "A"},
    {"question": "terlibat dengan proses perancangan dan menentukan visi", "category": "V"},
    {"question": "mengatur perjalanan program dan menyusunnya", "category": "D"},
    {"question": "membina perhubungan yang lebih baik antara ahli", "category": "K"},
    {"question": "menunjukkannya kepada saya adalah paling jelas", "category": "V"},
    {"question": "saya boleh ingat dengan baik hanya dengan mendengar", "category": "A"},
    {"question": "menuliskannya membantu saya untuk memahaminya", "category": "K"},
    {"question": "menerangkan fakta dengan cara logikal adalah lebih bermakna", "category": "D"},
    {"question": "mempercayai orang lain, situasi atau konsep", "category": "D"},
    {"question": "menjadi diplomatik, sebaliknya akan beterus terang", "category": "A"},
    {"question": "memisahkan emosi diri dengan perasaan orang lain", "category": "K"},
    {"question": "menjadi fleksibel dan menukar rancangan", "category": "V"},
    {"question": "menerima inspirasi dari dalam", "category": "D"},
    {"question": "memberitahu di mana idea baru boleh digunakan", "category": "A"},
    {"question": "mengikuti kaedah yang telah dibuktikan berkesan", "category": "K"},
    {"question": "mmerancang dan menguruskan aktiviti", "category": "V"}
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

st.title("Quiz Neural Linguistic Programming")

statements = {
    0: "1.Saya membuat keputusan penting bedasarkan:",
    4: "2.Ketika berlaku pertelingkahan, saya akan paling dipengaruhi oleh:",
    8: "3.Apabila berkomunikasi dengan orang, apa yang penting kepada saya ialah:",
    12:"4.Apabila orang bertanya soalan yang penting, saya akan",
    16:"5.Saya anggap diri saya:",
    20:"6.Orang lain akan dapat mengenali saya dengan baik apabila mereka:",
    24:"7.Apabila menjalankan projek dengan orang lain,saya lebih suka:",
    28:"8.Apabila menerangkan sesuatu kepada saya:",
    32:"9.Ketika stress, cabaran paling utama buat saya ialah:",
    36:"10.Saya menanggap mudah dan selesa untuk:"

}

responses = {}
for index, question in enumerate(questions):
    if index in statements:
        st.markdown(f'<div class="main-question">{statements[index]}</div>', unsafe_allow_html=True)

    with st.markdown('<div class="sub-question">', unsafe_allow_html=True):
        response = st.selectbox(question["question"], likert_scale, index=0, key=question["question"])
        response_value = likert_scale_values[response]
        responses[question["question"]] = {"response": response, "category": question["category"], "value": response_value}
        scores[question["category"]] += response_value
        scores["total"] += response_value
    st.markdown('</div>', unsafe_allow_html=True)

    all_questions_answered = all(response["response"] != "--Sila pilih--" for response in responses.values())

if st.button("Hantar"):
    if not all_questions_answered:
        st.warning("Sila pilih jawapan bagi setiap soalan sebelum menghantar.")
    else:
        for question_key in responses:
            question_response = responses[question_key]
            scores[question_response["category"]] += likert_scale_values[question_response["response"]]

        sorted_categories = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
        sorted_categories.remove("total")

        result = "".join(sorted_categories)

        st.header(f"Susunan saya memproses maklumat ialah: {result}")

        scores.pop("total", None)

        df = pd.DataFrame.from_dict(scores, orient='index', columns=['score'])
        df = df.reset_index().rename(columns={'index':'category'})
        chart = alt.Chart(df).mark_bar().encode(
            x='score',
            y=alt.Y('category', sort='-x'),
            color=alt.Color('category', scale=alt.Scale(domain=['V', 'A', 'K', 'D'], range=['#fde725', '#35b779', '#31688e', '#443983']))
        )  # Add the closing parenthesis here
        st.altair_chart(chart, use_container_width=True)

        # Update the Google Sheet with the scores and result
        update_google_sheet(sheet, SAMPLE_SPREADSHEET_ID, f"entry!E1:I1", [[scores["V"], scores["A"], scores["K"], scores["D"], result]])


