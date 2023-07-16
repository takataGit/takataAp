from django.shortcuts import render,redirect,get_object_or_404
from .models import Category,Log
from .forms import LogEditForm,CategoryEditForm


#トップページ
def flontpage(request):
    categorys = Category.objects.all()
    logs = Log.objects.all().order_by('-startDateTime','-endDateTime','-id')
    return render(request,"./flontpage.html", {"categorys": categorys, "logs": logs})

#修正処理
def LogEdit(request,slug):
    return Edit(request,slug,Log,LogEditForm,'ログの登録')

def CatEdit(request,slug):
    return Edit(request,slug,Category,CategoryEditForm,'カテゴリの登録')
    
def Edit(request,slug,model,Form,titleStr):
    record = model.objects.get(slug=slug) 
    
    if request.method == 'POST':
        fm = Form(request.POST, instance= record)                   
        if fm.is_valid():
            record2 = fm.save(commit=False)
            record2.post = record
            record2.save()
                  
            return flontpage(request) 
    elif request.method == "GET":
        fm = Form(instance= record)                            
    else:
        fm = Form()
            
    return render(request,"./Edit.html", {"form": fm, "title": titleStr,"IsKeisoku": False})

#削除処理
def CatDelete(request,slug):
    return Delete(request,slug,Category,'カテゴリ')

def LogDelete(request,slug):
    return Delete(request,slug,Log,'ログ')

def Delete(request,slug,model,recordStr):
    record = get_object_or_404(model, slug=slug)       
    if request.method == 'POST':
        logs = Log.objects.all()  
        for log in logs:
            if log.category == record:
                return ResultPage(request,'対象のカテゴリはログで仕様済みのため削除できませんでした。')
                   
        record.delete()
        return flontpage(request)
    return render(request, './delete.html', {"record": record, "DeleteRecord": recordStr})

#登録処理
def LogRegist(request):
    return Regist(request,LogEditForm,'ログの登録',True) 

def CatRegist(request):    
    return Regist(request,CategoryEditForm,'カテゴリの登録',False)       

def Regist(request,Form,titleStr,IsLog):    
    if request.method == 'POST':
        form = Form(request.POST)                   
        if form.is_valid():
            log2 = form.save(commit=False)
            log2.save()          
            return flontpage(request)                          
    else:
        form = Form()
            
    return render(request,"./Edit.html", {"form": form, "title": titleStr, "IsKeisoku": IsLog})

#結果ページ
def ResultPage(request, Msg):
     return render(request,"./Result.html", {"Msg": Msg})


 
    





