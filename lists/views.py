from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.exceptions import ValidationError

from .models import Item, List
from .forms import ItemForm, EMPTY_ITEM_ERROR

def home_page(request):
	return render(request, 'lists/home.html', {'form': ItemForm()})
	
def view_list(request, list_id):
	list_ = List.objects.get(id=list_id)
	error = None
	
	if request.method == 'POST':
		try:
			item = Item.objects.create(text=request.POST['text'], list=list_)
			item.full_clean()
			item.save()
			return redirect(list_)
		except ValidationError:
			error = EMPTY_ITEM_ERROR
	
	form = ItemForm()
	return render(request, 'lists/list.html', {'list': list_, 'form': form, 'error': error})
	
def new_list(request):
	form = ItemForm(data=request.POST)
	if form.is_valid():
		list_ = List.objects.create()
		Item.objects.create(text=request.POST['text'], list=list_)
		return redirect(list_)
	else:
		return render(request, 'lists/home.html', {'form': form})
	
