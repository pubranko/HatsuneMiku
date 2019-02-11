from django.urls import path

from . import views

app_name = 'saikutu'  
'''
テンプレート側からurlのパターンを参照するとき、アプリがpollsだけだとapp_nameは不要。
しかし他にもアプリがあり、その中に同名のビューがある場合区別がテンプレート側で区別が付かなくなる。
それを避けるため、上記の指定を行い、テンプレート側でその名前を指定するようにする
'''

urlpatterns = [
    path('', views.saikutu, name='saikutu'),
    #path('kaisyuu/', views.kaisyuu, name='kaisyuu'),
]


'''
# ex: /polls/
path('', views.index, name='index'),
# ex: /polls/5/
path('<int:question_id>/', views.detail, name='detail'),
# ex: /polls/5/results/
path('<int:question_id>/results/', views.results, name='results'),
# ex: /polls/5/vote/
path('<int:question_id>/vote/', views.vote, name='vote'),
'''