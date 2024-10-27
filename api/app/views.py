import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def MakeDecision(request):
    # Kiểm tra xem có file 'audio' trong request hay không
    audio_file = request.FILES.get('audio')
    if not audio_file:
        return Response({"status": "failure", "error": "Missing 'audio' file in request"}, status=400)

    # Nếu có file, in ra thông báo thành công
    return Response({"status": "success", "message": "Received audio file successfully"}, status=200)


# @api_view(['POST'])
# def MakeDecision(request):
#     # Kiểm tra xem có file 'audio' trong request hay không
#     audio_file = request.FILES.get('audio')
#     if not audio_file:
#         return Response({"status": "failure", "error": "Missing 'audio' file in request"}, status=400)

#     try:
#         # Gửi file đến API bên ngoài
#         response = requests.post(
#             "https://5ea5-35-243-255-223.ngrok-free.app/transcribe",
#             files={'file': audio_file}
#         )

#         # Kiểm tra nếu yêu cầu thành công
#         if response.status_code == 200:
#             # Lấy giá trị 'transcription' từ phản hồi
#             transcription = response.json().get('transcription', '')
#             return Response({"status": "success", "transcription": transcription})
#         else:
#             return Response({"status": "failure", "error": "Failed to transcribe audio"}, status=response.status_code)
#     except requests.RequestException as e:
#         # Xử lý lỗi kết nối hoặc yêu cầu
#         return Response({"status": "failure", "error": str(e)}, status=500)


    # if not audio_file:
    #     return Response({"status": "failure", "message": "Missing audio file in request"}, status=400)

    # # Xử lý file âm thanh ở đây (ví dụ: lưu vào máy chủ, phân tích, v.v.)
    # # Đây là ví dụ đơn giản trả về một thông báo đã nhận thành công
    # # Bạn có thể thực hiện thêm xử lý âm thanh và trả về kết quả phù hợp

    # return Response({"status": "success", "message": "Audio file received successfully"})
