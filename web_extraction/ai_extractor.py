import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

def extract_accident_info(article_text):
    if not article_text:
        return None
    
    prompt = f"""
    Bạn là chuyên gia phân tích dữ liệu giao thông. Đọc bài báo sau và trích xuất thông tin.
    
    Quy tắc bắt buộc:
    1. Chỉ trả về một đối tượng JSON hợp lệ, không có chú thích nào khác.
    2. Các key trong JSON bao gồm:
       - "location": Tên Tỉnh/Thành phố trực thuộc trung ương nơi xảy ra tai nạn (VD: "Hà Nội", "Đồng Nai"). Nếu không rõ, ghi "Unknown".
       - "deaths": Số người tử vong (chỉ ghi số nguyên, VD: 2). Nếu không có hoặc không rõ, ghi 0.
       - "injuries": Số người bị thương (chỉ ghi số nguyên, VD: 3). Nếu không có hoặc không rõ, ghi 0.
       - "vehicles": Loại phương tiện liên quan chính (VD: "Xe khách, Xe tải", "Xe máy").
    
    Nội dung bài báo:
    {article_text}
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )

        data = json.loads(response.text)
        return data
    
    except Exception as e:
        print(f"Error when calling Gemini API or parsing JSON: {e}")
        return None

if __name__ == "__main__":
    test_text = "Vào 15h chiều nay, một chiếc xe khách mất lái tông vào xe tải trên cao tốc qua địa phận tỉnh Quảng Trị. Vụ tai nạn làm 2 người chết tại chỗ và 3 người khác bị thương nặng."
    print("Analysing...")
    result = extract_accident_info(test_text)
    print("JSON Result:", result)