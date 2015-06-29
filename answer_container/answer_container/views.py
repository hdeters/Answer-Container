from django.shortcuts import redirect

def QandARedirect(request):
    return redirect('qanda:questions')
