import streamlit as st
import src.image_emotion_gender_demo as emo


# 页面展示，侧边栏上传图像并展示，主页面显示进度条和鉴定结果
# 设置网页信息
st.set_page_config(page_title="情绪检测系统", page_icon="🏥", layout="wide")
st.title("🏥 情绪检测系统")

# 上传图像并显示
img_file = st.sidebar.file_uploader("请上传人像")
image_slot = st.sidebar.empty()
if img_file:
    stringio = img_file.getvalue()
    img_file_path = 'face_file/' + img_file.name
    with open(img_file_path, 'wb') as f:
        f.write(stringio)
    # st.sidebar.write('上传的人像')
    image_slot.image(img_file_path)

# 开始鉴定，并显示进度条
if st.sidebar.button('开始鉴定'):
    my_bar = st.progress(10)
    gener_res, emo_res = emo.main(img_file_path)
    for i in range(0, 100, 10):
        my_bar.progress(i + 1)
    my_bar.progress(100)

    st.write('鉴定结果如下所示:')
    # st.image('')
    st.write('情绪分析:',emo_res)
    st.write('性别分析:',gener_res)