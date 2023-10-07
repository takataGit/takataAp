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
    learnDate= forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=False,label='勉強日時（直接入力）')
    learnMinut= forms.IntegerField(required=False,label='勉強時間（直接入力）/単位:分')
    category = CustomModelChoiceField(queryset=Category.objects.all(),label='カテゴリ')
    memo = forms.CharField(required=False,label='備考')
        
    field_order = ['startDateTime','endDateTime','learnDate','learnMinut','category','memo']             
        
    def __init__(self, *args, user=None, **kwargs):
        super(LogEditForm, self).__init__(*args, **kwargs)
        self.fields['category']  = CustomModelChoiceField(queryset=Category.objects.filter(user=user),label='カテゴリ')
               
    def clean(self):
        cleaned_data = super().clean()
        sd=self.cleaned_data.get('startDateTime')
        ed=self.cleaned_data.get('endDateTime')       
        DirectMinutes=self.cleaned_data.get('learnMinut')
        DirectDate=self.cleaned_data.get('learnDate')
        
        #開始時間終了時間、勉強時間（直接入力）両方ない場合は、バリデーション
        if (sd is None or ed is None) and DirectMinutes is None :
            raise forms.ValidationError('勉強時間を入力してください。')
        
        if (sd is None or ed is None) and DirectDate is None :
            raise forms.ValidationError('勉強日時を入力してください。')        
     
        if DirectMinutes is not None and DirectMinutes <=0:
            raise forms.ValidationError('時間は1以上で入力してください')
            
        if sd is not None and ed is not None and sd>ed:
            raise forms.ValidationError('時間の前後関係がおかしいです。')
        
        #直接時間に自動計算時間をセット
        if sd is not None and ed is not None:
            cleaned_data['learnMinut'] = (ed - sd).total_seconds() / 60
            cleaned_data['learnDate']  =sd;                
                     
        return cleaned_data
    
    class Meta:
        model = Log
        fields ={"startDateTime","endDateTime",'learnDate',"learnMinut","category","memo"}
    
    
class CategoryEditForm(ModelForm):
    name=  forms.CharField(label='カテゴリ名') 
    memo = forms.CharField(required=False,label='備考') 
    field_order = ['name','memo']   
 
    def __init__(self, *args, user=None, **kwargs):
        super(CategoryEditForm, self).__init__(*args, **kwargs)
            
    class Meta:
        model = Category
        fields ={"name","memo"}
        labels ={"name":"カテゴリ名","memo":"備考"}
        
class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(required=True)
            
    