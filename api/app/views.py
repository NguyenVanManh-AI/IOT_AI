from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def MakeDecision(request):
    # Kiểm tra xem có file 'audio' trong request hay không
    audio_file = request.FILES.get('audio')
    if not audio_file:
        return Response({"status": "failure", "message": "Missing audio file in request"}, status=400)

    # Xử lý file âm thanh ở đây (ví dụ: lưu vào máy chủ, phân tích, v.v.)
    # Đây là ví dụ đơn giản trả về một thông báo đã nhận thành công
    # Bạn có thể thực hiện thêm xử lý âm thanh và trả về kết quả phù hợp

    return Response({"status": "success", "message": "Audio file received successfully"})
