from django.shortcuts import render,redirect
from .models import Category,Log
from .forms import LogEditForm,CategoryEditForm,CSVUploadForm
from django.contrib.auth.decorators import login_required
import csv
from django.http import HttpResponse
import codecs
from datetime import datetime, time
from pytz import timezone
import pandas as pd


#トップページ
@login_required
def flontpage(request):
    categorys = Category.objects.filter(user=request.user)
    logs = Log.objects.filter(user=request.user).order_by('-learnDate','-startDateTime','-endDateTime','-id')
    return render(request,"./flontpage.html", {"categorys": categorys, "logs": logs,})

#修正処理
@login_required
def LogEdit(request,slug):
    return Edit(request,slug,Log,LogEditForm,'ログの登録')

@login_required
def CatEdit(request,slug):
    return Edit(request,slug,Category,CategoryEditForm,'カテゴリの登録')
 
@login_required    
def Edit(request,slug,model,Form,titleStr):
    rec = model.objects.get(slug=slug) 
    
    if request.method == 'POST':
        fm = Form(request.POST, instance= rec,user=request.user)                   
        if fm.is_valid():
            rec = fm.save(commit=False)
            rec.user = request.user
            rec.save()                          
            return redirect('flontpage')
    else:
        fm = Form(instance= rec,user=request.user)                            
            
    return render(request,"./Edit.html", {"form": fm, "title": titleStr,"IsKeisoku": False})

#削除処理
@login_required
def CatDelete(request,slug):
    return Delete(request,slug,Category,'カテゴリ')

@login_required
def LogDelete(request,slug):
    return Delete(request,slug,Log,'ログ')

@login_required
def Delete(request,slug,model,recordStr):
    record = model.objects.get(slug=slug)       
    if request.method == 'POST':
        logs = Log.objects.all()  
        for log in logs:
            if log.category == record:
                return ResultPage(request,'対象のカテゴリはログで仕様済みのため削除できませんでした。')
                   
        record.delete()
        return flontpage(request)
    return render(request, './Delete.html', {"record": record, "DeleteRecord": recordStr})

#登録処理
@login_required
def LogRegist(request):
    return Regist(request,LogEditForm,'ログの登録',True) 

@login_required
def CatRegist(request):    
    return Regist(request,CategoryEditForm,'カテゴリの登録',False)       

@login_required
def Regist(request,Form,titleStr,IsLog):    
    if request.method == 'POST':
        form = Form(request.POST,user=request.user)                   
        if form.is_valid():
            rec = form.save(commit=False)
            rec.user = request.user
            rec.save()          
            return redirect('flontpage')                         
    else:
        form = Form(user=request.user)
            
    return render(request,"./Edit.html", {"form": form, "title": titleStr, "IsKeisoku": IsLog})

#結果ページ
@login_required
def ResultPage(request, Msg):
     return render(request,"./Result.html", {"Msg": Msg})


def export_csv(request):
    # データを取得
    categorys = Category.objects.filter(user=request.user)
    logs = Log.objects.filter(user=request.user).order_by('-learnDate','-startDateTime','-endDateTime','-id')
    data = []
    for log in logs:
        for cat in categorys:
            if cat == log.category:
                break                
        rec= {'Category': cat.name, 
              'LearnDate': datetime.combine(log.learnDate, time()),  # datetime.dateオブジェクトをdatetime.datetimeオブジェクトに変換
              'startDateTime': log.startDateTime,  # datetime.datetimeオブジェクトをそのまま使う
              'endDateTime': log.endDateTime,  # datetime.datetimeオブジェクトをそのまま使う
              'learnMinut': log.learnMinut,
              'memo': log.memo}      
        data.append(rec)

    # CSVファイルを生成
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    # BOMを追加してUTF-8エンコーディングでファイルをラップ
    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response)

    writer.writerow(['カテゴリ', '勉強日', '開始時間', '終了時間', '勉強時間', '備考'])

    for item in data:
        writer.writerow([item['Category'], 
                         item['LearnDate'].astimezone(timezone('Asia/Tokyo')).strftime('%Y-%m-%d'),  # タイムゾーンを適用して文字列に変換
                         item['startDateTime'].astimezone(timezone('Asia/Tokyo')).strftime('%Y-%m-%d %H:%M:%S'),  # タイムゾーンを適用して文字列に変換
                         item['endDateTime'].astimezone(timezone('Asia/Tokyo')).strftime('%Y-%m-%d %H:%M:%S'),  # タイムゾーンを適用して文字列に変換
                         item['learnMinut'], 
                         item['memo']])

    return response

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST,request.FILES) 
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            # CSVファイルを1行ずつ読み込んでデータベースに保存
            df = pd.read_csv(csv_file)
            for index, row in df.iterrows():
                Log.objects.create(startDateTime=row[0], 
                                    endDateTime=row[1],
                                    learnDate=row[2],
                                    learnMinut=row[3],
                                    category=Category.objects.filter(user=request.user, name=row[4]),
                                    memo=row[5]
                                    )
            return ResultPage(request,'読み込みが完了しました')
            
    else:
        form = CSVUploadForm()
    return render(request, 'CSVUpload.html', {'form': form})









 


 
    





