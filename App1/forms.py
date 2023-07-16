from django import forms
from django.forms import ModelForm,ModelChoiceField,DateTimeInput
from .models import Log,Category

class CustomModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj): # label_from_instance 関数をオーバーライド
         return obj.name
    
class CustomDateTimeInput(DateTimeInput):
    input_type = 'datetime-local'
    format = '%Y-%m-%dT%H:%M:%S'

class LogEditForm(ModelForm):
    startDateTime= forms.DateTimeField(required=False,widget=CustomDateTimeInput,label='開始時間')
    endDateTime= forms.DateTimeField(required=False,widget=CustomDateTimeInput,label='終了時間')
    learnMinut= forms.IntegerField(required=False,label='勉強時間（直接入力）/単位:分')
    category = CustomModelChoiceField(queryset=Category.objects.all(),label='カテゴリ')
    memo = forms.CharField(required=False,label='備考')
    
    field_order = ['startDateTime','endDateTime','learnMinut','category','memo']             
    class Meta:
        model = Log
        fields ={"startDateTime","endDateTime","learnMinut","category","memo"}
        labels ={"startDateTime":"開始時間","endDateTime":"終了時間","learnMinut":"勉強時間（直接入力）","category":"カテゴリ" ,"memo":"メモ"}
        
    def clean(self):
        cleaned_data = super().clean()
        sd=self.cleaned_data.get('startDateTime')
        ed=self.cleaned_data.get('endDateTime')       
        DirectMinutes=self.cleaned_data.get('learnMinut')
        
        #開始時間終了時間、勉強時間（直接入力）両方ない場合は、バリデーション
        if (sd is None or ed is None) and DirectMinutes is None :
            raise forms.ValidationError('勉強時間を入力してください。')
     
        if DirectMinutes is not None and DirectMinutes <=0:
            raise forms.ValidationError('時間は1以上で入力してください')
            
        if sd is not None and ed is not None and sd>ed:
            raise forms.ValidationError('時間の前後関係がおかしいです。')
        
        #直接時間に自動計算時間をセット
        if sd is not None and ed is not None:
            cleaned_data['learnMinut'] = (ed - sd).total_seconds() / 60               
                     
        return cleaned_data
    
    
class CategoryEditForm(ModelForm):
    name=  forms.CharField(label='カテゴリ名') 
    memo = forms.CharField(required=False,label='備考') 
    field_order = ['name','memo']   
    
    class Meta:
        model = Category
        fields ={"name","memo"}
        labels ={"name":"カテゴリ名","memo":"備考"}
    