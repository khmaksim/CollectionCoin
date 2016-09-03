from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from collection.models import Section, Coin, Metal, TypeEdge, Collection
from collection.form import CoinForm, AddToCollectionForm, CollectionForm


def main(request):
    if not request.user.is_authenticated():
        return render(request, 'catalog.html')
    else:
        title = breadcrumbs = u'Каталог'
        section_list = Section.objects.all()
        return render(request, 'catalog.html', {'title': title,
                                                'breadcrumbs': breadcrumbs,
                                                'section_list': section_list})


@login_required
def catalog(request):
    title = breadcrumbs = u'Каталог'
    sections = Section.objects.all()
    coins = Coin.objects.all()[:48:3]
    return render(request, 'catalog.html',
                  {'title': title, 'breadcrumbs': breadcrumbs, 'sections': sections, 'coins': coins})


def section_catalog(request, id_section):
    coins = Coin.objects.filter(section=id_section).order_by('name')
    section = Section.objects.get(pk=id_section)
    return render_to_response('section_coin.html', {'section': section,
                                               'coins': coins}, context_instance=RequestContext(request))


def information_coin(request, id_coin):
    coin = Coin.objects.get(pk=id_coin)

    metal_list = []
    for metal in coin.metal.all():
        metal_list.append(metal.name)

    if coin.type_edge is not None:
        try:
            type_edge = TypeEdge.objects.get(id__exact=coin.type_edge.id)
            type_edge_name = type_edge.name
        except ObjectDoesNotExist:
            type_edge_name = ""
    else:
        type_edge_name = ""

    coin_form = CoinForm(instance=coin, initial={'type_edge': type_edge_name, 'metal': ','.join(metal_list)},
                         label_suffix='')
    return render_to_response('coin.html', {'coin': coin, 'coin_form': coin_form},
                              context_instance=RequestContext(request))


def add_to_collection(request, id_coin):
    coin = Coin.objects.get(pk=id_coin)

    if request.method == 'POST':
        add_to_collection_form = AddToCollectionForm(request.POST, label_suffix='')
        if add_to_collection_form.is_bound and add_to_collection_form.is_valid():
            collection = add_to_collection_form.save(commit=False)
            collection.coin = coin
            collection.user = request.user
            collection.save()
            return redirect('section_collection', id_section=coin.section_id)
    else:
        add_to_collection_form = AddToCollectionForm(label_suffix='')

    return render(request, 'add_to_collection.html', {'coin': coin,
                                                      'add_to_collection_form': add_to_collection_form})


def my_collection(request):
    title = u'Моя Коллекция'
    sections = Section.objects.filter(coin__collection__user=request.user).distinct()

    return render(request, 'collection.html', {'title': title,
                                               'breadcrumbs': [{'url': '', 'title': title}],
                                               'sections': sections})


def section_collection(request, id_section):
    collections = Collection.objects.filter(user=request.user).filter(coin__section=id_section)
    # coins = Coin.objects.filter(collection__user=request.user).filter(section=id_section)
    # if coins.count():
    #     section = Section.objects.get(pk=id_section)
    # if collections.count():
    #     section = Section.objects.get(pk=id_section)
    # else:
    #     section = coins[0].section.name
    if collections.count():
        section = Section.objects.get(pk=id_section)
    else:
        section = collections[0].section.name

    title = Section.objects.get(pk=id_section).name

    return render(request, 'section_coin.html', {'title': title,
                                                       'section': section,
                                                       'collections': collections})


def coin_collection(request, id_collection):
    collection = Collection.objects.get(pk=id_collection)
    coin = collection.coin

    metal_list = []
    for metal in coin.metal.all():
        metal_list.append(metal.name)

    if coin.type_edge is not None:
        try:
            type_edge = TypeEdge.objects.get(id__exact=coin.type_edge.id)
            type_edge_name = type_edge.name
        except ObjectDoesNotExist:
            type_edge_name = ""
    else:
        type_edge_name = ""

    coin_form = CoinForm(instance=coin, initial={'type_edge': type_edge_name, 'metal': ','.join(metal_list)},
                         label_suffix='')
    collection_form = CollectionForm(instance=collection, label_suffix='')

    return render(request, 'coin_collection.html', {'coin': coin,
                                                    'coin_form': coin_form,
                                                    'collection_form': collection_form})


def remove_from_collection(request, id_coin):
    coin = Coin.objects.get(pk=id_coin)

    # if request.method == 'POST':
    #     add_to_collection_form = AddToCollectionForm(request.POST, label_suffix='')
    #     if add_to_collection_form.is_bound and add_to_collection_form.is_valid():
    #         collection = add_to_collection_form.save(commit=False)
    #         collection.coin = coin
    #         collection.save()
    #         return redirect('coins_section', id_section=coin.section_id)
    # else:
    #     add_to_collection_form = AddToCollectionForm(label_suffix='')

    return render(request, 'remove_from_collection.html')