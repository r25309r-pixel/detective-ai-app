import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from pyvis.network import Network
import streamlit.components.v1 as components

# 1. تهيئة الصفحة العامة
st.set_page_config(
    page_title="منظومة التحري الذكي | Smart Detective AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تنسيق مخصص لطابع شرطي رسمي
st.markdown("""
    <style>
    .main-header { font-size: 28px; font-weight: bold; color: #1E3A8A; text-align: right; }
    .sub-header { font-size: 16px; color: #4B5563; text-align: right; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🛡️ المنظومة التنفيذية للتحري الذكي والتنبؤ الجنائي</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">الإدارة العامة للتحريات والمباحث الجنائية - وحدة الذكاء الاصطناعي وتحليل البيانات</p>', unsafe_allow_html=True)
st.divider()

# 2. قاعدة بيانات قضايا محاكية للواقع الجنائي
data = {
    'رقم_القضية': ['CR-2026-081', 'CR-2026-082', 'CR-2026-083', 'CR-2026-084', 'CR-2026-085', 'CR-2026-086'],
    'نوع_الجريمة': ['سرقة منازل', 'سرقة مركبات', 'سرقة منازل', 'احتيال مالي', 'سرقة منازل', 'سرقة مركبات'],
    'الأسلوب_الإجرامي': ['كسر الأقفال ليلاً + تعطيل الكاميرات', 'استخدام أجهزة استنساخ البصمة', 'كسر الأقفال ليلاً + تعطيل الكاميرات', 'انتحار صفة مصرفية', 'كسر الأقفال ليلاً + تعطيل الكاميرات', 'استخدام أجهزة استنساخ البصمة'],
    'المنطقة': ['النعيمية', 'الراشدية', 'النعيمية', 'الروضة', 'النعيمية', 'الراشدية'],
    'Latitude': [25.3980, 25.4050, 25.3995, 25.4120, 25.3972, 25.4062],
    'Longitude': [55.4790, 55.4850, 55.4810, 55.4910, 55.4782, 55.4865],
    'درجة_الخطورة': ['عالية جداً', 'متوسطة', 'عالية جداً', 'منخفضة', 'عالية جداً', 'متوسطة'],
    'نسبة_التطابق_%': [96, 78, 96, 40, 96, 78],
    'المشتبه_به_الرئيسي': ['خالد .م (سوابق)', 'راشد .ع', 'خالد .م (سوابق)', 'مجهول', 'خالد .م (سوابق)', 'راشد .ع']
}
df = pd.DataFrame(data)

# 3. القائمة الجانبية للتصفية والتحكم التنفيذي
st.sidebar.title("مركز التحكم والعمليات")
selected_crime = st.sidebar.selectbox("تصفية حسب نوع الجريمة:", ['عرض كافة الجرائم'] + list(df['نوع_الجريمة'].unique()))

if selected_crime != 'عرض كافة الجرائم':
    filtered_df = df[df['نوع_الجريمة'] == selected_crime]
else:
    filtered_df = df

# 4. المؤشرات الإحصائية المباشرة (KPIs)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("إجمالي البلاغات المحللة", len(filtered_df), "تحليل لحظي")
with col2:
    st.metric("الأنماط الإجرامية المتكررة", "2 نمط نشط", delta="تطابق 96%", delta_color="normal")
with col3:
    st.metric("البؤرة الأعلى خطورة", "منطقة النعيمية", "تنبؤ 24 ساعة")
with col4:
    st.metric("مستوى دقة التحليل الذكي", "95.8%", "AI Confirmed")

st.divider()

# 5. التبويبات الرئيسية للتنفيذ
tab1, tab2, tab3 = st.tabs(["🗺️ الخريطة الحرارية والتنبؤ الجنائي", "🔗 الربط التلقائي بين القضايا (MO)", "🕸️ شبكة العلاقات والمشتبه بهم"])

# --- التبويب الأول: الخريطة الحرارية ---
with tab1:
    st.subheader("توقع البؤر الساخنة وتوزيع الدوريات الاستباقي")
    st.caption("يعتمد النظام على خوارزميات التنبؤ الجغرافي لتحديد الأماكن المتوقع استهدافها خلال الـ 24 ساعة القادمة:")
    
    m = folium.Map(location=[25.4020, 55.4830], zoom_start=14, tiles="OpenStreetMap")
    heat_data = [[row['Latitude'], row['Longitude']] for idx, row in filtered_df.iterrows()]
    HeatMap(heat_data, radius=30, blur=15).add_to(m)
    
    for idx, row in filtered_df.iterrows():
        color = "red" if row['درجة_الخطورة'] == 'عالية جداً' else "orange" if row['درجة_الخطورة'] == 'متوسطة' else "blue"
        folium.Marker(
            [row['Latitude'], row['Longitude']],
            popup=f"<b>القضية:</b> {row['رقم_القضية']}<br><b>الأسلوب:</b> {row['الأسلوب_الإجرامي']}<br><b>المشتبه به:</b> {row['المشتبه_به_الرئيسي']}",
            tooltip=f"{row['رقم_القضية']} - {row['الأسلوب_الإجرامي']}",
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(m)
        
    st_folium(m, width=1200, height=480)

# --- التبويب الثاني: الربط بين القضايا ---
with tab2:
    st.subheader("تحليل الأسلوب الإجرامي الموحد (Modus Operandi)")
    st.write("يقوم النظام بمطابقة تفاصيل المحاضر والأسلوب الإجرامي تلقائياً لإثبات وحدة الفاعل:")
    
    st.dataframe(
        filtered_df[['رقم_القضية', 'نوع_الجريمة', 'الأسلوب_الإجرامي', 'المنطقة', 'نسبة_التطابق_%', 'المشتبه_به_الرئيسي']],
        use_container_width=True
    )
    
    st.success("💡 *توصية النظام الآلية:* يوصى بضم القضايا (CR-2026-081، CR-2026-083، CR-2026-085) في ملف تحقيق واحد لوجود تطابق بنسبة 96% في الأسلوب الإجرامي والنطاق الجغرافي.")

# --- التبويب الثالث: شبكة العلاقات الإجرامية ---
with tab3:
    st.subheader("رسم شبكة العلاقات والروابط الخفية (SNA)")
    st.write("رسم بياني تفاعلي يربط المشتبه بهم بالقضايا والأماكن وسوابق الاتصال:")
    
    net = Network(height="450px", width="100%", bgcolor="#222222", font_color="white")
    
    # إضافة العقد
    net.add_node("خالد .م", label="خالد .م (مشتبه رئيسي)", color="#EF4444", size=25)
    net.add_node("راشد .ع", label="راشد .ع (شريك)", color="#F59E0B", size=20)
    net.add_node("النعيمية", label="بؤرة النعيمية", color="#3B82F6", size=15)
    net.add_node("CR-2026-081", label="قضية 081", color="#10B981", size=12)
    net.add_node("CR-2026-083", label="قضية 083", color="#10B981", size=12)
    net.add_node("CR-2026-085", label="قضية 085", color="#10B981", size=12)
    
    # إضافة الروابط
    net.add_edge("خالد .م", "CR-2026-081", title="أسلوب إجرامي متطابق")
    net.add_edge("خالد .م", "CR-2026-083", title="أسلوب إجرامي متطابق")
    net.add_edge("خالد .م", "CR-2026-085", title="أسلوب إجرامي متطابق")
    net.add_edge("خالد .م", "النعيمية", title="تواجد ميداني")
    net.add_edge("خالد .م", "راشد .ع", title="اتصالات هاتفية رصدت")
    
    net.save_graph("network.html")
    
    with open("network.html", 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    components.html(html_content, height=470)

st.caption("تم تطوير هذا النموذج كإثبات مفهوم تنفيذي (POC) لصالح إدارة التحريات.")