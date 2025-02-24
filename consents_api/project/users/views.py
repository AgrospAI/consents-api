# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# from django.contrib.auth import get_user_model, login

# from users.utils import verify_signature

# User = get_user_model()


# @csrf_exempt
# def authenticate(request):
#     if request.method == "POST":
#         # Get the address, signature, and message from the request body
#         address = request.POST.get("address")
#         signature = request.POST.get("signature")
#         message = request.POST.get("message")
#         # Verify the signature
#         if verify_signature(address, signature, message):
#             # If the signature is valid, log in the user
#             user = User.objects.get_or_create(address=address)
#             login(request, user)
#             return JsonResponse({"status": "success"})

#     return JsonResponse({"status": "error"})
