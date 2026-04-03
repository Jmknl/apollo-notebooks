from django.urls import path
from . import views

app_name = "appliance"

urlpatterns = [
    path("", views.index, name="index"),
    path("api/traduzir/", views.word_translate, name="translate" ),  
    path("api/traduzir_idioma/", views.translate_to_language, name="traduzir_idioma"),
    path("api/traduzir_frase/", views.translate_sentence, name="traduzir_frase"),
    path("books/", views.book_list, name="books"),
    path("books/<int:book_id>/", views.book_detail, name="book_detail"),
    path("books/newbook/", views.new_book, name="new_book"),
    path("books/<int:book_id>/new_paper/", views.new_paper, name="new_paper"),
    path("edit_paper/<int:paper_id>/", views.edit_paper, name="edit_paper"),
    path("del_paper/<int:paper_id>/", views.del_paper, name="del_paper"),
    path("del_book/<int:book_id>/", views.del_book, name="del_book"),
    path("profile/", views.profile, name="profile"),
    path("api/calendar/get/", views.calendar_get, name="calendar_get"),
    path("api/calendar/post/", views.calendar_post, name="calendar_post"),
    path( "api/calendar/delete/<int:event_id>/",  views.calendar_delete,  name="calendar_delete",),
    
]
