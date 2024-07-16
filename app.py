import streamlit as st
import pandas as pd
import json
import glob
# 设置页面标题
st.set_page_config(page_title="Distractor Evaluation", layout="wide")

# 加载数据集
@st.cache_resource
def load_data(json_file):
    with open(json_file, 'r',encoding='utf-8') as file:
        data = list(map(eval,file.readlines()))
    df = pd.DataFrame(data)
    return df

json_files = glob.glob('./*evaluate.json')  # 替换为你的 JSON 文件路径模式

# 添加标题
st.title("Distractor Evaluation")

# 选择要评测的 JSON 文件
selected_file = st.selectbox('Select a JSON file to evaluate', json_files)

# 获取所选文件的数据
data = load_data(selected_file)

# 初始化 session state
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

if 'scores' not in st.session_state:
    st.session_state.scores = []

# 显示当前问题
current_index = st.session_state.current_index
story = data.iloc[current_index]['passage']
question = data.iloc[current_index]['question']
answer = data.iloc[current_index]['answer']
distractor = data.iloc[current_index]['pre_distractor']
id = data.iloc[current_index]['id']

# 添加故事部分
st.subheader("Passage")
st.write(story)

# 添加问题部分
st.subheader("Question")
st.write(question)

# 添加答案和干扰项
st.subheader("Answer")
st.write(answer)

st.subheader("Distractor")
st.write(distractor)

# 添加评分滑动条
st.subheader("Score: How good is the distractor?")
score = st.slider("1-差 2-较差 3-中 4-较好 5-好", min_value=1, max_value=5, value=1)

# 提交评分并保存
if st.button("Submit"):
    st.session_state.scores.append({
        'Passage': story,
        'Question': question,
        'Answer': answer,
        'Distractor': distractor,
        'Score': score
    })
    st.write(f"Score submitted: {score}")
    try:
        with open('user_scores.json', 'r') as f:
            scores_data = json.load(f)
    except FileNotFoundError:
        scores_data = []

    scores_data.append({
        'Id':id,
        'Passage': story,
        'Question': question,
        'Answer': answer,
        'Distractor': distractor,
        'Score': score,
        'File':selected_file
    })

    with open('user_scores.json', 'w') as f:
        json.dump(scores_data, f, indent=4)
    # 移动到下一个问题
    if st.session_state.current_index < len(data) - 1:
        st.session_state.current_index += 1
    else:
        st.write("You have completed all the questions!")

# 显示已保存的评分
if st.button("Show Saved Scores"):
    st.write(pd.DataFrame(st.session_state.scores))

# # 保存评分到 JSON 文件
# if st.button("Save Scores to JSON"):
#     scores_df = pd.DataFrame(st.session_state.scores)
#     scores_json = scores_df.to_json(orient='records', indent=4)
#     with open('user_scores.json', 'w') as f:
#         f.write(scores_json)
#     st.write("Scores saved to user_scores.json")
