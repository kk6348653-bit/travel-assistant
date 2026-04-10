# app.py - 旅行咨询助手 Web 界面版
import streamlit as st
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# 页面配置
st.set_page_config(
    page_title="旅行咨询助手",
    page_icon="✈️",
    layout="wide"
)

# 标题
st.title("✈️ 旅行咨询助手")
st.markdown("输入您的旅行需求，AI 将自动提取关键信息并给出专业回复")

# 侧边栏 - API Key 配置
with st.sidebar:
    st.header("⚙️ 配置")
    api_key = st.text_input("DeepSeek API Key", type="password", help="输入你的 DeepSeek API Key")
    st.markdown("---")
    st.markdown("### 使用说明")
    st.markdown("""
    1. 输入 DeepSeek API Key
    2. 在下方输入您的旅行咨询
    3. 点击「开始分析」
    4. 查看提取的信息和 AI 回复
    """)
    st.markdown("---")
    st.markdown("### 示例咨询")
    st.markdown("""
    - "I want to plan a 7-day trip to Japan in October for 2 people. Budget is around 3000 USD."
    - "Do you have family-friendly tours in Europe?"
    - "Need visa help for a trip to Canada."
    """)

# Prompt 模板
PROMPT_TEMPLATE = """
You are a travel assistant. Analyze the customer inquiry and return JSON only.

Customer inquiry: {message}

Return JSON in this exact format. Do not add any other text outside the JSON.
If a field cannot be determined, use null.

{{
  "destination": "extracted destination or null",
  "trip_type": "business/leisure/adventure/beach/cultural/honeymoon/family or null",
  "duration": "extracted duration like '7 days' or null",
  "travel_time": "extracted time like 'October' or 'next month' or null",
  "group_size": number or null,
  "budget": number or null,
  "intent": "trip planning/visa help/price inquiry/contact request/general",
  "missing_fields": ["list", "of", "missing", "important", "fields"],
  "reply_type": "initial_response or clarification",
  "reply": "short professional reply in English. If missing important info like destination/budget/duration, ask clarifying question. Do not invent prices or products."
}}
"""

def analyze_inquiry(message: str, api_key: str):
    """调用 DeepSeek API 分析用户咨询"""
    llm = ChatOpenAI(
        openai_api_key=api_key,
        openai_api_base="https://api.deepseek.com/v1",
        model_name="deepseek-chat",
        temperature=0.3
    )
    
    prompt = PROMPT_TEMPLATE.format(message=message)
    response = llm.invoke([HumanMessage(content=prompt)])
    
    # 提取 JSON 内容
    content = response.content
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0]
    elif "```" in content:
        content = content.split("```")[1].split("```")[0]
    
    return json.loads(content)

# 用户输入
user_message = st.text_area(
    "旅行咨询内容",
    placeholder="例如：I want to plan a 7-day trip to Japan in October for 2 people. Budget is around 3000 USD.",
    height=100
)

# 分析按钮
if st.button("🚀 开始分析", type="primary"):
    if not api_key:
        st.warning("请先在侧边栏输入 DeepSeek API Key")
    elif not user_message:
        st.warning("请输入旅行咨询内容")
    else:
        with st.spinner("AI 正在分析中..."):
            try:
                result = analyze_inquiry(user_message, api_key)
                
                # 显示结果
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📋 提取的信息")
                    st.markdown(f"""
                    - **目的地**：{result.get('destination', '未提取')}
                    - **旅行类型**：{result.get('trip_type', '未提取')}
                    - **时长**：{result.get('duration', '未提取')}
                    - **出行时间**：{result.get('travel_time', '未提取')}
                    - **人数**：{result.get('group_size', '未提取')}
                    - **预算**：{result.get('budget', '未提取')} USD
                    - **意图**：{result.get('intent', '未提取')}
                    - **缺失信息**：{', '.join(result.get('missing_fields', [])) if result.get('missing_fields') else '无'}
                    """)
                
                with col2:
                    st.subheader("💬 AI 回复")
                    st.info(result.get('reply', '无回复'))
                    st.markdown(f"**回复类型**：{result.get('reply_type', '未提取')}")
                
                # 显示原始 JSON（可选）
                with st.expander("查看原始 JSON 结果"):
                    st.json(result)
                    
            except Exception as e:
                st.error(f"分析失败：{str(e)}")
                st.info("请检查 API Key 是否正确，或稍后重试")

# 页脚
st.markdown("---")
st.markdown("💡 **提示**：本工具需要 DeepSeek API Key，可在 [platform.deepseek.com](https://platform.deepseek.com) 免费获取")