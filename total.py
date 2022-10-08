#!/usr/bin/python3
# author liuxinyu
import streamlit as st
# 舌苔
import tongue.effcient_Net.tongue_crack.crack_predict as crack
import tongue.effcient_Net.tongue_coated.coated_predict as coated
import tongue.effcient_Net.tongue_color.color_predict as color
import tongue.effcient_Net.tongue_indentation.indent_predict as indent
# 皮肤癌
# 语音情绪
# 面部表情
import face.src.image_emotion_gender_demo as emo

st.set_page_config(page_title="AI智能检测系统", page_icon="🏥", layout="wide")
st.sidebar.title("🏥 AI智能检测系统")
# 上传文件并显示
file = st.sidebar.file_uploader("请上传鉴定文件")
image_slot = st.sidebar.empty()
if file:
    stringio = file.getvalue()
    file_path = 'file/' + file.name
    with open(file_path, 'wb') as f:
        f.write(stringio)
    image_slot.image(file_path)
st.sidebar.write("请选择你要进入的系统")

# 舌苔
if st.sidebar.button('舌苔检测'):
    st.title("🏥 舌苔检测系统")
    my_bar = st.progress(10)
    # UHD_content_folder_path = 'PytorchWCT/content/UHD_content'
    crack_class, crack_prob = crack.main(file_path)
    coated_class, coated_prob = coated.main(file_path)
    color_class, color_prob = color.main(file_path)
    indent_class, indent_prob = indent.main(file_path)
    # 裂纹舌分析
    if crack_class == 'crack':
        crack_res = "裂纹舌"
    else:
        crack_res = "无裂纹"
    # 齿痕舌分析
    if indent_class == 'normal':
        indent_res = "无齿痕"
    else:
        indent_res = "齿痕舌"
    # 苔色分析
    if coated_class == "white":
        coated_res = "白苔"
    else:
        if coated_class == "yellow":
            coated_res = "黄苔"
        else:
            coated_res = "无苔"
    # 舌色分析
    if color_class == "red":
        color_res = "淡红舌"
    else:
        if color_class == "white":
            color_res = "淡白舌"
        else:
            color_res = "深红舌"
    # 体质鉴定
    if color_class == 'white' and crack_class == 'crack' and indent_class == 'indentation' and coated_class == "white":
        setText = "舌淡白，白舌苔，有齿痕，有裂纹:\n燥热伤津，阴液亏损，脾虚湿侵，脾失健运，湿邪内侵，精微不能濡养舌体。"
    elif color_class == 'white' and crack_class == 'crack' and indent_class == 'indentation' and coated_class == "yellow":
        setText = "舌淡白，黄舌苔，有齿痕，有裂纹:\n风热表证,或风寒化热入里，热势轻浅,脾虚湿侵，脾失健运，湿邪内侵，精微不能濡养舌体。"
    elif color_class == 'white' and crack_class == 'crack' and indent_class == 'indentation' and coated_class == "nocoated":
        setText = "舌淡白，有齿痕，有裂纹:\n热势轻浅，脾虚湿侵，脾失健运，湿邪内侵，精微不能濡养舌体。"
    elif color_class == 'white' and crack_class == 'crack' and indent_class == 'normal' and coated_class == "white":
        setText = "舌淡白，白舌苔，有裂纹:\n燥热伤津，阴液亏损,血虚不润,血虚不能上荣于活,精微不能濡养舌体。"
    elif color_class == 'white' and crack_class == 'crack' and indent_class == 'normal' and coated_class == "yellow":
        setText = "舌淡白，黄舌苔，有裂纹:\n血虚不润,血虚不能上荣于活,精微不能濡养舌体，风热表证,或风寒化热入里，热势轻浅。"
    elif color_class == 'white' and crack_class == 'crack' and indent_class == 'normal' and coated_class == "nocoated":
        setText = "舌淡白，有裂纹:\n血虚不润,血虚不能上荣于活,精微不能濡养舌体。"
    elif color_class == 'white' and crack_class == 'normal' and indent_class == 'indentation' and coated_class == "white":
        setText = "舌淡白，白舌苔，有齿痕：\n表证、寒证，主脾虚、血虚，水湿内盛证，舌胖大而多齿痕多属脾虚或湿困"
    elif color_class == 'white' and crack_class == 'normal' and indent_class == 'indentation' and coated_class == "yellow":
        setText = "舌淡白，黄舌苔，有齿痕：\n里证，热证主脾虚、血虚，水湿内盛证，舌胖大而多齿痕多属脾虚或湿困"
    elif color_class == 'white' and crack_class == 'normal' and indent_class == 'indentation' and coated_class == "nocoated":
        setText = "舌淡白，有齿痕：\n主脾虚、血虚，水湿内盛证，舌胖大而多齿痕多属脾虚或湿困"
    elif color_class == 'white' and crack_class == 'normal' and indent_class == 'normal' and coated_class == "white":
        setText = "舌淡白，白舌苔：\n血虚，也主表证、寒证"
    elif color_class == 'white' and crack_class == 'normal' and indent_class == 'normal' and coated_class == "yellow":
        setText = "舌淡白，黄舌苔：\n血虚，主里证，热证"
    elif color_class == 'white' and crack_class == 'normal' and indent_class == 'normal' and coated_class == "nocoated":
        setText = "舌淡白：\n血虚"
    elif color_class == 'red' and crack_class == 'normal' and indent_class == 'normal' and coated_class == 'nocoated':
        setText = "舌淡红，无舌苔：\n虚热证"
    elif color_class == 'red' and crack_class == 'normal' and indent_class == 'normal' and coated_class == 'white':
        setText = "舌淡红，白舌苔：\n心气充足，胃气旺盛，气血调和，常见于正常人或病情轻浅阶段"
    elif color_class == 'red' and crack_class == 'normal' and indent_class == 'normal' and coated_class == 'yellow':
        setText = "舌淡红，黄舌苔：虚热证，主里证"
    elif color_class == 'red' and crack_class == 'crack' and indent_class == 'normal' and coated_class == 'nocoated':
        setText = "舌淡红，无舌苔，有裂纹：\n虚热证，精血亏虚或阴津耗损，舌体失养，血虚之候，可能为全身营养不良"
    elif color_class == 'red' and crack_class == 'crack' and indent_class == 'normal' and coated_class == 'white':
        setText = "舌淡红，白舌苔，有裂纹：\n虚热证，主表证，精血亏虚或阴津耗损，舌体失养，血虚之候"
    elif color_class == 'red' and crack_class == 'crack' and indent_class == 'normal' and coated_class == 'yellow':
        setText = "舌淡红，黄舌苔，有裂纹：\n虚热证，风寒化热入里，热势轻浅，精血亏虚或阴津耗损，舌体失养，血虚之候"
    elif color_class == 'red' and crack_class == 'normal' and indent_class == 'indentation' and coated_class == 'yellow':
        setText = "舌淡红，黄舌苔，有齿痕:\n气虚证或脾虚证，气血不足，风寒化热入里，热势轻浅。"
    elif color_class == 'red' and crack_class == 'normal' and indent_class == 'indentation':
        setText = "舌淡红，有齿痕:\n气虚证或脾虚证，气血不足。"
    elif color_class == 'red' and crack_class == 'crack' and indent_class == 'indentation' and coated_class == 'yellow':
        setText = "舌淡红，黄舌苔，有裂纹，有齿痕:\n气虚证或虚热证，风寒化热入里，热势轻浅，精血亏虚或阴津耗损，舌体失养，气血不足。"
    elif color_class == 'red' and crack_class == 'crack' and indent_class == 'indentation':
        setText = "舌淡红，有裂纹，有齿痕:\n气虚证或虚热证，精血亏虚或阴津耗损，舌体失养，气血不足。"
    elif color_class == 'crimson' and crack_class == 'crack' and coated_class == 'white':
        setText = "舌深红，白舌苔，有裂纹:\n热症，热盛伤津，邪热内盛,阴液大伤，或阴虚液损，使舌体失于濡润,舌面萎缩。"
    elif color_class == 'crimson' and crack_class == 'crack' and coated_class == 'yellow':
        setText = "舌深红，黄舌苔，有裂纹:\n热症，热盛伤津，风寒化热入里，邪热内盛，阴液大伤。或阴虚液损，使舌体失于濡润，舌面萎缩，舌体失养。"
    elif color_class == 'crimson' and crack_class == 'crack' and coated_class == 'nocoated':
        setText = "舌深红，无舌苔，有裂纹:\n热症，热盛伤津，邪热内盛，阴液大伤，或阴虚液损，使舌体失于濡润，舌面萎缩，阴虚火旺。或热病后期阴液耗损。"
    elif color_class == 'crimson' and crack_class == 'normal' and indent_class == 'indentation' and coated_class == 'nocoated':
        setText = "舌深红，无舌苔，有齿痕:\n热症，久病阴虚火旺,或热病后期阴液耗损，水湿内盛证，舌胖大而多齿痕多属脾虚或湿困。"
    elif color_class == 'crimson' and crack_class == 'normal' and indent_class == 'normal' and coated_class == 'nocoated':
        setText = "舌深红，无舌苔:\n热症，久病阴虚火旺,或热病后期阴液耗损。"
    elif color_class == 'crimson' and crack_class == 'normal' and indent_class == 'normal' and coated_class == 'yellow':
        setText = "舌深红,黄苔:\n热症，温热病热入营血，或脏腑内热炽盛,风热表证,或风寒化热入里，热势轻浅。"
    elif color_class == 'crimson' and crack_class == 'normal' and indent_class == 'indentation' and coated_class == 'white':
        setText = "舌深红，白舌苔，有齿痕:\n热症，久病阴虚火旺,或热病后期阴液耗损，水湿内盛证，舌胖大而多齿痕多属脾虚或湿困。"
    elif color_class == 'crimson' and crack_class == 'normal' and indent_class == 'normal' and coated_class == 'white':
        setText = "舌深红，白苔:\n热症，温热病热入营血，或脏腑内热炽盛。"
    elif color_class == 'crimson' and crack_class == 'normal' and indent_class == 'indentation' and coated_class == 'white':
        setText = "舌深红，白舌苔，有齿痕:\n热症，温热病热入营血，或脏腑内热炽盛，水湿内盛证，舌胖大而多齿痕多属脾虚或湿困。"

    # output_path = WCT_func.process(content_file_path, style_file_path)
    for i in range(0, 100, 10):
        my_bar.progress(i + 1)
    my_bar.progress(100)
    st.write('鉴定结果如下所示:')
    # st.image('')
    st.write('舌色分析:',color_res)
    st.write('苔色分析:',coated_res)
    st.write('裂纹舌分析:',crack_res)
    st.write('齿痕舌分析:',indent_res)
    st.write('体质鉴定为:',setText)
    # st.image(output_path)
# 皮肤癌
if st.sidebar.button('皮肤癌检测'):
    None
# 语音情绪
if st.sidebar.button('语音情绪识别'):
    None
# 面部表情
if st.sidebar.button('面部表情识别'):
    my_bar = st.progress(10)
    gener_res, emo_res = emo.main(file_path)
    for i in range(0, 100, 10):
        my_bar.progress(i + 1)
    my_bar.progress(100)
    st.write('鉴定结果如下所示:')
    # st.image('')
    st.write('情绪分析:', emo_res)
    st.write('性别分析:', gener_res)