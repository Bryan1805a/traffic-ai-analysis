import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

def extract_location(article_text):
    if not article_text:
        return "No content"
    
    prompt = f"""
    Bạn là một trợ lý phân tích dữ liệu giao thông tại Việt Nam.
    Hãy đọc nội dung bài báo dưới đây và tìm ra tên Tỉnh hoặc Thành phố trực thuộc trung ương nơi xảy ra tai nạn giao thông.
    
    Quy tắc bắt buộc:
    1. CHỈ trả về đúng tên Tỉnh/Thành phố (ví dụ: "Hà Nội", "Đồng Nai", "TP HCM", "Quảng Trị").
    2. Tuyệt đối KHÔNG trả về các từ thừa thãi, KHÔNG giải thích, KHÔNG viết thành câu.
    3. Nếu trong bài không đề cập đến địa điểm, hãy trả về chữ "Unknown".
    
    Nội dung bài báo:
    {article_text}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        location = response.text.strip()
        return location
        
    except Exception as e:
        print(f"Error while calling Gemini API: {e}")
        return "Error"

# Test
if __name__ == "__main__":
    sample_text = "Vào khoảng 15h chiều nay, một vụ va chạm liên hoàn giữa 3 xe tải đã xảy ra trên tuyến quốc lộ 1A đoạn qua địa bàn huyện Trảng Bom, tỉnh Đồng Nai khiến giao thông ùn tắc kéo dài..."
    
    print("Waiting Gemini extract location from the article...")
    result = extract_location(sample_text)
    
    print(f"Extraction result: '{result}'")