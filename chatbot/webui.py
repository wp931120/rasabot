import streamlit as st
import requests
from streamlit_chat import message


URL = "http://localhost:5005/webhooks/rest/webhook"


def predict(text):

    data = {}
    data["message"] = text
    data["sender"] = "wp"

    response = requests.post(URL, json=data)
    answer = eval(response.text)[0]["text"]

    return answer


if __name__ == '__main__':
    st.header('机器人')

    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    with st.form('form', clear_on_submit=True):
        user_input = st.text_input('输入 : ', '')
        submitted = st.form_submit_button('提交')

    if submitted and user_input:
        ans = predict(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(ans)
    print(st.session_state)
    for i in range(len(st.session_state['past'])):
        message(st.session_state['past'][i], is_user=True)
        if len(st.session_state['generated']) > i:
            message(st.session_state['generated'][i])