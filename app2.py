import streamlit as st

# placeholder = st.empty()

# input = placeholder.text_input('text')
# click_clear = st.button('clear text input', key=1)
# # if click_clear:
# #     input = placeholder.text_input('text', value=str(input)+"qkweunnqwew", key=1)





# placeholder = st.empty()
# options = ["A","B","C","D"]
# selected = placeholder.multiselect('option',  options=options, default=options[0])

# # button = st.button('button', key=2)
# # if button:
# #     selected.append("D")
# #     selected = placeholder.multiselect('option',options=options, default=selected, key=2)

# for o in options:
#     button = st.button(o, key=2)
#     if button:
#         selected.append(o)

# selected = placeholder.multiselect('option',options=options, default=selected, key=2)

import SessionState
import streamlit as st

session_state = SessionState.get(checkboxed=False)

if st.button('Click me') or session_state.checkboxed:
    session_state.checkboxed = True
    if st.button("Click me too !"):
        st.write("Hello world")
