import base64
from io import BytesIO

def pdf_to_base64(file_obj: BytesIO) -> str:
    """BytesIO 객체에서 PDF 파일을 읽어 Base64 문자열로 변환"""
    try:
        file_obj.seek(0) 
        binary_data = file_obj.read()
        base64_encoded = base64.b64encode(binary_data).decode('utf-8')
        return base64_encoded
    except Exception as e:
        print(f"Error converting PDF to Base64: {e}")
        raise